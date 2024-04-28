from django.urls import path
from . import views

urlpatterns = [
    path('register_doctor/', views.register_doctor, name="register_doctor"),    
    path('open_calendar/', views.open_calendar, name="open_calendar"),    
    path('queries_doctor/', views.queries_doctor, name="queries_doctor"), 
    path('consultation_area_doctor/<int:id_query>', views.consultation_area_doctor, name="consultation_area_doctor"),
    path('end_query/<int:id_query>', views.end_query, name='end_query'), 
    path('add_document/<int:id_query>/', views.add_document, name="add_document"),
    path('dashboard/', views.dashboard, name="dashboard"),
]