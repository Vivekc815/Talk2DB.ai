# 🚀 Talk2db.ai Deployment Guide

Complete step-by-step guide to deploy your app on Render.

## 📋 Prerequisites

1. GitHub account
2. Render account (free at https://render.com)
3. OpenAI API key
4. Your code pushed to GitHub

---

## Step 1: Push Code to GitHub

### 1.1 Initialize Git (if not already done)

```bash
cd /Users/vivekchenganassery/Documents/Projects/Talk2DB
git init
git add .
git commit -m "Initial commit - Ready for deployment"
```

### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `talk2db` (or any name)
3. **Don't** initialize with README, .gitignore, or license
4. Copy the repository URL

### 1.3 Push to GitHub

```bash
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend on Render

### 2.1 Create New Web Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository

### 2.2 Configure Backend Service

**Basic Settings:**
- **Name:** `talk2db-backend` (or any name)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2.3 Add PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Name: `talk2db-db`
3. Plan: **Free** (for testing)
4. Click **"Create Database"**
5. Wait for it to be created
6. Copy the **Internal Database URL** (you'll need this)

### 2.4 Set Environment Variables

In your backend service settings, go to **"Environment"** and add:

```
DATABASE_URL=<Internal Database URL from PostgreSQL service>
OPENAI_API_KEY=<Your OpenAI API Key>
FRONTEND_URL=https://your-frontend-name.onrender.com
ALLOWED_ORIGINS=https://your-frontend-name.onrender.com
ENVIRONMENT=production
```

**Important:** 
- Replace `your-frontend-name` with your actual frontend service name
- You'll update `FRONTEND_URL` after deploying frontend

### 2.5 Deploy Backend

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Copy your backend URL (e.g., `https://talk2db-backend.onrender.com`)

### 2.6 Initialize Database

Once backend is deployed, you need to run the SQL script to create tables:

1. Go to your PostgreSQL service in Render
2. Click **"Connect"** → **"External Connection"**
3. Use a PostgreSQL client (like pgAdmin or DBeaver) to connect
4. Run the SQL from `backend/app/utils/students.sql` to create tables

**OR** use Render's Shell:

1. In your backend service, go to **"Shell"**
2. Run:
```bash
psql $DATABASE_URL -f app/utils/students.sql
```

---

## Step 3: Deploy Frontend on Render

### 3.1 Create Static Site

1. In Render dashboard, click **"New +"** → **"Static Site"**
2. Connect your GitHub repository (same one)
3. Select your repository

### 3.2 Configure Frontend

**Settings:**
- **Name:** `talk2db-frontend` (or any name)
- **Branch:** `main`
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `build`

### 3.3 Set Environment Variables

Add one environment variable:

```
REACT_APP_API_URL=https://your-backend-name.onrender.com
```

Replace `your-backend-name` with your actual backend service name.

### 3.4 Deploy Frontend

1. Click **"Create Static Site"**
2. Wait for deployment (3-5 minutes)
3. Copy your frontend URL (e.g., `https://talk2db-frontend.onrender.com`)

---

## Step 4: Update CORS Settings

### 4.1 Update Backend Environment Variables

1. Go back to your backend service
2. Go to **"Environment"**
3. Update:
   ```
   FRONTEND_URL=https://your-frontend-name.onrender.com
   ALLOWED_ORIGINS=https://your-frontend-name.onrender.com
   ```
4. Click **"Save Changes"**
5. Render will automatically redeploy

---

## Step 5: Test Your Deployment

1. Visit your frontend URL
2. Try asking a question like "Show me all students"
3. Check if results appear

---

## 🔧 Troubleshooting

### Backend Issues

**Problem:** Backend won't start
- Check logs in Render dashboard
- Verify all environment variables are set
- Check if DATABASE_URL is correct

**Problem:** Database connection error
- Verify DATABASE_URL format (should start with `postgresql://`)
- Check if database is running
- Ensure tables are created

### Frontend Issues

**Problem:** Frontend shows API errors
- Check if `REACT_APP_API_URL` is set correctly
- Verify backend URL is accessible
- Check browser console for errors

**Problem:** CORS errors
- Update `ALLOWED_ORIGINS` in backend
- Ensure frontend URL matches exactly (including https://)

---

## 📝 Quick Checklist

- [ ] Code pushed to GitHub
- [ ] Backend service created on Render
- [ ] PostgreSQL database created
- [ ] Backend environment variables set
- [ ] Backend deployed successfully
- [ ] Database tables initialized
- [ ] Frontend service created on Render
- [ ] Frontend environment variables set
- [ ] Frontend deployed successfully
- [ ] CORS settings updated
- [ ] App tested and working

---

## 🎉 You're Done!

Your app should now be live at your frontend URL!

**Backend URL:** `https://your-backend-name.onrender.com`
**Frontend URL:** `https://your-frontend-name.onrender.com`
**API Docs:** `https://your-backend-name.onrender.com/docs`

---

## 💡 Pro Tips

1. **Free Tier Limits:** Render free tier spins down after 15 minutes of inactivity. First request may take 30-60 seconds.

2. **Upgrade:** For always-on service, upgrade to paid plan ($7/month)

3. **Custom Domain:** You can add custom domain in Render settings

4. **Monitoring:** Check logs regularly in Render dashboard

5. **Backups:** Render automatically backs up PostgreSQL databases

---

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Render Support: support@render.com
- Check application logs in Render dashboard
