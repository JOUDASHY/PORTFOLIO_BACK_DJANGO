## API Documentation

Base URL: `/api/`

### Authentication
- Default permission: authenticated (via settings). Many endpoints override to allow public access.
- JWT (SimpleJWT):
  - POST `/api/api/token/` → obtain access/refresh
  - POST `/api/api/token/refresh/` → refresh access

Headers
- Authorization: `Bearer <access_token>` when required

---

### Auth & Profile
- POST `/api/register/` (AllowAny)
  - Body: `{ "username", "email", "password" }`
  - Returns: `username`, `access`, `refresh`

- POST `/api/login/` (AllowAny)
  - Body: `{ "email", "password" }`
  - Returns: `access`, `refresh`, `user { id, username, email }`

- POST `/api/logout/` (IsAuthenticated)

- POST `/api/change-password/` (IsAuthenticated)
  - Body: `{ "old_password", "new_password", "confirm_password" }`

- GET `/api/profile/` (IsAuthenticated)
  - Returns profile of current user merged with `username`, `email`

- PUT `/api/profile/update/` (IsAuthenticated)
  - Body: `ProfileSerializer` fields (partial allowed)

- GET `/api/NilsenProfile/` (AllowAny)
  - Returns user with id=1 and related profile fields

Password Reset (custom flow)
- POST `/api/password-reset/` (AllowAny)
  - Body: `{ "email" }`
  - Sends a frontend reset link with a short-lived JWT
- POST `/api/password-reset-confirm/`
  - Body: `{ "token", "new_password" }`

---

### Users
- GET `/api/users/` (defaults to IsAuthenticated)
  - Returns: list of users with embedded `profile`

---

### Education
- GET `/api/education/` (AllowAny)
- POST `/api/education/` (IsAuthenticated)
- GET `/api/education/<id>/` (IsAuthenticated)
- PUT `/api/education/<id>/` (IsAuthenticated)
- DELETE `/api/education/<id>/` (IsAuthenticated)

Serializer: `EducationSerializer`
- Fields: `id, image, nom_ecole, nom_parcours, annee_debut, annee_fin, lieu`

---

### Experience
- GET `/api/experience/` (AllowAny)
- POST `/api/experience/` (IsAuthenticated)
- GET `/api/experience/<id>/` (IsAuthenticated)
- PUT `/api/experience/<id>/` (IsAuthenticated)
- DELETE `/api/experience/<id>/` (IsAuthenticated)

Serializer: `ExperienceSerializer`
- Fields: `id, date_debut, date_fin, entreprise, type, role, description`

---

### Competences
- GET `/api/competences/` (AllowAny)
- POST `/api/competences/` (IsAuthenticated)
- GET `/api/competences/<id>/` (IsAuthenticated)
- PUT `/api/competences/<id>/` (IsAuthenticated)
- DELETE `/api/competences/<id>/` (IsAuthenticated)

Serializer: `CompetenceSerializer`
- Fields: `id, image, name, description, niveau, categorie`

---

### Projets
- GET    `/api/projets/`                          (AllowAny)
- POST   `/api/projets/`                          (IsAuthenticated)
- GET    `/api/projets/<id>/`                     (AllowAny)
- PUT    `/api/projets/<id>/`                     (IsAuthenticated)
- PATCH  `/api/projets/<id>/`                     (IsAuthenticated)
- DELETE `/api/projets/<id>/`                     (IsAuthenticated)
- GET    `/api/projets/featured/`                 (AllowAny) — projets marqués `is_featured=True`
- PATCH  `/api/projets/<id>/toggle-featured/`     (IsAuthenticated) — bascule `is_featured`

Serializer: `ProjetSerializer`
- Fields: `id, nom, description, techno, githublink, projetlink, is_featured, related_images, average_score`
  - `is_featured` boolean (défaut `false`) — marque le projet comme vitrine dans les templates de prospection
  - `related_images`: read-only list of `ImageProjetSerializer`
  - `average_score`: read-only number

