#!/usr/bin/env python
# -*- coding: utf-8 -*-

def format_walk_time(walk_time):
    """
    takes argument: float walkTime in seconds
    returns argument: string time  "xx minutes xx seconds"
    """
    if walk_time > 0.0:
        return str(int(walk_time / 60.0)) + " minutes " + str(int(round(walk_time % 60))) + " seconds"
    else:
        return "Walk time is less than zero! something is wrong"


def calc_distance_walktime(rows):
    """
    calculates distance and walk_time.
    rows must be an array of linestrings --> a route, retrieved from the DB.
    rows[5]: type of line (stairs, elevator, etc)
    rows[3]: cost as length of segment
    returns a dict with key/value pairs route_length, walk_time
    """

    route_length = 0
    walk_time = 0

    for row in rows:

        route_length += row[3]
        # calculate walk time
        if row[5] == 3 or row[5] == 4:  # stairs
            walk_speed = 1.2  # meters per second m/s
        elif row[5] == 5 or row[5] == 6:  # elevator
            walk_speed = 1.1  # m/s
        else:
            walk_speed = 1.39  # m/s

        walk_time += (row[3] / walk_speed)

    length_format = "%.2f" % route_length
    real_time = format_walk_time(walk_time)
    print {"route_length": length_format, "walk_time": real_time}
