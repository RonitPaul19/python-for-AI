import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

# =========================
# Get Current Location
# =========================

try:
  location_response = requests.get(
      "https://ipinfo.io/json",
      timeout=10
  )

  location_response.raise_for_status()

  location_data = location_response.json()

except requests.RequestException as e:
  print(f"Error fetching location data: {e}")
  exit()

if "loc" not in location_data:
  print("Could not determine location from IP.")
  print(location_data)
  exit()

city = location_data.get("city", "Unknown_City")
region = location_data.get("region", "Unknown_Region")

latitude, longitude = location_data["loc"].split(",")

print(f"Location : {city}, {region}")
print(f"Latitude : {latitude}")
print(f"Longitude: {longitude}")

# =========================
# Calculate Last 7 Days
# =========================

today = datetime.now()

# Exactly 7 days including today
start_date = (today - timedelta(days=6)).strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

print(f"\nFetching weather data from {start_date} to {end_date}")

# =========================
# Fetch Weather Data
# =========================

weather_url = (
    "https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    f"&start_date={start_date}"
    f"&end_date={end_date}"
    "&daily=temperature_2m_max,temperature_2m_min"
)

try:
  weather_response = requests.get(
      weather_url,
      timeout=15
  )

  weather_response.raise_for_status()

  weather_data = weather_response.json()

except requests.RequestException as e:
  print(f"Error fetching weather data: {e}")
  exit()

if "daily" not in weather_data:
  print("Weather data unavailable.")
  print(weather_data)
  exit()

# =========================
# Create DataFrame
# =========================

df = pd.DataFrame({
    "date": weather_data["daily"]["time"],
    "max_temp": weather_data["daily"]["temperature_2m_max"],
    "min_temp": weather_data["daily"]["temperature_2m_min"]
})

df["date"] = pd.to_datetime(df["date"])

df["avg_temp"] = (
    df["max_temp"] + df["min_temp"]
) / 2

print("\nWeather Data:")
print(df)

# =========================
# Safe File Names
# =========================

safe_city = re.sub(
    r'[^a-zA-Z0-9_\- ]',
    '',
    city
).replace(" ", "_")

# =========================
# Create Data Folder
# =========================

os.makedirs("data", exist_ok=True)

csv_file = f"data/{safe_city}_weather.csv"

# Save CSV
df.to_csv(csv_file, index=False)

print(f"\nData saved to:")
print(csv_file)

# =========================
# Plot Weather Graph
# =========================

plt.figure(figsize=(10, 6))

plt.plot(
    df["date"],
    df["max_temp"],
    marker="o",
    label="Max Temperature"
)

plt.plot(
    df["date"],
    df["min_temp"],
    marker="o",
    label="Min Temperature"
)

plt.plot(
    df["date"],
    df["avg_temp"],
    marker="o",
    linestyle="--",
    label="Average Temperature"
)

plt.title(
    f"{city}, {region} Weather - Last 7 Days"
)

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

plt.grid(True)
plt.legend()

plt.xticks(rotation=45)

plt.tight_layout()

# =========================
# Save Chart
# =========================

chart_file = (
    f"{safe_city.lower()}_weather_chart.png"
)

plt.savefig(
    chart_file,
    dpi=300,
    bbox_inches="tight"
)

print(f"\nChart saved as:")
print(chart_file)

# Show Plot
plt.show()
