# Vehicle Tracking Dashboard - Surat Municipal Corporation

## 🚛 Overview
Complete vehicle tracking system for waste management fleet in Surat Municipal Corporation.

## ✨ Features
- **Automated Data Fetching**: Logs in and retrieves real-time GPS data for 1000+ vehicles
- **JSON Export**: Saves complete vehicle data with GPS coordinates
- **Web Dashboard**: Beautiful search interface with real-time statistics
- **Vehicle Search**: Search by RTO number or Vehicle ID
- **Detailed Information**: View complete vehicle details including location, speed, status
- **Google Maps Integration**: Direct links to vehicle locations

## 📦 Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Method 1: All-in-One Launcher (Recommended)
```bash
python3 start.py
```
Then choose:
- **Option 1**: Fetch vehicle data only
- **Option 2**: Launch web dashboard only (requires existing data)
- **Option 3**: Fetch data then launch dashboard

### Method 2: Manual Steps

#### Step 1: Fetch Vehicle Data
```bash
python3 server.py
```
This will:
- Login to the tracking system  
- Fetch GPS data for all vehicles
- Save to `vechile_lat_lon.json`

#### Step 2: Launch Web Dashboard
```bash
python3 app.py
```
Then open your browser to: **http://localhost:5001**

## 🎯 Using the Web Dashboard

1. **View Statistics**: See fleet overview (total, running, idle, disconnected)
2. **Search Vehicle**: Enter RTO number (e.g., GJ05GV2306) or Vehicle ID
3. **View Details**: See complete vehicle information including:
   - Current location and GPS coordinates
   - Speed and direction
   - Vehicle type and model
   - Driver and vendor details
   - Ignition status and load status
   - Last update time
4. **Google Maps**: Click "View on Google Maps" to see exact location

## 📊 Data Structure

Each vehicle record contains:
- Vehicle identification (ID, RTO number, IMEI)
- GPS data (latitude, longitude, location)
- Status (speed, direction, ignition)
- Assignment (driver, vendor, zone, ward)
- Metrics (odometer, last update)

## 🔐 Credentials

Login credentials are configured in `server.py`:
- Username: `Public`
- Password: `Public#1`

## 📁 File Structure

```
sunny_bro/
├── server.py              # Data fetching script
├── app.py                 # Flask web application
├── start.py              # All-in-one launcher
├── requirements.txt       # Python dependencies
├── vechile_lat_lon.json  # Vehicle data (generated)
└── templates/
    └── index.html        # Web dashboard UI
```

## 🛠️ Technical Details

- **Backend**: Python 3.12, Flask, Selenium
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Data Source**: Surat Municipal Corporation API
- **Browser**: Chrome (headless mode)

## 📝 Notes

- The system fetches data in headless mode (no browser window)
- Data is refreshed each time you run `server.py`
- Web dashboard reads from the JSON file (no real-time updates)
- For real-time tracking, re-run the data fetch script

## 🐛 Troubleshooting

**Web dashboard shows "No data":**
- Run `python3 server.py` first to fetch data

**Login fails:**
- Check credentials in server.py
- Verify internet connection
- Check if website is accessible

**Port 5000 already in use:**
- Stop other Flask apps or change port in app.py

## 📄 License

For Surat Municipal Corporation internal use.
