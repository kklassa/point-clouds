import numpy as np
from scipy.spatial import distance


def calculate_distances(vertices: list) -> list:
    # reshape the array into a 2D array where each row represents a point
    points = np.array(vertices).reshape(-1, 3)

    # calculate the pairwise Euclidean distance between all points
    distance_matrix = distance.cdist(points, points, 'euclidean')

    # sort each row and take the second smallest element (i.e. the smallest non-zero distance)
    distances = np.sort(distance_matrix, axis=1)[:, 1]

    return distances

def scale_distances(distances, new_min, new_max):
    # calculate the old min and max
    original_min = distances.min()
    original_max = distances.max()

    # scale the distances array
    scales = (new_max - new_min) * (distances - original_min) / (original_max - original_min) + new_min

    return scales

def scale_distances_log(distances, new_min, new_max):

    # calculate the old min and max
    original_min = distances.min()
    original_max = distances.max()

    # make sure there are no zero or negative values for the log scaling
    distances = np.log(distances - original_min + 0.0001)

    # calculate the new min and max after log transformation
    log_min = np.log(new_min)
    log_max = np.log(new_max)

    # scale the log-transformed distances
    scales = (log_max - log_min) * (distances - np.min(distances)) / (np.max(distances) - np.min(distances)) + log_min

    # convert back from log scale
    scales = np.exp(scales)

    return scales