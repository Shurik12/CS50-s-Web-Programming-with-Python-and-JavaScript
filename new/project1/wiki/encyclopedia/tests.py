from django.test import TestCase
from django.shortcuts import render
import markdown2
import os

from . import views

# Create your tests here.
class CreatePageTests(TestCase):
	
	def test_empty_name_empty_contetn_page(self):
		name, text = "", ""
		self.assertEqual(views.create_new_entry(name, text), False)

	def test_empty_name_fill_contetn_page(self):
		name, text = "", "bjbsavbds"
		self.assertEqual(views.create_new_entry(name, text), False)

	def test_fill_name_empty_contetn_page(self):
		name, text = "egewqgrefq", ""
		self.assertEqual(views.create_new_entry(name, text), False)

	def test_fill_name_fill_contetn_page(self):
		name, text = "dewgfwb", "breqrqbre"
		self.assertEqual(views.create_new_entry(name, text), True)
		os.remove("./entries/%s" % name+".md")