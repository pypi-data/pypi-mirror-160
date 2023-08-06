from .views import *
from django.urls import path

urlpatterns = [
    path('',  my_page, name='home'),
    path('offline/',  offline, name='offline'),
    path('say-something/<str:key>',  say_something, name='say_something'),
    path('random-response',  random_response, name='random_response'),
    path('fill-dynamic-cache/<int:id>',  fill_dynamic_cache, name='fill_dynamic_cache'),
    path('must-not-cache',  must_not_cache, name='must_not_cache'),

    # The service worker cannot be in /static because its scope will be limited to /static.
    # Since we want it to have a scope of the full application, we rely on this TemplateView
    # trick to make it work.
    path(
        'sw.js',
        ServiceWorkerView.as_view(),
        name= ServiceWorkerView.name,
    ),
]
