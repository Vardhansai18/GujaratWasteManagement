import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -------------------------------
# Step 1: Launch browser
# -------------------------------
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # optional

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# -------------------------------
# Step 2: Open URL & Login
# -------------------------------
url = "https://swm.suratmunicipal.org/Tracking/LiveTrackingO"
driver.get(url)

try:
    print("Attempting to log in...")

    # Username
    username_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))
    )
    username_field.clear()
    username_field.send_keys("Public")

    # Password
    password_field = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))
    )
    password_field.clear()
    password_field.send_keys("Public#1")

    # Login button
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()

    print("Login submitted")

    # Wait for redirect / page load
    time.sleep(5)

except Exception as e:
    print("Login failed:", e)
    driver.quit()
    exit()

# -------------------------------
# Step 3: Extract cookies
# -------------------------------
session = requests.Session()

for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

print("Cookies transferred")

# -------------------------------
# Step 4: Extract CSRF token
# -------------------------------
token = driver.execute_script("""
var el = document.querySelector('input[name="__RequestVerificationToken"]');
return el ? el.value : null;
""")

print("CSRF Token:", token)

# -------------------------------
# Step 5: Prepare API request
# -------------------------------
api_url = "https://swm.suratmunicipal.org/Dashboard/VehicleGPSStatus/GetVehicleGPSStatus"

headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://swm.suratmunicipal.org/Dashboard/VehicleGPSStatus",
    "Origin": "https://swm.suratmunicipal.org",
    "User-Agent": "Mozilla/5.0"
}

# Important for ASP.NET
if token:
    headers["RequestVerificationToken"] = token

payload = {
    "zone": "0",
    "ward": "0",
    "vendor": "",
    "vehicletype": "0",
    "dept_id": "0"
}

# -------------------------------
# Step 6: Call API
# -------------------------------
response = session.post(api_url, json=payload, headers=headers)

print("Status Code:", response.status_code)

# -------------------------------
# Step 7: Handle response
# -------------------------------
try:
    data = response.json()
    print("Total records:", len(data))
    print("First 2 records:", data[:2])
    
    # Save the complete JSON response to file
    output_file = "vechile_lat_lon.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully saved {len(data)} records to {output_file}")
    
except Exception as e:
    print("Non-JSON response or error:", e)
    print(response.text[:1000])

# -------------------------------
# Step 8: Cleanup
# -------------------------------
driver.quit()

print("\n" + "="*60)
print("✅ SUCCESS! Vehicle data saved to: vechile_lat_lon.json")
print("="*60)
print("\nNext steps:")
print("  1. To view data in web dashboard, run:")
print("     python3 app.py")
print("\n  2. Or use the launcher:")
print("     python3 start.py")
print("="*60)