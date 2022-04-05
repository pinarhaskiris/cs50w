from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

#model for auction listings
class Listing(models.Model):
	title = models.CharField(max_length=64) #name of the listing
	description = models.CharField(max_length=2048, default="No description.")
	price = models.IntegerField(default=0)
	creationDate = models.DateField()
	imgUrl = models.CharField(max_length=512, default="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png")
	isWatchlisted = models.BooleanField(default=False)
	creator = models.CharField(max_length=64, default="username")
	isOpen = models.BooleanField(default=True)
	category = models.CharField(default="no category", max_length=32)

	@classmethod
	def create_listing(cls, title, description, price, creationDate, imgUrl, creator, category):
		listItem = cls(title=title, description=description, price=price, creationDate=creationDate, imgUrl=imgUrl, creator=creator, category=category)
		return listItem

	def __str__(self):
		return f"{self.title}: {self.description}"


#model for bids
class Bid(models.Model):
	bidder = models.CharField(max_length=64)
	bid = models.IntegerField()
	bidItem = models.CharField(max_length=64, default="no such item")

	@classmethod
	def create_bid(cls, bidder, bid, bidItem):
		bidItem = cls(bidder=bidder, bid=bid, bidItem=bidItem)
		return bidItem

	def __str__(self):
		return f"{self.bidder} bid {self.bid} to {self.bidItem}"

#model for comments made on auction listings
class Comment(models.Model):
	commenter = models.CharField(max_length=64)
	comment = models.CharField(max_length=1024)
	listingName = models.CharField(max_length=64, default="no such item")

	@classmethod
	def create_comment(cls, commenter, comment, listingName):
		listingName = cls(commenter=commenter, comment=comment, listingName=listingName)
		return listingName

	def __str__(self):
		return f"{self.comment}"


