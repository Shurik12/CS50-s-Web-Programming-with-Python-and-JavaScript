from django.contrib import admin
from .models import *

class AuctionBidsInline(admin.TabularInline): # табличная реализация
# class ChoiceInline(admin.StackedInline): # списочная реализация
	model = AuctionBids
	extra = 1

class CategoriesInline(admin.TabularInline): # табличная реализация
# class ChoiceInline(admin.StackedInline): # списочная реализация
	model = Categories
	extra = 1

class AuctionCommentsInline(admin.TabularInline): # табличная реализация
# class ChoiceInline(admin.StackedInline): # списочная реализация
	model = AuctionComments
	extra = 1

class AuctionListingsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name', 'price', 'description', 'image_url']}),
		('Add info', {'fields': ['created_date', 'user_name', 'actual', 'count_bids'],
		'classes': ['collapse']}),
	]
	inlines = [
		AuctionBidsInline,
		CategoriesInline,
		AuctionCommentsInline
	]
	list_display = ('name', 'user_name', 'count_bids', 'price', 'description', 
		'image_url', 'created_date', 'actual')
	list_filter = ['created_date']
	search_fields = ['description']

admin.site.register(AuctionListings, AuctionListingsAdmin)