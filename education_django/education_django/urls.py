"""
Роутинг
"""

from django.conf import  settings
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from graphene_django.views import GraphQLView
from .schema import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('education_app.urls', namespace='education_app')),
    path('users/', include('users.urls', namespace='users')),
    path('django-rq/', include('django_rq.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )
