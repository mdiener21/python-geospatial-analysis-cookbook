#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import xml.etree.ElementTree as el_tree

# British Geological Survey WMS  BGS OneGeology Europe geology
url = "http://ogc.bgs.ac.uk/cgi-bin/BGS_1GE_Geology/wms?service=WMS&version=1.3.0&request=GetCapabilities"

open_xml_obj = urllib.urlopen(url)
tree = el_tree.parse(open_xml_obj)

root = tree.getroot()

namespace_ogis = "{http://www.opengis.net/wms}"
tag_to_find = "CRS"

wms_crs_tag = namespace_ogis + tag_to_find

capability_element = root[1]

for wms in capability_element:
    for crs in wms:
        if crs.tag == wms_crs_tag:
            print crs.text