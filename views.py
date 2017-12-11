from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext	#needed for passing the conf details

import time
import os





#
# ===========
# May 3, 2015 : new bootstrap views
# ===========
#


from extempore.models import *


def index(request):
	
	q = request.GET.get("q", "")
	
	if q:
		qset = XTMFundocEntry.objects.filter(name__icontains=q)		
		items = sorted(qset, key=lambda a: a.get_namespace())
		# namespaces = sorted(list(set([a.get_namespace() for a in qset])))
		namespaces = None
	else:
		qset = XTMFundocEntry.objects.all()			
		items = sorted(qset, key=lambda a: a.get_namespace())
		namespaces = sorted(list(set([a.get_namespace() for a in qset])))	
		
		
	context = {	'items' : items , 'q' : q , 'namespaces' : namespaces}

	return render_to_response("extempore/home.html", 
								context,
								context_instance=RequestContext(request))



def funpage(request, num):
	"""view that returns a specific function documentation
		if parameter is wrong, gives a 404
	"""
	from django.db.models import Q
	
	try:
		item = XTMFundocEntry.objects.get(pk=int(num))
		
		name_bits = item.name.replace("_", " ").split()
		
		# related_items = XTMFundocEntry.objects.filter(name__icontains=item.name)
		# related_items = XTMFundocEntry.objects.filter(name__in=name_bits)
		
		related_items = XTMFundocEntry.objects.exclude(pk=item.id).filter(reduce(lambda x, y: x | y, [Q(name__icontains=n) for n in name_bits]))
		
		
		context = {	'item' : item, 'related_items' : related_items }

		return render_to_response("extempore/item.html", 
									context,
									context_instance=RequestContext(request))
	except:
		# raise Http404
		# return HttpResponseRedirect(reverse('impromptu_home', kwargs={'q': num}))
		return redirect("%s%s" % (reverse('extempore_home'), "?q=" + str(num)))
		# return HttpResponseRedirect(reverse('impromptu_home', kwargs={'q': num}))






