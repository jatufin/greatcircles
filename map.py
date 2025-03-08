import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from  cartopy.geodesic import Geodesic


def plotdistances(starts, targets,
                  whole_globe=True, projection="Robinson", great_circles=True,
                  names=True,
                  distances=True,
                  figsize=(10,8),
                  padding=5):
    """ Plot a map and draw distances between points
    """

    match projection:
            case "Robinson":
              subplot_kw={"projection": ccrs.Robinson()}
            case _:
              subplot_kw={"projection": ccrs.Mercator()}

    
    transform = ccrs.Geodetic() if great_circles else ccrs.PlateCarree()

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=subplot_kw)

    # Crop area
    PADDING = 5

    if whole_globe:
        ax.set_global()
    else:
        start_lats, start_longs = zip(*starts.values())
        target_lats, target_longs = zip(*targets.values())

        lats = start_lats + target_lats
        longs = start_longs + target_longs

        ax.set_extent([min(longs) - padding, max(longs) + padding,
                       min(lats) - padding, max(lats) + padding])

    # Features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    ### Plot places and routes
    for start, (start_lat, start_lon) in starts.items():
        ax.plot(start_lon, start_lat, "ro", markersize=8, transform=ccrs.PlateCarree())
        ax.text(start_lon + 1, start_lat, start, fontsize=12, transform=ccrs.PlateCarree())
        
        for target, (target_lat, target_lon) in targets.items():
            if target == start:
                continue

            if target not in starts:
                ax.plot(target_lon, target_lat, "ro", markersize=8, transform=ccrs.PlateCarree())
                ax.text(target_lon + 1, target_lat, target, fontsize=12, transform=ccrs.PlateCarree())
      
            plt.plot((start_lon, target_lon), (start_lat, target_lat),
                 color='red',  transform=transform)

    plt.show()
    return

if __name__ == "__main__":
    starts = {
        "Helsinki": (60.1699, 24.9384),
        "London": (51.5074, -0.1278)
    }

    targets = {
        "Berlin": (52.5200, 13.4050),
        "Paris": (48.8566, 2.3522),
        "Rome": (41.9028, 12.4964),
        "Madrid": (40.4168, -3.7038),
        "Vienna": (48.2082, 16.3738),
    }

    plotdistances(starts, targets, whole_globe=False, great_circles=False)