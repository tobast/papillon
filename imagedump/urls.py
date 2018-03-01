from django.urls import path

from .views import (
    UploadImageView,
    ServeImageView,
)

urlpatterns = [
    path('', UploadImageView.as_view(), name='upload'),
    path('img/<uuid:uuid>.<str:ext>',
         ServeImageView.as_view(),
         name='serve_image'),
]
