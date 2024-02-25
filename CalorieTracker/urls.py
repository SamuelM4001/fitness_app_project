from django.urls import path
from . import views

urlpatterns = [
    path('calorietracker/', views.calorietracker,name='calorietracker'),
    path('calorietracker2/', views.calorietracker2,name='calorietracker2'),
    path('modifyvalues/', views.modifyvalues,name='modifyvalues'),
    path('dailystats/', views.dailystats,name='dailystats')
]   