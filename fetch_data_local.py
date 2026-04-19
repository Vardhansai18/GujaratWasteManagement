#!/usr/bin/env python3
"""
Fetch vehicle data from local machine with network access.
Run this script on a machine that can access swm.suratmunicipal.org,
then upload the generated vechile_lat_lon.json file to the server.

Usage:
    python3 fetch_data_local.py
    
    # Then upload to server:
    scp vechile_lat_lon.json root@10.197.36.30:/root/projects/GujaratWasteManagement/
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fetch_vehicle_data():
    """Fetch latest vehicle data from Surat Municipal website"""
    driver = None
    try:
        print("=" * 60)
        print("🚛 Fetching Vehicle Data from Surat Municipal Corporation")
        print("=" * 60)
        
        # Launch browser
        print("\n🌐 Launching Chrome...")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 20)
        
        # Open URL & Login
        url = "https://swm.suratmunicipal.org/Tracking/LiveTrackingO"
        print(f"📡 Navigating to {url}...")
        driver.get(url)
        
        # Fill username
        print("🔐 Logging in...")
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
        print("🍪 Extracting session...")
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
        print("📊 Fetching vehicle data...")
        response = session.post(api_url, json=payload, headers=headers)
        driver.quit()
        driver = None
        
        if response.status_code == 200:
            data = response.json()
            
            # Save to file
            output_file = "vechile_lat_lon.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Successfully fetched {len(data)} vehicle records")
            print(f"📁 Saved to: {output_file}")
            print("\n" + "=" * 60)
            print("📤 Upload to server using:")
            print(f"   scp {output_file} root@10.197.36.30:/root/projects/GujaratWasteManagement/")
            print("=" * 60)
            
            return True
        else:
            print(f"\n❌ API returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if driver:
            driver.quit()
        return False

if __name__ == "__main__":
    success = fetch_vehicle_data()
    exit(0 if success else 1)
