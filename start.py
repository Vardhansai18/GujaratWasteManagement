#!/usr/bin/env python3
"""
Complete Vehicle Tracking System
Surat Municipal Corporation - Waste Management

This script:
1. Logs into the tracking system
2. Fetches vehicle GPS data from API
3. Saves data to JSON file
4. Optionally launches web dashboard
"""

import subprocess
import sys
import os

def main():
    print("="*70)
    print(" 🚛 SURAT MUNICIPAL CORPORATION - VEHICLE TRACKING SYSTEM")
    print("="*70)
    print("\nOptions:")
    print("1. Fetch vehicle data and generate JSON")
    print("2. Launch web dashboard (requires existing JSON file)")
    print("3. Do both (fetch data then launch dashboard)")
    print("="*70)
    
    choice = input("\nEnter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\n📡 Fetching vehicle data...")
        subprocess.run([sys.executable, "server.py"])
        
    elif choice == "2":
        if not os.path.exists("vechile_lat_lon.json"):
            print("\n❌ Error: vechile_lat_lon.json not found!")
            print("Please run option 1 first to fetch vehicle data.")
            return
        print("\n🚀 Launching web dashboard...")
        subprocess.run([sys.executable, "app.py"])
        
    elif choice == "3":
        print("\n📡 Step 1: Fetching vehicle data...")
        result = subprocess.run([sys.executable, "server.py"])
        
        if result.returncode == 0 and os.path.exists("vechile_lat_lon.json"):
            print("\n✅ Data fetched successfully!")
            print("\n🚀 Step 2: Launching web dashboard...")
            input("\nPress Enter to launch dashboard...")
            subprocess.run([sys.executable, "app.py"])
        else:
            print("\n❌ Failed to fetch data. Dashboard not launched.")
    else:
        print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()
