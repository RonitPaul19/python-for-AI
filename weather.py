import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# Get current location from IP
location_data = requests.get("https://ipinfo.io/json").json()

city = location_data.get("city", "Unknown City")
region = location_data.get("region", "Unknown Region")
latitude, longitude = location_data["loc"].split(",")

print(f"Location: {city}, {region}")
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")

# Calculate date range (last 7 days)
today = datetime.now()
week_ago = today - timedelta(days=7)

start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

# Fetch historical weather data
url = (
    f"https://archive-api.open-meteo.com/v1/archive"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    f"&start_date={start_date}"
    f"&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min"
)

response = requests.get(url)
data = response.json()

# Create DataFrame
df = pd.DataFrame({
    "date": data["daily"]["time"],
    "max_temp": data["daily"]["temperature_2m_max"],
    "min_temp": data["daily"]["temperature_2m_min"]
})

df["date"] = pd.to_datetime(df["date"])
df["avg_temp"] = (df["max_temp"] + df["min_temp"]) / 2

print("\nWeather Data:")
print(df)

# Plot
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

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title(f"{city}, {region} Weather - Past 7 Days")

plt.grid(True)
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()

# Save chart
filename = f"{city.lower().replace(' ', '_')}_weather_chart.png"
plt.savefig(filename, dpi=300)

print(f"\nChart saved as: {filename}")

plt.show()
