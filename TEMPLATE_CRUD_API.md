# Message Template CRUD API Documentation

## 🎯 Overview

Complete CRUD (Create, Read, Update, Delete) API for managing message templates.

**Base URL:**
```
http://localhost:8000/api/message-templates/
```

---

## 🔐 Authentication

All endpoints require JWT authentication:

```http
Authorization: Bearer <your_jwt_token>
```

---

## 📋 Available Operations

### 1️⃣ **LIST All Templates (READ)**

```http
GET /api/message-templates/
```

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `language` | string | ❌ | Filter by language: `fr` or `en` |
| `stage` | string | ❌ | Filter by stage: `initial`, `follow_up`, `proposal`, `closing`, `thank_you`, `acceptance` |
| `usage_type` | string | ❌ | Filter by type: `prospecting` or `internship` |
| `is_default` | boolean | ❌ | Filter: `true` (system templates) or `false` (user-created) |

#### Examples

```javascript
// Get all templates
GET /api/message-templates/

// Get only French templates
GET /api/message-templates/?language=fr

// Get only internship templates
GET /api/message-templates/?usage_type=internship

// Get only user-created templates (not system defaults)
GET /api/message-templates/?is_default=false

// Get French prospecting templates, initial stage
GET /api/message-templates/?language=fr&usage_type=prospecting&stage=initial
```

#### Response

```json
[
  {
    "id": 9,
    "name": "Candidature Stage Dev Web",
    "language": "fr",
    "stage": "initial",
    "stage_display": "Initial Contact",
    "usage_type": "internship",
    "usage_type_display": "Internship Request",
    "subject": "Candidature spontanée pour un stage en développement web",
    "body": "Cher(e) responsable {company_name},\n\nÉtudiant en 3ème année...",
    "cover_letter_html": "<!DOCTYPE html><html>...</html>",
    "is_default": true,
    "created_at": "2026-03-14T10:00:00Z",
    "updated_at": "2026-03-14T10:00:00Z"
  },
  {
    "id": 25,
    "name": "My Custom Template",
    "language": "fr",
    "stage": "initial",
    "stage_display": "Initial Contact",
    "usage_type": "prospecting",
    "usage_type_display": "Prospecting (Sales)",
    "subject": "Custom subject for {company_name}",
    "body": "Custom body...",
    "cover_letter_html": "",
    "is_default": false,
    "created_at": "2026-03-16T14:00:00Z",
    "updated_at": "2026-03-16T14:00:00Z"
  }
]
```

---

### 2️⃣ **GET Single Template (READ)**

```http
GET /api/message-templates/{id}/
```

#### Example

```javascript
GET /api/message-templates/9/
```

#### Response

```json
{
  "id": 9,
  "name": "Candidature Stage Dev Web",
  "language": "fr",
  "stage": "initial",
  "stage_display": "Initial Contact",
  "usage_type": "internship",
  "usage_type_display": "Internship Request",
  "subject": "Candidature spontanée pour un stage en développement web",
  "body": "Cher(e) responsable {company_name},\n\nÉtudiant en 3ème année...",
  "cover_letter_html": "<!DOCTYPE html><html>...</html>",
  "is_default": true,
  "created_at": "2026-03-14T10:00:00Z",
  "updated_at": "2026-03-14T10:00:00Z"
}
```

---

### 3️⃣ **CREATE Template (CREATE)**

```http
POST /api/message-templates/
```

#### Request Body

```json
{
  "name": "My Custom Prospect Template",
  "language": "fr",                    // Required: 'fr' or 'en'
  "stage": "initial",                  // Required: initial, follow_up, proposal, closing, thank_you, acceptance
  "usage_type": "prospecting",         // Required: prospecting or internship
  "subject": "Proposition pour {company_name}",
  "body": "Bonjour {contact_name},\n\nJe suis développeur web...",
  "cover_letter_html": "",             // Optional: HTML for PDF generation
  "is_default": false                  // Optional: default false
}
```

#### Required Fields

- `name`: Template name
- `language`: `fr` or `en`
- `stage`: One of `initial`, `follow_up`, `proposal`, `closing`, `thank_you`, `acceptance`
- `usage_type`: `prospecting` or `internship`

#### Optional Fields

