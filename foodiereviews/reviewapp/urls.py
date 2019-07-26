from django.urls import path

from . import views

app_name = 'reviewapp'
urlpatterns = [

    # ex: /reviewapp/
    path('', views.home, name='home'),

    # ex: /reviewapp/resto/5
    path('resto/<int:restaurant_id>/', views.details, name='details'),

    # ex: /reviewapp/resto/5/add
    path('resto/<int:restaurant_id>/add/', views.add, name='add'),

    # ex: /reviewapp/resto/5/reviewed
    path('resto/<int:restaurant_id>/reviewed/', views.reviewed, name='reviewed'),

    # ex: /reviewapp/api/comment/add/
    path('api/comment/add/', views.CommentAdd.as_view(), name="comment"),
    
    # ex: /reviewapp/api/reply/add/
    path('api/reply/add/', views.ReplyAdd.as_view(), name="reply"),

    # ex: /reviewapp/api/comment/add/
    path('api/like/add/', views.LikeAdd.as_view(), name="like"),

    # ex: /reviewapp/api/restaurants/list/
    path('api/restaurants/list/', views.GetRestaurantsByCategory.as_view(), name="restaurants_by_category"),
    
]