from django.urls import path

from . import views

app_name = 'reviewapp'
urlpatterns = [

    # ex: /reviewapp/
    path('', views.categories, name='categories'),

    # ex: /reviewapp/2
    path('<int:category_id>/', views.restaurants, name='restaurants'),

    # ex: /reviewapp/search/
    path('search/', views.search, name='search'),

    # ex: /reviewapp/resto/5
    path('resto/<int:restaurant_id>/', views.details, name='details'),

    # ex: /reviewapp/resto/5/add
    path('resto/<int:restaurant_id>/add', views.add, name='add'),

    # ex: /reviewapp/comment/6
    path('comment/<int:review_id>/', views.comment, name='comment'),

    # ex: /reviewapp/reply/6
    path('reply/<int:comment_id>/', views.reply, name='reply'),

    # ex: /reviewapp/resto/5/reviewed
    path('resto/<int:restaurant_id>/reviewed', views.reviewed, name='reviewed'),

    # ex: /reviewapp/test
    path('test', views.test, name='test'),

    

]
