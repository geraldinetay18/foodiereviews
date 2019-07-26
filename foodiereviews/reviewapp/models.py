from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

import statistics


class Category(models.Model):
    category_text = models.CharField(max_length=50)
    

    def get_restaurants(self):
        return self.restaurant_set


    def __str__(self):
        return self.category_text


class Restaurant(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    restaurant_text= models.CharField(max_length=100)
    restaurant_address= models.CharField(max_length=100)


    def __str__(self):
        return self.restaurant_text


    def review_amount(self):
        return self.review_set.count()
    
    
    def rating(self):
        if self.review_amount() is 0:
            return 0
        ratings = [r.review_rate for r in self.review_set.all()]
        avg_rate = round(statistics.mean(ratings))
        avg_rate = 1 if avg_rate is 0 else avg_rate
        return avg_rate
    
    
    def pricing(self):
        if self.review_amount() is 0:
            return 0
        prices = [r.review_price for r in self.review_set.all()]
        avg_price = round(statistics.mean(prices))
        avg_price = 1 if avg_price is 0 else avg_price
        return avg_price


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=100)
    review_description = models.CharField(max_length=500)
    review_rate = models.IntegerField(default = 0)
    review_price = models.IntegerField(default = 0)
    review_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.review_description



class Comment(models.Model):
    review = models.ForeignKey(Review,on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_description = models.CharField(max_length=500)


    def __str__(self):
        return self.comment_description



class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_description = models.CharField(max_length=500)


    def __str__(self):
        return self.reply_description



class Like(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        string = 'review: '+ str(self.review.pk) + 'user: ' + self.user.username
        return string
