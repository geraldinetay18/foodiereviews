from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response


def categories(request):
    categories = Category.objects.all()
    return render(request, 'reviewapp/categories.html', context={'categories': categories})


def search(request):
    search_detail = request.GET.get('q')
    restaurants = Restaurant.objects.filter(restaurant_text__icontains=search_detail)
    context = {
        'restaurants': restaurants,
        'search_detail': search_detail
    }
    return render(request, 'reviewapp/restaurants.html', context)


def restaurants(request, category_id):
    category = Category.objects.get(id=category_id)
    restaurants = category.get_restaurants()
    context = {
        'category': category, 
        'restaurants': restaurants
    }
    return render(request, 'reviewapp/restaurants.html', context)


def details(request, restaurant_id):
    restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
    user_liked_reviews = []
    if not request.user.is_anonymous:
        user_liked_reviews = get_liked_reviews_by_user_and_restaurant(request.user, restaurant)
    return render(request, 'reviewapp/details.html', {'restaurant': restaurant, 'user': request.user, 'user_liked_reviews': user_liked_reviews })


def get_liked_reviews_by_user_and_restaurant(user, restaurant):
    liked_reviews = []
    for review in restaurant.review_set.all():
        like = review.like_set.filter(user=user).first()
        if like:
            liked_reviews.append(review.id)
    return liked_reviews


@login_required
def add(request, restaurant_id):
    form = ReviewForm()
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    context = {
        'restaurant': restaurant, 
        'form': form
    }
    return render(request, 'reviewapp/add.html', context)
    

@login_required
def comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review:
        review.comment_set.create(comment_user=request.user, comment_description=request.POST.get('comment_description'))
    else:
        print("Invalid fields for comment. Required: review id, username and comment description.")

    return render(request, 'reviewapp/details.html', {'restaurant': review.restaurant, 'user': request.user})


@login_required
def reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment:
        comment.reply_set.create(reply_user=request.user, reply_description=request.POST.get('reply_description'))
    else:
        print("Invalid fields for reply. Required: comment id, username and reply description.")

    return render(request, 'reviewapp/details.html', {'restaurant': comment.review.restaurant, 'user': request.user})


@login_required
def like(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review:
        # check if user has liked before
        like = review.like_set.filter(user=request.user).first()
        if like:
            print("User has already liked the review. A new like will not be created again.")
        else:
            review.like_set.create(user=request.user)
    else:
        print("Invalid fields for like. Required: review id and username.")
    user_liked_reviews = get_liked_reviews_by_user_and_restaurant(request.user, review.restaurant)
    return render(request, 'reviewapp/details.html', {'restaurant': review.restaurant, 'user': request.user, 'user_liked_reviews': user_liked_reviews })


@login_required
def reviewed(request, restaurant_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        rtg = request.POST.get("rate", 1)
        p = request.POST.get("price", 1)
        res = get_object_or_404(Restaurant, pk=restaurant_id)
        res.review_set.create(review_user=request.user, **form.cleaned_data, review_rate=rtg, review_price=p)
    else:
        print(form.errors)

    return render(request, 'reviewapp/details.html', {'restaurant': res, 'user': request.user})


def comment_add(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review:
        review.comment_set.create(comment_user=request.user, comment_description=request.POST.get('comment_description'))
    else:
        print("Invalid fields for comment. Required: review id, username and comment description.")

    return render(request, 'reviewapp/details.html', {'restaurant': review.restaurant, 'user': request.user})


class CommentAdd(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        success = False
        review_id = request.POST.get('review_id', None)
        comment_user_id = request.POST.get('comment_user_id', None)
        comment_description = request.POST.get('comment_description', None)
        
        if review_id and comment_user_id and comment_description:
            review = get_object_or_404(Review, pk=review_id)
            comment_user = get_object_or_404(User, pk=comment_user_id)
            try:
                new_review = review.comment_set.create(comment_user=comment_user, comment_description=comment_description)
                success = True
            except Exception as e:
                print(e, "Invalid fields for comment. Required: review id, username and comment description.")
            data = {
                'success': success,
                'new_review_pk': new_review.pk
            }
        return Response(data)