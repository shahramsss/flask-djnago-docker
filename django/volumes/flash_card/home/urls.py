"""
URL configuration for flash_card project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import *


app_name = "home"
urlpatterns = [
    path("home/" ,HomeView.as_view(),name="home"),
    path("homeapi/", Home.as_view(), name="homeapi"),
    path("wordapi/<int:pk>/", Word.as_view(), name="word"),
    path("cards/" ,CardsView.as_view(),name="cards"),
    path("cardsdetails/<int:id>/" ,CardDetialsView.as_view(),name="cardsdetails"),
    path("cardswrong/" ,CardsWrongView.as_view(),name="cardswrong"),
    path("cardcreate/" ,CardCreatView.as_view(),name="cardcreate"),
    path("cardedit/<int:id>/" ,CardEditView.as_view(),name="cardedit"),
    path("cardsearch/" ,CardsSearchView.as_view(),name="cardsearch"),
    path("cardnewest/" ,CardsNewestView.as_view(),name="cardnewest"),

]
