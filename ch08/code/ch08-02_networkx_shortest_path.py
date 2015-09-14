#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import json
from shapely.geometry import asLineString, asMultiPoint


def get_path(n0, n1):
    """If n0 and n1 are connected nodes in the graph,
    this function will return an array of point
    coordinates along the line linking
    these two nodes."""

    return np.array(json.loads(nx_list_subgraph[n0][n1]['Json'])['coordinates'])


def get_full_path(path):
    """
    Create numpy array line result
    :param path: results of nx.shortest_path function
    :return: coordinate pairs along a path
    """
    p_list = []
    curp = None
    for i in range(len(path)-1):
        p = get_path(path[i], path[i+1])
        if curp is None:
            curp = p
        if np.sum((p[0]-curp)**2) > np.sum((p[-1]-curp)**2):
            p = p[::-1, :]
        p_list.append(p)
        curp = p[-1]
    return np.vstack(p_list)


def write_geojson(outfilename, indata):
    """
    create GeoJSON file
    :param outfilename: name of output file
    :param indata:
    :return: a new GeoJSON file
    """

    with open(outfilename, "w") as file_out:
        file_out.write(json.dumps(indata))


if __name__ == '__main__':

    # use Networkx to load a Noded shapefile
    # returns a graph where each node is a coordinate pair
    # and the edge is the line connecting the two nodes

    nx_load_shp = nx.read_shp("../geodata/shp/e01_network_lines_3857.shp")

    # A graph is not always connected, so we take the largest connected subgraph
    # by using the connected_component_subgraphs function.
    nx_list_subgraph = list(nx.connected_component_subgraphs(nx_load_shp.to_undirected()))[0]

    # get all the nodes in the network
    nx_nodes = np.array(nx_list_subgraph.nodes())

    # output the nodes to a GeoJSON file to view in QGIS
    network_nodes = asMultiPoint(nx_nodes)
    write_geojson("../geodata/ch08_final_netx_nodes.geojson",
                  network_nodes.__geo_interface__)

    # this number represents the nodes position
    # in the array to identify the node
    start_node_pos = 30
    end_node_pos = 21

    # Compute the shortest path. Dijkstra's algorithm.
    nx_short_path = nx.shortest_path(nx_list_subgraph,
                                     source=tuple(nx_nodes[start_node_pos]),
                                     target=tuple(nx_nodes[end_node_pos]),
                                     weight='distance')

    # create numpy array of coordinates representing result path
    nx_array_path = get_full_path(nx_short_path)

    # convert numpy array to Shapely Linestring
    out_shortest_path = asLineString(nx_array_path)

    write_geojson("../geodata/ch08_final_netx_sh_path.geojson",
                  out_shortest_path.__geo_interface__)
