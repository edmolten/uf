from django.conf.urls import url, include
from rest_framework import routers
from uf_app import views
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^uf/list$', views.UFList.as_view()),
    url(r'^uf/', views.UFList.as_view()),
    url(r'^uf/price$', views.UFtoCLP.as_view()),
]
