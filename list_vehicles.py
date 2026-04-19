#!/usr/bin/env python3
"""
List all vehicles from vechile_lat_lon.json
"""

import json
import os

def list_all_vehicles():
    json_file = 'vechile_lat_lon.json'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        print("Please run 'python3 server.py' first to fetch vehicle data.")
        return
    
    # Load vehicle data
    with open(json_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    print("=" * 80)
    print(f"🚛 VEHICLE LIST - SURAT MUNICIPAL CORPORATION")
    print(f"Total Vehicles: {len(vehicles)}")
    print("=" * 80)
    print()
    
    # Group by vendor for better organization
    vendors = {}
    for vehicle in vehicles:
        vendor = vehicle.get('VENDOR_NAME', 'Unknown')
        if vendor not in vendors:
            vendors[vendor] = []
        vendors[vendor].append(vehicle)
    
    # Display by vendor
    for vendor_name in sorted(vendors.keys()):
        vendor_vehicles = vendors[vendor_name]
        print(f"\n📦 {vendor_name}")
        print(f"   Vehicles: {len(vendor_vehicles)}")
        print("   " + "-" * 76)
        
        for i, vehicle in enumerate(vendor_vehicles, 1):
            rto = vehicle.get('VEHICLE_RTO_NO', 'N/A')
            vehicle_id = vehicle.get('VEHICLE_ID', 'N/A')
            v_type = vehicle.get('VEHICLE_TYPE', 'N/A')
            status = vehicle.get('VEHICLE_STATUS', 'N/A')
            speed = vehicle.get('VEHICLE_SPEED', 0)
            location = vehicle.get('VEHICLE_LOCATION', 'N/A')
            
            # Status indicator
            if speed > 0:
                status_icon = "🟢 RUNNING"
            elif status == "NGF":
                status_icon = "🔴 NO GPS"
            else:
                status_icon = "🟡 IDLE"
            
            print(f"   {i:3d}. {rto:15s} | ID: {vehicle_id:15s} | {v_type:20s} | {status_icon}")
    
    print("\n" + "=" * 80)
    
    # Summary statistics
    print("\n📊 SUMMARY STATISTICS:")
    print("-" * 80)
    
    first_vehicle = vehicles[0] if vehicles else {}
    print(f"Total Fleet:        {first_vehicle.get('TOTAL_FLEET', 0)}")
    print(f"Connected:          {first_vehicle.get('CONNECTED_FLEET', 0)}")
    print(f"Disconnected:       {first_vehicle.get('DISCONNECTED_FLEET', 0)}")
    print(f"Running:            {first_vehicle.get('RUNNING_FLEET', 0)}")
    print(f"Idle:               {first_vehicle.get('IDEL_FLEET', 0)}")
    
    # Count by vehicle type
    print("\n📋 BY VEHICLE TYPE:")
    print("-" * 80)
    types = {}
    for vehicle in vehicles:
        v_type = vehicle.get('VEHICLE_TYPE', 'Unknown')
        types[v_type] = types.get(v_type, 0) + 1
    
    for v_type, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        print(f"{v_type:30s}: {count:4d} vehicles")
    
    print("\n" + "=" * 80)
    
    # Export options
    print("\n💾 EXPORT OPTIONS:")
    print("   1. To export to CSV: python3 export_to_csv.py")
    print("   2. To view in web dashboard: python3 app.py")
    print("=" * 80)

if __name__ == "__main__":
    list_all_vehicles()
