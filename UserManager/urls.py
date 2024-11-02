from django.contrib import admin
from django.urls import path, include
from Posts import urls as PostsUrls
from django.contrib.auth import urls as authurls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(authurls)),
    path("posts/",include(PostsUrls)),
]
