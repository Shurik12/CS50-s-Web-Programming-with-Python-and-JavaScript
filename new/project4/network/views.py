from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import ast

from .models import *

@csrf_exempt
def index(request):
	return render(request, "network/index.html")


def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "network/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "network/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "network/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "network/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "network/register.html")

# @login_required
@csrf_exempt
def network(request):

	if request.method == "POST":
		
		data = ast.literal_eval(request.body.decode("UTF-8")) # data = repr(b)
		post = Post(user = request.user, post_name = data["name"], post_body = data["body"], timestamp = timezone.now())
		post.save()


	posts = Post.objects.all().order_by('-timestamp')
	paginator = Paginator(posts, 10)
	if request.GET.get("page") != None:
		try:
			posts = paginator.page(request.GET.get("page"))
		except:
			posts = paginator.page(1)
	else:
		posts = paginator.page(1)
	posts_next = posts.has_next() 
	posts_previous = posts.has_previous()

	user = request.user

	new_posts = []
	for post in posts:
		if user in post.like.all():
			is_liked = True
		else: is_liked = False
		count_likes = post.like.count()
		post = post.serialize()
		post["is_liked"] = is_liked
		post["count_likes"] = count_likes
		new_posts.append(post)
 
	context = {
		"next" : posts_next,
		"prev": posts_previous,
		"username": user.username,
		"auth": user.is_authenticated,
		"posts": new_posts
	}
	return JsonResponse(context)

@csrf_exempt
def profile(request):
	if request.method == "POST":
		user_request = request.user
		data = ast.literal_eval(request.body.decode("UTF-8")) # data = repr(b)
		user_post = data["username"]
		user_post_object = User.objects.get(username=user_post)
		profile = Profile.objects.get(user=user_post_object)
		count_followers = profile.follower.count()
		count_followings = profile.following.count()
		if user_request in profile.follower.all():
			is_follower = True
		else: is_follower = False


		posts = Post.objects.filter(user=user_post).order_by('-timestamp')
		paginator = Paginator(posts, 10)
		if request.GET.get("page") != None:
			try:
				posts = paginator.page(request.GET.get("page"))
			except:
				posts = paginator.page(1)
		else:
			posts = paginator.page(1)
		posts_next = posts.has_next() 
		posts_previous = posts.has_previous()

		new_posts = []
		for post in posts:
			if user_request in post.like.all():
				is_liked = True
			else: is_liked = False
			count_likes = post.like.count()
			post = post.serialize()
			post["is_liked"] = is_liked
			post["count_likes"] = count_likes
			new_posts.append(post)
	 
		context = {
			"next" : posts_next,
			"prev": posts_previous,
			"username": user_request.username,
			"user_post": user_post,
			"auth": user_request.is_authenticated,
			"count_followers": count_followers,
			"count_followings": count_followings,
			"is_follower": is_follower,
			"posts": new_posts
		}
	return JsonResponse(context)


@csrf_exempt
def editpost(request):

	if request.method == "POST":

		user = request.user
		
		data = ast.literal_eval(request.body.decode("UTF-8")) # data = repr(b)
		post = Post.objects.get(id=data["id"])
		post.post_name = data["name"]
		post.post_body = data["body"]
		post.save()


		posts = Post.objects.all().order_by('-timestamp')
		paginator = Paginator(posts, 10)
		if request.GET.get("page") != None:
			try:
				posts = paginator.page(request.GET.get("page"))
			except:
				posts = paginator.page(1)
		else:
			posts = paginator.page(1)
		posts_next = posts.has_next() 
		posts_previous = posts.has_previous()

		new_posts = []
		for post in posts:
			if user in post.like.all():
				is_liked = True
			else: is_liked = False
			count_likes = post.like.count()
			post = post.serialize()
			post["is_liked"] = is_liked
			post["count_likes"] = count_likes
			new_posts.append(post)
	 
		context = {
			"next" : posts_next,
			"prev": posts_previous,
			"username": user.username,
			"auth": user.is_authenticated,
			"posts": new_posts
		}
		return JsonResponse(context)


# @login_required
@csrf_exempt
def following(request):

	user = request.user
	profile = Profile.objects.get(user=user)
	followings = profile.following.all()
	users = []
	for foll in followings:
		users.append(foll.username)

	posts = Post.objects.filter(user__in=users).order_by('-timestamp')
	paginator = Paginator(posts, 10)
	if request.GET.get("page") != None:
		try:
			posts = paginator.page(request.GET.get("page"))
		except:
			posts = paginator.page(1)
	else:
		posts = paginator.page(1)
	posts_next = posts.has_next() 
	posts_previous = posts.has_previous()

	new_posts = []
	for post in posts:
		if user in post.like.all():
			is_liked = True
		else: is_liked = False
		count_likes = post.like.count()
		post = post.serialize()
		post["is_liked"] = is_liked
		post["count_likes"] = count_likes
		new_posts.append(post)
 
	context = {
		"next" : posts_next,
		"prev": posts_previous,
		"username": user.username,
		"auth": user.is_authenticated,
		"posts": new_posts
	}
	return JsonResponse(context)