import matplotlib.pyplot as plt
import numpy as np


def show_extremes(timeseries, threshold):
    """
    Given a timeseries, this script identifies all independent fluctuations
    above a specified threshold.

    Parameters
    ----------
    timeseries: numpy.array
        the timeseries
    threshold: float
        the threshold above which to sample extremes
    min_time_between_extremes: float
        the minimal time above which two extreme events are considered
        independant from each other.

    Returns
    -------
    plot_extremes
        A matplotlib figure representing the timeseries, with the identified
        fluctations marked with red dots. The value of the threshold is
        represented by a horizontal line.
    """

    def group_correlated_points(series, dist):
        """
        Given a series of numbers SERIES, return a list of lists, each sublist
        containing subsequent elements distant from less than DIST elements of
        the next one.

        Parameters
        -----------
        series: numpy.array
        dist: int

        Returns
        --------
        list of lists
        """
        group = []
        list_of_groups = []
        group.append(series[0])
        for tup in zip(series, series[1:]):
            if (tup[1] - tup[0]) < dist:
                group.append(tup[1])
            else:
                list_of_groups.append(group.copy())
                group.clear()
                group.append(tup[1])

        list_of_groups.append(group.copy())
        return list_of_groups

    timepoints_with_value_above_threshold = np.argwhere(timeseries[:, 1] > threshold)
    distance_bet_extremes = 10
    groups_of_correlated_points = group_correlated_points(
        timepoints_with_value_above_threshold, distance_bet_extremes
    )
    # groups_of_correlated_points is a list of lists (each group is a list)
    # Each group of points correspond to an independant fluctuations, but
    # points within the group are correlated (oscillations above threshold).
    # Next the maximum value within each group is identified.
    extremes_timepoints = np.zeros(len(groups_of_correlated_points))
    extremes_values = np.zeros(len(groups_of_correlated_points))
    timepoints = timeseries[:, 0]
    for i, bundle in enumerate(groups_of_correlated_points):
        # argmax return the index relative to origin of timeseries[bundle,1]
        # so must add offset bundle[0]
        extremes_timepoints[i] = timepoints[
            np.argmax(timeseries[bundle, 1]) + bundle[0]
        ]
        extremes_values[i] = np.amax(timeseries[bundle, 1])

    # Make figure
    fig, ax = plt.subplots()
    ax.set_xlim(0, np.amax(timepoints))

    (line,) = ax.plot(timepoints, timeseries[:, 1])  # Signal (or "trajectory")

    # Mark extremes above threshold with a dot
    (line2,) = ax.plot(
        extremes_timepoints,
        extremes_values,
        "o",
        linestyle="None",
        markersize=4,
    )

    # Horizontal line at threshold value
    (line3,) = ax.plot(
        [timepoints[0], timepoints[-1]],
        [threshold, threshold],
        linestyle="--",
        linewidth=0.7,
    )
    line3.set_color(line2.get_color())
    line.set_linewidth(0.8)

    return fig, ax
