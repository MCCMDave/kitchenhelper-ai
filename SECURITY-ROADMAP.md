# Security Roadmap

## ✅ Completed (Backend 10/10, Frontend 7.5/10)

### Backend
- [x] JWT_SECRET_KEY validation
- [x] DEBUG=False default
- [x] JWT expiration (60min)
- [x] Security Headers Middleware
- [x] Login Rate Limiting
- [x] Email-Enumeration Protection
- [x] CORS locked down
- [x] Password-Reset Token protection (DEBUG-only)
- [x] Prompt Injection Protection
- [x] Admin endpoints secured (DEBUG-only)
- [x] **Email Verification Middleware**
- [x] **HTTPS Redirect Middleware**

### Frontend
- [x] CSP Headers
- [x] Sensitive console.log removed
- [x] CSP tightened (no external CDNs)
- [x] **Session Timeout (15min inactivity)**
- [x] **Sanitize Helper created (Sanitize.js)**

---

## 🔄 In Progress / TODO

### Frontend → 10/10 (Remaining)

#### 1. innerHTML Sanitization (~1-2 hours)
**Priority:** HIGH
**Impact:** +1.5 points (7.5/10 → 9/10)
**Status:** Helper ready, needs migration

25 innerHTML occurrences across 9 files need migration to use `Sanitize.escapeHTML()`:
- `js/recipes.js` (6 occurrences) - Recipe display
- `js/ui.js` (8 occurrences) - Error messages, notifications
- `js/profiles.js` (3 occurrences) - Diet profiles
- `js/ingredients.js` (3 occurrences) - Ingredient list
- `js/favorites.js` (1 occurrence)
- `js/scanner.js` (1 occurrence)
- `js/pro-model.js` (1 occurrence)

**Migration Pattern:**
```javascript
// Before:
element.innerHTML = userInput;

// After (safe):
element.textContent = userInput; // No HTML needed
// OR
element.innerHTML = Sanitize.escapeHTML(userInput); // HTML needed
```

**Files to update:**
1. Add `<script src="js/sanitize.js"></script>` to all HTML files ✅
2. Replace innerHTML with Sanitize.escapeHTML() in above files
3. Test all affected features (recipes, ingredients, profiles)

---

#### 2. JWT → httpOnly Cookie Migration (~3-4 hours)
**Priority:** CRITICAL
**Impact:** +1 point (9/10 → 10/10)
**Status:** Not started - Large refactoring required

**Current Issue:**
- JWT stored in localStorage → XSS = Account Takeover
- Any XSS vulnerability can steal tokens

**Solution:**
Migrate to httpOnly cookies (immune to XSS):

**Backend Changes:**
1. `/api/auth/login`: Set httpOnly cookie instead of returning token
   ```python
   response = JSONResponse({"message": "Login successful"})
   response.set_cookie(
       key="access_token",
       value=token,
       httponly=True,
       secure=True,  # HTTPS only
       samesite="lax",
       max_age=3600
   )
   ```

2. Create cookie extraction dependency:
   ```python
   def get_token_from_cookie(request: Request):
       token = request.cookies.get("access_token")
       if not token:
           raise HTTPException(401, "Not authenticated")
       return token
   ```

3. Update `get_current_user()` to read from cookies

**Frontend Changes:**
1. Remove all `localStorage.getItem/setItem('token')`
2. Remove `Authorization: Bearer ${token}` headers
3. Change all API calls to use `credentials: 'include'`:
   ```javascript
   fetch(url, {
       credentials: 'include',  // Send cookies
       ...
   })
   ```

4. Update `Auth.isAuthenticated()` to call `/api/auth/verify`
5. Update logout to clear cookie

**Files to modify:**
- Backend:
  - `app/routes/auth.py` (login, logout)
  - `app/utils/auth.py` (get_current_user)
  - All routes using `get_current_user`

- Frontend:
  - `js/api.js` (all fetch calls)
  - `js/auth.js` (login, logout, isAuthenticated)
  - `js/config.js` (remove TOKEN_KEY)

**Testing checklist:**
- [ ] Login sets cookie
- [ ] API calls include cookie automatically
- [ ] Logout clears cookie
- [ ] Protected routes require cookie
- [ ] Token expiration works
- [ ] Refresh page maintains session

**Estimated time:** 3-4 hours (full refactor + testing)

---

## 🎯 Current Scores

- **Backend:** 10/10 ✅
- **Frontend:** 7.5/10 (After Session Timeout + Sanitize Helper)

**To reach Frontend 10/10:**
1. innerHTML Sanitization: 7.5 → 9 (+1.5)
2. JWT → httpOnly Cookie: 9 → 10 (+1)

---

## 📝 Notes

- **innerHTML Migration:** Can be done gradually (file by file)
- **httpOnly Cookie:** Requires full refactoring in one session (breaking change)
- **Priority:** Do innerHTML first (lower risk), then httpOnly (high impact)

**Recommendation:** Schedule httpOnly migration for a dedicated session with testing time.
