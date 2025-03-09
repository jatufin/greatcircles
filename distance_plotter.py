import matplotlib.pyplot as plt

import cartopy.crs as ccrs
import cartopy.feature as cfeature
from  cartopy.geodesic import Geodesic
from geopy.distance import geodesic as geo_distance

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

def _plot_places_and_routes(ax, location: dict, targets: dict, plot_names: bool, transform) -> dict:
    """ Plots distances from the location to all targets
    
    Returns the location name and a list containing target names and distances
    """
    distances = []

    # Loop through starting points
    location_name, (location_lat, location_lon) = list(location.items())[0]
    
    # Place marker
    ax.plot(location_lon, location_lat, "ro", markersize=8, transform=ccrs.PlateCarree())

    # Place name
    if plot_names:
        ax.text(location_lon + 1, location_lat, location_name, fontsize=12, transform=ccrs.PlateCarree())
    
    # Loop through targets
    for target_name, (target_lat, target_lon) in targets.items():
        if target_name == location_name:
            continue
        
        # Place marker and name
        if target_name not in location:
            ax.plot(target_lon, target_lat, "ro", markersize=8, transform=ccrs.PlateCarree())

            if plot_names:
                ax.text(target_lon + 1, target_lat, target_name, fontsize=12, transform=ccrs.PlateCarree())
        
        # The distance line
        plt.plot((location_lon, target_lon), (location_lat, target_lat),
                color='red',  transform=transform)

        # Distance
        distance = geo_distance((location_lat, location_lon), (target_lat, target_lon), ).km
        distance = int(distance)

        distances += [[target_name, distance]]
        
    return location_name, distances

def _get_subplot_kw(projection, location):
    _ , (location_lat, location_lon) = list(location.items())[0]
    
    match projection:
        case "Robinson":
            subplot_kw={"projection": ccrs.Robinson()}
        case "Orthographic":
            subplot_kw={"projection": ccrs.Orthographic(central_latitude=location_lat,
                                                        central_longitude=location_lon)}
        case _:
            subplot_kw={"projection": ccrs.Mercator()}

    return subplot_kw

def plot_distances(location: dict,
                   targets: dict,
                   subplot_args=None,
                   whole_globe=False,
                   pairwaise=False, # TODO: Implement
                   projection="Robinson",
                   great_circles=True,
                   plot_names=True,
                   figsize=(10,8),
                   padding=5):
    """ Plot a map and draw distances between points

    Returns the axis, location name, and the distances in a dictionary
    """

    subplot_kw = _get_subplot_kw(projection, location)

    if not subplot_args:
        _, ax = plt.subplots(figsize=figsize, subplot_kw=subplot_kw)
    else:
        ax = plt.subplot(subplot_args, projection=subplot_kw["projection"])
    
    ### Draw straight lines or great circles
    transform = ccrs.Geodetic() if great_circles else ccrs.PlateCarree()

    _crop_map_area(ax, whole_globe, location, targets, padding)

    _select_map_features(ax)

    location_name, distances = _plot_places_and_routes(ax, location, targets, plot_names, transform)

    return ax, location_name, distances

def distance_table(location,
                    distances,
                    title=None,
                    target_label="Target",
                    distance_label="Distance",
                    font_size=12,
                    subplot_args=None,
                    figsize=(10,8)):
    """ Plot a table of the distances
    
    Arguments:
        distances : The dictionary returned by plot_distances()

    Returns the axis and the table object
    """
    if not subplot_args:
        _, ax = plt.subplots(figsize=figsize)
    else:
        ax = plt.subplot(subplot_args)

    ax.axis("off")
    ax.set_title(title if title else f"Distance from {location} in km")

    table = ax.table(
        cellText=distances,
        colLabels=[target_label, distance_label],
        loc="center",
        cellLoc="center",
        colWidths=[0.7, 0.3]
    )

    table.auto_set_font_size(False)
    table.set_fontsize(font_size)

    return ax, table