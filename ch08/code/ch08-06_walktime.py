#!/usr/bin/env python
# -*- coding: utf-8 -*-

def calc_distance_walktime(rows, cursor):
    """
    calculates distance and walk_time.
    rows must be an array of linestrings --> a route, retrieved from the DB.
    rows[x][5]: type of line (stairs, elevator, etc)
    rows[x][6]: geometry:linestring
    cursor: connection to the db
    returns a dict with key/value pairs route_length, walk_time
    """

    route_length = 0
    walk_time = 0

    for row in rows:
        cursor.execute("select st_length(%(geom)s) as length", {"geom": row[6]})
        result = cursor.fetchall()
        route_length += result[0][0]
        #calculate walk time
        if row[5] == 3 or row[5] == 4:  # stairs
            walk_speed = 0.7 # meters per second m/s
        elif row[5] == 5 or row[5] == 6:  # elevator
            walk_speed = 0.4  # m/s
        else:
            walk_speed = 1.25 # m/s

        walk_time += (result[0][0] / walk_speed)

    return {"route_length": route_length, "walk_time": walk_time}


def format_walk_time(walk_time):
    """
    takes argument: float walkTime in seconds
    returns argument: string time  "xx minutes xx seconds"
    """
    if walk_time > 0.0:
        return str(int(walk_time / 60.0)) + " minutes " + str(int(round(walk_time % 60))) + " seconds"
    else:
        return "Walk time is less than zero! something is wrong"