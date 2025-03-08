import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from  cartopy.geodesic import Geodesic

def _crop_map_area(ax, whole_globe, starts, targets, padding):
    if whole_globe:
        ax.set_global()
    else:
        start_lats, start_longs = zip(*starts.values())
        target_lats, target_longs = zip(*targets.values())

        lats = start_lats + target_lats
        longs = start_longs + target_longs

        ax.set_extent([min(longs) - padding, max(longs) + padding,
                       min(lats) - padding, max(lats) + padding])

def _select_map_features(ax):
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=":")
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

def _plot_places_and_routes(ax, starts, targets, plot_names, transform):
    for start, (start_lat, start_lon) in starts.items():
        ax.plot(start_lon, start_lat, "ro", markersize=8, transform=ccrs.PlateCarree())

        if plot_names:
            ax.text(start_lon + 1, start_lat, start, fontsize=12, transform=ccrs.PlateCarree())
        
        for target, (target_lat, target_lon) in targets.items():
            if target == start:
                continue

            if target not in starts:
                ax.plot(target_lon, target_lat, "ro", markersize=8, transform=ccrs.PlateCarree())

                if plot_names:
                    ax.text(target_lon + 1, target_lat, target, fontsize=12, transform=ccrs.PlateCarree())
      
            plt.plot((start_lon, target_lon), (start_lat, target_lat),
                 color='red',  transform=transform)

def _get_subplot_kw(projection):
    match projection:
        case "Robinson":
            subplot_kw={"projection": ccrs.Robinson()}
        case "Orthographic":
            subplot_kw={"projection": ccrs.Orthographic()}
        case _:
            subplot_kw={"projection": ccrs.Mercator()}

    return subplot_kw

def plot_distances(starts: dict,
                   targets: dict,
                   whole_globe=True,
                   projection="Robinson",
                   great_circles=True,
                   plot_names=True,
                   distances=True,
                   figsize=(10,8),
                   padding=5):
    """ Plot a map and draw distances between points
    """

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=_get_subplot_kw(projection))
    
    ### Draw straight lines or great circles
    transform = ccrs.Geodetic() if great_circles else ccrs.PlateCarree()

    _crop_map_area(ax, whole_globe, starts, targets, padding)

    _select_map_features(ax)

    _plot_places_and_routes(ax, starts, targets, plot_names, transform)

    plt.show()

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

    plot_distances(starts, targets, whole_globe=False, great_circles=True)