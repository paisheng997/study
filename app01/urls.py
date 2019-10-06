from django.urls import path
from app01.views import *

urlpatterns = [
    path('index/',index),
    path('addPerson/',addperson),
    path('queryPerson/',queryperson),
    path('updatePerson/',updateperson),
    path('removePerson/',removeperson),

    path('addmore/',addmore),
    path('querymore/',querymore),
    path('updatemore/',updatemore),
    path('removemore/',removemore),

    path('addmany/',addmany),
    path('querymany/',querymany),
    path('updatemany/',updatemany),
    path('removemany/',removemany),

    path('juhe/',juhe),
    path('Ffunc/',Ffunc),
    path('Qfunc/',Qfunc),
]