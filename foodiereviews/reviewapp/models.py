from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Category(models.Model):
    category_text = models.CharField(max_length=50)
    
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
        amount = self.review_amount()
        if amount==0:
            return 0
        total_rating =0
        for review in self.review_set.all():
            total_rating+=review.review_rate
        return total_rating/amount

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_description = models.CharField(max_length=500)
    review_rate = models.IntegerField(default = 0)
    review_likes = models.IntegerField(default = 0)

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