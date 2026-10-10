"""Interface commune à toutes les sources d'offres.

Chaque provider renvoie une liste de `NormalizedJob`. La couche services
(jobs/services.py) se charge ensuite de la persistance et du dédoublonnage.
Ajouter une source = ajouter un fichier qui sous-classe JobProvider, rien d'autre.
"""
from __future__ import annotations

import json
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import requests

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
_LD_JSON_RE = re.compile(
    r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S
)


def extract_email(text: str) -> str:
    """Renvoie le premier email trouvé dans un texte (ou '')."""
    if not text:
        return ""
    m = _EMAIL_RE.search(text)
    return m.group(0) if m else ""


def extract_jobposting(html: str) -> dict | None:
    """Renvoie le bloc JSON-LD schema.org JobPosting d'une page (ou None).

    Standard stable utilisé par Asako, Recruteo… → extraction fiable.
    """
    for block in _LD_JSON_RE.findall(html):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        for item in data if isinstance(data, list) else [data]:
            if isinstance(item, dict) and item.get("@type") == "JobPosting":
                return item
    return None


def jsonld_location(job_location) -> str:
    """Extrait un libellé de lieu depuis le champ jobLocation d'un JobPosting."""
    loc = job_location[0] if isinstance(job_location, list) and job_location else job_location
    if not isinstance(loc, dict):
        return ""
    addr = loc.get("address")
    if isinstance(addr, dict):
        parts = [
            addr.get("addressLocality"),
            addr.get("addressRegion"),
            addr.get("addressCountry"),
        ]
        return ", ".join(p for p in parts if isinstance(p, str) and p)
    if isinstance(addr, str):
        return addr
    return ""

logger = logging.getLogger("jobs")

DEFAULT_TIMEOUT = 15
USER_AGENT = "PortfolioJobWatcher/1.0 (+https://portfolio.unityfianar.site)"

#: Indices textuels d'une offre informatique, pour les sources généralistes
#: qui n'exposent pas de filtre catégorie côté API.
TECH_TERMS = {
    "develop", "développ", "developer", "software", "logiciel", "web", "frontend",
    "front-end", "backend", "back-end", "fullstack", "full-stack", "devops", "data",
    "python", "django", "java", "javascript", "typescript", "react", "angular", "vue",
    "node", "php", "laravel", "symfony", "c#", ".net", "golang", "rust", "ruby",
    "kubernetes", "docker", "cloud", "aws", "azure", "sql", "informatique", "it ",
    "programmeur", "ingénieur logiciel", "sysadmin", "cyber", "machine learning",
    "ai", "ia ", "mobile", "android", "ios", "qa", "test automation", "sre",
}


def looks_like_it(text: str) -> bool:
    """Heuristique : le texte évoque-t-il un métier informatique ?"""
    low = f" {text.lower()} "
    return any(term in low for term in TECH_TERMS)


@dataclass
class NormalizedJob:
    """Offre brute normalisée, indépendante de la source."""

    source: str
    external_id: str
    title: str
    url: str
    company: str = ""
    location: str = ""
    is_remote: bool = False
    contract_type: str = ""
    description: str = ""
    salary: str = ""
    apply_email: str = ""
    tags: list = field(default_factory=list)
    published_at: Optional[datetime] = None


class JobProvider(ABC):
    """Classe de base. `source_key` doit matcher JobOffer.SOURCE_CHOICES."""

    source_key: str = ""
    #: True si le provider est utilisable sans configurer de clé API.
    needs_credentials: bool = False

    def is_configured(self) -> bool:
        """Surchargé par les providers qui ont besoin de clés."""
        return not self.needs_credentials

    @abstractmethod
    def search(
        self,
        keywords: str = "",
        location: str = "",
        remote: bool = False,
        category: str = "it",
    ) -> list[NormalizedJob]:
        """Interroge la source et renvoie une liste normalisée (jamais None).

        `category` vaut "it" (informatique, défaut) ou "all" (tous secteurs).
        Chaque provider applique ce filtre au mieux de ce que son API permet.
        """
        raise NotImplementedError

    # -- helpers partagés -------------------------------------------------

    def _get(self, url: str, params: dict | None = None, headers: dict | None = None):
        merged = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        if headers:
            merged.update(headers)
        resp = requests.get(url, params=params, headers=merged, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def safe_search(
        self, keywords="", location="", remote=False, category="it"
    ) -> list[NormalizedJob]:
        """Enveloppe search() : ne lève jamais, log et renvoie [] en cas d'erreur."""
        if not self.is_configured():
            logger.info("Provider %s non configuré, ignoré.", self.source_key)
            return []
        try:
            return self.search(
                keywords=keywords, location=location, remote=remote, category=category
            )
        except Exception as exc:  # réseau, format, quota…
            logger.warning("Provider %s a échoué : %s", self.source_key, exc)
            return []
