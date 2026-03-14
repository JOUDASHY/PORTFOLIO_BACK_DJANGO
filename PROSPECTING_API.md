# Prospecting & Internship Module API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints require JWT authentication:
```
Authorization: Bearer <your_jwt_token>
```

---

## Unified Message Templates System

The `MessageTemplate` model now supports **two usage types**:
- `prospecting` - For sales/prospecting emails (selling websites)
- `internship` - For internship applications (with PDF generation)

### Filter by Usage Type
```bash
# Get all prospecting templates
GET /api/message-templates/?usage_type=prospecting

# Get all internship templates
GET /api/message-templates/?usage_type=internship

# Filter by language and type
GET /api/message-templates/?usage_type=internship&language=fr

# Filter by stage and type
GET /api/message-templates/?usage_type=internship&stage=initial
```

---

## Prospects

### List Prospects
```
GET /prospects/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | string | Filter by status: `new`, `contacted`, `interested`, `proposal_sent`, `negotiation`, `won`, `lost` |
| `source` | string | Filter by source: `google_maps`, `referral`, `social`, `direct`, `other` |
| `search` | string | Search by company name |

**Response:**
```json
[
  {
    "id": 1,
    "company_name": "Restaurant Chez Mario",
    "contact_name": "Mario Dupont",
    "email": "mario@restaurant.fr",
    "phone": "06 12 34 56 78",
    "status": "new",
    "status_display": "New",
    "estimated_value": "300.00",
    "city": "Paris",
    "notes_count": 2,
    "messages_count": 1,
    "created_at": "2026-03-13T14:00:00Z",
    "updated_at": "2026-03-13T14:00:00Z"
  }
]
```

---

### Create Prospect
```
POST /prospects/
```

**Request Body:**
```json
{
  "company_name": "Restaurant Chez Mario",
  "contact_name": "Mario Dupont",
  "email": "mario@restaurant.fr",
  "phone": "06 12 34 56 78",
  "address": "15 rue de la Paix",
  "city": "Paris",
  "google_maps_url": "https://maps.google.com/...",
  "website_url": "",
  "has_website": false,
  "has_facebook": true,
  "estimated_value": 300.00,
  "source": "google_maps",
  "notes": "Found on Google Maps, no website"
}
```

---

### Get Prospect Details
```
GET /prospects/{id}/
```

**Response:** Includes nested `notes` and `messages` arrays.

---

### Update Prospect
```
PUT /prospects/{id}/
```

---

### Delete Prospect
```
DELETE /prospects/{id}/
```

---

### Update Prospect Status
```
PATCH /prospects/{id}/status/
```

**Request Body:**
```json
{
  "status": "interested"
}
```

---

### Dashboard Statistics
```
GET /prospects/stats/
```

**Response:**
```json
{
  "total_prospects": 45,
  "new": 20,
  "contacted": 10,
  "interested": 5,
  "proposal_sent": 3,
  "negotiation": 2,
  "won": 3,
  "lost": 2,
  "conversion_rate": "20.0%",
  "estimated_revenue": 1500.00,
  "won_revenue": 900.00,
  "average_deal_value": 300.00
}
```

---

## Prospect Notes

### List Notes
```
GET /prospects/{prospect_id}/notes/
```

### Add Note
```
POST /prospects/{prospect_id}/notes/
```

**Request Body:**
```json
{
  "content": "Called client, they are interested"
}
```

---

## Prospect Messages

### List Messages
```
GET /prospects/{prospect_id}/messages/
```

---

### Send Message (Log)
```
POST /prospects/{prospect_id}/messages/send/
```

**Request Body (using template):**
```json
{
  "template_id": 1
}
```

**Request Body (custom message):**
```json
{
  "subject": "Custom subject",
  "body": "Custom message body"
}
```

**Response:**
```json
{
  "id": 1,
  "prospect": 1,
  "template": 1,
  "subject": "Création de site web pour Restaurant Chez Mario",
  "body": "Bonjour Mario Dupont,\n\nJe suis développeur web...",
  "status": "sent",
  "sent_at": "2026-03-13T14:30:00Z",
  "created_at": "2026-03-13T14:30:00Z"
}
```

---

### Preview Message
```
POST /prospects/{prospect_id}/messages/preview/
```

**Request Body:**
```json
{
  "template_id": 1
}
```

**Response:**
```json
{
  "subject": "Création de site web pour Restaurant Chez Mario",
  "body": "Bonjour Mario Dupont,\n\nJe suis développeur web..."
}
```

---

## Message Templates

### List Templates
```
GET /message-templates/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `language` | string | `fr` or `en` |
| `stage` | string | `initial`, `follow_up`, `proposal`, `closing` (prospecting) or `thank_you`, `acceptance` (internship) |
| `usage_type` | string | `prospecting` or `internship` |

**Response:**
```json
[
  {
    "id": 1,
    "name": "Premier contact",
    "language": "fr",
    "stage": "initial",
    "stage_display": "Initial Contact",
    "usage_type": "prospecting",
    "usage_type_display": "Prospecting (Sales)",
    "subject": "Création de site web pour {company_name}",
    "body": "Bonjour {contact_name}...",
    "cover_letter_html": "",
    "is_default": true,
    "created_at": "2026-03-13T14:00:00Z",
    "updated_at": "2026-03-13T14:00:00Z"
  },
  {
    "id": 9,
    "name": "Candidature Stage Dev Web",
    "language": "fr",
    "stage": "initial",
    "stage_display": "Initial Contact",
    "usage_type": "internship",
    "usage_type_display": "Internship Request",
    "subject": "Candidature spontanée pour un stage en développement web",
    "body": "Madame, Monsieur...",
    "cover_letter_html": "<html>...</html>",
    "is_default": true,
    "created_at": "2026-03-14T10:00:00Z",
    "updated_at": "2026-03-14T10:00:00Z"
  }
]
```

---

### Create Template
```
POST /message-templates/
```

**Request Body:**
```json
{
  "name": "Custom Template",
  "language": "fr",
  "stage": "initial",
  "subject": "Subject with {company_name}",
  "body": "Hello {contact_name}...",
  "is_default": false
}
```

---

### Update/Delete Template
```
PUT /message-templates/{id}/
DELETE /message-templates/{id}/
```

---

## Template Variables

### Prospecting Variables
| Variable | Replaced By |
|----------|-------------|
| `{company_name}` | Prospect's company name |
| `{contact_name}` | Contact person name |
| `{email}` | Prospect's email |
| `{phone}` | Prospect's phone |
| `{address}` | Full address |
| `{city}` | City |
| `{estimated_value}` | Estimated project value |

### Internship Variables
| Variable | Replaced By |
|----------|-------------|
| `{company_name}` | Company name |
| `{contact_name}` | Contact person name |
| `{city}` | City |
| `{student_name}` | Student name (you) |
| `{school_name}` | School name (e.g., "ENI") |
| `{internship_type}` | Type of internship (e.g., "Développement Web") |
| `{internship_duration}` | Duration (e.g., "3 mois") |
| `{internship_start_date}` | Start date |
| `{email}` | Your email |
| `{phone}` | Your phone |

---

## Status Pipeline

```
NEW → CONTACTED → INTERESTED → PROPOSAL_SENT → NEGOTIATION → WON
                                                        ↓
                                                      LOST
```

| Status | Description |
|--------|-------------|
| `new` | Just found, not contacted |
| `contacted` | First message sent |
| `interested` | Client responded positively |
| `proposal_sent` | Price quote sent |
| `negotiation` | Discussing details |
| `won` | Deal closed! |
| `lost` | Not interested / no response |