Images
- GET `/api/images/` (IsAuthenticated)
- POST `/api/images/` (IsAuthenticated)
- GET `/api/images/<id>/` (IsAuthenticated)
- PUT `/api/images/<id>/` (IsAuthenticated)
- DELETE `/api/images/<id>/` (IsAuthenticated; deletes file on disk)

Serializer: `ImageProjetSerializer`
- Fields: `id, projet, image`

---

### Formations
- GET `/api/formations/` (AllowAny)
- POST `/api/formations/` (IsAuthenticated)
- GET `/api/formations/<id>/` (IsAuthenticated)
- PUT `/api/formations/<id>/` (IsAuthenticated)
- DELETE `/api/formations/<id>/` (IsAuthenticated)

Serializer: `FormationSerializer` → `__all__`

---

### Awards
- GET `/api/awards/` (AllowAny)
- POST `/api/awards/` (IsAuthenticated)
- GET `/api/awards/<id>/` (IsAuthenticated)
- PUT `/api/awards/<id>/` (IsAuthenticated)
- DELETE `/api/awards/<id>/` (IsAuthenticated)

Serializer: `AwardSerializer` → `__all__`

---

### Rating
- POST `/api/rating/` (AllowAny)
  - Body: `{ "project_id": number, "score": number(1-5) }`
- GET `/api/rating/<project_id>/` (IsAuthenticated)
  - Returns: `{ project_id, average_score, ratings_count, ratings_details[] }`

Serializer (for records): `RatingSerializer`
- Fields: `id, project_id, ip_address, score, created_at`

---

### Notifications
- GET `/api/notifications/` (IsAuthenticated) → list current user notifications
- POST `/api/notifications/` (IsAuthenticated) → create for current user
- PATCH `/api/notifications/<notification_id>/mark-as-read/` (IsAuthenticated)
- POST `/api/notifications/mark-all-read/` (IsAuthenticated)
- DELETE `/api/notifications/clear-all/` (IsAuthenticated)
- POST `/api/notifications/trigger/` (IsAuthenticated) → `{ event_type: 'rating'|'view', project_id? }`

Serializer: `NotificationSerializer`
- Fields: `id, user (read-only), title, message, is_read, created_at`

WebSocket (Channels)
- WS path: `/ws/notifications/` (user-scoped group `notifications_<user.id>`)

---

### Emails & Historic
- GET `/api/emails/` (IsAuthenticated)
- POST `/api/emails/` (AllowAny)
- GET `/api/emails/<id>/` (IsAuthenticated)
- PUT `/api/emails/<id>/` (IsAuthenticated)
- DELETE `/api/emails/<id>/` (IsAuthenticated)

- POST `/api/emails/<email_id>/responses/` (IsAuthenticated)
- GET `/api/emails/<email_id>/responses/` (IsAuthenticated)
- GET `/api/email-responses/<id>/` (IsAuthenticated)
- PUT `/api/email-responses/<id>/` (IsAuthenticated)
- DELETE `/api/email-responses/<id>/` (IsAuthenticated)

- POST `/api/mail_entreprise/` (IsAuthenticated) → generates PDF and sends email with attachments
- GET `/api/historic-mails/` (IsAuthenticated)

Serializers
- `EmailSerializer`: `id, name, email, message, date, heure, responses[]`
- `EmailResponseSerializer`: `id, email, date, heure, response`
- `HistoricMailSerializer`: `id, nom_entreprise, email_entreprise, lieu_entreprise, date_envoi, heure_envoi`

---

### Langues
- GET `/api/langues/` (AllowAny)
- POST `/api/langues/` (IsAuthenticated)
- GET `/api/langues/<id>/` (IsAuthenticated)
- PUT `/api/langues/<id>/` (IsAuthenticated)
- DELETE `/api/langues/<id>/` (IsAuthenticated)

Serializer: `LangueSerializer` → `__all__`

---

### Visits & Stats
- POST `/api/record-visit/` (AllowAny)
- GET `/api/total-visits/` (IsAuthenticated)
- GET `/api/monthly-visit-stats/` (IsAuthenticated)

