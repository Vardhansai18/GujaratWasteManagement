#!/usr/bin/env python3
"""
Generate HTML table with all vehicle details
"""

import json
import os
from datetime import datetime

def generate_html_table():
    json_file = 'vechile_lat_lon.json'
    html_file = f'vehicles_table_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    
    if not os.path.exists(json_file):
        print(f"❌ Error: {json_file} not found!")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        vehicles = json.load(f)
    
    print(f"📄 Generating HTML table for {len(vehicles)} vehicles...")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Surat Municipal Corporation - Vehicle Fleet Table</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2em;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 15px;
            font-size: 0.9em;
        }}
        
        .stat {{
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .controls {{
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }}
        
        .search-box {{
            flex: 1;
            min-width: 300px;
        }}
        
        .search-box input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            font-size: 1em;
        }}
        
        .search-box input:focus {{
            outline: none;
            border-color: #667eea;
        }}
        
        .filter-group {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .filter-group select {{
            padding: 10px;
            border: 2px solid #dee2e6;
            border-radius: 5px;
            background: white;
            cursor: pointer;
        }}
        
        .table-container {{
            overflow-x: auto;
            max-height: calc(100vh - 300px);
            overflow-y: auto;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}
        
        thead {{
            position: sticky;
            top: 0;
            background: #495057;
            color: white;
            z-index: 10;
        }}
        
        th {{
            padding: 15px 10px;
            text-align: left;
            font-weight: 600;
            white-space: nowrap;
            border-right: 1px solid #6c757d;
        }}
        
        th:last-child {{
            border-right: none;
        }}
        
        tbody tr {{
            border-bottom: 1px solid #dee2e6;
            transition: background 0.2s;
        }}
        
        tbody tr:hover {{
            background: #f8f9fa;
        }}
        
        tbody tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        
        tbody tr:nth-child(even):hover {{
            background: #e9ecef;
        }}
        
        td {{
            padding: 12px 10px;
            border-right: 1px solid #dee2e6;
        }}
        
        td:last-child {{
            border-right: none;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .status-running {{
            background: #d4edda;
            color: #155724;
        }}
        
        .status-idle {{
            background: #fff3cd;
            color: #856404;
        }}
        
        .status-ngf {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .map-link {{
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        
        .map-link:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            padding: 20px;
            text-align: center;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            color: #6c757d;
        }}
        
        .no-results {{
            text-align: center;
            padding: 40px;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚛 Surat Municipal Corporation</h1>
            <p>Waste Management - Complete Vehicle Fleet</p>
            <div class="stats">
                <div class="stat">
                    <div class="stat-value">{len(vehicles)}</div>
                    <div>Total Vehicles</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{vehicles[0].get('CONNECTED_FLEET', 0)}</div>
                    <div>Connected</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{vehicles[0].get('RUNNING_FLEET', 0)}</div>
                    <div>Running</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{vehicles[0].get('IDEL_FLEET', 0)}</div>
                    <div>Idle</div>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search by RTO Number, Vehicle ID, Location, Vendor, Zone..." onkeyup="filterTable()">
            </div>
            <div class="filter-group">
                <label>Type:</label>
                <select id="typeFilter" onchange="filterTable()">
                    <option value="">All Types</option>
                    <option value="DOOR TO DOOR">Door to Door</option>
                    <option value="TEMPO - BOGCV">Tempo - BOGCV</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Status:</label>
                <select id="statusFilter" onchange="filterTable()">
                    <option value="">All Status</option>
                    <option value="running">Running</option>
                    <option value="idle">Idle</option>
                    <option value="ngf">No GPS</option>
                </select>
            </div>
        </div>
        
        <div class="table-container">
            <table id="vehicleTable">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>RTO Number</th>
                        <th>Vehicle ID</th>
                        <th>Type</th>
                        <th>Model</th>
                        <th>Speed</th>
                        <th>Status</th>
                        <th>Ignition</th>
                        <th>Load</th>
                        <th>Location</th>
                        <th>Latitude</th>
                        <th>Longitude</th>
                        <th>Map</th>
                        <th>Ward</th>
                        <th>Zone</th>
                        <th>Vendor</th>
                        <th>Driver</th>
                        <th>Odometer</th>
                        <th>IMEI</th>
                        <th>Last Update</th>
                    </tr>
                </thead>
                <tbody>
"""
    
    # Add vehicle rows
    for i, vehicle in enumerate(vehicles, 1):
        speed = vehicle.get('VEHICLE_SPEED', 0)
        status = vehicle.get('VEHICLE_STATUS', 'N/A')
        
        # Determine status badge
        if speed > 0:
            status_class = "status-running"
            status_text = "RUNNING"
        elif status == "NGF":
            status_class = "status-ngf"
            status_text = "NO GPS"
        else:
            status_class = "status-idle"
            status_text = "IDLE"
        
        lat = vehicle.get('VEHICLE_LATITUDE', '')
        lon = vehicle.get('VEHICLE_LONGITUDE', '')
        map_url = f"https://www.google.com/maps?q={lat},{lon}"
        
        html += f"""
                    <tr data-type="{vehicle.get('VEHICLE_TYPE', '')}" data-status="{status_text.lower()}">
                        <td>{i}</td>
                        <td><strong>{vehicle.get('VEHICLE_RTO_NO', 'N/A')}</strong></td>
                        <td>{vehicle.get('VEHICLE_ID', 'N/A')}</td>
                        <td>{vehicle.get('VEHICLE_TYPE', 'N/A')}</td>
                        <td>{vehicle.get('VEHICLE_MODEL', 'N/A')}</td>
                        <td><strong>{speed} km/h</strong></td>
                        <td><span class="status-badge {status_class}">{status_text}</span></td>
                        <td>{vehicle.get('ACIGNONOFF', 'N/A')}</td>
                        <td>{vehicle.get('UNLOADED', 'N/A')}</td>
                        <td style="max-width: 300px;">{vehicle.get('VEHICLE_LOCATION', 'N/A')}</td>
                        <td>{lat}</td>
                        <td>{lon}</td>
                        <td><a href="{map_url}" target="_blank" class="map-link">📍 View</a></td>
                        <td>{vehicle.get('WARD_NAME', 'N/A')}</td>
                        <td>{vehicle.get('ZONE_NAME', 'N/A')}</td>
                        <td>{vehicle.get('VENDOR_NAME', 'N/A')}</td>
                        <td>{vehicle.get('DRIVER_NAME', 'N/A')}</td>
                        <td>{vehicle.get('VEHICLE_ODOMETER', 'N/A')} km</td>
                        <td>{vehicle.get('IMEI', 'N/A')}</td>
                        <td>{vehicle.get('DCDATETIME', 'N/A')}</td>
                    </tr>
"""
    
    html += f"""
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Total Records: <strong>{len(vehicles)}</strong></p>
            <p>© 2026 Surat Municipal Corporation - Waste Management Division</p>
        </div>
    </div>
    
    <script>
        function filterTable() {{
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const typeFilter = document.getElementById('typeFilter').value.toLowerCase();
            const statusFilter = document.getElementById('statusFilter').value.toLowerCase();
            const table = document.getElementById('vehicleTable');
            const rows = table.getElementsByTagName('tr');
            
            let visibleCount = 0;
            
            for (let i = 1; i < rows.length; i++) {{
                const row = rows[i];
                const text = row.textContent.toLowerCase();
                const rowType = row.getAttribute('data-type').toLowerCase();
                const rowStatus = row.getAttribute('data-status').toLowerCase();
                
                let showRow = true;
                
                // Search filter
                if (searchInput && !text.includes(searchInput)) {{
                    showRow = false;
                }}
                
                // Type filter
                if (typeFilter && !rowType.includes(typeFilter)) {{
                    showRow = false;
                }}
                
                // Status filter
                if (statusFilter && rowStatus !== statusFilter) {{
                    showRow = false;
                }}
                
                row.style.display = showRow ? '' : 'none';
                if (showRow) visibleCount++;
            }}
            
            // Update footer count
            const footer = document.querySelector('.footer p');
            footer.innerHTML = `Showing <strong>${{visibleCount}}</strong> of <strong>{len(vehicles)}</strong> vehicles | Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`;
        }}
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Successfully generated: {html_file}")
    print(f"📊 Total vehicles: {len(vehicles)}")
    print(f"📂 File size: {os.path.getsize(html_file) / 1024:.2f} KB")
    print(f"\n🌐 Open in browser:")
    print(f"   open {html_file}  (macOS)")
    print(f"   or double-click the file")

if __name__ == "__main__":
    generate_html_table()
