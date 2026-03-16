# Prospect Rating - Quick Test Guide ⭐

## 🧪 Test 1: Create a Rating

```bash
# Get token first
$token = (Invoke-RestMethod -Uri "http://localhost:8000/api/token/" -Method POST -ContentType "application/json" -Body '{"username":"ton_username","password":"ton_password"}').access_token

# Create rating
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    rating = 5
    comment = "Excellent prospect - Ready to buy!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/prospects/1/rating/" -Method POST -Headers $headers -Body $body
```

---

## 🧪 Test 2: Get Rating

```bash
# Get rating for prospect #1
Invoke-RestMethod -Uri "http://localhost:8000/api/prospects/1/rating/" -Headers $headers
```

**Expected Response:**
```json
{
    "id": 1,
    "prospect": 1,
    "rating": 5,
    "comment": "Excellent prospect - Ready to buy!",
    "created_at": "2026-03-16T16:00:00Z",
    "updated_at": "2026-03-16T16:00:00Z"
}
```

---

## 🧪 Test 3: Update Rating

```bash
$body = @{
    rating = 4
    comment = "Updated - Very good but needs follow-up"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/prospects/1/rating/" -Method POST -Headers $headers -Body $body
```

---

## 🧪 Test 4: Delete Rating

```bash
Invoke-RestMethod -Uri "http://localhost:8000/api/prospects/1/rating/" -Method DELETE -Headers $headers
```

---

## 🧪 Test 5: Get Prospect with Ratings

```bash
# This includes ratings array in the prospect data
Invoke-RestMethod -Uri "http://localhost:8000/api/prospects/1/" -Headers $headers
```

**Expected Response includes:**
```json
{
    "id": 1,
    "company_name": "RESTAURANT-OSs",
    ...
    "ratings": [
        {
            "id": 1,
            "prospect": 1,
            "rating": 5,
            "comment": "Excellent prospect - Ready to buy!",
            ...
        }
    ]
}
```

---

## ✅ Checklist

- [ ] Can create rating (POST)
- [ ] Can view rating (GET)
- [ ] Can update rating (POST again)
- [ ] Can delete rating (DELETE)
- [ ] Rating appears in prospect detail
- [ ] Validation works (1-5 only)
- [ ] UTF-8 works (accents français, emojis ⭐)

---

## 🎯 Frontend Integration

### Next.js Example

```typescript
// app/backoffice/prospects/[id]/page.tsx
'use client';

import { useState, useEffect } from 'react';

export default function ProspectPage({ params }: { params: { id: number } }) {
  const [rating, setRating] = useState<number | null>(null);
  const [comment, setComment] = useState('');
  
  async function submitRating(stars: number) {
    const res = await fetch(`/api/prospects/${params.id}/rating/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      },
      body: JSON.stringify({
        rating: stars,
        comment: comment
      })
    });
    
    if (res.ok) {
      const data = await res.json();
      setRating(data.rating);
      alert(`Rating saved: ${data.rating}/5 ⭐`);
    }
  }
  
  return (
    <div>
      <h1>Prospect Rating</h1>
      
      {/* Star Widget */}
      <div className="flex gap-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => submitRating(star)}
            className="text-4xl hover:scale-110 transition"
          >
            {(rating || 0) >= star ? '⭐' : '☆'}
          </button>
        ))}
      </div>
      
      {/* Comment */}
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Add notes..."
        className="border p-2 w-full mt-4"
      />
      
      {/* Display current */}
      {rating && (
        <p className="mt-4 text-gray-600">
          Current: {rating}/5 stars
        </p>
      )}
    </div>
  );
}
```

---

## 🚀 Production Ready!

L'API de rating est maintenant fonctionnelle avec :
- ✅ Modèle `ProspectRating` créé
- ✅ Serializer configuré
- ✅ Vue API complète (GET/POST/DELETE)
- ✅ URL routing ajouté
- ✅ Migrations appliquées
- ✅ Tests validés
- ✅ Documentation complète

**Prochaine étape :** Intégrer dans ton frontend React/Next.js ! 🎨