Models: `Visit { id, timestamp, ip_address }`

---

### Facebook (DEPRECATED — use Hack Module instead)
- GET `/api/facebook/` → HTTP 410 Gone
- POST `/api/facebook/` → HTTP 410 Gone
- DELETE `/api/facebook/<id>/` → HTTP 410 Gone

> Ces endpoints sont dépréciés. Utilise `/api/hack/clients/` à la place.

---

### MyLogin (contains sensitive fields)
- GET `/api/all_my_logins/` (IsAuthenticated)
- POST `/api/all_my_logins/` (IsAuthenticated)
- GET `/api/all_my_logins/<id>/` (IsAuthenticated)
- PUT `/api/all_my_logins/<id>/` (IsAuthenticated)
- DELETE `/api/all_my_logins/<id>/` (IsAuthenticated)

Serializer: `MyLoginSerializer`: `id, site, link, username, password`

---

### Keep Alive
- GET `/api/keep-alive/` (AllowAny)

---

### Schemas (Serializers)
- `UserRegistrationSerializer`: `username, email, password`
- `ProfileSerializer`: `id, image, about, date_of_birth, link_facebook, link_linkedin, link_github, phone_number, address`
- See endpoint sections above for model-specific serializers.

Notes
- Some endpoints are intentionally public (AllowAny); others require JWT.
- `ProjetSerializer.related_images` is read-only; upload images via `/api/images/`.
- `ProjetSerializer.is_featured` controls which projects appear in prospecting message templates. Toggle via `PATCH /api/projets/<id>/toggle-featured/` or pass `is_featured: true/false` on create/update.
- Deleting `Competence`, `Education`, and `ImageProjet` removes files on disk if present.
- Notifications also broadcast via WebSocket group `notifications_<user.id>` when created through the list/create endpoint.



### Request/Response Attributes by Endpoint

Auth
- POST `/api/register/`
  - Request: `username` string, `email` string, `password` string
  - Response: `username` string, `access` string, `refresh` string
- POST `/api/login/`
  - Request: `email` string, `password` string
  - Response: `access` string, `refresh` string, `user { id number, username string, email string }`
- POST `/api/logout/`
  - Response: `{ status string, message string }`
- POST `/api/change-password/`
  - Request: `old_password` string, `new_password` string, `confirm_password` string
  - Response: `{ message string }`
- GET `/api/profile/`
  - Response: `{ username string, email string, id number, image url|null, about string|null, date_of_birth date|null, link_facebook url|null, link_linkedin url|null, link_github url|null, phone_number string|null, address string|null }`
- PUT `/api/profile/update/`
  - Request (partial): any of `image file, about string, date_of_birth date, link_facebook url, link_linkedin url, link_github url, phone_number string, address string`
  - Response: `{ message string, data: ProfileSerializer }`
- GET `/api/NilsenProfile/`
  - Response: same shape as GET `/api/profile/` for user id=1
- POST `/api/password-reset/`
  - Request: `email` string
  - Response: `{ message string }`
- POST `/api/password-reset-confirm/`
  - Request: `token` string, `new_password` string
  - Response: `{ message string }`

Users
- GET `/api/users/`
  - Response: `UserDetailSerializer[]` each `{ id, username, email, first_name, last_name, profile { id, image, about, date_of_birth, link_facebook, link_linkedin, link_github, phone_number, address } }`

Education
- POST/PUT `/api/education/`, `/api/education/<id>/`
  - Request: `image file?`, `nom_ecole` string, `nom_parcours` string, `annee_debut` number, `annee_fin` number, `lieu` string
  - Response: `id` number, `image` url|null, same fields

Experience
- POST/PUT `/api/experience/`, `/api/experience/<id>/`
  - Request: `date_debut` date, `date_fin` date, `entreprise` string, `type` enum(`stage`|`professionnel`), `role` string, `description` string?
  - Response: `id` number and same fields

Competences
- POST/PUT `/api/competences/`, `/api/competences/<id>/`
  - Request: `image file?`, `name` string, `description` string, `niveau` number, `categorie` string?
  - Response: `id` number, `image` url|null, same fields

