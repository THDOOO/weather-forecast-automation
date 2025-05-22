import requests
import pandas as pd
from datetime import datetime
import os

# Coordinates for Berlin Pankow Französich Bucholz
lat = 52.5913
lon = 13.4138

# Define API URL and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
    "timezone": "Europe/Berlin",
    "forecast_days": 16
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    daily_data = data["daily"]

    df = pd.DataFrame(daily_data)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)

    df.rename(columns={
        "temperature_2m_max": "Temp Max (°C)",
        "temperature_2m_min": "Temp Min (°C)",
        "precipitation_probability_max": "Rain Chance (%)",
        "precipitation_sum": "Rain Amount (mm)"
    }, inplace=True)

    df["Temp Avg (°C)"] = (df["Temp Max (°C)"] + df["Temp Min (°C)"]) / 2

    run_date = datetime.now().strftime("%Y-%m-%d")
    df["Forecast Run Date"] = run_date

    df = df[["Temp Max (°C)", "Rain Chance (%)", "Rain Amount (mm)", "Forecast Run Date"]]

    csv_file = "berlin_pankow_franzbucholz_weather_forecast.csv"

    # Debug output before writing
    print("\n=== DEBUG INFO BEFORE WRITE ===")
    file_exists = os.path.exists(csv_file)
    file_size_before = os.path.getsize(csv_file) if file_exists else 0
    print("CSV file exists:", file_exists)
    print("CSV file size before write:", file_size_before)

    # Determine whether to write header
    write_header = not file_exists or file_size_before == 0

    # Append data
    df.to_csv(csv_file, mode='a', header=write_header)

    # Debug output after writing
    print("\n=== DEBUG INFO AFTER WRITE ===")
    file_size_after = os.path.getsize(csv_file)
    print("CSV file size after write:", file_size_after)

    print("\n=== LAST LINES OF CSV ===")
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-10:]
            for line in lines:
                print(line.strip())
    except Exception as e:
        print("Error reading back CSV:", e)

    print(f"\n✅ Forecast data saved to {csv_file}")

else:
    print("❌ Failed to fetch data:", response.status_code)
