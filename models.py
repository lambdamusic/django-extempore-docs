from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings as django_settings
from django import forms
from django.conf.urls.defaults import *	 #for the ajax autocomplete

import datetime
# 
import myutils.modelextra.mymodels as mymodels
# from utils.myutils import blank_or_string, preview_string
# from utils.adminextra.autocomplete_tree_admin import *
# 
from settings import printdebug

EXTRA_SAVING_ACTIONS = True



class XTMFundocEntry(mymodels.EnhancedModel):
	"""(XTMFundocEntry enhanced model - timestamps and creation fields inherited)"""
	
	name = models.CharField(blank=True, max_length=200, verbose_name="name")
	url = models.CharField(blank=True, max_length=350, verbose_name="url")
	source = models.TextField(blank=True, verbose_name="implementation")
	fungroup = models.CharField(blank=True, max_length=350, verbose_name="group eg by prefix normally")
	funtype = models.CharField(blank=True, max_length=350, verbose_name="type eg whether r a macro or scheme function or xtlang")	
	# unused for now
	desc = models.TextField(blank=True, verbose_name="desc")
	signature = models.CharField(blank=True, max_length=300, verbose_name="signature")
	examples = models.TextField(blank=True, verbose_name="examples")
	args = models.TextField(blank=True, verbose_name="args")
	returns = models.CharField(blank=True, max_length=300, verbose_name="returns")	
	related = models.CharField(blank=True, max_length=300, verbose_name="related")
	
	class Admin(admin.ModelAdmin):
		list_display = ('id', 'name', 'funtype', 'fungroup', 'updated_at')
		list_display_links = ('id', 'name',)
		search_fields = ['id', 'name', 'desc']
		list_filter = ('created_at', 'updated_at', 'created_by', 'editedrecord', 'review', 'funtype', 'fungroup')
		#filter_horizontal = (,) 
		#related_search_fields = { 'fieldname': ('searchattr_name',)}
		#inlines = (inlineModel1, inlineModel2)
		fieldsets = [
			('Administration',	
				{'fields':	
					['editedrecord', 'review', 'internal_notes', ('created_at', 'created_by'), 
					  ('updated_at', 'updated_by')
					 ],	 
				'classes': ['collapse']
				}),
			('',	
				{'fields':	
					['name', 'url', 'source', 'desc', 'fungroup', 'funtype', 'signature', 'examples', 'args', 'returns', 'related'
					 ],	 
				# 'classes': ['collapse']
				}),	
			]
		#class Media:
			#js = ("js/admin_fixes/fix_fields_size.js",)
			
		def save_model(self, request, obj, form, change):
			"""adds the user information when the rec is saved"""
			if getattr(obj, 'created_by', None) is None:
				  obj.created_by = request.user
			obj.updated_by = request.user
			obj.save()	
			

	def get_admin_url(self):
		from django.core import urlresolvers
		# TODO: substitute and downcase the path!
		return urlresolvers.reverse('admin:MYAPP_XTMFundocEntry_change', args=(self.id,))
	get_admin_url.allow_tags = True

	def get_namespace(self):
		if self.fungroup:
			return self.fungroup
		else:
			return " top level"

	@models.permalink
	def get_absolute_url(self):
		return ('extempore_fun_detail', [str(self.id)])
			
	def save(self, force_insert=False, force_update=False):
		if EXTRA_SAVING_ACTIONS:
			super(XTMFundocEntry, self).save(force_insert, force_update)
			pass
		super(XTMFundocEntry, self).save(force_insert, force_update)	
			
	class Meta:
		verbose_name_plural="XTMFundocEntry"
		verbose_name = "XTMFundocEntry"
		ordering = ["id"]
		
	def __unicode__(self):
		return "XTMFundocEntry %d" % self.id
	




