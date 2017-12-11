
##################
#  2015-05-02
# various things that help create strings etc.. used by the textmate bundle 
#
##################




from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from django.conf import settings
from django.db import connection, models
from django.utils.http import urlquote
from time import strftime
import time, csv, os, sys

from extempore.models import *
from extempore.management.commands.parse import parse_extempore_src
			
			
from settings import printdebug




#  helper for django models 
def get_or_new(model, somename):
	"""helper method"""
	try:
		# if there's an object with same name, we keep that one!
		obj = model.objects.get(name=somename)
		print "++++++++++++++++++++++++++ found existing obj:	%s"	 % (obj)
	except:
		obj = model(name=somename)
		obj.save()
		print "======= created new obj:	  %s"  % (obj)
	return obj





# EG:
# bash-3.2$ python manage.py bootstrap_db

class Command(BaseCommand):
	args = '<no args >'
	help = 'bootstrap the db'
	option_list = BaseCommand.option_list  + (
						make_option('--reset', action='store', dest='reset', default='yes',
									help='The _reset_ option removes all previously saved values in the DB'),
				  )

	def handle(self, *args, **options): 
		"""
		args - args 
		options - configurable command line options
		"""

		# feedback:
		print >> sys.stderr, "\n\n++ = ++ = ++ \n%s\nSTARTING:"  % strftime("%Y-%m-%d %H:%M:%S")	
		print >> sys.stderr,  "++ = ++ = ++ \n"

		if options['reset'] == 'yes':
			# print "++ = ++ = ++ = ++ Cleaning all previously saved contents ...."
			# Subject.objects.all().delete()
			# print '.........successfully erased all previously saved contents!\n'
			pass # nothing to delete


		if False:			

			# 1) extract all offical fun names from DB (for autocompletion)

			# rset = XTMFundocEntry.objects.filter(fungroup="")
			rset = XTMFundocEntry.objects.filter()
			print ", ".join(["'%s'" % f.name for f in rset])

					
		if True:			


			DIRS = ['/Users/michele.pasin/Dropbox/code/extempore/utils']
		
			index = parse_extempore_src(DIRS)

			if False:  # debugging
				for fun in index:
					print fun['name']
						
			print ", ".join(["'%s'" % fun['name'] for fun in index])
			

		print >> sys.stderr, "\n\n++ = ++ = ++ \nCOMPLETED\n++ = ++ = ++ "





