# ✅ Deployment Checklist

Use this checklist to ensure everything is ready for deployment.

## Pre-Deployment

- [ ] Code is working locally
- [ ] All environment variables documented
- [ ] Database tables can be created
- [ ] Frontend builds successfully (`npm run build`)
- [ ] Backend runs successfully (`uvicorn app.main:app`)

## GitHub Setup

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] Repository is public (or Render has access)

## Render - PostgreSQL Database

- [ ] PostgreSQL service created
- [ ] Database URL copied
- [ ] Database is running

## Render - Backend Service

- [ ] Web service created
- [ ] Root directory set to `backend`
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set:
  - [ ] `DATABASE_URL` (from PostgreSQL service)
  - [ ] `OPENAI_API_KEY` (your OpenAI key)
  - [ ] `FRONTEND_URL` (will update after frontend deploy)
  - [ ] `ALLOWED_ORIGINS` (will update after frontend deploy)
- [ ] Service deployed successfully
- [ ] Backend URL copied

## Render - Frontend Service

- [ ] Static site created
- [ ] Root directory set to `frontend`
- [ ] Build command: `npm install && npm run build`
- [ ] Publish directory: `build`
- [ ] Environment variable set:
  - [ ] `REACT_APP_API_URL` (your backend URL)
- [ ] Service deployed successfully
- [ ] Frontend URL copied

## Post-Deployment

- [ ] Backend CORS updated with frontend URL
- [ ] Database initialized (run `init_db.py` or SQL script)
- [ ] Frontend tested - can access the app
- [ ] Test query works - "Show me all students"
- [ ] Results display correctly
- [ ] History feature works

## Testing

- [ ] Can submit a query
- [ ] SQL is generated correctly
- [ ] Results table displays
- [ ] History shows past queries
- [ ] Database schema viewer works
- [ ] No console errors in browser
- [ ] No errors in Render logs

## Final Steps

- [ ] Share your app URL!
- [ ] Update README with live URLs
- [ ] Celebrate! 🎉

---

## 🆘 If Something Goes Wrong

1. **Check Render Logs**: Go to your service → Logs tab
2. **Verify Environment Variables**: All should be set correctly
3. **Check Database Connection**: Verify DATABASE_URL is correct
4. **Test Backend**: Visit `/docs` endpoint to see if API is working
5. **Check CORS**: Ensure frontend URL is in ALLOWED_ORIGINS

---

**Need help?** Check the DEPLOYMENT_GUIDE.md for detailed instructions.