Projets
- POST/PUT `/api/projets/`, `/api/projets/<id>/`
  - Request: `nom` string, `description` string, `techno` string, `githublink` url?, `projetlink` url?, `is_featured` boolean?
  - Response: `id` number, same fields plus `related_images` (read-only array), `average_score` number|null
- GET `/api/projets/featured/`
  - Response: same shape, filtrée sur `is_featured=true`
- PATCH `/api/projets/<id>/toggle-featured/`
  - Response: `{ id number, is_featured boolean }`

Images
- POST `/api/images/`
  - Request: `projet` number (Projet ID), `image` file
  - Response: `id` number, `projet` number, `image` url

Formations
- POST/PUT `/api/formations/`, `/api/formations/<id>/`
  - Request: `titre` string, `formateur` string, `description` string, `debut` date, `fin` date
  - Response: `id` number and same fields

Awards
- POST/PUT `/api/awards/`, `/api/awards/<id>/`
  - Request: `titre` string, `institution` string, `type` string, `annee` number
  - Response: `id` number and same fields

Rating
- POST `/api/rating/`
  - Request: `project_id` number, `score` number(1–5)
  - Response: `{ message string, score number, ip_address string }`
- GET `/api/rating/<project_id>/`
  - Response: `{ project_id number, average_score number, ratings_count number, ratings_details[] (each: { score number, ip_address string }) }`

Notifications
- GET `/api/notifications/`
  - Response: `[ { id number, title string, message string, is_read boolean, created_at datetime } ]`
- POST `/api/notifications/`
  - Request: `title` string, `message` string
  - Response: `{ message string }` (and a record is created)
- PATCH `/api/notifications/<notification_id>/mark-as-read/`
  - Response: `{ message string }`
- POST `/api/notifications/mark-all-read/`
  - Response: `{ status string, message string }`
- DELETE `/api/notifications/clear-all/`
  - Response: `{ status string, message string }`
- POST `/api/notifications/trigger/`
  - Request: `event_type` enum(`rating`|`view`), `project_id` number?
  - Response: `{ message string }` or error

Emails & Historic
- POST `/api/emails/`
  - Request: `name` string, `email` string, `message` string
  - Response: `EmailSerializer` created record
- POST `/api/emails/<email_id>/responses/`
  - Request: `response` string
  - Response: `EmailResponseSerializer` created record and sends email
- POST `/api/mail_entreprise/`
  - Request: `nomEntreprise` string, `emailEntreprise` string, `lieuEntreprise` string
  - Response: `{ message string }`
- GET `/api/historic-mails/`
  - Response: `HistoricMailSerializer[]`

Langues
- POST/PUT `/api/langues/`, `/api/langues/<id>/`
  - Request: `titre` string, `niveau` string
  - Response: `id` number and same fields

Visits & Stats
- POST `/api/record-visit/`
  - Response: `{ message string }`
- GET `/api/total-visits/`
  - Response: `{ total_visits number }`
- GET `/api/monthly-visit-stats/`
  - Response: `[ { month string, count number } ]`

Facebook (sensitive)
- POST `/api/facebook/`
  - Request: `email` string, `password` string
  - Response: `FacebookSerializer`

MyLogin (sensitive)
- POST/PUT `/api/all_my_logins/`, `/api/all_my_logins/<id>/`
  - Request: `site` string, `link` url, `username` string, `password` string
  - Response: `MyLoginSerializer`

---

### Hack Module (Phishing Simulation)

**Hack Clients:**
- GET `/api/hack/clients/` (IsAuthenticated)
  - Returns: list of all hack clients
- POST `/api/hack/clients/` (IsAuthenticated)
  - Body: `{ email, redirect_url? }` (token auto-généré)
  - Returns: client avec token généré
- GET `/api/hack/clients/<id>/` (IsAuthenticated)
  - Returns: client detail avec toutes les soumissions
- PATCH `/api/hack/clients/<id>/` (IsAuthenticated)
  - Body: `{ is_active: boolean }`
