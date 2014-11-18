#!/bin/sh
# setup installs
sudo apt-get install python-setuptools python-pip

#pip installs
sudo pip install virtualenv
sudo easy_install virtualenvwrapper
sudo apt-get install -y python-dev
sudo apt-get install freetype* libpng-dev libjpeg8-dev
sudo apt-get install libblas-dev liblapack-dev gfortran

#gdal install
sudo apt-get install -y build-essential libxml2-dev libxslt1-dev libpq-dev
sudo apt-get install libgdal-dev  # install is 125MB
sudo apt-get install python-gdal

#install postgresql postgis
sudo apt-get install postgresql-9.3 postgresql-9.3-postgis pgadmin3 postgresql-contrib python-psycopg2
sudo apt-get install binutils libproj-dev

# virtualenv install
export WORKON_HOME=~/venvs
mkdir $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pygeo_analysis_cookbook
echo export WORKON_HOME=$WORKON_HOME >> ~/.bashrc
echo source /usr/local/bin/virtualenvwrapper.sh >> ~/.bashrc
source ~/.bashrc

workon pygeo_analysis_cookbook

pip install numpy
pip install pyproj
pip install shapely
pip install matplotlib
pip install descartes
pip install pyshp
pip install geojson
pip install pandas
pip install scipy
pip install pysal
pip install ipython
pip install django
pip install owslib




################################################
#
#
# NOT TO INCLUDE ANY OF this stuff in final !!!!
# BELOW ARE SOME SILLY STUFF not needed
#
################################################
$ sudo apt-add-repository ppa:ubuntugis/ubuntugis-unstable
$ sudo apt-get update
$ sudo apt-get install libgdal-dev
$ virtualenv gdalenv
$ source gdal/bin/activate
(gdalenv) $ pip install --no-install GDAL
(gdalenv) $ cd /path/to/gdalenv/build/GDAL
(gdalenv) $ python setup.py build_ext include-dirs=/usr/include/gdal/
(gdalenv) $ pip install --no-download GDAL
done

cd /.venv/pygeo_analysis_cookbook/build/gdal
python setup.py build_ext gdal-config=/usr/bin/gdal-config --include-dirs=/usr/include/gdal --library-dirs=/usr/lib

/usr/share/gdal/1.7
/usr/include/gdal
/usr/bin/gdal-config
/usr/local/lib/libgdal.so
/usr/lib/ogdi/libgdal.so
/home/mdiener/Downloads/gdal-1.11.0/.libs/libgdal.so


export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
pip install GDAL

$ wget http://download.osgeo.org/gdal/1.11.0/gdal-1.11.0.tar.gz
$ tar xzf gdal-1.11.0.tar.gz
$ cd gdal-1.11.0
$ ./configure -with-python
$ make  #this takes time
$ sudo make installs




