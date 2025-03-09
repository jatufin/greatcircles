import matplotlib.pyplot as plt

from distance_plotter import plot_distances, distance_table
from place_coords import *

if __name__ == "__main__":
    #############
    # From London and Helsinki to all other European capitals
    names = ["London", "Helsinki"]
    starts = { city: europe_capitals[city] for city in names \
              if city in europe_capitals }
    print("Starts ***************************")
    print(starts)
    ax, distances = plot_distances(starts, europe_capitals)

    plt.show()

    #############
    # 4x4 subplots
    #
    # Straight line from Paris to Vienna
    ax, distances = plot_distances({"Paris": (48.8566, 2.3522)},
                                {"Vienna": (48.2082, 16.3738)},
                                great_circles=False,
                                subplot_args=221)

    # Distance on the subplot below
    ax, table = distance_table(distances, subplot_args=223)

    # Great circles from Berlin to Paris, Rome and Madrid
    ax, distances = plot_distances({"Berlin": (52.5200, 13.4050)},
                                {"Paris": (48.8566, 2.3522),
                                    "Rome": (41.9028, 12.4964),
                                    "Madrid": (40.4168, -3.7038)},
                                subplot_args=222,
                                projection="Mercator")
    
    # Distances on the subplot below
    ax, table = distance_table(distances, subplot_args=224)
    
    plt.show()

    #############
    # The map and the distances side by side
    #
    # Distances from Point Nemo to the nearest islands
    ax, distances = plot_distances(point_nemo, closest_to_point_nemo,
                                    whole_globe=True,
                                    subplot_args=121)

    # Distances on the subplot to the right
    ax, table = distance_table(distances, subplot_args=122)

    plt.show()