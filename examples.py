import matplotlib.pyplot as plt

from distance_plotter import plot_distances
from examples import *

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

    plot_distances(starts, targets, great_circles=False)
    plt.show()

    plot_distances({"Paris": (48.8566, 2.3522)},
                   {"Vienna": (48.2082, 16.3738)},
                   whole_globe=True,
                   subplot_args=121)

    plot_distances({"Berlin": (52.5200, 13.4050)},
                   {"Paris": (48.8566, 2.3522),
                    "Rome": (41.9028, 12.4964),
                    "Madrid": (40.4168, -3.7038)},
                   subplot_args=122,
                   projection="Mercator")
    plt.show()