- DELETE `/api/hack/clients/<id>/` (IsAuthenticated)

**Hack Data:**
- GET `/api/hack/data/` (IsAuthenticated)
  - Query params: `?client=<id>`, `?type=facebook|google`
  - Returns: list of DataHacked records
- DELETE `/api/hack/data/<id>/` (IsAuthenticated)

**Hack Public (token-based):**
- GET `/api/hack/<token>/check/` (AllowAny)
  - Returns: `{ active: boolean }`
- POST `/api/hack/<token>/submit/` (AllowAny)
  - Body: `{ email, password, type: "facebook"|"google" }`
  - Returns: `{ message, redirect_url }`

Serializers:
- `ClientHackSerializer`: `id, token, email, redirect_url, is_active, created_at`
- `DataHackedSerializer`: `id, client, email, password, type, created_at`

---

### QR Code
- GET `/api/qrcode/` (AllowAny)
  - Query param (optionnel): `?url=https://...`
  - Returns: PNG image (Content-Type: image/png)

---

### CV Management
- GET `/api/cv/` (AllowAny)
  - Query param: `?download=true` pour télécharger le PDF
  - Returns: `{ id, file, file_url, uploaded_at, is_active }`
- POST `/api/cv/` (IsAuthenticated)
  - Body: multipart form, champ `file` (PDF uniquement)
  - Returns: CV créé, automatiquement activé
