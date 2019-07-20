from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


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
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'reviewapp/details.html', {'restaurant': restaurant, 'user': request.user})


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
        review.review_likes = review.review_likes + 1
        review.save()
    else:
        print("Invalid fields for comment. Required: review id, username and comment description.")
    return render(request, 'reviewapp/details.html', {'restaurant': review.restaurant, 'user': request.user})


@login_required
def reviewed(request, restaurant_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        rtg = request.POST.get("rate", 1)
        p = request.POST.get("price", 1)
        res = get_object_or_404(Restaurant, pk=restaurant_id)
        res.review_set.create(review_user=request.user, **form.cleaned_data, review_rate=rtg, review_price=p, review_likes=0)
    else:
        print(form.errors)

    return render(request, 'reviewapp/details.html', {'restaurant': res, 'user': request.user})
