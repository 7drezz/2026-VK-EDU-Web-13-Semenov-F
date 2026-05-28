from django.urls import path
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    
    path('api/question/<int:question_id>/like/', views.question_like, name='question_like'),
    path('api/answer/<int:answer_id>/like/', views.answer_like, name='answer_like'),
    path('api/answer/<int:answer_id>/correct/', views.answer_correct, name='answer_correct'),
    path('api/answer/<int:answer_id>/unmark/', views.answer_unmark, name='answer_unmark'),
    path('api/search/', views.search_suggestions, name='search_suggestions'),
    path('centrifugo/token/', views.centrifugo_token, name='centrifugo_token'),
]