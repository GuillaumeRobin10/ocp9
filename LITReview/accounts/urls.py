from django.urls import path


from . import views


urlpatterns = [
    path('', views.home),
    path("home", views.home, name="login_page"),
    path("register", views.register, name="register"),
    path("feed", views.feed, name="feed"),
    path("ticket/<int:pk_ticket>/", views.editaticket, name="ticket"),
    path("ticket/", views.makeaticket, name="newticket"),
    path("review/<int:pk_review>/", views.editareview, name="review"),
    path("review/", views.makeareview, name="newreview"),
    path("post/", views.posts, name="posts"),
    path("deletereview/<int:pk_review>/", views.deletereview, name="deletereview"),
    path("reviewed/<int:pk_ticket>/", views.reviewed, name="reviewed"),
    path("uniquereviewedit/<int:pk_review>/", views.uniquereviewedit, name="uniquereviewedit"),
    path("deleteticket/<int:pk_ticket>/", views.deleteticket, name="deleteticket"),
    path("deconnection/", views.deconnection, name="logout"),
    path("following/", views.abonnements, name="following"),
    path("desabonnement/<int:pk_user>/", views.desabonnement, name="desabonnement"),

]


