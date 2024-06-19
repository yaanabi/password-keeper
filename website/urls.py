from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('add/', views.AddCredentialView.as_view(), name='add'),
    path("vault/", views.VaultView.as_view(), name="vault"),
    path("vault/delete/<int:pk>", views.DeleteCredentialView.as_view(), name="delete_credential"),
    path("vault/edit/<int:pk>", views.edit_credential, name="edit_credential"),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name="profile"),
    path('profile/edit/<int:pk>', views.UserProfileEditView.as_view(), name="edit_profile")
]
