# 🚀 Deploy Gujarat Waste Management Dashboard from GitHub

## 📋 Prerequisites
- GitHub account
- Your code pushed to: `github.com/Vardhansai18/GujaratWasteManagement`

---

## ✨ Option 1: Deploy with Render (Recommended - FREE)

Render offers free hosting with auto-deployment from GitHub.

### Step 1: Sign Up for Render
1. Go to [render.com](https://render.com)
2. Click "Get Started" and sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `Vardhansai18/GujaratWasteManagement`
3. Configure the service:
   - **Name**: `gujarat-waste-management`
   - **Region**: Oregon (US West)
   - **Branch**: `main` (or `master`)
   - **Runtime**: Python 3
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     gunicorn --bind 0.0.0.0:$PORT --timeout 300 --workers 2 wsgi:app
     ```
   - **Plan**: Free

### Step 3: Environment Variables (if needed)
Add any environment variables in the "Environment" section.

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 3-5 minutes for the first deploy
3. Your app will be live at: `https://gujarat-waste-management.onrender.com`

### Auto-Deploy
Every time you push to GitHub, Render will automatically redeploy! 🎉

**Note**: Free tier sleeps after 15 minutes of inactivity. First request may be slow.

---

## ✨ Option 2: Deploy with Railway (FREE)

Railway is another excellent free hosting option.

### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "Start a New Project"

### Step 2: Deploy from GitHub
1. Select "Deploy from GitHub repo"
2. Choose `Vardhansai18/GujaratWasteManagement`
3. Railway will auto-detect it's a Python app
4. Click "Deploy"

### Step 3: Configure
Railway auto-detects settings, but verify:
- **Start Command**: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
- **Install Command**: `pip install -r requirements.txt`

### Step 4: Get URL
1. Go to Settings → Domains
2. Click "Generate Domain"
3. Your app will be at: `https://your-app.railway.app`

---

## ✨ Option 3: Deploy with Fly.io (FREE)

Fly.io offers free hosting with excellent global performance.

### Step 1: Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Initialize
```bash
cd /root/projects/GujaratWasteManagement
fly auth login
fly launch
```

### Step 3: Follow Prompts
- App name: `gujarat-waste-tracker` (or your choice)
- Region: Choose closest to your users
- Use existing Dockerfile: Yes

### Step 4: Deploy
```bash
fly deploy
```

Your app will be at: `https://gujarat-waste-tracker.fly.dev`

---

## ✨ Option 4: Deploy with Vercel (Serverless)

**Warning**: Selenium won't work well on Vercel due to serverless limitations. Only use if you remove Selenium features.

### Setup
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel auto-deploys on push

---

## ⚠️ Important Notes

### Selenium/Chrome Requirements
- **Render**: Requires Dockerfile or custom build script
- **Railway**: Supports Chrome via Nixpacks
- **Fly.io**: Use Dockerfile (already included)
- **Vercel**: Not recommended for Selenium

### Free Tier Limitations
| Platform | Sleep After | Cold Start | Monthly Hours |
|----------|-------------|------------|---------------|
| Render   | 15 min      | ~30s       | 750 hrs       |
| Railway  | No sleep    | Fast       | $5 credit     |
| Fly.io   | No sleep    | Fast       | 3 VMs         |

---

## 🔧 Troubleshooting

### Chrome/ChromeDriver Issues
If Selenium fails, add this to your start command:
```bash
apt-get update && apt-get install -y chromium chromium-driver
```

### Port Issues
Ensure your app binds to `0.0.0.0:$PORT` (not localhost):
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
```

### Database/File Storage
Free tiers have ephemeral storage. Files may be deleted on redeploy.

---

## 📊 Monitoring

After deployment, monitor your app:
- **Render**: Check logs in dashboard
- **Railway**: View logs and metrics in project
- **Fly.io**: `fly logs` command

---

## 🔄 Continuous Deployment

All platforms automatically redeploy when you push to GitHub:
```bash
git add .
git commit -m "Update features"
git push origin main
```

Your app will redeploy automatically! 🚀

---

## 💡 Recommended Choice

For your Gujarat Waste Management app:
- **Best Overall**: Render (easy, reliable, good docs)
- **Fastest Deploy**: Railway (instant, no config)
- **Best Performance**: Fly.io (global CDN, persistent)

Choose based on your priority: ease vs performance vs features.
