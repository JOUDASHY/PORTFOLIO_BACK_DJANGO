# CORS Configuration Fix 🔧

## 🐛 Problem

**Errors:**
```
Access to XMLHttpRequest at 'https://test-back.unityfianar.site/api/NilsenProfile/' 
from origin 'https://portfolio-nilsen.onrender.com' has been blocked by CORS policy
```

```
Access to XMLHttpRequest at 'https://test-back.unityfianar.site/api/facebook/' 
from origin 'https://areagreen.onrender.com' has been blocked by CORS policy
```

---

## ✅ Solution Applied

### 1. **Updated `CORS_ALLOWED_ORIGINS`**

Added all frontend domains:

```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',           # Local dev (Vite)
    'http://localhost:3000',           # Local dev (Next.js)
    'http://127.0.0.1:5173',
    'http://127.0.0.1:3000',
    'https://portfolio-nilsen.onrender.com',   # ✅ NEW
    'https://areagreen.onrender.com',          # ✅ NEW
    'https://test-back.unityfianar.site',
    'https://portfolio.unityfianar.site',
]
```

### 2. **Updated `CSRF_TRUSTED_ORIGINS`**

```python
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8069",
    "http://127.0.0.1:8069",
    "https://test-back.unityfianar.site",
    "https://portfolio.unityfianar.site",
    "https://portfolio-nilsen.onrender.com",   # ✅ NEW
    "https://areagreen.onrender.com",          # ✅ NEW
]
```

### 3. **Fixed Middleware Order**

`CorsMiddleware` must be **near the top** of the middleware list:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # ← MUST BE HERE (before CommonMiddleware)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... rest of middleware
]
```

---

## 📋 What Was Fixed

| Issue | Before | After |
|-------|--------|-------|
| **CORS Origins** | Only localhost + unityfianar | ✅ Added onrender.com domains |
| **CSRF Origins** | Missing render domains | ✅ Added onrender.com domains |
| **Middleware Order** | CorsMiddleware at bottom | ✅ Moved to top (required!) |

---

## 🧪 Testing

### Test 1: Check CORS Headers

```bash
curl -I https://test-back.unityfianar.site/api/NilsenProfile/ \
  -H "Origin: https://portfolio-nilsen.onrender.com"
```

**Expected Response Headers:**
```http
Access-Control-Allow-Origin: https://portfolio-nilsen.onrender.com
Access-Control-Allow-Credentials: true
```

### Test 2: Browser Console

Open browser console on `https://portfolio-nilsen.onrender.com`:

```javascript
fetch('https://test-back.unityfianar.site/api/NilsenProfile/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);
```

**Should work without CORS error!** ✅

---

## 🚀 Deployment Steps

### 1. **Commit Changes**
```bash
git add back_django_portfolio_me/settings.py
git commit -m "Fix CORS for portfolio-nilsen.onrender.com and areagreen.onrender.com"
git push origin main
```

### 2. **Deploy to Production**

If using Docker/Render:
```bash
# Docker
docker-compose restart

# Or if SSH access
ssh your_server
cd /path/to/project
git pull origin main
sudo systemctl restart gunicorn
```

### 3. **Verify in Browser**

1. Open `https://portfolio-nilsen.onrender.com`
2. Open DevTools → Network tab
3. Check API calls to `test-back.unityfianar.site`
4. Should see `Access-Control-Allow-Origin` header present

---

## 📝 Notes

### Why Middleware Order Matters

Django processes middleware **top to bottom**. `CorsMiddleware` needs to run **early** to add CORS headers before other middleware process the response.

**Wrong order (❌):**
```python
'django.middleware.common.CommonMiddleware',      # Processes response first
'corsheaders.middleware.CorsMiddleware',         # Too late!
```

**Correct order (✅):**
```python
'corsheaders.middleware.CorsMiddleware',         # Adds headers early
'django.middleware.common.CommonMiddleware',     # Then processes
```

### Environment Variables Alternative

Instead of hardcoding, you can use environment variables:

```python
# In .env
CORS_ALLOWED_ORIGINS=https://portfolio-nilsen.onrender.com,https://areagreen.onrender.com

# In settings.py
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
```

But hardcoding is fine for now! ✅

---

## ✅ Checklist

- [x] Added `portfolio-nilsen.onrender.com` to CORS allowed origins
- [x] Added `areagreen.onrender.com` to CORS allowed origins
- [x] Updated CSRF trusted origins
- [x] Moved CorsMiddleware to top of list
- [ ] Commit and push changes
- [ ] Deploy to production server
- [ ] Test from frontend

---

## 🔒 Security Note

**Never use `CORS_ALLOW_ALL_ORIGINS = True` in production!**

This allows ANY website to make requests to your API (security risk).

Instead, always specify exact domains in `CORS_ALLOWED_ORIGINS`. ✅

---

**Fixed and ready to deploy!** 🚀
