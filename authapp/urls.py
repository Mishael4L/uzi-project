from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register_user, name = 'register'),
    path('activate/<uidb64>/<token>',views.activate_account, name='activate_user'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("logout/", views.logout_view, name='logout'),

    path('password-reset/', views.CustomPasswordResetView.as_view(), name = 'password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name = 'password_reset_complete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])