- `subject`: Email subject line
- `body`: Message body
- `cover_letter_html`: HTML template for PDF generation (internship only)
- `is_default`: Mark as system template (default: false)

#### Example

```javascript
const response = await fetch('/api/message-templates/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    name: "Relance Client Intéressé",
    language: "fr",
    stage: "follow_up",
    usage_type: "prospecting",
    subject: "Suite à notre discussion - {company_name}",
    body: "Bonjour {contact_name},\n\nJe reviens vers vous suite à notre échange...",
    cover_letter_html: "",
    is_default: false
  })
});

const template = await response.json();
console.log('Created template ID:', template.id);
```

#### Response (201 Created)

```json
{
  "id": 26,
  "name": "Relance Client Intéressé",
  "language": "fr",
  "stage": "follow_up",
  "stage_display": "Follow Up",
  "usage_type": "prospecting",
  "usage_type_display": "Prospecting (Sales)",
  "subject": "Suite à notre discussion - {company_name}",
  "body": "Bonjour {contact_name},\n\nJe reviens vers vous suite à notre échange...",
  "cover_letter_html": "",
  "is_default": false,
  "created_at": "2026-03-16T14:30:00Z",
  "updated_at": "2026-03-16T14:30:00Z"
}
```

---

### 4️⃣ **UPDATE Template (UPDATE)**

```http
PUT /api/message-templates/{id}/
```

#### Request Body (Partial Update with PATCH)

```http
PATCH /api/message-templates/{id}/
```

#### Example - Full Update (PUT)

```javascript
const response = await fetch('/api/message-templates/26/', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    name: "Updated Template Name",
    language: "en",
    stage: "initial",
    usage_type: "prospecting",
    subject: "New subject",
    body: "New body content",
    cover_letter_html: "",
    is_default: false
  })
});
```

#### Example - Partial Update (PATCH)

```javascript
const response = await fetch('/api/message-templates/26/', {
  method: 'PATCH',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    // Only update specific fields
    "subject": "Updated subject here"
  })
});
```

#### Response (200 OK)

```json
{
  "id": 26,
  "name": "Updated Template Name",
  "language": "en",
  "stage": "initial",
  "stage_display": "Initial Contact",
  "usage_type": "prospecting",
  "usage_type_display": "Prospecting (Sales)",
  "subject": "Updated subject here",
  "body": "New body content",
  "cover_letter_html": "",
  "is_default": false,
  "created_at": "2026-03-16T14:30:00Z",
  "updated_at": "2026-03-16T14:35:00Z"  // Updated timestamp
}
```

---

### 5️⃣ **DELETE Template (DELETE)**

```http
DELETE /api/message-templates/{id}/
```

#### ⚠️ Restrictions

**Cannot delete default system templates!** (`is_default=true`)

#### Example - Delete User Template (Allowed)

```javascript
const response = await fetch('/api/message-templates/26/', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

if (response.ok) {
  console.log('Template deleted successfully');
} else if (response.status === 403) {
  const error = await response.json();
  console.error('Cannot delete:', error.detail);
}
```

#### Example - Delete System Template (Forbidden)

```javascript
// Try to delete template ID 9 (default system template)
const response = await fetch('/api/message-templates/9/', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

// Response: 403 Forbidden
{
  "detail": "Cannot delete default system templates."
}
```

#### Response (204 No Content)

Successful deletion returns **204 No Content** (empty body).

---

## 🎯 Template Variables

### Prospecting Templates

Use these variables in `subject` and `body`:

| Variable | Replaced By |
|----------|-------------|
| `{company_name}` | Prospect's company name |
| `{contact_name}` | Contact person name |
| `{email}` | Prospect's email |
| `{phone}` | Prospect's phone |
| `{address}` | Full address |
| `{city}` | City |
| `{estimated_value}` | Estimated project value |

### Internship Templates

| Variable | Replaced By |
|----------|-------------|
| `{company_name}` | Company name |
| `{contact_name}` | Contact person name |
| `{city}` | City |
| `{student_name}` | Student name (you) |
| `{school_name}` | School name (e.g., "ENI") |
| `{internship_type}` | Type of internship |
| `{internship_duration}` | Duration (e.g., "3 mois") |
| `{internship_start_date}` | Start date |
| `{email}` | Your email |
| `{phone}` | Your phone |

