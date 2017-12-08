from django.conf.urls import url, include
from rest_framework import routers
from uf_app import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^uf/list/$', views.UFList.as_view()),
    url(r'^uf/price/$', views.UFtoCLP.as_view()),
    url(r'^uf/$', views.UFCreateMany.as_view())
]
