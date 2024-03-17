from django.urls import path
from . import views

urlpatterns = [
    # for image test
    path('car-plate/image/', views.plate_recog),
    
    # recog carplate number at entrance
    path('entrance/', views.entrance),

    # recog carplate number at hallway and open parking section
    path('hall/', views.hall),
    
    # recog carplate number at exit and open exit
    path('exit-way/', views.exit_way),
    
    # auto report system
    # check lately exit car's parking section is empty
    # path('auto-report/', views.auto_report),

    # managing system via manager
    path('open-area/<str:area>/', views.bar),

    # check-Isneed to open
    path('bar-open/', views.bar_open),

    # open entrance
    path('ent-open/', views.entrance_barricate),
]
