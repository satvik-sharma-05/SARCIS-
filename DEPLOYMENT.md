# 🚀 Deployment Guide

Deploy SARCIS to production in 3 steps!

---

## 📋 Pre-Deployment Checklist

- [ ] MongoDB Atlas account created
- [ ] Vercel account created
- [ ] Render account created (or Railway)
- [ ] GitHub repository ready
- [ ] Environment variables prepared

---

## 1️⃣ Deploy Database (MongoDB Atlas)

### Step 1: Create Cluster
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up / Log in
3. Create a **FREE** M0 cluster
4. Choose region closest to your users
5. Wait for cluster to deploy (~3 minutes)

### Step 2: Create Database User
1. Go to **Database Access**
2. Click **Add New Database User**
3. Username: `sarcis_user`
4. Password: Generate strong password
5. Database User Privileges: **Read and write to any database**
6. Click **Add User**

### Step 3: Configure Network Access
1. Go to **Network Access**
2. Click **Add IP Address**
3. Click **Allow Access from Anywhere** (0.0.0.0/0)
   - For production, restrict to your server IPs
4. Click **Confirm**

### Step 4: Get Connection String
1. Go to **Database** → **Connect**
2. Choose **Connect your application**
3. Copy connection string:
   ```
   mongodb+srv://sarcis_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `<password>` with your actual password
5. Save this for backend deployment

---

## 2️⃣ Deploy Backend (Render)

### Step 1: Prepare Repository
```bash
# Ensure requirements.txt is up to date
cd backend
pip freeze > requirements.txt

# Commit and push to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Create Web Service
1. Go to https://render.com
2. Sign up / Log in
3. Click **New +** → **Web Service**
4. Connect your GitHub repository
5. Configure:
   - **Name**: `sarcis-backend`
   - **Region**: Choose closest to users
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

### Step 3: Add Environment Variables
Click **Environment** → **Add Environment Variable**:

```
MONGO_URI=mongodb+srv://sarcis_user:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=sarcis
JWT_SECRET_KEY=<generate-strong-random-key>
WHISPER_MODEL=base
```

Generate JWT secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Deploy
1. Click **Create Web Service**
2. Wait for deployment (~5-10 minutes)
3. Note your backend URL: `https://sarcis-backend.onrender.com`

### Step 5: Test Backend
```bash
curl https://sarcis-backend.onrender.com/health
# Should return: {"status":"ok"}
```

---

## 3️⃣ Deploy Frontend (Vercel)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Configure Environment
```bash
cd frontend

# Create .env.production
echo "NEXT_PUBLIC_API_URL=https://sarcis-backend.onrender.com" > .env.production
```

### Step 3: Deploy
```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod
```

Follow prompts:
- Set up and deploy? **Y**
- Which scope? Choose your account
- Link to existing project? **N**
- Project name? `sarcis-frontend`
- Directory? `./`
- Override settings? **N**

### Step 4: Configure Environment Variables (Vercel Dashboard)
1. Go to https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add:
   ```
   NEXT_PUBLIC_API_URL=https://sarcis-backend.onrender.com
   ```
5. Redeploy if needed

### Step 5: Test Frontend
1. Open your Vercel URL: `https://sarcis-frontend.vercel.app`
2. Sign up and test the flow

---

## 🔧 Post-Deployment Configuration

### Update Backend CORS
Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sarcis-frontend.vercel.app",  # Add your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push - Render will auto-deploy.

---

## 📊 Monitoring & Maintenance

### Backend (Render)
- View logs: Dashboard → Logs
- Monitor usage: Dashboard → Metrics
- Free tier: 750 hours/month (enough for MVP)

### Frontend (Vercel)
- View deployments: Dashboard → Deployments
- Monitor analytics: Dashboard → Analytics
- Free tier: Unlimited for personal projects

### Database (MongoDB Atlas)
- Monitor usage: Dashboard → Metrics
- Free tier: 512MB storage (enough for thousands of files)

---

## 🚨 Important Notes

### Free Tier Limitations

**Render Free Tier:**
- Spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month (enough for MVP)

**Solution for production:**
- Upgrade to paid plan ($7/month)
- Or use Railway (similar pricing)

**MongoDB Atlas Free Tier:**
- 512MB storage
- Shared CPU
- Enough for MVP and testing

**Vercel Free Tier:**
- Unlimited bandwidth
- 100GB bandwidth/month
- Perfect for frontend

---

## 🔐 Security Checklist

- [ ] Change JWT_SECRET_KEY to strong random value
- [ ] Use strong MongoDB password
- [ ] Restrict MongoDB network access to server IPs (production)
- [ ] Enable HTTPS (automatic on Vercel/Render)
- [ ] Add rate limiting (optional)
- [ ] Set up monitoring/alerts

---

## 🐛 Troubleshooting

### Backend not responding
1. Check Render logs
2. Verify environment variables
3. Test MongoDB connection
4. Check if service is sleeping (free tier)

### Frontend can't connect to backend
1. Verify NEXT_PUBLIC_API_URL is correct
2. Check CORS settings in backend
3. Test backend health endpoint directly

### MongoDB connection error
1. Verify connection string
2. Check network access settings
3. Ensure database user has correct permissions

---

## 📈 Scaling Considerations

### When to upgrade:

**Backend:**
- Processing > 100 files/day → Upgrade Render plan
- Need faster processing → Add more workers (paid plan)
- Need 24/7 availability → Paid plan (no spin-down)

**Database:**
- Storage > 500MB → Upgrade MongoDB Atlas
- Need better performance → M10 cluster ($0.08/hour)

**Frontend:**
- High traffic → Vercel auto-scales (free)
- Need analytics → Upgrade Vercel plan

---

## 🎯 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] MongoDB Atlas configured
- [ ] Environment variables set
- [ ] CORS configured correctly
- [ ] Health endpoints working
- [ ] Test complete user flow
- [ ] Monitor logs for errors
- [ ] Set up error tracking (optional: Sentry)
- [ ] Document API for users

---

## 🚀 You're Live!

Your SARCIS platform is now deployed and accessible worldwide!

**Next steps:**
1. Share your frontend URL
2. Monitor usage and performance
3. Gather user feedback
4. Iterate and improve

---

**Deployment complete! 🎉**
