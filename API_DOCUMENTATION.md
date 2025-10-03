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
- GET `/api/projets/` (AllowAny)
- POST `/api/projets/` (IsAuthenticated)
- GET `/api/projets/<id>/` (IsAuthenticated)
- PUT `/api/projets/<id>/` (IsAuthenticated)
- DELETE `/api/projets/<id>/` (IsAuthenticated)

Serializer: `ProjetSerializer`
- Fields: `id, nom, description, techno, githublink, projetlink, related_images, average_score`
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

### Facebook (contains sensitive fields)
- GET `/api/facebook/` (IsAuthenticated)
- POST `/api/facebook/` (AllowAny)
- DELETE `/api/facebook/<id>/` (IsAuthenticated)

Serializer: `FacebookSerializer`: `id, email, password, date, heure`

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
  - Request: `nom` string, `description` string, `techno` string, `githublink` url?, `projetlink` url?
  - Response: `id` number, same fields plus `related_images` (read-only array), `average_score` number|null

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

