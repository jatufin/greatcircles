import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from  cartopy.geodesic import Geodesic

coordinates = {
    "Berlin": (52.5200, 13.4050),
    "Paris": (48.8566, 2.3522),
    "Rome": (41.9028, 12.4964),
    "Madrid": (40.4168, -3.7038),
    "Vienna": (48.2082, 16.3738),
    "Helsinki": (60.1699, 24.9384)
}

### Setup the map (Europe)
fix, ax = plt.subplots(figsize=(10, 8), subplot_kw={"projection": ccrs.PlateCarree()})

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=":")
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

ax.set_extent([-10, 30, 35, 65])

### Plot cities
for city, (lat, lon) in coordinates.items():
    ax.plot(lon, lat, "ro", markersize=8, transform=ccrs.PlateCarree())
    ax.text(lon + 1, lat, city, fontsize=12, transform=ccrs.PlateCarree())


### Draw routes
geodesic = Geodesic()

target_name = "Helsinki"
others = dict(coordinates)
target_lat, target_lon = others.pop(target_name)

for city_name, (city_lat, city_lon) in others.items():
    distance = geodesic.inverse((city_lon, city_lat), (target_lon, target_lat))[0, 0]
    points = geodesic.circle
    ax.plot(line[:, 1], line[:, 0],
            "b-", transform=ccrs.PlateCarree())

plt.title(f"From {target_name}")
plt.show()