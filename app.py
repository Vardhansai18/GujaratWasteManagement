from flask import Flask, render_template, request, jsonify
import json
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Load vehicle data
def load_vehicle_data():
    json_file = 'vechile_lat_lon.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    """Main page with search interface"""
    return render_template('index.html')

@app.route('/table')
def table_view():
    """Complete table view with all vehicles"""
    return render_template('table.html')

@app.route('/vechile_lat_lon.json')
def get_json_data():
    """Serve the JSON file directly"""
    vehicles = load_vehicle_data()
    return jsonify(vehicles)

@app.route('/api/vehicles')
def get_all_vehicles():
    """Get all vehicle IDs for autocomplete"""
    vehicles = load_vehicle_data()
    vehicle_ids = [v.get('VEHICLE_RTO_NO', '') for v in vehicles if v.get('VEHICLE_RTO_NO')]
    return jsonify(vehicle_ids)

@app.route('/api/search')
def search_vehicle():
    """Search for a specific vehicle by ID"""
    query = request.args.get('q', '').strip().upper()
    
    if not query:
        return jsonify({'error': 'Please provide a search query'}), 400
    
    vehicles = load_vehicle_data()
    
    # Search by VEHICLE_RTO_NO or VEHICLE_ID
    results = []
    for vehicle in vehicles:
        rto_no = vehicle.get('VEHICLE_RTO_NO', '').upper()
        vehicle_id = vehicle.get('VEHICLE_ID', '').upper()
        
        if query in rto_no or query in vehicle_id or query == rto_no or query == vehicle_id:
            results.append(vehicle)
    
    if results:
        return jsonify(results)
    else:
        return jsonify({'error': f'No vehicle found with ID: {query}'}), 404

@app.route('/api/stats')
def get_stats():
    """Get statistics about the fleet"""
    vehicles = load_vehicle_data()
    
    if not vehicles:
        return jsonify({'error': 'No data available'}), 404
    
    # Get stats from first vehicle (they all have same fleet stats)
    first_vehicle = vehicles[0]
    
    stats = {
        'total_fleet': first_vehicle.get('TOTAL_FLEET', 0),
        'connected_fleet': first_vehicle.get('CONNECTED_FLEET', 0),
        'disconnected_fleet': first_vehicle.get('DISCONNECTED_FLEET', 0),
        'idle_fleet': first_vehicle.get('IDEL_FLEET', 0),
        'running_fleet': first_vehicle.get('RUNNING_FLEET', 0),
        'total_vehicles': len(vehicles)
    }
    
    return jsonify(stats)

@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Fetch latest data from API and update JSON file"""
    try:
        print("\n🔄 Starting data refresh...")
        
        # Launch browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        
        # Open URL & Login
        url = "https://swm.suratmunicipal.org/Tracking/LiveTrackingO"
        driver.get(url)
        
        # Fill username
        username_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))
        )
        username_field.clear()
        username_field.send_keys("Public")
        
        # Fill password
        password_field = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
        )
        password_field.clear()
        password_field.send_keys("Public#1")
        
        # Click login
        login_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()
        time.sleep(5)
        
        # Extract cookies
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Extract CSRF token
        token = driver.execute_script("""
        var el = document.querySelector('input[name="__RequestVerificationToken"]');
        return el ? el.value : null;
        """)
        
        # Prepare API request
        api_url = "https://swm.suratmunicipal.org/Dashboard/VehicleGPSStatus/GetVehicleGPSStatus"
        
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://swm.suratmunicipal.org/Dashboard/VehicleGPSStatus",
            "Origin": "https://swm.suratmunicipal.org",
            "User-Agent": "Mozilla/5.0"
        }
        
        if token:
            headers["RequestVerificationToken"] = token
        
        payload = {
            "zone": "0",
            "ward": "0",
            "vendor": "",
            "vehicletype": "0",
            "dept_id": "0"
        }
        
        # Call API
        response = session.post(api_url, json=payload, headers=headers)
        driver.quit()
        
        if response.status_code == 200:
            data = response.json()
            
            # Save to file
            output_file = "vechile_lat_lon.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Successfully refreshed {len(data)} records")
            
            return jsonify({
                'success': True,
                'message': f'Successfully refreshed {len(data)} vehicle records',
                'count': len(data),
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({
                'success': False,
                'error': f'API returned status code {response.status_code}'
            }), 500
            
    except Exception as e:
        print(f"❌ Refresh failed: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Support for cloud deployment (Render, Railway, etc.)
    port = int(os.environ.get('PORT', 5001))
    print("=" * 60)
    print("🚛 Vehicle Tracking Dashboard")
    print("=" * 60)
    print(f"Server starting at: http://0.0.0.0:{port}")
    print("Press CTRL+C to stop")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=port)
