"""Registre des providers. Pour brancher une nouvelle source : l'importer ici
et l'ajouter à ALL_PROVIDERS. Rien d'autre à toucher dans l'app.
"""
from .adzuna import AdzunaProvider
from .arbeitnow import ArbeitnowProvider
from .base import JobProvider, NormalizedJob
from .france_travail import FranceTravailProvider
from .himalayas import HimalayasProvider
from .jobicy import JobicyProvider
from .remoteok import RemoteOkProvider
from .remotive import RemotiveProvider
from .themuse import TheMuseProvider
from .weworkremotely import WeWorkRemotelyProvider

ALL_PROVIDERS: list[type[JobProvider]] = [
    RemotiveProvider,
    ArbeitnowProvider,
    RemoteOkProvider,
    TheMuseProvider,
    JobicyProvider,
    HimalayasProvider,
    WeWorkRemotelyProvider,
    FranceTravailProvider,
    AdzunaProvider,
]

PROVIDERS_BY_KEY = {cls.source_key: cls for cls in ALL_PROVIDERS}


def get_providers(keys: list[str] | None = None) -> list[JobProvider]:
    """Instancie les providers demandés (ou tous si keys vide/None)."""
    if keys:
        classes = [PROVIDERS_BY_KEY[k] for k in keys if k in PROVIDERS_BY_KEY]
    else:
        classes = ALL_PROVIDERS
    return [cls() for cls in classes]


__all__ = [
    "JobProvider",
    "NormalizedJob",
    "ALL_PROVIDERS",
    "PROVIDERS_BY_KEY",
    "get_providers",
]
