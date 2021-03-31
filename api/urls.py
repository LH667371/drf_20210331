from django.urls import path

from api import views

urlpatterns = [
    path('book1/<str:id>/', views.BookAPIView.as_view()),
    path('book1/', views.BookAPIView.as_view()),
    path('book2/<str:id>/', views.BookAPIViewV2.as_view()),
    path('book2/', views.BookAPIViewV2.as_view()),
]