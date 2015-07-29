from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

# all urls begin with http://localhost:8000/maps/
urlpatterns = patterns('maps.views',
    #  ex valid call from to  /api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2
    # url(r'^\w+/$', 'route_map', name='routemap'),
    url(r'^routemap/$', 'route_map', name='routemap'),

)

urlpatterns = format_suffix_patterns(urlpatterns)
