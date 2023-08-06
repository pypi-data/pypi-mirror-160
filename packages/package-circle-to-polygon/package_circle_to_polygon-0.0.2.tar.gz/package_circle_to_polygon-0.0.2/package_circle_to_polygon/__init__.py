import math

DEFAULT_EARTH_RADIUS = 6378137

def to_radians(angle_in_degrees):
    return (angle_in_degrees * math.pi) / 180

def to_degrees(angle_in_radians):
    return (angle_in_radians * 180) / math.pi

def offset(c1, distance, earch_radius, bearing):
    lat1 = to_radians(c1[1])
    lon1 = to_radians(c1[0])
    d_by_r = distance / earch_radius;
    lat = math.asin(math.sin(lat1) * math.cos(d_by_r) + math.cos(lat1) * math.sin(d_by_r) * math.cos(bearing))
    lon = lon1 + math.atan2(math.sin(bearing) * math.sin(d_by_r) * math.cos(lat1), math.cos(d_by_r) - math.sin(lat1) * math.sin(lat))
    return [to_degrees(lon), to_degrees(lat)]

def circle_to_polygon(center, radius, options = { "edges": 32, "bearing": 0, "direction": 1 }):
    edges = options["edges"]
    earch_radius = DEFAULT_EARTH_RADIUS
    bearing = options["bearing"]
    direction = options["direction"]

    start = to_radians(bearing)
    coordinates = []
    for i in range(edges):
        coordinates.append(offset(center, radius, earch_radius, start + (direction * 2 * math.pi * -i) / edges))
    coordinates.append(coordinates[0])
    return { "type": "Polygon", "coordinates": [coordinates] }

