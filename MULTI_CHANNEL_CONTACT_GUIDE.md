# Multi-Channel Contact System Guide

## 🎯 Overview

The system now supports **3 contact channels** for prospects:
- ✅ **Email** - Automatic sending via backend (free)
- ✅ **WhatsApp** - Manual redirection (free app)
- ✅ **Facebook Messenger** - Manual redirection (free)

---

## 📋 Frontend Workflow

### Step 1: Select Contact Channels

```html
<!-- Form Example -->
<form id="contact-form">
  <h3>Contact Methods</h3>
  
  <!-- Email (Automatic) -->
  <label>
    <input type="checkbox" name="channels" value="email" checked>
    📧 Email (Automatic send)
  </label>
  
  <!-- WhatsApp (Manual) -->
  <label>
    <input type="checkbox" name="channels" value="whatsapp">
    📱 WhatsApp (Open in app)
  </label>
  
  <!-- Facebook (Manual) -->
  <label>
    <input type="checkbox" name="channels" value="facebook">
    💬 Facebook Messenger (Open in browser)
  </label>
  
  <button type="submit">Send Message</button>
</form>
```

---

### Step 2: Handle Submission (JavaScript)

```javascript
async function sendProspectMessage(prospectId, formData) {
  const channels = formData.channels || ['email']; // Default to email
  
  // For each selected channel
  for (const channel of channels) {
    if (channel === 'email') {
      // ✅ BACKEND: Send email automatically
      await sendEmail(prospectId, formData);
      
    } else if (channel === 'whatsapp') {
      // 📱 FRONTEND: Redirect to WhatsApp
      openWhatsApp(prospectId, formData);
      
    } else if (channel === 'facebook') {
      // 💬 FRONTEND: Redirect to Facebook Messenger
      openFacebookMessenger(prospectId, formData);
    }
  }
}

// Send Email via Backend
async function sendEmail(prospectId, formData) {
  try {
    const response = await fetch(`/api/prospects/${prospectId}/messages/send/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        template_id: formData.template_id,
        channel: 'email',  // Log as email
        subject: formData.subject,
        body: formData.body
      })
    });
    
    if (response.ok) {
      console.log('✅ Email sent successfully');
    }
  } catch (error) {
    console.error('❌ Email send failed:', error);
  }
}

// Open WhatsApp (Frontend Redirection)
function openWhatsApp(prospectId, formData) {
  // Get prospect data
  const prospect = getProspectData(prospectId);
  
  // Build message
  const message = encodeURIComponent(formData.body);
  
  // Build WhatsApp URL
  const whatsappUrl = `https://wa.me/${prospect.whatsapp_phone}?text=${message}`;
  
  // Log the action (optional)
  logMessage(prospectId, {
    channel: 'whatsapp',
    subject: formData.subject,
    body: formData.body
  });
  
  // Open WhatsApp
  window.open(whatsappUrl, '_blank');
}

// Open Facebook Messenger (Frontend Redirection)
function openFacebookMessenger(prospectId, formData) {
  // Get prospect data
  const prospect = getProspectData(prospectId);
  
  // Build Facebook Messenger URL
  const fbUrl = prospect.facebook_url || `https://m.me/${prospect.contact_name}`;
  
  // Log the action (optional)
  logMessage(prospectId, {
    channel: 'facebook',
    subject: formData.subject,
    body: formData.body
  });
  
  // Open Messenger
  window.open(fbUrl, '_blank');
}

// Log message to backend (for tracking)
async function logMessage(prospectId, messageData) {
  try {
    await fetch(`/api/prospects/${prospectId}/messages/send/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        ...messageData,
        channel: messageData.channel || 'email'
      })
    });
  } catch (error) {
    console.error('Failed to log message:', error);
  }
}
```

---

## 🔧 Backend API Endpoints

### 1. Send/Log Message

```http
POST /api/prospects/{id}/messages/send/
```

**Request Body:**
```json
{
  "template_id": 1,              // Optional: Use template
  "channel": "email",            // email, whatsapp, or facebook
  "subject": "Your subject here",
  "body": "Your message body"
}
```

**Response:**
```json
{
  "id": 1,
  "prospect": 1,
  "template": 1,
  "channel": "email",
  "channel_display": "Email",
  "subject": "Web development for Your Company",
  "body": "Hello...",
  "status": "sent",
  "sent_at": "2026-03-16T12:00:00Z",
  "created_at": "2026-03-16T12:00:00Z"
}
```

---

### 2. List Messages

```http
GET /api/prospects/{id}/messages/
```

**Response:**
```json
[
  {
    "id": 1,
    "channel": "email",
    "channel_display": "Email",
    "subject": "...",
    "body": "...",
    "status": "sent",
    "sent_at": "2026-03-16T12:00:00Z"
  },
  {
    "id": 2,
    "channel": "whatsapp",
    "channel_display": "WhatsApp",
    "subject": "",
    "body": "Hello...",
    "status": "sent",
    "sent_at": "2026-03-16T12:05:00Z"
  }
]
```

---

## 📊 Prospect Model Fields

New fields added to Prospect model:

```json
{
  "id": 1,
  "company_name": "TechCorp",
  "email": "contact@techcorp.com",
  "phone": "+261 XX XX XXX XX",
  "whatsapp_phone": "+261 XX XX XXX XX",  // NEW: WhatsApp number
  "facebook_url": "https://facebook.com/techcorp",  // NEW: FB page
  "has_website": false,
  "has_facebook": true
}
```

---

## 🎯 Complete Example

### Full Frontend Flow

```javascript
// Form submission handler
document.getElementById('contact-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const channels = Array.from(formData.getAll('channels'));
  const prospectId = 123;
  
  // Show loading
  showLoading('Sending messages...');
  
  try {
    // Process each channel
    for (const channel of channels) {
      if (channel === 'email') {
        await sendEmail(prospectId, {
          template_id: formData.get('template_id'),
          subject: formData.get('subject'),
          body: formData.get('body')
        });
        showMessage('✅ Email sent!');
        
      } else if (channel === 'whatsapp') {
        openWhatsApp(prospectId, {
          body: formData.get('body')
        });
        showMessage('📱 Opening WhatsApp...');
        
      } else if (channel === 'facebook') {
        openFacebookMessenger(prospectId, {});
        showMessage('💬 Opening Messenger...');
      }
    }
    
    // Update UI
    hideLoading();
    showSuccess('All messages processed!');
    
  } catch (error) {
    hideLoading();
    showError('Error: ' + error.message);
  }
});
```

---

## ✅ Summary

| Channel | How It Works | Cost | Automation |
|---------|--------------|------|------------|
| **Email** | Backend sends via SMTP | Free | ✅ 100% Auto |
| **WhatsApp** | Frontend opens `wa.me` link | Free | ❌ Manual |
| **Facebook** | Frontend opens Messenger URL | Free | ❌ Manual |

---

## 🚀 Quick Start

1. **Backend**: Already configured (JWT auth required)
2. **Frontend**: Add checkboxes for channels
3. **Logic**: 
   - Email → Call backend API
   - WhatsApp/FB → Redirect user
4. **Tracking**: All actions logged in database

**Ready to use!** 🎉
