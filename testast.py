from astral import LocationInfo
city = LocationInfo("London", "England", "Europe/London", 51.5, -0.116)
print((
    f"Information for {city.name}/{city.region}\n"
    f"Timezone: {city.timezone}\n"
    f"Latitude: {city.latitude:.02f}; Longitude: {city.longitude:.02f}\n"
))

