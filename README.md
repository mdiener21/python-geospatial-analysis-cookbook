python-geospatial-analysis-cookbook
==================================

Welcome to the code repository for "Python Geospatial Analysis Cookbook" over 60 python recipes to perform spatial operations and of course build an indoor routing Django web application.   

**Please post any comments and questions directly as an issue/ticket here in the GitHub** Repo.

If you are interested in more about indoor routing see Chapter 10 and 11.  Also please visit the Github repo INDRZ https://www.github.com/indrz  to see the official indoor routing and mapping code.  The project homepage is [indrz](http://www.indrz.com)

Code for the book [*Python Geospatial Analysis Cookbook*](https://github.com/mdiener21/python-geospatial-analysis-cookbook/archive/master.zip).

Description
-----------

A book for developoers, gis programmers, analysts, researchers, gis geeks, IT administrators who ever that want to dabble with python and geospatial analysis.

The reciepes are short and long, full of descriptions and code comments.  The book takes you on a journey from installation of spatial libraries to executing fun analysis in a cookbook like tutorial.

Technologies
pyshp, gdal, ogr, proj4, django, jinja2, Shapely, folium, matplotlib, networkx, numpy, pandas, psycopg2, pyproj, bootstrap, jquery, typeahead.js, bloodhound.js, openlayers, leaflet


With pip you can install:

```bash
pip install [location-path]/master.zip
```

Or directly from GitHub like this:

```bash
pip install https://github.com/mdiener21/python-geospatial-analysis-cookbook/archive/master.zip
```


# Updates

Page number: 46 
Currently step 7 includes

```bash
sudo su createdb –O pluto –U postgres py_geoan_cb
```
Correction is:
```bash
sudo -u postgres createdb -U postgrs -P pluto py_geoan_cb"
```
