#!/usr/bin/env python3
"""
Export vehicles to CSV file
"""

import json
import csv
import os
from datetime import datetime

def export_to_csv():
    json_file = 'vechile_lat_lon.json'
    csv_file = f'vehicles_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        return
    
    # Load vehicle data
    with open(json_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    print(f"📄 Exporting {len(vehicles)} vehicles to CSV...")
    
    # Define CSV columns
    columns = [
        'VEHICLE_RTO_NO',
        'VEHICLE_ID',
        'VEHICLE_TYPE',
        'VEHICLE_MODEL',
        'VEHICLE_STATUS',
        'VEHICLE_SPEED',
        'VEHICLE_LATITUDE',
        'VEHICLE_LONGITUDE',
        'VEHICLE_LOCATION',
        'VEHICLE_ODOMETER',
        'WARD_NAME',
        'ZONE_NAME',
        'VENDOR_NAME',
        'DRIVER_NAME',
        'ACIGNONOFF',
        'UNLOADED',
        'IMEI',
        'DCDATETIME'
    ]
    
    # Write CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(vehicles)
    
    print(f"✅ Successfully exported to: {csv_file}")
    print(f"📊 Total records: {len(vehicles)}")
    print(f"📂 File size: {os.path.getsize(csv_file) / 1024:.2f} KB")

if __name__ == "__main__":
    export_to_csv()
