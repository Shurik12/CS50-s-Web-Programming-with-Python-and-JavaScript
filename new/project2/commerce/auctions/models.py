from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass

class AuctionListings(models.Model):
	name = models.CharField(max_length = 100, unique=True)
	user_name = models.CharField(max_length = 20)
	count_bids = models.IntegerField(default = 0)
	price = models.FloatField()
	description = models.TextField()
	image_url = models.TextField()
	created_date = models.DateTimeField('date published')
	actual = models.BooleanField(default = True)

class AuctionBids(models.Model):
	listing_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, to_field='name')
	bid_price = models.FloatField()
	user_bid = models.CharField(max_length = 20)
	date = models.DateTimeField('date click')

class AuctionComments(models.Model):
	listing_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, to_field='name')
	comment_text = models.TextField()
	user = models.CharField(max_length = 20)
	date = models.DateTimeField('date comment')
	def __str__(self):
		return self.comment_text

class Categories(models.Model):
	listing_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, to_field='name')
	category = models.CharField(max_length = 50)

class Watchlists(models.Model):
	user = models.CharField(max_length = 20)
	listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, to_field='name')


