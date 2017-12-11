
##################
#  2015-05-02
#
#  This script facilitate testing and developing
#
#  python manage.py extempore_docs_loader
#

#  note: this extracts functions from standard extmpore dir (usr/Cellar)
#  the script was developed within code/extempore/xtm-utils-public/..
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
from extempore.management.commands.parse import parse_extempore_src, _dirname


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



DEFAULT_XTMDIR = ['/Applications/-Other-Apps/2-Music/_synthesys/extempore/']



# EG:
# bash-3.2$ python manage.py extempore_docs_loader

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
		print "\n\n++ = ++ = ++ \n%s\nSTARTING:"  % strftime("%Y-%m-%d %H:%M:%S")
		print "++ = ++ = ++ \n"

		if options['reset'] == 'yes':
			print "++ = ++ = ++ = ++ Cleaning all previously saved contents ...."
			XTMFundocEntry.objects.all().delete()
			print '.........successfully erased all previously saved contents!\n'
			# pass # nothing to delete


		if True:

			DIRS = DEFAULT_XTMDIR

			index = parse_extempore_src(DIRS)

			#
			# css = HtmlFormatter().get_style_defs('.highlight')

			for fun in index:

				f1 = XTMFundocEntry()
				f1.name = fun['name']
				f1.url = fun['url']
				f1.source = fun['codepygments'] #note: css needs manually added to page
				f1.fungroup = fun['group']
				f1.funtype = fun['functiontype']
				f1.save()
				print >> sys.stderr, f1.name, f1.id



		printdebug("\n\n++ = ++ = ++ \nCOMPLETED\n++ = ++ = ++ ")
