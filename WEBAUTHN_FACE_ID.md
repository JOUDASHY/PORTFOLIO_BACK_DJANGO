# 🔐 WebAuthn / Face ID — Guide d'intégration complet

Authentification biométrique (Face ID, Touch ID, Windows Hello) via le standard **WebAuthn / FIDO2**.  
La biométrie ne quitte **jamais** l'appareil — seule une signature cryptographique est envoyée au serveur.

---

## 📋 Sommaire

1. [Architecture & Principe](#1-architecture--principe)
2. [Variables d'environnement](#2-variables-denvironnement)
3. [Endpoints API](#3-endpoints-api)
4. [Flux complet — Enregistrement](#4-flux-complet--enregistrement)
5. [Flux complet — Authentification](#5-flux-complet--authentification)
6. [Code Frontend (JavaScript/React)](#6-code-frontend-javascriptreact)
7. [Exemples cURL](#7-exemples-curl)
8. [Modèle BDD](#8-modèle-bdd)
9. [Notes de sécurité](#9-notes-de-sécurité)
10. [Dépannage](#10-dépannage)

---

## 1. Architecture & Principe

```
┌─────────────────────────────────────────────────────────────────┐
│                     PROTOCOLE WEBAUTHN                          │
├───────────────────────┬─────────────────────────────────────────┤
│     APPAREIL USER     │           BACKEND DJANGO                │
│  (iPhone / Android /  │                                         │
│   Windows / Mac)      │                                         │
├───────────────────────┼─────────────────────────────────────────┤
│                       │                                         │
│  ENREGISTREMENT       │                                         │
│  ──────────────       │                                         │
│                       │ ← POST /api/webauthn/register/begin/    │
│                       │   (JWT requis)                          │
│                       │ → { challenge, rp, user, ... }          │
│                       │                                         │
│  [Scan Face ID]       │                                         │
│  Génère clé privée    │                                         │
│  + clé publique       │                                         │
│                       │                                         │
│                       │ ← POST /api/webauthn/register/complete/ │
│                       │   { id, rawId, response, type }         │
│                       │ → { message: "✅ Enregistré !" }        │
│                       │   (clé publique sauvée en BDD)          │
│                       │                                         │
│  AUTHENTIFICATION     │                                         │
│  ────────────────     │                                         │
│                       │ ← POST /api/webauthn/login/begin/       │
│                       │   { email: "..." }                      │
│                       │ → { challenge, allowCredentials, ... }  │
│                       │                                         │
│  [Scan Face ID]       │                                         │
│  Signe le challenge   │                                         │
│  avec clé privée      │                                         │
│                       │                                         │
│                       │ ← POST /api/webauthn/login/complete/    │
│                       │   { email, id, rawId, response, type }  │
│                       │ → { access, refresh, user }             │
│                       │                                         │
└───────────────────────┴─────────────────────────────────────────┘
```

> 🔒 **La clé privée ne quitte JAMAIS l'appareil.**  
> Le serveur ne stocke que la **clé publique** — même si la BDD est compromise, aucune donnée biométrique n'est exposée.

---

## 2. Variables d'environnement

Ajoutez ces variables dans votre fichier `.env` :

```env
# ─── WebAuthn / Face ID ───────────────────────────────────────────
# RP_ID : domaine EXACT de votre frontend (sans https://, sans slash)
# En développement local :
WEBAUTHN_RP_ID=localhost

# En production :
# WEBAUTHN_RP_ID=portfolio.unityfianar.site

# RP_NAME : nom affiché à l'utilisateur lors du scan biométrique
WEBAUTHN_RP_NAME=Portfolio Nilsen

# ORIGIN : URL complète du frontend (avec protocole + port si besoin)
# En développement local :
WEBAUTHN_ORIGIN=http://localhost:5173

# En production :
# WEBAUTHN_ORIGIN=https://portfolio.unityfianar.site
```

> ⚠️ **IMPORTANT** : `WEBAUTHN_RP_ID` doit correspondre EXACTEMENT au domaine
> depuis lequel le frontend fait ses requêtes. Une erreur ici cause des échecs
> de vérification silencieux.

---

## 3. Endpoints API

### Vue d'ensemble

| Méthode | URL | Auth | Description |
|---------|-----|------|-------------|
| `POST` | `/api/webauthn/register/begin/` | 🔒 JWT | Étape 1 : génère le challenge d'enregistrement |
| `POST` | `/api/webauthn/register/complete/` | 🔒 JWT | Étape 2 : vérifie et sauvegarde le credential |
| `POST` | `/api/webauthn/login/begin/` | 🌐 Public | Étape 1 : génère le challenge d'authentification |
| `POST` | `/api/webauthn/login/complete/` | 🌐 Public | Étape 2 : vérifie et retourne les tokens JWT |
| `GET` | `/api/webauthn/credentials/` | 🔒 JWT | Liste les credentials enregistrés |
| `DELETE` | `/api/webauthn/credentials/<id>/` | 🔒 JWT | Supprime un credential |

---

### POST `/api/webauthn/register/begin/`

**Headers :**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body :** *(optionnel)*
```json
{}
```

**Réponse 200 :**
```json
{
  "rp": {
    "id": "localhost",
    "name": "Portfolio Nilsen"
  },
  "user": {
    "id": "MQ==",
    "name": "nilsen",
    "displayName": "Eddy Nilsen"
  },
  "challenge": "base64url_encoded_challenge",
  "pubKeyCredParams": [...],
  "timeout": 60000,
  "excludeCredentials": [],
  "authenticatorSelection": {
    "authenticatorAttachment": "platform",
    "userVerification": "required",
    "residentKey": "preferred"
  },
  "attestation": "none"
}
```

---

### POST `/api/webauthn/register/complete/`

**Headers :**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Body :** *(réponse du navigateur + nom optionnel)*
```json
{
  "id": "credential_id_base64url",
  "rawId": "credential_id_base64url",
  "response": {
    "clientDataJSON": "base64url...",
    "attestationObject": "base64url..."
  },
  "type": "public-key",
  "device_name": "Mon iPhone 15"
}
```

**Réponse 201 :**
```json
{
  "message": "✅ Face ID 'Mon iPhone 15' enregistré avec succès !"
}
```

---

### POST `/api/webauthn/login/begin/`

**Body :**
```json
{
  "email": "nilsen@example.com"
}
```
*Ou par username :*
```json
{
  "username": "nilsen"
}
```

**Réponse 200 :**
```json
{
  "challenge": "base64url_encoded_challenge",
  "timeout": 60000,
  "rpId": "localhost",
  "allowCredentials": [
    {
      "id": "credential_id_base64url",
      "type": "public-key"
    }
  ],
  "userVerification": "required"
}
```

---

### POST `/api/webauthn/login/complete/`

**Body :**
```json
{
  "email": "nilsen@example.com",
  "id": "credential_id_base64url",
  "rawId": "credential_id_base64url",
  "response": {
    "clientDataJSON": "base64url...",
    "authenticatorData": "base64url...",
    "signature": "base64url...",
    "userHandle": "base64url_or_null"
  },
  "type": "public-key"
}
```

**Réponse 200 :**
```json
{
  "message": "✅ Authentification Face ID réussie !",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "nilsen",
    "email": "nilsen@example.com"
  }
}
```

---

### GET `/api/webauthn/credentials/`

**Réponse 200 :**
```json
[
  {
    "id": 1,
    "device_name": "iPhone 15 Face ID",
    "aaguid": "adce0002-35bc-c60a-648b-0b25f1f05503",
    "created_at": "2025-01-15T10:30:00Z",
    "last_used_at": "2025-06-01T08:15:00Z"
  },
  {
    "id": 2,
    "device_name": "MacBook Touch ID",
    "aaguid": "00000000-0000-0000-0000-000000000000",
    "created_at": "2025-02-01T14:00:00Z",
    "last_used_at": null
  }
]
```

---

### DELETE `/api/webauthn/credentials/<id>/`

**Réponse 200 :**
```json
{
  "message": "🗑️ Credential 'iPhone 15 Face ID' supprimé avec succès."
}
```

---

## 4. Flux complet — Enregistrement

```
1. L'utilisateur est connecté (JWT valide)
2. Frontend appelle  → POST /api/webauthn/register/begin/
3. Backend génère un challenge aléatoire + options WebAuthn
4. Backend stocke le challenge en cache (TTL 2 min)
5. Frontend passe les options à navigator.credentials.create()
6. L'APPAREIL demande le Face ID / Touch ID à l'utilisateur
7. L'appareil génère une paire de clés (privée garde en local, publique envoyée)
8. Frontend appelle  → POST /api/webauthn/register/complete/
9. Backend vérifie la réponse cryptographique
10. Backend sauvegarde la clé publique + credential_id en BDD
11. ✅ Face ID opérationnel pour les prochaines connexions
```

---

## 5. Flux complet — Authentification

```
1. L'utilisateur n'est PAS connecté
2. Frontend appelle  → POST /api/webauthn/login/begin/   { email }
3. Backend trouve les credentials de cet utilisateur en BDD
4. Backend génère un challenge + liste des credentials autorisés
5. Backend stocke challenge + user_id en cache (TTL 2 min)
6. Frontend passe les options à navigator.credentials.get()
7. L'APPAREIL demande le Face ID / Touch ID à l'utilisateur
8. L'appareil signe le challenge avec la clé privée locale
9. Frontend appelle  → POST /api/webauthn/login/complete/   { email, ...réponse }
10. Backend vérifie la signature avec la clé publique stockée
11. Backend met à jour sign_count (protection anti-replay)
12. Backend retourne les tokens JWT
13. ✅ Utilisateur connecté
```

---

## 6. Code Frontend (JavaScript/React)

### Installation

```bash
# Aucune librairie requise — l'API WebAuthn est native dans tous les navigateurs modernes
# Optionnel : helper pour simplifier la gestion du base64url
npm install @simplewebauthn/browser
```

### Utilitaires base64url

```javascript
// utils/webauthn.js

/**
 * Convertit un ArrayBuffer en chaîne base64url
 */
export function bufferToBase64url(buffer) {
  const bytes = new Uint8Array(buffer);
  let str = '';
  for (const byte of bytes) {
    str += String.fromCharCode(byte);
  }
  return btoa(str)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}

/**
 * Convertit une chaîne base64url en ArrayBuffer
 */
export function base64urlToBuffer(base64url) {
  const base64 = base64url
    .replace(/-/g, '+')
    .replace(/_/g, '/')
    .padEnd(base64url.length + ((4 - (base64url.length % 4)) % 4), '=');
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes.buffer;
}

/**
 * Prépare les options de création reçues du backend pour navigator.credentials.create()
 */
export function prepareCreationOptions(options) {
  return {
    ...options,
    challenge: base64urlToBuffer(options.challenge),
    user: {
      ...options.user,
      id: base64urlToBuffer(options.user.id),
    },
    excludeCredentials: (options.excludeCredentials || []).map((cred) => ({
      ...cred,
      id: base64urlToBuffer(cred.id),
    })),
  };
}

/**
 * Prépare les options de requête reçues du backend pour navigator.credentials.get()
 */
export function prepareRequestOptions(options) {
  return {
    ...options,
    challenge: base64urlToBuffer(options.challenge),
    allowCredentials: (options.allowCredentials || []).map((cred) => ({
      ...cred,
      id: base64urlToBuffer(cred.id),
    })),
  };
}

/**
 * Sérialise la réponse du credential pour l'envoyer au backend
 */
export function serializeCredential(credential) {
  const response = credential.response;
  const serialized = {
    id: credential.id,
    rawId: bufferToBase64url(credential.rawId),
    type: credential.type,
    response: {},
  };

  // Réponse d'enregistrement
  if (response.attestationObject) {
    serialized.response = {
      clientDataJSON: bufferToBase64url(response.clientDataJSON),
      attestationObject: bufferToBase64url(response.attestationObject),
    };
  }
  // Réponse d'authentification
  else {
    serialized.response = {
      clientDataJSON: bufferToBase64url(response.clientDataJSON),
      authenticatorData: bufferToBase64url(response.authenticatorData),
      signature: bufferToBase64url(response.signature),
      userHandle: response.userHandle
        ? bufferToBase64url(response.userHandle)
        : null,
    };
  }

  return serialized;
}
```

---

### Hook React — Enregistrement Face ID

```javascript
// hooks/useWebAuthnRegister.js
import { useState } from 'react';
import { prepareCreationOptions, serializeCredential } from '../utils/webauthn';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export function useWebAuthnRegister() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const registerFaceId = async (deviceName = 'Mon appareil') => {
    setLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('access_token');
      if (!token) throw new Error('Vous devez être connecté pour enregistrer un Face ID.');

      // ─── Étape 1 : obtenir les options du backend ───
      const beginRes = await fetch(`${API_BASE}/webauthn/register/begin/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      if (!beginRes.ok) {
        const err = await beginRes.json();
        throw new Error(err.error || 'Impossible de démarrer l\'enregistrement.');
      }

      const options = await beginRes.json();

      // ─── Étape 2 : déclencher le scan biométrique ───
      const publicKeyOptions = { publicKey: prepareCreationOptions(options) };
      const credential = await navigator.credentials.create(publicKeyOptions);

      if (!credential) throw new Error('Enregistrement annulé par l\'utilisateur.');

      // ─── Étape 3 : envoyer la réponse au backend ───
      const serialized = serializeCredential(credential);

      const completeRes = await fetch(`${API_BASE}/webauthn/register/complete/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ ...serialized, device_name: deviceName }),
      });

      if (!completeRes.ok) {
        const err = await completeRes.json();
        throw new Error(err.error || 'Échec de la vérification.');
      }

      const result = await completeRes.json();
      return { success: true, message: result.message };

    } catch (err) {
      // NotAllowedError = l'utilisateur a refusé / timeout
      if (err.name === 'NotAllowedError') {
        setError('Scan annulé ou refusé. Veuillez réessayer.');
      } else {
        setError(err.message);
      }
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  return { registerFaceId, loading, error };
}
```

---

### Hook React — Authentification Face ID

```javascript
// hooks/useWebAuthnLogin.js
import { useState } from 'react';
import { prepareRequestOptions, serializeCredential } from '../utils/webauthn';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export function useWebAuthnLogin() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loginWithFaceId = async (email) => {
    setLoading(true);
    setError(null);

    try {
      // ─── Étape 1 : obtenir le challenge du backend ───
      const beginRes = await fetch(`${API_BASE}/webauthn/login/begin/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      if (!beginRes.ok) {
        const err = await beginRes.json();
        throw new Error(err.error || 'Impossible de démarrer l\'authentification.');
      }

      const options = await beginRes.json();

      // ─── Étape 2 : déclencher le scan biométrique ───
      const publicKeyOptions = { publicKey: prepareRequestOptions(options) };
      const credential = await navigator.credentials.get(publicKeyOptions);

      if (!credential) throw new Error('Authentification annulée.');

      // ─── Étape 3 : envoyer la réponse signée au backend ───
      const serialized = serializeCredential(credential);

      const completeRes = await fetch(`${API_BASE}/webauthn/login/complete/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, ...serialized }),
      });

      if (!completeRes.ok) {
        const err = await completeRes.json();
        throw new Error(err.error || 'Authentification échouée.');
      }

      const { access, refresh, user } = await completeRes.json();

      // Sauvegarder les tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      return { success: true, user };

    } catch (err) {
      if (err.name === 'NotAllowedError') {
        setError('Scan annulé ou refusé. Veuillez réessayer.');
      } else {
        setError(err.message);
      }
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  };

  return { loginWithFaceId, loading, error };
}
```

---

### Composant React — Bouton Face ID

```jsx
// components/FaceIdLoginButton.jsx
import { useWebAuthnLogin } from '../hooks/useWebAuthnLogin';

export function FaceIdLoginButton({ email, onSuccess }) {
  const { loginWithFaceId, loading, error } = useWebAuthnLogin();

  // Vérifier si WebAuthn est supporté
  const isSupported =
    window.PublicKeyCredential !== undefined &&
    typeof navigator.credentials?.get === 'function';

  if (!isSupported) {
    return (
      <p className="text-gray-400 text-sm">
        ⚠️ Face ID non supporté sur ce navigateur/appareil.
      </p>
    );
  }

  const handleClick = async () => {
    const result = await loginWithFaceId(email);
    if (result.success) {
      onSuccess?.(result.user);
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <button
        onClick={handleClick}
        disabled={loading || !email}
        className="flex items-center gap-2 px-6 py-3 bg-black text-white rounded-xl
                   hover:bg-gray-800 disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all duration-200"
      >
        {loading ? (
          <>
            <span className="animate-spin">⏳</span>
            Scan en cours...
          </>
        ) : (
          <>
            <span className="text-xl">🪪</span>
            Se connecter avec Face ID
          </>
        )}
      </button>

      {error && (
        <p className="text-red-500 text-sm text-center max-w-xs">{error}</p>
      )}
    </div>
  );
}
```

---

### Composant React — Paramètres Face ID

```jsx
// components/FaceIdSettings.jsx
import { useState, useEffect } from 'react';
import { useWebAuthnRegister } from '../hooks/useWebAuthnRegister';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export function FaceIdSettings() {
  const [credentials, setCredentials] = useState([]);
  const [deviceName, setDeviceName] = useState('Mon appareil');
  const { registerFaceId, loading, error } = useWebAuthnRegister();

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    const token = localStorage.getItem('access_token');
    const res = await fetch(`${API_BASE}/webauthn/credentials/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      setCredentials(await res.json());
    }
  };

  const handleRegister = async () => {
    const result = await registerFaceId(deviceName);
    if (result.success) {
      await fetchCredentials();
      alert(result.message);
    }
  };

  const handleDelete = async (id, name) => {
    if (!confirm(`Supprimer "${name}" ?`)) return;
    const token = localStorage.getItem('access_token');
    const res = await fetch(`${API_BASE}/webauthn/credentials/${id}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });
    if (res.ok) {
      setCredentials((prev) => prev.filter((c) => c.id !== id));
    }
  };

  return (
    <div className="p-6 max-w-lg">
      <h2 className="text-xl font-bold mb-4">🔐 Gestion Face ID / Biométrie</h2>

      {/* Enregistrement */}
      <div className="border rounded-lg p-4 mb-6">
        <h3 className="font-semibold mb-3">Ajouter un nouvel appareil</h3>
        <input
          type="text"
          value={deviceName}
          onChange={(e) => setDeviceName(e.target.value)}
          placeholder="Nom de l'appareil (ex: iPhone 15)"
          className="w-full border rounded px-3 py-2 mb-3 text-sm"
        />
        <button
          onClick={handleRegister}
          disabled={loading}
          className="w-full bg-blue-600 text-white rounded-lg py-2 hover:bg-blue-700
                     disabled:opacity-50 transition-colors"
        >
          {loading ? '⏳ Scan en cours...' : '➕ Enregistrer Face ID'}
        </button>
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
      </div>

      {/* Liste des credentials */}
      <div>
        <h3 className="font-semibold mb-3">
          Appareils enregistrés ({credentials.length})
        </h3>
        {credentials.length === 0 ? (
          <p className="text-gray-500 text-sm">Aucun appareil enregistré.</p>
        ) : (
          <ul className="space-y-2">
            {credentials.map((cred) => (
              <li
                key={cred.id}
                className="flex items-center justify-between border rounded-lg px-4 py-3"
              >
                <div>
                  <p className="font-medium text-sm">{cred.device_name}</p>
                  <p className="text-xs text-gray-400">
                    Ajouté le {new Date(cred.created_at).toLocaleDateString('fr-FR')}
                    {cred.last_used_at && (
                      <>
                        {' '}· Utilisé le{' '}
                        {new Date(cred.last_used_at).toLocaleDateString('fr-FR')}
                      </>
                    )}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(cred.id, cred.device_name)}
                  className="text-red-500 hover:text-red-700 text-sm ml-4"
                  title="Supprimer"
                >
                  🗑️
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
```

---

## 7. Exemples cURL

### Étape 1 — Début d'enregistrement
```bash
curl -X POST http://localhost:8000/api/webauthn/register/begin/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### Étape 2 — Fin d'enregistrement
```bash
curl -X POST http://localhost:8000/api/webauthn/register/complete/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "CREDENTIAL_ID",
    "rawId": "CREDENTIAL_ID",
    "response": {
      "clientDataJSON": "BASE64URL...",
      "attestationObject": "BASE64URL..."
    },
    "type": "public-key",
    "device_name": "Mon iPhone"
  }'
```

### Étape 1 — Début d'authentification
```bash
curl -X POST http://localhost:8000/api/webauthn/login/begin/ \
  -H "Content-Type: application/json" \
  -d '{"email": "nilsen@example.com"}'
```

### Lister les credentials
```bash
curl -X GET http://localhost:8000/api/webauthn/credentials/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Supprimer un credential
```bash
curl -X DELETE http://localhost:8000/api/webauthn/credentials/1/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 8. Modèle BDD

Table : `core_webauthncredential`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | BIGINT PK | Clé primaire auto |
| `user_id` | FK → auth_user | Utilisateur propriétaire |
| `credential_id` | TEXT UNIQUE | ID du credential (base64url, généré par l'appareil) |
| `public_key` | TEXT | Clé publique COSE (base64url) |
| `sign_count` | INT | Compteur de signatures (anti-replay) |
| `aaguid` | VARCHAR(255) | Identifiant du modèle d'authenticator |
| `device_name` | VARCHAR(255) | Nom lisible ("iPhone 15 Face ID") |
| `created_at` | DATETIME | Date d'enregistrement |
| `last_used_at` | DATETIME NULL | Dernière utilisation |

**Migration :** `core/migrations/0036_webauthn_credential.py`

```bash
# Appliquer la migration
python manage.py migrate

# Vérifier
python manage.py showmigrations core
```

---

## 9. Notes de sécurité

### ✅ Ce qui est sécurisé par design
- **Biométrie locale** : Face ID ne quitte jamais l'iPhone/appareil
- **Clé privée non exportable** : générée dans le Secure Enclave de l'appareil
- **Protection anti-replay** : le `sign_count` est incrémenté à chaque connexion
- **Challenge unique** : nouveau challenge aléatoire à chaque tentative (TTL 2 min)
- **Lié au domaine** : un credential enregistré sur `portfolio.unityfianar.site` ne peut PAS être utilisé sur un autre domaine

### ⚙️ Configuration recommandée en production

```python
# settings.py — Production

# Cache Redis pour les challenges (multi-workers Gunicorn)
# pip install django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 300,
    }
}

# WebAuthn — domaine de production
WEBAUTHN_RP_ID = "portfolio.unityfianar.site"
WEBAUTHN_RP_NAME = "Portfolio Nilsen"
WEBAUTHN_ORIGIN = "https://portfolio.unityfianar.site"
```

### ⚠️ Compatibilité navigateurs

| Navigateur / Plateforme | Face ID | Touch ID | Windows Hello |
|------------------------|---------|----------|---------------|
| Safari iOS 14+ | ✅ | ✅ | — |
| Chrome Android 70+ | — | — | ✅ |
| Safari macOS 13+ | — | ✅ | — |
| Chrome / Edge Windows | — | — | ✅ |
| Firefox | ⚠️ Partiel | ⚠️ Partiel | ⚠️ Partiel |

> Vérifiez la compatibilité avec `window.PublicKeyCredential !== undefined`
> avant d'afficher le bouton Face ID.

---

## 10. Dépannage

### ❌ `InvalidStateError: The authenticator is already registered`
**Cause :** Credential déjà enregistré pour cet appareil.  
**Solution :** Supprimez l'ancien credential via `DELETE /api/webauthn/credentials/<id>/`.

---

### ❌ `NotAllowedError: The operation either timed out or was not allowed`
**Cause :** L'utilisateur a refusé le scan, ou le timeout a expiré.  
**Solution :** Réessayez l'enregistrement / l'authentification.

---

### ❌ `Challenge expiré ou introuvable`
**Cause :** Plus de 2 minutes se sont écoulées entre le `begin` et le `complete`.  
**Solution :** Recommencez depuis l'étape 1 (begin).

---

### ❌ `Vérification échouée : Invalid origin`
**Cause :** `WEBAUTHN_ORIGIN` dans `.env` ne correspond pas à l'URL depuis laquelle
le frontend envoie les requêtes.  
**Solution :** Vérifiez que `WEBAUTHN_ORIGIN=http://localhost:5173` (en dev)
correspond exactement à l'URL affichée dans votre navigateur.

---

### ❌ `Vérification échouée : Invalid rpId`
**Cause :** `WEBAUTHN_RP_ID` ne correspond pas au domaine du frontend.  
**Solution :** En développement, mettez `WEBAUTHN_RP_ID=localhost`.
En production, mettez le domaine sans `https://` ni chemin.

---

### ❌ En production : challenge non trouvé avec plusieurs workers Gunicorn
**Cause :** Le cache `FileBasedCache` peut être lent entre workers.  
**Solution :** Installez Redis et utilisez `django_redis.cache.RedisCache`.

```bash
pip install django-redis
```

---

*Dernière mise à jour : intégration WebAuthn 2.2.0 + Django 5.1.4*