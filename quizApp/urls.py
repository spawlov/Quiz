from django.urls import path

from .views import IndexView, TestView, user_answer, UserResult

app_name = 'quizApp'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('quest/<int:pk>/', TestView.as_view(), name='quest'),
    path('answer/', user_answer, name='answer'),
    path('result/<int:group>/', UserResult.as_view(), name='result')
]
