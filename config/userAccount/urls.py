from django.urls import path
from . import views



urlpatterns = [
    path('signup', views.AddUserAccount.as_view(), name='AddUserAccount'),
    path('login', views.Login.as_view(), name='Login'),
    path('logout', views.Logout.as_view(), name='Logout'),
    path('edit-profile', views.EditUserAccount.as_view(), name='EditUserAccount'),
    path('update-email', views.EditEmail.as_view(), name='EditEmail'),
    path('delete', views.DeleteUserAccount.as_view(), name='DeleteUserAccount'),
    path('profile', views.UserAccountProfile.as_view(), name='UserAccountProfile'),
    path('activate/<uidb64>/<token>',
        views.ActivateUserAccount.as_view(), name='Activate'),
    path('activate-new-email/<uidb64>/<token>',
        views.ActivateNewEmail.as_view(), name='ActivateNewEmail'), 
    # next 6 paths are for changing and reseting password.
    path(
        "password_change/", views.PasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change/done/",
        views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path(
        "password_reset/done/",
        views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ), 
]
