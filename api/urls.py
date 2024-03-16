from django.urls import path
from api import views

urlpatterns = [
    path("applicant/", views.ApplicantListApiView.as_view()),
    path("applicant/<int:id>/", views.ApplicantDetailApiView.as_view()),
    path("applicant/<int:id>/note/", views.ApplicantNoteListApiView.as_view()),
]
