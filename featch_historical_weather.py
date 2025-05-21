import requests
import pandas as pd
from datetime import datetime, timedelta

# Define coordinates for Berlin (Französisch Buchholz)
latitude = 52.5913
longitude = 13.4138

# Calculate date range for the past 14 days
end_date = datetime.today()
start_date = end_date - timedelta(days=14)

# Format dates as strings
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

# Define API endpoint and parameters
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date_str,
    "end_date": end_date_str,
    "daily": "temperature_2m_max,precipitation_sum",
    "timezone": "Europe/Berlin"
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    daily_data = data.get("daily", {})
    
    # Create a DataFrame from the data
    df = pd.DataFrame(daily_data)
    
    # Rename columns to match desired format
    df.rename(columns={
        "temperature_2m_max": "Temp Max (°C)",
        "precipitation_sum": "Rain Amount (mm)"
    }, inplace=True)
    
    # Add 'Rain Chance (%)' column as NaN (not available)
    df["Rain Chance (%)"] = None
    
    # Add 'Forecast Run Date' column with the current date
    df["Forecast Run Date"] = datetime.today().strftime('%Y-%m-%d')
    
    # Reorder columns
    df = df[["time", "Temp Max (°C)", "Rain Chance (%)", "Rain Amount (mm)", "Forecast Run Date"]]
    
    # Save to CSV
    df.to_csv("berlin_pankow_franzbucholz_weather_history.csv", index=False)
    
    print("Historical weather data saved successfully.")
else:
    print(f"Failed to fetch data: {response.status_code}")