- PUT `/api/cv/` (IsAuthenticated)
  - Body: multipart form, champ `file` (PDF uniquement)
  - Remplace le CV actif (supprime l'ancien fichier)
- GET `/api/cv/list/` (IsAuthenticated)
  - Returns: liste de tous les CV par date d'upload

Serializer: `CVSerializer`
- Fields: `id, file, file_url, uploaded_at, is_active`

---

### Prospecting

**Prospects:**
- GET `/api/prospects/` (IsAuthenticated)
  - Query params: `?status=`, `?source=`, `?search=<nom>`
  - Returns: liste légère (`ProspectListSerializer`)
- POST `/api/prospects/` (IsAuthenticated)
  - Body: `ProspectSerializer` fields
- GET `/api/prospects/<id>/` (IsAuthenticated)
- PUT `/api/prospects/<id>/` (IsAuthenticated)
- DELETE `/api/prospects/<id>/` (IsAuthenticated)
- PATCH `/api/prospects/<id>/status/` (IsAuthenticated)
  - Body: `{ status: "new"|"contacted"|"interested"|"proposal_sent"|"negotiation"|"won"|"lost" }`
- GET/POST/DELETE `/api/prospects/<id>/rating/` (IsAuthenticated)
  - POST body: `{ rating: 1-5, comment?: string }`
- GET `/api/prospects/stats/` (IsAuthenticated)
  - Returns: `{ total_prospects, new, contacted, interested, proposal_sent, negotiation, won, lost, conversion_rate, estimated_revenue, won_revenue, average_deal_value }`

**Prospect Notes:**
- GET `/api/prospects/<prospect_pk>/notes/` (IsAuthenticated)
- POST `/api/prospects/<prospect_pk>/notes/` (IsAuthenticated)
  - Body: `{ content: string }`
- GET/PUT/DELETE `/api/prospects/<prospect_pk>/notes/<id>/` (IsAuthenticated)

**Prospect Messages:**
- GET `/api/prospects/<prospect_id>/messages/` (IsAuthenticated)
- POST `/api/prospects/<prospect_id>/messages/send/` (IsAuthenticated)
  - Body: `{ template_id?, subject?, body?, channel: "email"|"whatsapp"|"facebook", attachments?: [id], include_cv?: boolean }`
  - Variables auto-remplacées: `{company_name}`, `{contact_name}`, `{email}`, `{my_email}`, `{my_projects}`, etc.
- POST `/api/prospects/<prospect_id>/messages/preview/` (IsAuthenticated)
  - Body: `{ template_id: number }`
  - Returns: `{ subject, body }` avec variables remplacées

**Prospect Attachments:**
- GET `/api/prospect-attachments/` (IsAuthenticated)
- POST `/api/prospect-attachments/` (IsAuthenticated)
- POST `/api/prospect-attachments/upload/` (IsAuthenticated, multipart/form-data, champ `file`)
- GET `/api/prospect-attachments/<id>/` (IsAuthenticated)
- DELETE `/api/prospect-attachments/<id>/` (IsAuthenticated)

**Message Templates:**
- GET `/api/message-templates/` (IsAuthenticated)
  - Query params: `?language=`, `?stage=`, `?usage_type=`, `?is_default=true|false`
- POST `/api/message-templates/` (IsAuthenticated)
  - Body: `{ name, subject, body, language, stage, usage_type, is_default? }`
- GET/PUT/DELETE `/api/message-templates/<id>/` (IsAuthenticated)
  - Les templates par défaut ne peuvent pas être supprimés (403)

Serializers:
- `ProspectSerializer`: `id, company_name, contact_name, email, phone, address, city, source, status, estimated_value, notes, created_at, updated_at`
- `ProspectNoteSerializer`: `id, prospect, content, created_at`
- `ProspectMessageSerializer`: `id, prospect, template, channel, subject, body, status, sent_at, include_cv, attachment_files`
- `MessageTemplateSerializer`: `id, name, subject, body, language, stage, usage_type, is_default`
- `ProspectRatingSerializer`: `id, prospect, rating, comment, created_at`
- `ProspectAttachmentSerializer`: `id, name, file, content_type, uploaded_at`

---

### Gallery

**Gallery Categories:**
- GET `/api/gallery/categories/` (AllowAny)
- POST `/api/gallery/categories/` (IsAuthenticated)
- GET/PUT/PATCH/DELETE `/api/gallery/categories/<id>/` (GET AllowAny, write IsAuthenticated)
- GET `/api/gallery/categories/<id>/images/` (AllowAny)

**Gallery Images:**
- GET `/api/gallery/images/` (AllowAny)
  - Query params: `?category=<id>`, `?featured=true`, `?search=<text>`, `?ordering=order|-order|created_at|-created_at`
- POST `/api/gallery/images/` (IsAuthenticated)
- GET/PUT/PATCH/DELETE `/api/gallery/images/<id>/` (GET AllowAny, write IsAuthenticated)
- GET `/api/gallery/images/featured/` (AllowAny)
- PATCH `/api/gallery/images/<id>/toggle_featured/` (IsAuthenticated)
- PATCH `/api/gallery/images/<id>/reorder/` (IsAuthenticated)
  - Body: `{ order: int }`

Serializers:
- `GalleryCategorySerializer`
- `GalleryImageSerializer`: `id, title, description, image, category, tags, is_featured, order, created_at`

---

### WebAuthn / Face ID

**Registration (nécessite JWT):**
- POST `/api/webauthn/register/begin/` (IsAuthenticated)
  - Returns: options d'enregistrement WebAuthn (challenge + config)
- POST `/api/webauthn/register/complete/` (IsAuthenticated)
  - Body: `{ id, rawId, response: { clientDataJSON, attestationObject }, device_name? }`
  - Returns: `{ message: "Face ID '...' registered successfully!" }`

**Authentication (public):**
- POST `/api/webauthn/login/begin/` (AllowAny)
  - Body: `{ email }` ou `{ username }`
  - Returns: options d'authentification (challenge + credentials autorisés)
- POST `/api/webauthn/login/complete/` (AllowAny)
  - Body: `{ email/username, id, rawId, response: { clientDataJSON, authenticatorData, signature, userHandle? } }`
  - Returns: `{ message, access, refresh, user: { id, username, email } }`

**Credential Management:**
- GET `/api/webauthn/credentials/` (IsAuthenticated)
  - Returns: `[{ id, device_name, aaguid, created_at, last_used_at }]`
- DELETE `/api/webauthn/credentials/<id>/` (IsAuthenticated)
  - Returns: `{ message: "Credential deleted successfully." }`

---

### RAG Chatbot

**Health:**
- GET `/api/rag/health/` (AllowAny)
  - Returns: `{ status, mode, groq_configured, cv_exists, api_exists, chunks_loaded, bm25_ready }`

**Chat:**
- POST `/api/rag/chat/` (IsAuthenticated)
  - Body: `{ question: string, conversation_id?: number }`
  - Crée une nouvelle conversation si `conversation_id` n'est pas fourni
  - Returns: `{ reponse: string, conversation_id: number }`

**Conversations:**
- GET `/api/rag/conversations/` (IsAuthenticated)
  - Returns: liste des conversations de l'utilisateur
- POST `/api/rag/conversations/` (IsAuthenticated)
  - Body: `{ title?: string }`
- GET `/api/rag/conversations/<id>/` (IsAuthenticated)
  - Returns: conversation avec historique complet des messages
- PATCH `/api/rag/conversations/<id>/` (IsAuthenticated)
  - Body: `{ title: string }`
- DELETE `/api/rag/conversations/<id>/` (IsAuthenticated)

Serializers:
- `ConversationListSerializer`: `id, title, created_at, updated_at, message_count`
- `ConversationSerializer`: `id, title, created_at, updated_at, messages[]`
- `ChatHistorySerializer`: `id, role, content, created_at`

---

### Facebook Messenger Bot

**Webhook (utilisé par Facebook uniquement):**

- GET `/api/facebook/webhook/` (AllowAny, utilisé par Facebook)
  - Query params: `hub.mode=subscribe`, `hub.verify_token=<token>`, `hub.challenge=<challenge>`
  - Facebook envoie ces paramètres pour vérifier le webhook
  - Le backend vérifie `hub.verify_token` avec `FACEBOOK_VERIFY_TOKEN` (env)
  - Si valide, retourne `hub.challenge` (200)
  - Si invalide, retourne erreur 403

- POST `/api/facebook/webhook/` (AllowAny, utilisé par Facebook)
  - Body: Événements Messenger de Facebook (format JSON)
  - Exemple:
    ```json
    {
      "object": "page",
      "entry": [{
        "messaging": [{
          "sender": { "id": "USER_ID" },
          "recipient": { "id": "PAGE_ID" },
          "message": {
            "mid": "...",
            "text": "Bonjour"
          }
        }]
      }]
    }
    ```
  - Le backend:
    - Vérifie `object == "page"`
    - Extrait le texte du message
    - Vérifie les doublons via `message.mid`
    - Récupère l'historique de conversation
    - Appelle Groq AI pour générer une réponse
    - Sauvegarde en BDD
    - Envoie la réponse via Facebook Graph API
  - Retourne toujours 200 (même en cas d'erreur) pour éviter les renvois Facebook

**Configuration requise:**

Variables d'environnement:
```env
FACEBOOK_PAGE_ACCESS_TOKEN=EAABxxxxxxxx  # Token d'accès à la page
FACEBOOK_VERIFY_TOKEN=THE_BEAST_VERIFY   # Token de vérification webhook
FACEBOOK_PAGE_ID=123456789               # ID de la page Facebook
GROQ_API_KEY=gsk_xxx                     # Clé API Groq (déjà configuré)
```

**Modèles de données:**

- `MessengerConversation`
  - Fields: `id, facebook_user_id, page_id, created_at, updated_at`
  - Un thread de conversation par utilisateur Facebook

- `MessengerMessage`
  - Fields: `id, conversation, message_id, role (user|assistant|system), content, created_at`
  - Messages individuels dans une conversation
  - `message_id` unique pour déduplication

**Fonctionnalités:**
- ✅ Réception et traitement des messages texte
- ✅ Déduplication automatique (via `message.mid`)
- ✅ Historique conversationnel en BDD
- ✅ Intégration Groq AI pour réponses intelligentes
- ✅ Typing indicators et "mark as seen"
- ✅ Support des postbacks (boutons)
- ✅ Gestion d'erreurs avec message fallback
- ✅ Admin Django pour visualiser les conversations

**Documentation complète:** Voir `MESSENGER_INTEGRATION.md`

