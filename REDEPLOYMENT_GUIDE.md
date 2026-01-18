# 🚀 Re-deployment Guide - Talk2db.ai with New Features

Since you already have your app deployed, here's how to redeploy with the new features.

## ✅ What's New

Your app now has:
- 📁 **SQL File Upload** - Upload .sql files to extract schema
- 📊 **CSV File Upload** - Upload .csv files to extract schema  
- 🔌 **Database Connections** - Connect to external databases
- 🎯 **Dynamic Schema Support** - Use different schemas for queries
- 📚 **Schema Management** - Manage multiple schemas per user

## 🔄 How to Redeploy on Render

### Step 1: Backend Redeployment

Your backend will **automatically redeploy** when Render detects the new commit!

**Manual trigger (if needed):**
1. Go to your backend service in Render dashboard
2. Click **"Manual Deploy"** tab
3. Click **"Deploy latest commit"**
4. Wait for deployment (5-10 minutes)

**What happens:**
- Render will pull latest code from GitHub
- Install new dependencies (`pandas`, `python-multipart`)
- Redeploy the service

### Step 2: Frontend Redeployment

Your frontend will also **automatically redeploy**!

**Manual trigger (if needed):**
1. Go to your frontend service in Render dashboard
2. Click **"Manual Deploy"** tab
3. Click **"Deploy latest commit"**
4. Wait for deployment (3-5 minutes)

### Step 3: Database Migration

The new `database_schemas` table needs to be created:

**Option A: Automatic (Recommended)**
- The table will be created automatically when backend starts
- SQLAlchemy's `Base.metadata.create_all()` handles this

**Option B: Manual (if needed)**
1. Go to backend service → **"Shell"** tab
2. Run:
```bash
python -c "from app.models.database_models import Base, database_schema; from app.core.database import engine; Base.metadata.create_all(bind=engine)"
```

### Step 4: Verify Deployment

1. **Check Backend:**
   - Visit: `https://your-backend-url.onrender.com/docs`
   - You should see new endpoints:
     - `/upload/sql`
     - `/upload/csv`
     - `/connect/database`
     - `/schemas/{user_id}`

2. **Check Frontend:**
   - Visit your frontend URL
   - You should see:
     - File Upload section in sidebar
     - Schema Manager section
     - New UI elements

3. **Test New Features:**
   - Try uploading a SQL file
   - Select a schema
   - Ask a query using that schema

## 🆕 New Endpoints

### Backend Endpoints:

1. **POST `/upload/sql`** - Upload SQL file
   - Form data: `user_id`, `schema_name`, `file`
   - Returns: Schema information

2. **POST `/upload/csv`** - Upload CSV file
   - Form data: `user_id`, `schema_name`, `file`
   - Returns: Schema information

3. **POST `/connect/database`** - Connect to external database
   - Body: `user_id`, `schema_name`, `db_type`, `connection_string`
   - Returns: Schema information

4. **GET `/schemas/{user_id}`** - Get all user schemas
   - Returns: List of schemas

5. **GET `/schemas/{user_id}/{schema_id}`** - Get schema details
   - Returns: Schema details

6. **DELETE `/schemas/{user_id}/{schema_id}`** - Delete schema
   - Returns: Success status

7. **POST `/answer`** - Updated with optional `schema_id` parameter
   - Body: `user_id`, `query`, `schema_id` (optional)

## 📋 Deployment Checklist

- [ ] Code pushed to GitHub ✓ (Done!)
- [ ] Backend service redeployed (Auto or Manual)
- [ ] Frontend service redeployed (Auto or Manual)
- [ ] New dependencies installed (pandas, python-multipart)
- [ ] Database schema table created (Auto or Manual)
- [ ] Test file upload feature
- [ ] Test schema selection
- [ ] Test queries with custom schema

## 🔧 Troubleshooting

### Issue: Backend fails to start

**Check:**
- New dependencies installed? (Check logs)
- Database migration successful?
- All environment variables still set?

**Fix:**
- Check Render logs
- Verify `pandas` and `python-multipart` are in requirements.txt
- Ensure DATABASE_URL is still correct

### Issue: Frontend build fails

**Check:**
- All new components imported correctly?
- API endpoints updated?

**Fix:**
- Check build logs in Render
- Verify all files are committed to GitHub

### Issue: File upload doesn't work

**Check:**
- Backend endpoint `/upload/sql` accessible?
- File size limits?
- CORS settings?

**Fix:**
- Test endpoint in API docs: `/docs`
- Check backend logs for errors
- Verify file size is reasonable (< 10MB)

## 🎉 After Deployment

Your app will have:

1. **File Upload Feature:**
   - Upload SQL files to extract schema
   - Upload CSV files to extract schema
   - All schemas stored per user

2. **Schema Management:**
   - View all uploaded schemas
   - Select schema to use for queries
   - Delete schemas when not needed

3. **Dynamic Queries:**
   - Ask questions using custom schemas
   - Switch between schemas easily
   - All queries still work with default schema

## 📝 Quick Test

After deployment, try:

1. **Upload a SQL file:**
   - Go to File Upload section
   - Upload any `.sql` file
   - See schema extracted

2. **Use custom schema:**
   - Select uploaded schema
   - Ask a query: "Show me all tables"
   - See SQL generated for your schema!

---

**That's it!** Your app should automatically redeploy. Just wait 5-10 minutes and check your Render dashboard!
