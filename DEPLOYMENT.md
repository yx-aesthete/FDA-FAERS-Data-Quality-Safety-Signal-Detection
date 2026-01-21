# 🚀 Deployment Guide

## Quick Deploy Options

### Option 1: Railway.app (Recommended - Easiest)

**Railway provides free hosting with automatic deployments.**

#### Steps:

1. **Create GitHub Repository**
```bash
cd /Users/macbook/Code/roche-poc
git init
git add .
git commit -m "Initial commit: FDA FAERS PoC Dashboard"
```

2. **Push to GitHub**
```bash
# Create new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/faers-poc.git
git branch -M main
git push -u origin main
```

3. **Deploy on Railway**
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `faers-poc` repository
   - Railway auto-detects Python and uses `railway.toml` config
   - **Data downloads automatically on first run!** (see `data_loader.py`)
   - Wait 3-5 minutes for build
   - Click "Generate Domain" to get public URL

4. **Share with Interviewers**
   - URL will be: `https://your-app-name.railway.app`
   - Send them the link!

**Pros:**
- ✅ Free tier available
- ✅ Auto-downloads 73MB FAERS data on startup
- ✅ Zero configuration needed
- ✅ HTTPS by default
- ✅ Automatic deployments on git push

**Cons:**
- ⏱️ First load takes ~1 minute (downloads data)
- 💤 Sleeps after inactivity (free tier)

---

### Option 2: Streamlit Cloud (Official, Super Easy)

**Streamlit's official hosting - optimized for Streamlit apps.**

#### Steps:

1. **Push to GitHub** (same as Railway steps 1-2 above)

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Connect GitHub account
   - Select repository: `faers-poc`
   - Main file: `app.py`
   - Click "Deploy"

3. **Public URL**
   - URL: `https://YOUR_USERNAME-faers-poc.streamlit.app`

**Pros:**
- ✅ Free forever
- ✅ Built for Streamlit
- ✅ No configuration needed
- ✅ Auto-downloads data

**Cons:**
- 💤 Limited resources (may timeout on data download)
- 📦 1GB storage limit (FAERS zip is 73MB - should fit)

---

### Option 3: Render.com (Reliable)

#### Steps:

1. **Push to GitHub** (same steps as above)

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true`
   - Choose Free tier

**Pros:**
- ✅ Reliable free tier
- ✅ Always-on (doesn't sleep)
- ✅ Good performance

**Cons:**
- ⏱️ Slower cold starts

---

## 🔧 Configuration Files Created

All deployment files are ready:

- ✅ `Procfile` - Railway/Heroku deployment config
- ✅ `railway.toml` - Railway-specific settings
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Minimal dependencies for fast deployment
- ✅ `data_loader.py` - Auto-downloads FAERS data on first run
- ✅ `.gitignore` - Excludes venv and local data files

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [x] All files committed to git
- [x] `data/` folder in `.gitignore` (don't commit 400MB data!)
- [x] `venv/` folder in `.gitignore`
- [x] `requirements.txt` has all dependencies
- [x] `app.py` calls `download_and_extract_faers_data()`
- [x] Test locally: `streamlit run app.py`

---

## 🎯 Recommended for Interview

**Use Railway.app** because:
1. Fastest deployment (< 5 minutes)
2. Professional custom domain
3. Auto-downloads data (no manual setup)
4. Free tier sufficient for demo
5. Easy to share URL with stakeholders

---

## 📊 After Deployment

### Send to Interviewers:

```
Subject: FDA FAERS Data Quality PoC - Live Demo

Hi Team,

I've prepared an interactive demonstration of AI-driven pharmacovigilance 
data quality monitoring for the DART program. You can explore it here:

🔗 https://your-app.railway.app

Features:
- Real-time data quality analysis on 50K FDA FAERS cases
- Safety signal detection using PRR methodology  
- Interactive visualizations and metrics
- Production-ready architecture demonstration

The dashboard includes 4 sections:
1. Overview - Executive summary
2. Data Quality Analysis - 4-stage quality assessment
3. Safety Signal Detection - PRR-based signal identification
4. About - Technical implementation details

Feel free to explore before our meeting!

Best regards,
Michał
```

---

## 🐛 Troubleshooting

### If data download fails on Railway:

Add this environment variable in Railway dashboard:
```
FAERS_DATA_URL=https://fis.fda.gov/content/Exports/faers_ascii_2025q3.zip
```

### If app crashes on startup:

Check Railway logs for:
- Memory issues → Reduce `sample_size` in `load_data(50000)` to `25000`
- Timeout → Data download may have failed, redeploy

### If you want to deploy faster (skip data download):

Upload data manually:
1. Remove auto-download call from `app.py`
2. Use Railway's persistent volume for data storage
3. Upload via Railway CLI

---

## 🚀 You're Ready to Deploy!

**Fastest path:**
1. Initialize git: `git init`
2. Create GitHub repo
3. Push code: `git push`
4. Deploy on Railway: < 5 minutes
5. Share URL with interviewers

**The dashboard will be live and accessible worldwide!** 🌍
