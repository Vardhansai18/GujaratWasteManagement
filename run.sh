#!/bin/bash
# Quick Start Script for Vehicle Tracking Dashboard

echo "=============================================="
echo " Vehicle Tracking Dashboard - Quick Start"
echo "=============================================="
echo ""

# Check if JSON file exists
if [ ! -f "vechile_lat_lon.json" ]; then
    echo "⚠️  No data file found!"
    echo "Would you like to fetch vehicle data now? (y/n)"
    read -r response
    if [[ "$response" == "y" || "$response" == "Y" ]]; then
        echo "📡 Fetching vehicle data..."
        python3 server.py
    else
        echo "❌ Cannot start dashboard without data!"
        exit 1
    fi
fi

echo ""
echo "🚀 Starting web dashboard..."
echo "📍 Access at: http://localhost:5001"
echo "Press CTRL+C to stop"
echo "=============================================="
echo ""

python3 app.py
