from django.urls import path
from robodino import views

urlpatterns = [
    path('board-create/',views.BoardCreateApiView.as_view()),
    path('board-status/',views.BoardStatusApiView.as_view()),
    path('board-generate-debug/',views.BoardGenerateApiView.as_view()),
    path('dino-create/',views.DinoCreateApiView.as_view()),
    path('robot-create/',views.RobotCreateApiView.as_view()),
    path('robot-move/',views.RobotMoveApiView.as_view()),
    path('robot-attack/',views.RobotAttackApiView.as_view()),
]
