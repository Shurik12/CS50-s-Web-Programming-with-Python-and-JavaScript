from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length = 20)
    post_name = models.CharField(max_length=100, null=True, blank=True)
    post_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(to=User,  blank=True, related_name="liked_user")
    def serialize(self):
        return {
            "id": self.id,
            "username": self.user,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "post_name": self.post_name,
            "post_body": self.post_body
        }

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User,  blank=True, related_name="follower_user")
    following = models.ManyToManyField(User,  blank=True, related_name="following_user")

    def __str__(self):
        return self.user.username


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username, self.comment


class WatchList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username, self.post.post_name
