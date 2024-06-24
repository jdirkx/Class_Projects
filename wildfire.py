"""Geographic clustering of historical wildfire data
CS 210, University of Oregon
Jacob Dirkx
Credits: Myself
"""
import doctest
import csv
import graphics.utm_plot
import random
import math

def make_map() -> graphics.utm_plot.Map:
    """Create and return a basemap display"""
    map = graphics.utm_plot.Map("wildfire-main/data/Oregon.png",
                                (1024, 783),
                                (342151, 4629315),
                                (1014041, 5171453))
    return map

def get_fires_utm(path: str) -> list[tuple[int, int]]:
    """Read CSV file specified by path, returning a list 
    of (easting, northing) coordinate pairs within the 
    study area. 
    """
    coordinates = []
    with open(path, newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        for row in reader:
            easting = int(row["Easting"])
            northing = int(row["Northing"])
            if in_bounds(easting, northing) == True:
                coordinates.append([easting,northing])
    return coordinates

def in_bounds(easting: float, northing: float) -> bool:
    """Is the UTM value within bounds of the map?"""
    if (easting < 342151
        or easting > 1014041
        or northing < 4629315
        or northing > 5171453):
        return False
    return True

def plot_points(fire_map: graphics.utm_plot.Map,
                points:  list[tuple[int, int]],
                size_px: int = 5,
                color: str = "green") -> list:
    """Plot all the points and return a list of handles that
    can be used for moving them.
    """
    symbols = []
    for point in points:
        easting, northing = point
        symbol = fire_map.plot_point(easting, northing, 
                                     size_px=size_px, color=color)
        symbols.append(symbol)
    return symbols

def assign_random(points: list[tuple[int, int]], n: int) -> list[list[tuple[int, int]]]:
    """Returns a list of n lists of coordinate pairs.
    The i'th list is the points assigned randomly to the i'th cluster.
    """
    # Initially the assignments is a list of n empty lists
    assignments = []
    for i in range(n):
        assignments.append([])
    # Then we randomly assign points to lists
    for point in points:
        choice = random.randrange(n)
        assignments[choice].append(point)
    return assignments

def centroid(points: list[tuple[int, int]]) -> tuple[int, int]:
    """The centroid of a set of points is the mean of x and mean of y"""
    totalpts = len(points)
    if not points:
        centroid = (0,0)
    else:
        easting, northing =zip(*points)
        eastings = math.fsum(easting)
        northings = math.fsum(northing)
        centroid = (eastings//totalpts, northings//totalpts)
    return centroid

def cluster_centroids(clusters: list[list[tuple[int,int]]]) -> list[tuple[int,int]]:
    """Return a list containing the centroid corresponding to each assignment of
    points to a cluster.
    """
    centroids = []
    for cluster in clusters:
        centroids.append(centroid(cluster))
    return centroids

def sq_dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Square of Euclidean distance between p1 and p2
    """
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1
    return dx*dx + dy*dy

def closest_index(point: tuple[int, int], centroids: list[tuple[int, int]]) -> int:
    """Returns the index of the centroid closest to point
    """
    distances =[]
    for i in centroids:
        dist = sq_dist(point, i)
        distances.append(dist)
    closest = min(distances)
    index = distances.index(closest)
    return index

def assign_closest(points: list[tuple[int,int]],
                   centroids: list[tuple[int, int]]
                   ) -> list[list[int, int]]:
    """Returns a list of lists.  The i'th list contains the points
    assigned to the i'th centroid.  Each point is assigned to the
    centroid it is closest to.
    """
    assignments = []
    for i in range(len(centroids)):
        assignments.append([])
    for point in points:
        choice = closest_index(point, centroids)
        assignments[choice].append(point)
    return assignments

def move_points(fire_map: graphics.utm_plot.Map,
                points:  list[tuple[int, int]], 
                symbols: list): 
    """Move a set of symbols to new points"""
    for i in range(len(points)):
        fire_map.move_point(symbols[i], points[i])

def show_clusters(fire_map: graphics.utm_plot.Map, 
                  centroid_symbols: list, 
                  assignments: list[list[tuple[int, int]]]):
    """Connect each centroid to all the points in its cluster"""
    for i in range(len(centroid_symbols)):
        fire_map.connect_all(centroid_symbols[i], assignments[i])

def main():
    doctest.testmod()
    fire_map = make_map()
    points = get_fires_utm("wildfire-main/data/fire_locations_utm.csv")
    plot_points(fire_map, points, color="red")

    # Initial random assignment
    partition = assign_random(points, 10)
    centroids = cluster_centroids(partition)
    centroid_symbols = plot_points(fire_map, centroids, size_px=10, color="blue")    
    
    # Continue improving assignment until assignment doesn't change
    for i in range(30):
        old_partition = partition
        partition = assign_closest(points, centroids)
        if partition == old_partition:
            # No change ... this is "convergence"
            break
        centroids = cluster_centroids(partition)
        move_points(fire_map, centroids, centroid_symbols)
    
    #Show connections at end
    show_clusters(fire_map, centroid_symbols, partition)
    input("Press enter to quit")

if __name__ == "__main__":
    main()
