#!/bin/bash
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
sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 pgadmin3 postgresql-contrib python-psycopg2
sudo apt-get install binutils libproj-dev

# virtualenv install
export WORKON_HOME=~/venvs
mkdir $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv pygeo_analysis_cookbook
echo "export WORKON_HOME=$WORKON_HOME" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

workon pygeoan_cb

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
pip install folium
toggleglobalsitepackages
enable global site-packages

