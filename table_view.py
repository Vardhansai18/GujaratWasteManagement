#!/usr/bin/env python3
"""
Display all vehicles in a formatted table
"""

import json
import os
from datetime import datetime

def display_table():
    json_file = 'vechile_lat_lon.json'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    print("\n" + "="*200)
    print(f"🚛 SURAT MUNICIPAL CORPORATION - COMPLETE VEHICLE TABLE")
    print(f"Total Vehicles: {len(vehicles)} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*200)
    
    # Table header
    header = (
        f"{'No.':<5} "
        f"{'RTO Number':<15} "
        f"{'Vehicle ID':<18} "
        f"{'Type':<20} "
        f"{'Model':<18} "
        f"{'Speed':<7} "
        f"{'Status':<10} "
        f"{'Latitude':<12} "
        f"{'Longitude':<12} "
        f"{'Location':<40}"
    )
    
    print("\n" + header)
    print("-"*200)
    
    # Display each vehicle
    for i, vehicle in enumerate(vehicles, 1):
        rto = vehicle.get('VEHICLE_RTO_NO', 'N/A')[:15]
        vid = vehicle.get('VEHICLE_ID', 'N/A')[:18]
        vtype = vehicle.get('VEHICLE_TYPE', 'N/A')[:20]
        model = vehicle.get('VEHICLE_MODEL', 'N/A')[:18]
        speed = f"{vehicle.get('VEHICLE_SPEED', 0)} km/h"
        status = vehicle.get('VEHICLE_STATUS', 'N/A')[:10]
        lat = vehicle.get('VEHICLE_LATITUDE', 'N/A')[:12]
        lon = vehicle.get('VEHICLE_LONGITUDE', 'N/A')[:12]
        location = vehicle.get('VEHICLE_LOCATION', 'N/A')[:40]
        
        # Status emoji
        if vehicle.get('VEHICLE_SPEED', 0) > 0:
            status_icon = "🟢"
        elif status == "NGF":
            status_icon = "🔴"
        else:
            status_icon = "🟡"
        
        row = (
            f"{i:<5} "
            f"{rto:<15} "
            f"{vid:<18} "
            f"{vtype:<20} "
            f"{model:<18} "
            f"{speed:<7} "
            f"{status_icon} {status:<8} "
            f"{lat:<12} "
            f"{lon:<12} "
            f"{location:<40}"
        )
        print(row)
        
        # Add separator every 50 rows for readability
        if i % 50 == 0 and i < len(vehicles):
            print("-"*200)
    
    print("="*200)
    print(f"\n✅ Displayed {len(vehicles)} vehicles")
    print("\n💡 TIP: Redirect to file for easier viewing:")
    print("   python3 table_view.py > vehicles_table.txt")
    print("="*200 + "\n")

if __name__ == "__main__":
    display_table()
