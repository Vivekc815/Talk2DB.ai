# PDF Upload Network Error - Troubleshooting Guide

## 🔍 Problem
You're seeing: "Network error: Cannot connect to server"

This means the **frontend cannot reach the backend API**.

## ✅ Solution Steps

### Step 1: Check Browser Console
1. Open your browser's Developer Tools (F12)
2. Go to the **Console** tab
3. Look for messages like:
   - `🔗 API Base URL: http://...`
   - `❌ API Response Error: ...`

This will tell you what URL the frontend is trying to connect to.

### Step 2: Set Backend URL in Render (Frontend Service)

**If your frontend is deployed on Render:**

1. Go to your **Render Dashboard**
2. Find your **Frontend Static Site** service
3. Go to **Environment** tab
4. Add a new environment variable:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend-service.onrender.com`)
5. **Save** the environment variable
6. **Redeploy** your frontend service

### Step 3: Verify Backend is Running

**Check if your backend is accessible:**

1. Open your backend URL in a browser (e.g., `https://your-backend.onrender.com/`)
2. You should see: `{"message": "Welcome to Talk2DB API", "status": "running", ...}`
3. If you see an error, your backend isn't running properly

### Step 4: Check CORS Settings

**In your backend service on Render:**

1. Go to **Environment** tab
2. Make sure you have:
   - `FRONTEND_URL` = Your frontend URL (e.g., `https://your-frontend.onrender.com`)
   - Or `ALLOWED_ORIGINS` = Your frontend URL

### Step 5: Common Issues

#### Issue: Frontend shows `http://localhost:8000`
**Fix**: Set `REACT_APP_API_URL` environment variable in Render

#### Issue: Backend returns CORS error
**Fix**: Update `FRONTEND_URL` or `ALLOWED_ORIGINS` in backend environment variables

#### Issue: Backend returns 404
**Fix**: Check that your backend service is running and the URL is correct

#### Issue: Backend returns 500 error
**Fix**: Check backend logs in Render dashboard

## 🔧 Quick Test

After setting `REACT_APP_API_URL`:

1. **Rebuild and redeploy** your frontend
2. Open browser console
3. You should see: `🔗 API Base URL: https://your-backend.onrender.com`
4. Try uploading a PDF again

## 📝 Example Configuration

**Frontend Environment Variables (Render):**
```
REACT_APP_API_URL=https://talk2db-backend.onrender.com
```

**Backend Environment Variables (Render):**
```
FRONTEND_URL=https://talk2db-frontend.onrender.com
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

## 🆘 Still Having Issues?

1. **Check Render logs** for both frontend and backend
2. **Verify URLs** are correct (no typos, correct protocol https://)
3. **Test backend directly** by visiting the URL in browser
4. **Check browser console** for detailed error messages
