from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
import random

from . import util

# вспомогательные функции
def create_new_entry(name_page, text_page):
	if name_page == "" or text_page == "": return False
	else:
		with open("./entries/%s" % name_page+".md", "w") as f_w: 
			f_w.write(text_page)
		return True

# основные функции 
def index(request):

	if request.method == 'GET':
		return render(request, "encyclopedia/index.html", {
			"entries": util.list_entries()
		})

	if request.method == 'POST':
		text_page = request.POST['text_page']
		name_page = request.POST['name_page']
		create_new_entry(name_page, text_page)
		return render(request, "encyclopedia/index.html", {
			"entries": util.list_entries()
		})		

def show_page(request, page_name):

	if request.method == 'GET':
		if page_name in util.list_entries():
			context = {
				"name": page_name,
				"content": markdown2.markdown_path("./entries/%s" % page_name+".md")
			}
			return render(request, "encyclopedia/entry.html", context)
		else:
			return render(request, "encyclopedia/errors.html") 

	if request.method == 'POST':
		content = request.POST['page_changes']
		create_new_entry(page_name, content)
		context = {
			"name": page_name,
			"content": markdown2.markdown(content)
		}
		# return render(request, "encyclopedia/entry.html", context)
		return render(request, "encyclopedia/entry.html", context)

def edit_page(request, page_name):
	with open("./entries/%s" % page_name+".md", "r") as f_r: 
		content = f_r.read()
	context = {
		"name": page_name,
		"content": content
	}
	return render(request, "encyclopedia/edit.html", context)	

def create_page(request):
	return render(request, "encyclopedia/create.html")	

def random_page(request):
	pages = util.list_entries()
	page = random.choices(pages, k=1)[0]
	context = {
		"name": page,
		"content": markdown2.markdown_path("./entries/%s" % page+".md")
	}
	return render(request, "encyclopedia/entry.html", context)

def search_page(request):
	search_page = request.POST['q']
	list_entries = util.list_entries()
	if search_page in list_entries:
		context = {
			"name": search_page,
			"content": markdown2.markdown_path("./entries/%s" % search_page+".md")
		}
		return render(request, "encyclopedia/entry.html", context)
	else:
		new_list = []
		for entry in list_entries:
			if search_page in entry: new_list.append(entry)
		return render(request, "encyclopedia/index.html", {"entries": new_list})