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
mkvirtualenv pygeoan_cb
echo "export WORKON_HOME=$WORKON_HOME" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc

workon pygeoan_cb

# use the requirements.txt file for quick install found in the root project directory
# pip install -r ../../requirements.txt

pip install numpy
pip install pyproj
pip install shapely==1.5.2
pip install matplotlib
pip install descartes
pip install pyshp
pip install geojson==1.3.1
pip install pandas==0.16.12
pip install scipy
pip install pysal
pip install ipython
pip install django==1.8.3
pip install jinja2==2.7.3
pip install owslib==0.9.0
pip install tilestache==1.50.1
pip install folium==0.1.4
pip install gdal==1.11.0
pip install ipython==2.3.0
pip install kartograph.py==0.6.8
pip install networkx==1.9.1

toggleglobalsitepackages
enable global site-packages

