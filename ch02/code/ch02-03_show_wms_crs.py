#!/usr/bin/env python
# -*- coding: utf-8 -*-

from owslib.wms import WebMapService

url = "http://ogc.bgs.ac.uk/cgi-bin/BGS_1GE_Geology/wms"

get_wms_url = WebMapService(url)

crs_list = get_wms_url.contents['GBR_Kilmarnock_BGS_50K_CompressibleGround'].crsOptions

print crs_list