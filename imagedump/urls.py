from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (
    UploadImageView,
    ServeImageView,
    ShowImageView,
)

urlpatterns = [
    path('', login_required(UploadImageView.as_view()), name='upload'),
    path('raw/<uuid:uuid>.<str:ext>',
         ServeImageView.as_view(),
         name='raw_image'),
    path('img/<uuid:uuid>.<str:ext>',
         ShowImageView.as_view(),
         name='show_image'),
]
