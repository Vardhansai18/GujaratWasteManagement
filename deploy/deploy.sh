#!/bin/bash

# Deployment script for Surat Municipal Vehicle Tracking Dashboard
# Run this script on the Ubuntu server (10.197.36.30)

set -e

echo "======================================"
echo "🚀 Deploying Vehicle Tracking Dashboard"
echo "======================================"

# Update system
echo "📦 Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required packages
echo "📦 Installing Python, Nginx, and dependencies..."
sudo apt install -y python3 python3-pip python3-venv nginx

# Install Chrome and ChromeDriver for Selenium
echo "🌐 Installing Google Chrome..."
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb

echo "🔧 Installing ChromeDriver..."
sudo apt install -y chromium-chromedriver

# Create application directory
APP_DIR="/home/ubuntu/sunny_bro"
echo "📁 Setting up application directory at $APP_DIR..."
mkdir -p $APP_DIR
cd $APP_DIR

# Create virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install flask gunicorn selenium requests

# Set permissions
echo "🔒 Setting permissions..."
sudo chown -R ubuntu:www-data $APP_DIR
chmod -R 755 $APP_DIR

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/sunny_bro
sudo ln -sf /etc/nginx/sites-available/sunny_bro /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Configure systemd service
echo "⚙️ Setting up systemd service..."
sudo cp deploy/sunny_bro.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sunny_bro
sudo systemctl start sunny_bro

# Restart Nginx
echo "🔄 Restarting Nginx..."
sudo systemctl restart nginx

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Check status
echo ""
echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"
echo ""
echo "📊 Service Status:"
sudo systemctl status sunny_bro --no-pager
echo ""
echo "🌐 Nginx Status:"
sudo systemctl status nginx --no-pager
echo ""
echo "======================================"
echo "🎉 Application is now running at:"
echo "   http://10.197.36.30"
echo "======================================"
echo ""
echo "📝 Useful Commands:"
echo "   - View logs: sudo journalctl -u sunny_bro -f"
echo "   - Restart app: sudo systemctl restart sunny_bro"
echo "   - Restart Nginx: sudo systemctl restart nginx"
echo "   - Stop app: sudo systemctl stop sunny_bro"
echo "======================================"
