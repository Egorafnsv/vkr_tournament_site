from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_tournaments, name="redirect-to-list"),
    path("choose-window/", views.type_tournament_create, name="choose-window"),
    path("create-tournament/<str:type_tournament>/", views.create_new_tournament, name="create-tournament"),
    path("view/", views.list_tournaments, name="list-tournaments"),
    path("tournament/<str:uid>/", views.view_tournament, name="view-tournament"),
    path("club/<str:uid>/<int:id>/", views.view_club, name="view-club"),
    path("view-match/<str:uid>/<int:match_id>/", views.view_match, name="view-match-id"),
    path("add-score/<str:tournament_uid>/<int:match_id>/", views.add_score, name="add-score"),
    path("admins/<str:uid>/", views.tournament_admins, name="trn-admins")
]
