"""France Travail (ex-Pôle Emploi) — API officielle gratuite.
Auth OAuth2 client_credentials, puis endpoint "Offres d'emploi v2".
Doc : https://francetravail.io/data/api/offres-emploi
"""
from __future__ import annotations

import os
from datetime import datetime

import requests

from .base import DEFAULT_TIMEOUT, USER_AGENT, JobProvider, NormalizedJob

TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
SCOPE = "api_offresdemploiv2 o2dsoffre"

# Famille ROME M18 = "Systèmes d'information et de télécommunication" (informatique).
# Études/dev, production/exploitation, expertise/support, conseil SI, data, hotline.
IT_ROME_CODES = "M1805,M1806,M1802,M1810,M1803,M1801,M1804,M1809"


class FranceTravailProvider(JobProvider):
    source_key = "france_travail"
    needs_credentials = True

    def __init__(self):
        self.client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID", "")
        self.client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET", "")

    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)

    def _token(self) -> str:
        resp = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "scope": SCOPE,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    def search(self, keywords="", location="", remote=False, category="it") -> list[NormalizedJob]:
        token = self._token()
        params = {"range": "0-49"}
        if category == "it":
            # Restreint aux métiers informatiques via le référentiel ROME.
            params["codeROME"] = IT_ROME_CODES
        if keywords:
            params["motsCles"] = keywords[:200]
        data = self._get(
            SEARCH_URL,
            params=params,
            headers={"Authorization": f"Bearer {token}", "User-Agent": USER_AGENT},
        )

        jobs = []
        for item in data.get("resultats", []):
            pub = None
            raw_date = item.get("dateCreation")
            if raw_date:
                try:
                    pub = datetime.fromisoformat(raw_date)
                except ValueError:
                    pub = None
            lieu = (item.get("lieuTravail") or {}).get("libelle", "")
            salaire = (item.get("salaire") or {}).get("libelle", "") or ""

            jobs.append(
                NormalizedJob(
                    source=self.source_key,
                    external_id=str(item.get("id")),
                    title=item.get("intitule", ""),
                    company=(item.get("entreprise") or {}).get("nom", ""),
                    location=lieu,
                    is_remote=item.get("dureeTravailLibelleConverti", "").lower().find("télétravail") >= 0,
                    contract_type=item.get("typeContratLibelle", "") or item.get("typeContrat", ""),
                    description=item.get("description", ""),
                    salary=salaire,
                    url=(item.get("origineOffre") or {}).get("urlOrigine", ""),
                    tags=[item.get("romeLibelle")] if item.get("romeLibelle") else [],
                    published_at=pub,
                )
            )
        return jobs
