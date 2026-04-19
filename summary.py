#!/usr/bin/env python3
"""
Quick Summary of Vehicle Fleet
"""

import json
import os

def quick_summary():
    json_file = 'vechile_lat_lon.json'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    # Get first vehicle for fleet stats
    first = vehicles[0] if vehicles else {}
    
    print("\n" + "="*60)
    print("🚛 SURAT MUNICIPAL CORPORATION")
    print("   WASTE MANAGEMENT - VEHICLE FLEET SUMMARY")
    print("="*60)
    
    # Fleet Statistics
    print("\n📊 FLEET STATISTICS:")
    print("-" * 60)
    print(f"  Total Fleet:          {first.get('TOTAL_FLEET', 0):>6}")
    print(f"  Connected Vehicles:   {first.get('CONNECTED_FLEET', 0):>6}")
    print(f"  Disconnected:         {first.get('DISCONNECTED_FLEET', 0):>6}")
    print(f"  Currently Running:    {first.get('RUNNING_FLEET', 0):>6}")
    print(f"  Currently Idle:       {first.get('IDEL_FLEET', 0):>6}")
    
    # Count by status
    running = sum(1 for v in vehicles if v.get('VEHICLE_SPEED', 0) > 0)
    idle = sum(1 for v in vehicles if v.get('VEHICLE_SPEED', 0) == 0 and v.get('VEHICLE_STATUS') != 'NGF')
    no_gps = sum(1 for v in vehicles if v.get('VEHICLE_STATUS') == 'NGF')
    
    print(f"\n📍 CURRENT STATUS:")
    print("-" * 60)
    print(f"  🟢 Running (Speed > 0):       {running:>6}")
    print(f"  🟡 Idle (Speed = 0):          {idle:>6}")
    print(f"  🔴 No GPS Fix:                {no_gps:>6}")
    
    # Vehicle Types
    types = {}
    for v in vehicles:
        vtype = v.get('VEHICLE_TYPE', 'Unknown')
        types[vtype] = types.get(vtype, 0) + 1
    
    print(f"\n🚗 VEHICLE TYPES:")
    print("-" * 60)
    for vtype, count in sorted(types.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(vehicles) * 100)
        print(f"  {vtype:<30} {count:>4} ({percentage:>5.1f}%)")
    
    # Vendors
    vendors = {}
    for v in vehicles:
        vendor = v.get('VENDOR_NAME', 'Unknown')
        vendors[vendor] = vendors.get(vendor, 0) + 1
    
    print(f"\n📦 TOP VENDORS:")
    print("-" * 60)
    for i, (vendor, count) in enumerate(sorted(vendors.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        percentage = (count / len(vehicles) * 100)
        print(f"  {i}. {vendor[:45]:<45} {count:>4} ({percentage:>5.1f}%)")
    
    # Zones
    zones = {}
    for v in vehicles:
        zone = v.get('ZONE_NAME', 'Unknown')
        zones[zone] = zones.get(zone, 0) + 1
    
    print(f"\n🗺️  ZONES:")
    print("-" * 60)
    for zone, count in sorted(zones.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(vehicles) * 100)
        print(f"  {zone:<40} {count:>4} ({percentage:>5.1f}%)")
    
    print("\n" + "="*60)
    print(f"📅 Data loaded: {len(vehicles)} vehicles")
    print("="*60 + "\n")

if __name__ == "__main__":
    quick_summary()
