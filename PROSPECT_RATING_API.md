# Prospect Rating API - 5-Star System ⭐

## 🎯 Overview

Rate your prospects from 1 to 5 stars based on:
- Quality/Interest level
- Potential value
- Engagement level
- Fit with your services

---

## 📋 API Endpoints

### **Base URL**
```
http://localhost:8000/api/prospects/{id}/rating/
```

---

## 🔐 Authentication

All endpoints require JWT authentication:

```http
Authorization: Bearer <your_jwt_token>
```

---

## 📊 Available Operations

### 1️⃣ **GET Current Rating**

```http
GET /api/prospects/{id}/rating/
```

#### Example
```javascript
GET /api/prospects/1/rating/
```

#### Response (200 OK)
```json
{
    "id": 1,
    "prospect": 1,
    "rating": 4,
    "comment": "Very interested, has budget",
    "created_at": "2026-03-16T14:00:00Z",
    "updated_at": "2026-03-16T14:30:00Z"
}
```

#### Response (404 Not Found)
```json
{
    "detail": "No rating found for this prospect."
}
```

---

### 2️⃣ **POST Create/Update Rating**

```http
POST /api/prospects/{id}/rating/
```

#### Request Body
```json
{
    "rating": 5,                    // Required: 1-5
    "comment": "Excellent prospect!" // Optional
}
```

#### Example
```javascript
const response = await fetch('/api/prospects/1/rating/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    rating: 5,
    comment: "Has website project ready, budget confirmed"
  })
});

const rating = await response.json();
console.log('Rating:', rating);
```

#### Response (201 Created - New rating)
```json
{
    "id": 1,
    "prospect": 1,
    "rating": 5,
    "comment": "Has website project ready, budget confirmed",
    "created_at": "2026-03-16T14:00:00Z",
    "updated_at": "2026-03-16T14:00:00Z"
}
```

#### Response (200 OK - Updated rating)
```json
{
    "id": 1,
    "prospect": 1,
    "rating": 5,
    "comment": "Updated comment",
    "created_at": "2026-03-16T14:00:00Z",
    "updated_at": "2026-03-16T14:30:00Z"
}
```

#### Validation Errors (400 Bad Request)
```json
{
    "detail": "Rating must be between 1 and 5."
}
```

---

### 3️⃣ **DELETE Remove Rating**

```http
DELETE /api/prospects/{id}/rating/
```

#### Example
```javascript
const response = await fetch('/api/prospects/1/rating/', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

if (response.ok) {
  console.log('Rating removed successfully');
}
```

#### Response (204 No Content)
Empty response - rating deleted successfully.

---

## ⭐ Rating Scale Guide

### ⭐⭐⭐⭐⭐ (5 stars) - Excellent
- Ready to buy NOW
- Budget confirmed
- Highly engaged
- Perfect fit

### ⭐⭐⭐⭐ (4 stars) - Very Good
- Strong interest
- Budget available
- Good timeline
- Minor concerns

### ⭐⭐⭐ (3 stars) - Average
- Some interest
- Uncertain budget
- Long timeline
- Some concerns

### ⭐⭐ (2 stars) - Low
- Minimal interest
- No budget
- Just browsing
- Many concerns

### ⭐ (1 star) - Poor
- Not interested
- Wrong fit
- Unresponsive
- Red flags

---

## 🎯 Complete Frontend Example

### React Component

