from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response


def home(request):
    categories = Category.objects.all()
    return render(request, 'reviewapp/home.html', context={'categories': categories})


def details(request, restaurant_id):
    restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
    user_liked_reviews = []
    if request.user.is_authenticated:
        user_liked_reviews = get_liked_reviews_by_user_and_restaurant(request.user, restaurant)
    context = {
        'restaurant': restaurant, 
        'user': request.user, 
        'user_liked_reviews': user_liked_reviews
    }   
    return render(request, 'reviewapp/details.html', context)


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
def reply(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if comment:
        comment.reply_set.create(reply_user=request.user, reply_description=request.POST.get('reply_description'))
    else:
        print("Invalid fields for reply. Required: comment id, username and reply description.")

    return render(request, 'reviewapp/details.html', {'restaurant': comment.review.restaurant, 'user': request.user})


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
        new_comment_pk = None

        try:
            review_id = request.POST.get('review_id', None)
            comment_user_id = request.POST.get('comment_user_id', None)
            comment_description = request.POST.get('comment_description', None)

            if review_id and comment_user_id and comment_description:
                review = get_object_or_404(Review, pk=review_id)
                comment_user = get_object_or_404(User, pk=comment_user_id)
                new_comment = review.comment_set.create(comment_user=comment_user, comment_description=comment_description)
                success = True
                new_comment_pk = new_comment.pk
        except Exception as e:
            print(e, "Invalid fields for comment. Required: review id, username and comment description.")

        data = {
            'success': success,
            'new_comment_pk': new_comment_pk
        }
        return Response(data)


class ReplyAdd(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        success = False
        new_reply_pk = None

        try:
            comment_id = request.POST.get('comment_id', None)
            reply_user_id = request.POST.get('reply_user_id', None)
            reply_description = request.POST.get('reply_description', None)

            if comment_id and reply_user_id and reply_description:
                comment = get_object_or_404(Comment, pk=comment_id)
                reply_user = get_object_or_404(User, pk=reply_user_id)
                new_reply = comment.reply_set.create(reply_user=reply_user, reply_description=reply_description)
                success = True
                new_reply_pk = new_reply.pk
        except Exception as e:
            print(e, "Invalid fields for reply. Required: comment id, username and reply description.")

        data = {
            'success': success,
            'new_reply_pk': new_reply_pk
        }
        return Response(data)


class LikeAdd(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):

        success = False
        total_likes = None

        try:
            review_id = int(request.POST.get('review_id', None))
            user_id = int(request.POST.get('user_id', None))
        
            if review_id and user_id:
                review = get_object_or_404(Review, pk=review_id)
                print('got review!')
                user = get_object_or_404(User, pk=user_id)
                print('got user!')
                # check if user has liked before
                liked_before = review.like_set.filter(user=user).first()
                if liked_before:
                    print("User has already liked the review. A new like will not be created again.")
                else:
                    # try:
                    new_like = review.like_set.create(user=user)
                    success = True
                    # except Exception as e:
                    #     print(e, "Invalid fields for like. Required: review id, user_id.")
                    total_likes = review.like_set.count()
        except Exception as e:
            print(e, "Review id and user_id need to be integers.")

        data = {
                'success': success,
                'total_likes': total_likes
            }
        return Response(data)


# reviewapp/api/restaurants/list
class GetRestaurantsByCategory(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        restaurants = None

        try:
            category_id = request.GET.get('category_id', None)
        
            if category_id:
                # 0 = All categories
                if category_id == "0":
                    restaurants = list(Restaurant.objects.all().values())
                else:
                    category = get_object_or_404(Category, pk=category_id)
                    restaurants = list(category.restaurant_set.all().values())

                for r in restaurants:
                    restaurant = Restaurant.objects.filter(pk=r['id']).first()
                    r['review_amount'] = restaurant.review_amount()
                    r['rating'] = restaurant.rating()
                    r['pricing'] = restaurant.pricing()
                    r['category'] = restaurant.category.category_text
                
                restaurants.sort(key=lambda x: int(x['rating']), reverse=False)

        except Exception as e:
            print(e, "Invalid category id.")

        data = {
            'restaurants': restaurants
        }
        return Response(data)
