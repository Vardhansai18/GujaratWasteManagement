#!/bin/bash

# Quick Deploy Script - Run from LOCAL machine
# This script transfers files and initiates deployment on remote server

SERVER_IP="10.197.36.30"
SERVER_USER="root"
REMOTE_DIR="/root/projects/GujaratWasteManagement"

echo "======================================"
echo "🚀 Quick Deploy to Ubuntu Server"
echo "======================================"
echo "Target: $SERVER_USER@$SERVER_IP"
echo ""

# Check if we can connect to server
echo "📡 Testing connection to server..."
if ! ssh -o ConnectTimeout=5 $SERVER_USER@$SERVER_IP "echo 'Connection successful'"; then
    echo "❌ Cannot connect to server. Please check:"
    echo "  - Server IP: $SERVER_IP"
    echo "  - SSH access configured"
    echo "  - Server is online"
    exit 1
fi

echo "✅ Connection successful!"
echo ""

# Transfer files
echo "📤 Transferring files to server..."
rsync -avz --progress \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='vechile_lat_lon.json' \
    ./ $SERVER_USER@$SERVER_IP:$REMOTE_DIR/

if [ $? -eq 0 ]; then
    echo "✅ Files transferred successfully!"
else
    echo "❌ File transfer failed!"
    exit 1
fi

echo ""
echo "======================================"
echo "🔧 Starting deployment on server..."
echo "======================================"

# Run deployment script on server
ssh $SERVER_USER@$SERVER_IP "cd $REMOTE_DIR && chmod +x deploy/deploy.sh && ./deploy/deploy.sh"

echo ""
echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"
echo ""
echo "🌐 Your application is now available at:"
echo "   http://$SERVER_IP"
echo ""
echo "📝 Next steps:"
echo "   - Visit http://$SERVER_IP to test"
echo "   - Check logs: ssh $SERVER_USER@$SERVER_IP 'sudo journalctl -u sunny_bro -f'"
echo "======================================"
