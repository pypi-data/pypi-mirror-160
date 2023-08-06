===================================================================================================================
                               DJANGO PROGRESSIVE WEB APPLICATIONS
===================================================================================================================

  Django pwa can convert your project into a progressive web application within seconds. Just install the package 
  add into INSTALLED_APPS and add urlpatterns and you are done.                                                    

Quickstart
===========

1.Add pwa to your INSTALLED_APPS settings like this:

INSTALLED_APPS = [

    ......,
    'pwa',   

  ]



2. Include the polls URLconf in your project urls.py like this

urlpatterns = [

    path('',include('pwa.urls')),

  ]


3. Place the static folder in your main project directory

