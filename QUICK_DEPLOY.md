# ⚡ Quick Deployment Guide - Talk2db.ai

## 🎯 Fast Track (5 Steps)

### Step 1: Push to GitHub
```bash
cd /Users/vivekchenganassery/Documents/Projects/Talk2DB
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Create PostgreSQL on Render
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `talk2db-db`
4. Plan: **Free**
5. Click **"Create"**
6. **Copy the Internal Database URL**

### Step 3: Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repo
3. Settings:
   - **Name:** `talk2db-backend`
   - **Root Directory:** `backend`
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   DATABASE_URL=<paste Internal Database URL>
   OPENAI_API_KEY=<your OpenAI key>
   FRONTEND_URL=https://talk2db-frontend.onrender.com
   ALLOWED_ORIGINS=https://talk2db-frontend.onrender.com
   ```
5. Click **"Create"**
6. **Copy your backend URL** (e.g., `https://talk2db-backend.onrender.com`)

### Step 4: Deploy Frontend
1. Click **"New +"** → **"Static Site"**
2. Connect same GitHub repo
3. Settings:
   - **Name:** `talk2db-frontend`
   - **Root Directory:** `frontend`
   - **Build:** `npm install && npm run build`
   - **Publish:** `build`
4. Environment Variable:
   ```
   REACT_APP_API_URL=<your backend URL from step 3>
   ```
5. Click **"Create"**
6. **Copy your frontend URL**

### Step 5: Update Backend CORS
1. Go back to backend service
2. Update environment variables:
   ```
   FRONTEND_URL=<your frontend URL>
   ALLOWED_ORIGINS=<your frontend URL>
   ```
3. Save (auto-redeploys)

### Step 6: Initialize Database
1. Go to backend service → **"Shell"** tab
2. Run:
```bash
python init_db.py
```

**OR** manually:
1. Go to PostgreSQL service → **"Connect"** → **"External Connection"**
2. Use pgAdmin or psql to connect
3. Run SQL from `backend/app/utils/students.sql`

## ✅ Done!

Visit your frontend URL and test with: **"Show me all students"**

---

## 📋 Your URLs

- **Frontend:** `https://talk2db-frontend.onrender.com`
- **Backend:** `https://talk2db-backend.onrender.com`
- **API Docs:** `https://talk2db-backend.onrender.com/docs`

---

## 🆘 Quick Fixes

**Backend won't start?**
- Check logs in Render
- Verify DATABASE_URL format (should be `postgresql://...`)

**Frontend shows errors?**
- Check REACT_APP_API_URL is correct
- Verify backend is running

**CORS errors?**
- Update ALLOWED_ORIGINS with exact frontend URL

**Database empty?**
- Run `init_db.py` in backend shell

---

**Full guide:** See DEPLOYMENT_GUIDE.md for detailed instructions.
