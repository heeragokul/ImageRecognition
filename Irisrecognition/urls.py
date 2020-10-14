from django.urls import path

from Irisrecognition.views import TestView, ImageParser

urlpatterns = [

    # path('', HomeView.as_view(), name='homeview'),
    path('test', TestView.as_view(), name='test'),
    path('img', ImageParser.as_view(), name='image'),
]