---

## 📊 Complete CRUD Example

### Frontend Template Manager

```javascript
class TemplateManager {
  constructor() {
    this.baseUrl = '/api/message-templates/';
    this.token = localStorage.getItem('token');
  }

  // CREATE
  async createTemplate(templateData) {
    const response = await fetch(this.baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify(templateData)
    });
    
    if (!response.ok) throw new Error('Failed to create template');
    return await response.json();
  }

  // READ (List)
  async listTemplates(filters = {}) {
    const params = new URLSearchParams(filters);
    const response = await fetch(`${this.baseUrl}?${params}`, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });
    
    if (!response.ok) throw new Error('Failed to fetch templates');
    return await response.json();
  }

  // READ (Single)
  async getTemplate(id) {
    const response = await fetch(`${this.baseUrl}/${id}/`, {
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });
    
    if (!response.ok) throw new Error('Template not found');
    return await response.json();
  }

  // UPDATE
  async updateTemplate(id, updates) {
    const response = await fetch(`${this.baseUrl}/${id}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`
      },
      body: JSON.stringify(updates)
    });
    
    if (!response.ok) throw new Error('Failed to update template');
    return await response.json();
  }

  // DELETE
  async deleteTemplate(id) {
    const response = await fetch(`${this.baseUrl}/${id}/`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${this.token}`
      }
    });
    
    if (response.status === 403) {
      throw new Error('Cannot delete default system templates');
    }
    if (!response.ok) throw new Error('Failed to delete template');
    return true;
  }
}

// Usage Example
const manager = new TemplateManager();

// Create custom template
await manager.createTemplate({
  name: "My Custom Follow Up",
  language: "en",
  stage: "follow_up",
  usage_type: "prospecting",
  subject: "Following up - {company_name}",
  body: "Hi {contact_name},\n\nJust checking in...",
  is_default: false
});

// List all user-created templates
const templates = await manager.listTemplates({ is_default: false });
console.log('My templates:', templates);

// Update a template
await manager.updateTemplate(26, {
  subject: "Updated subject"
});

// Delete a template
await manager.deleteTemplate(26);
```

---

## 🔒 Permissions

| Operation | Permission Required | Notes |
|-----------|---------------------|-------|
| **LIST** | IsAuthenticated | Anyone authenticated can list |
| **GET** | IsAuthenticated | Anyone authenticated can view |
| **CREATE** | IsAuthenticated | Anyone authenticated can create |
| **UPDATE** | IsAuthenticated | Anyone authenticated can update |
| **DELETE** | IsAuthenticated | ❌ Cannot delete `is_default=true` |

---

## 📝 Best Practices

### 1. **Always Set `is_default=false` for User Templates**

```javascript
// ✅ Good
{
  "name": "My Template",
  "is_default": false  // Explicitly mark as user template
}

// ⚠️ Risky (defaults to false, but be explicit)
{
  "name": "My Template"
}
```

### 2. **Use PATCH for Partial Updates**

```javascript
// ✅ Better - Only update what changed
PATCH /api/message-templates/26/
{
  "subject": "New subject"
}

// ❌ Unnecessary - Send entire object
PUT /api/message-templates/26/
{
  "name": "...",
  "language": "...",
  "stage": "...",
  "subject": "New subject",  // Only this changed
  "body": "..."
}
```

### 3. **Handle Deletion Errors Gracefully**

```javascript
try {
  await manager.deleteTemplate(9);  // System template
} catch (error) {
  if (error.message.includes('Cannot delete')) {
    alert('This is a system template and cannot be deleted');
  } else {
    alert('Delete failed: ' + error.message);
  }
}
```

---

## ✅ Summary

| Operation | Method | Endpoint | Protected |
|-----------|--------|----------|-----------|
| **List** | GET | `/api/message-templates/` | ✅ Yes |
| **Get One** | GET | `/api/message-templates/{id}/` | ✅ Yes |
| **Create** | POST | `/api/message-templates/` | ✅ Yes |
| **Update** | PUT/PATCH | `/api/message-templates/{id}/` | ✅ Yes |
| **Delete** | DELETE | `/api/message-templates/{id}/` | ✅ Yes* |

*Cannot delete system templates (`is_default=true`)

---

**Ready to use!** 🚀
