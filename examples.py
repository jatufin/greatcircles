import matplotlib.pyplot as plt

from distance_plotter import plot_distances, distance_table
from place_coords import *

if __name__ == "__main__":
    #############
    # From London and Helsinki to all other European capitals
    location = { "Helsinki": europe_capitals["Helsinki"] }

    ax, location_name, distances = plot_distances(location, europe_capitals)

    plt.show()

    #############
    # 4x4 subplots
    #
    # Straight line from Paris to Vienna
    ax, location_name, distances = plot_distances({"Paris": (48.8566, 2.3522)},
                                {"Vienna": (48.2082, 16.3738)},
                                great_circles=False,
                                subplot_args=221)

    # Distance on the subplot below
    ax, table = distance_table(location_name, distances, subplot_args=223)

    # Great circles from Berlin to Paris, Rome and Madrid
    ax, location_name, distances = plot_distances({"Berlin": (52.5200, 13.4050)},
                                {"Paris": (48.8566, 2.3522),
                                    "Rome": (41.9028, 12.4964),
                                    "Madrid": (40.4168, -3.7038)},
                                subplot_args=222,
                                projection="Mercator")
    
    # Distances on the subplot below
    ax, table = distance_table(location_name, distances, subplot_args=224)
    
    plt.show()

    #############
    # The map and the distances side by side
    #
    # Distances from Point Nemo to the nearest islands
    ax, location_name, distances = plot_distances(point_nemo, closest_to_point_nemo,
                                    whole_globe=True,
                                    subplot_args=121,
                                    projection="Orthographic")

    # Distances on the subplot to the right
    ax, table = distance_table(location_name, distances, subplot_args=122)

    plt.show()