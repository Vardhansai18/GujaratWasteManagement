# 🚀 Deployment Guide - Ubuntu Server

Deploy the Vehicle Tracking Dashboard to Ubuntu server at **10.197.36.30**

## 📋 Prerequisites

- Ubuntu server (18.04 or later) at IP: 10.197.36.30
- SSH access to the server
- sudo privileges

## 🎯 Quick Deployment (Automated)

### Step 1: Transfer Files to Server

From your local machine:

```bash
# Navigate to the project directory
cd /Users/sa.pallerla/Desktop/CODE-REPOS/work/aiwebagent/sunny_bro

# Transfer files to server (replace 'ubuntu' with your username if different)
scp -r * ubuntu@10.197.36.30:/home/ubuntu/sunny_bro/
```

### Step 2: Run Deployment Script

SSH into the server and run the automated deployment:

```bash
# SSH into server
ssh ubuntu@10.197.36.30

# Navigate to project directory
cd /home/ubuntu/sunny_bro

# Make deployment script executable
chmod +x deploy/deploy.sh

# Run deployment script
./deploy/deploy.sh
```

The script will automatically:
- ✅ Update system packages
- ✅ Install Python, Nginx, Chrome, ChromeDriver
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Configure Nginx reverse proxy
- ✅ Set up systemd service
- ✅ Configure firewall
- ✅ Start the application

### Step 3: Access Your Application

Open browser and visit: **http://10.197.36.30**

---

## 🔧 Manual Deployment (Step by Step)

If you prefer manual setup or the automated script fails:

### 1. Update System & Install Dependencies

```bash
ssh ubuntu@10.197.36.30

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Nginx
sudo apt install -y python3 python3-pip python3-venv nginx

# Install Chrome for Selenium
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

# Install ChromeDriver
sudo apt install -y chromium-chromedriver
```

### 2. Set Up Application

```bash
# Create and navigate to app directory
mkdir -p /home/ubuntu/sunny_bro
cd /home/ubuntu/sunny_bro

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install flask gunicorn selenium requests
```

### 3. Transfer Application Files

From your local machine:

```bash
cd /Users/sa.pallerla/Desktop/CODE-REPOS/work/aiwebagent/sunny_bro
scp -r * ubuntu@10.197.36.30:/home/ubuntu/sunny_bro/
```

### 4. Configure Nginx

On the server:

```bash
# Copy Nginx configuration
sudo cp /home/ubuntu/sunny_bro/deploy/nginx.conf /etc/nginx/sites-available/sunny_bro

# Enable site
sudo ln -s /etc/nginx/sites-available/sunny_bro /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### 5. Set Up Systemd Service

```bash
# Copy service file
sudo cp /home/ubuntu/sunny_bro/deploy/sunny_bro.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable sunny_bro
sudo systemctl start sunny_bro

# Check status
sudo systemctl status sunny_bro
```

### 6. Configure Firewall

```bash
# Allow HTTP and SSH
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 Production Configuration

### Gunicorn Settings

The app runs with:
- **3 worker processes** for handling concurrent requests
- **Timeout: 300 seconds** for refresh operations
- **Bound to**: 127.0.0.1:5001 (internal only)

### Nginx Settings

- **Reverse proxy** on port 80
- **Increased timeouts** for API refresh operations (300s)
- **Static file caching** for 30 days

---

## 🛠️ Management Commands

### View Application Logs

```bash
# Real-time logs
sudo journalctl -u sunny_bro -f

# Last 100 lines
sudo journalctl -u sunny_bro -n 100

# Today's logs
sudo journalctl -u sunny_bro --since today
```

### Restart Services

```bash
# Restart application
sudo systemctl restart sunny_bro

# Restart Nginx
sudo systemctl restart nginx

# Restart both
sudo systemctl restart sunny_bro nginx
```

### Stop/Start Services

```bash
# Stop application
sudo systemctl stop sunny_bro

# Start application
sudo systemctl start sunny_bro

# Check status
sudo systemctl status sunny_bro
```

### Update Application Code

```bash
# Transfer updated files from local machine
cd /Users/sa.pallerla/Desktop/CODE-REPOS/work/aiwebagent/sunny_bro
scp -r app.py templates/ ubuntu@10.197.36.30:/home/ubuntu/sunny_bro/

# On server, restart application
ssh ubuntu@10.197.36.30
sudo systemctl restart sunny_bro
```

---

## 🔍 Troubleshooting

### Application Won't Start

```bash
# Check logs for errors
sudo journalctl -u sunny_bro -n 50

# Check if port is already in use
sudo netstat -tlnp | grep 5001

# Verify Python environment
cd /home/ubuntu/sunny_bro
source venv/bin/activate
python3 app.py  # Test manually
```

### Nginx Errors

```bash
# Check Nginx configuration
sudo nginx -t

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Verify Nginx is running
sudo systemctl status nginx
```

### ChromeDriver Issues

```bash
# Verify Chrome installation
google-chrome --version

# Verify ChromeDriver
chromedriver --version

# If version mismatch, reinstall ChromeDriver
sudo apt remove chromium-chromedriver
sudo apt install chromium-chromedriver
```

### Can't Access from Browser

```bash
# Check firewall status
sudo ufw status

# Ensure port 80 is allowed
sudo ufw allow 80/tcp

# Check if service is listening
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5001
```

### Permission Issues

```bash
# Fix ownership
sudo chown -R ubuntu:www-data /home/ubuntu/sunny_bro

# Fix permissions
chmod -R 755 /home/ubuntu/sunny_bro
```

---

## 🔐 Security Recommendations

1. **Enable HTTPS**: Set up SSL certificate using Let's Encrypt
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **Change Default Credentials**: Update the API credentials in `server.py` and `app.py`

3. **Restrict Access**: Use Nginx IP whitelisting if needed
   ```nginx
   allow 192.168.1.0/24;
   deny all;
   ```

4. **Regular Updates**: Keep system and packages updated
   ```bash
   sudo apt update && sudo apt upgrade
   ```

---

## 📱 Access Points

After deployment, access your application:

- **Main Dashboard**: http://10.197.36.30/
- **Table View**: http://10.197.36.30/table
- **API Endpoints**:
  - Stats: http://10.197.36.30/api/stats
  - Search: http://10.197.36.30/api/search?q=GJ05
  - Data: http://10.197.36.30/vechile_lat_lon.json

---

## 📞 Support

If you encounter issues:

1. Check application logs: `sudo journalctl -u sunny_bro -f`
2. Check Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. Verify all services are running: `sudo systemctl status sunny_bro nginx`
4. Test manually: `cd /home/ubuntu/sunny_bro && source venv/bin/activate && python3 app.py`

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible at http://10.197.36.30
- [ ] Main dashboard loads correctly
- [ ] Table view displays all vehicles
- [ ] Search functionality works
- [ ] Refresh button fetches new data
- [ ] No errors in logs
- [ ] Service starts on boot
- [ ] Firewall configured properly

**🎉 Deployment Complete! Your vehicle tracking dashboard is now live!**