```typescript
import { useState, useEffect } from 'react';

interface ProspectRating {
  id: number;
  prospect: number;
  rating: number;
  comment: string;
  created_at: string;
  updated_at: string;
}

interface Props {
  prospectId: number;
  token: string;
}

export default function ProspectRatingWidget({ prospectId, token }: Props) {
  const [rating, setRating] = useState<ProspectRating | null>(null);
  const [hoverRating, setHoverRating] = useState(0);
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch current rating
  useEffect(() => {
    fetchRating();
  }, [prospectId]);

  async function fetchRating() {
    try {
      const response = await fetch(`/api/prospects/${prospectId}/rating/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setRating(data);
        setComment(data.comment || '');
      }
    } catch (error) {
      console.error('Error fetching rating:', error);
    }
  }

  async function submitRating(newRating: number) {
    setLoading(true);
    try {
      const response = await fetch(`/api/prospects/${prospectId}/rating/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          rating: newRating,
          comment: comment
        })
      });

      if (response.ok) {
        const data = await response.json();
        setRating(data);
        alert(`Rating saved: ${data.rating}/5 ⭐`);
      }
    } catch (error) {
      console.error('Error saving rating:', error);
      alert('Failed to save rating');
    } finally {
      setLoading(false);
    }
  }

  async function deleteRating() {
    if (!confirm('Remove this rating?')) return;

    try {
      const response = await fetch(`/api/prospects/${prospectId}/rating/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setRating(null);
        setComment('');
        alert('Rating removed');
      }
    } catch (error) {
      console.error('Error deleting rating:', error);
    }
  }

  return (
    <div className="p-4 border rounded-lg bg-white">
      <h3 className="text-lg font-semibold mb-3">
        Prospect Rating
      </h3>

      {/* Star Rating */}
      <div className="flex gap-2 mb-4">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            type="button"
            disabled={loading}
            onClick={() => submitRating(star)}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            className="text-3xl focus:outline-none transition-transform hover:scale-110"
          >
            {(hoverRating || rating?.rating || 0) >= star ? '⭐' : '☆'}
          </button>
        ))}
      </div>

      {/* Current Rating Display */}
      {rating && (
        <div className="mb-3 text-sm text-gray-600">
          Current: {rating.rating}/5 stars
          <br />
          Updated: {new Date(rating.updated_at).toLocaleDateString()}
        </div>
      )}

      {/* Comment */}
      <div className="mb-3">
        <label className="block text-sm font-medium mb-1">
          Comment (optional)
        </label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Add notes about this prospect..."
          rows={3}
          className="w-full border rounded-md p-2 text-sm"
          onBlur={() => {
            if (rating) {
              submitRating(rating.rating);
            }
          }}
        />
      </div>

      {/* Actions */}
      <div className="flex gap-2">
        {rating && (
          <button
            onClick={deleteRating}
            disabled={loading}
            className="px-3 py-1 text-sm text-red-600 border border-red-600 rounded hover:bg-red-50"
          >
            Remove Rating
          </button>
        )}
      </div>
    </div>
  );
}
```

---

## 📊 Integration with Prospect List

### Add Rating to Prospect Data

```typescript
// When fetching prospects, ratings are included
const response = await fetch('/api/prospects/');
const prospects = await response.json();

prospects.forEach(prospect => {
  console.log(`${prospect.company_name}:`);
  
  if (prospect.ratings.length > 0) {
    const rating = prospect.ratings[0];
    console.log(`  Rating: ${rating.rating}/5 ⭐`);
    console.log(`  Comment: ${rating.comment}`);
  } else {
    console.log('  No rating yet');
  }
});
```

### Filter by Rating

```typescript
// Get highly-rated prospects (4-5 stars)
const hotProspects = prospects.filter(p => 
  p.ratings.length > 0 && p.ratings[0].rating >= 4
);

// Get unrated prospects
const unratedProspects = prospects.filter(p => 
  p.ratings.length === 0
);
```

---

## 🔒 Permissions

| Operation | Permission | Notes |
|-----------|-----------|-------|
| GET | IsAuthenticated | Can view own ratings |
| POST | IsAuthenticated | Can create/update |
| DELETE | IsAuthenticated | Can remove |

**Note:** Only one rating per prospect (can be updated but not duplicated).

---

## 📝 Best Practices

### 1. **Rate After Initial Contact**
```typescript
// After first conversation
await rateProspect(id, {
  rating: 3,
  comment: "Initial contact made, needs follow-up"
});
```

### 2. **Update After Each Interaction**
```typescript
// After proposal sent
await rateProspect(id, {
  rating: 4,
  comment: "Proposal sent, very interested, budget confirmed"
});
```

### 3. **Use Comments for Context**
```typescript
✅ Good: "Budget: 2000€, Timeline: Q2 2026, Decision maker: Yes"
❌ Bad: "Good client"
```

### 4. **Prioritize Follow-ups**
```typescript
// Focus on 4-5 star prospects first
const priorityList = prospects
  .filter(p => p.ratings.length > 0)
  .sort((a, b) => b.ratings[0].rating - a.ratings[0].rating);
```

---

## ✅ Summary

| Operation | Method | Endpoint | Auth |
|-----------|--------|----------|------|
| **Get Rating** | GET | `/api/prospects/{id}/rating/` | ✅ |
| **Create/Update** | POST | `/api/prospects/{id}/rating/` | ✅ |
| **Delete** | DELETE | `/api/prospects/{id}/rating/` | ✅ |
| **Included in Prospect** | GET | `/api/prospects/{id}/` | ✅ |

---

## 🎯 Use Cases

### Sales Pipeline Management
- ⭐⭐⭐⭐⭐ Close immediately
- ⭐⭐⭐⭐ Send proposal
- ⭐⭐⭐ Nurture relationship
- ⭐⭐ Keep in touch
- ⭐ Remove from pipeline

### Lead Qualification
- Score leads from Google Maps scraping
- Prioritize follow-ups by rating
- Track engagement over time

### Performance Tracking
- Average rating of all prospects
- Conversion rate by rating level
- Time to close by rating

---

**Ready to use!** 🚀
