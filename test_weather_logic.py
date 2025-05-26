# test_weather_logic.py
from weather_logic import process_weather_data

def test_process_weather_data():
    sample_data = {
        "time": ["2025-05-26"],
        "temperature_2m_max": [25.0],
        "temperature_2m_min": [15.0],
        "precipitation_probability_max": [80],
        "precipitation_sum": [5.5]
    }

    df = process_weather_data(sample_data)

    assert list(df.columns) == [
        "Temp Max (°C)",
        "Rain Chance (%)",
        "Rain Amount (mm)",
        "Forecast Run Date"
    ]

    assert df.iloc[0]["Temp Max (°C)"] == 25.0
    assert df.iloc[0]["Rain Chance (%)"] == 80
    assert df.iloc[0]["Rain Amount (mm)"] == 5.5
    assert df.iloc[0]["Forecast Run Date"].startswith("2025-")
