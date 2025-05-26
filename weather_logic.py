# weather_logic.py
import pandas as pd
from datetime import datetime

def process_weather_data(daily_data: dict) -> pd.DataFrame:
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

    return df[["Temp Max (°C)", "Rain Chance (%)", "Rain Amount (mm)", "Forecast Run Date"]]
