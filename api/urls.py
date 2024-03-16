from django.urls import path
from api import views

urlpatterns = [
    path("applicant/", views.ApplicantListApiView.as_view()),
    path("applicant/<uuid:uuid>", views.ApplicantDetailApiView.as_view()),
    path("applicant/<uuid:uuid>/note", views.ApplicantNoteListApiView.as_view()),
]
