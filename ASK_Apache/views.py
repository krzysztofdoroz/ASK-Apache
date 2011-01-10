from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response

from Parser.parser import *
from forms import *

import datetime

def hello(request):
	return HttpResponse("Hello world")

def current_datetime(request):
	current_date = datetime.datetime.now()
	return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
	return HttpResponse(html)

def show_virtual_hosts(request):
	virtualHost = VirtualHost()
	virtualHost.parse("C:/Users/krzysztof/Desktop/administracja/src/default")
	print len(virtualHost.nodes)
	return render_to_response('current_datetime.html', locals())

def edit_virtual_host(request, virtualHostId):
	virtualHost = VirtualHost()
	return render_to_response('editVirtualHost.html', locals())

def edit_node(request, nodeId):
	
	print "inside edit_node:"
	print nodeId
	
	try:
		nodeId = int(nodeId)
		nodeId = nodeId - 1
	except ValueError:
		raise Http404()

	virtualHost = VirtualHost()
	#virtualHost.parse( "/etc/httpd/conf/httpd.conf" )
	virtualHost.parse("C:/Users/krzysztof/Desktop/administracja/src/default")
	if nodeId > len(virtualHost.nodes):
		raise Http404()

	if request.method == 'POST': # If the form has been submitted...
		
		nodeId = nodeId + 1
		form = request.POST
		
		print "FORM:"
		print form
		
		modifiedNode = virtualHost.nodes[nodeId - 1]
		
		modifiedNode.data = []
		
		index = 0
		for a in form:
			
			str = ""
			for list_el in form.getlist(a):
				str = str + list_el
			
			new_data = Data([],a,str)
			
			modifiedNode.data.append(new_data)
			print a
			print form.getlist(a)
		
		virtualHost.save_to_file("C:/Users/krzysztof/Desktop/administracja/src/default")	
		
		return HttpResponseRedirect('/test/')
		
		form = NodeForm(request.POST) # A form bound to the POST data
		
	else:
		
		print "ELSE:"
		node = virtualHost.nodes[nodeId]
		nodeId = nodeId + 1
		
	return render_to_response('editNode.html', locals())


def edit_data(request, dataNodeId):
	
	print "inside edit_data:"
	print dataNodeId
	
	try:
		nodeId = int(dataNodeId)
		nodeId = nodeId - 1
	except ValueError:
		raise Http404()

	virtualHost = VirtualHost()
	#virtualHost.parse( "/etc/httpd/conf/httpd.conf" )
	virtualHost.parse("C:/Users/krzysztof/Desktop/administracja/src/default")
	if nodeId > len(virtualHost.data):
		raise Http404()

	if request.method == 'POST': # If the form has been submitted...
		
		nodeId = nodeId + 1
		form = request.POST
		
		print "FORM:"
		
		for a in form:
			print a
			print form.get(a)
		
		dataNode = virtualHost.data[nodeId - 1]
		
		print form.get(dataNode.key)
		dataNode.value = form.get(dataNode.key)
		
		
		
		virtualHost.save_to_file("C:/Users/krzysztof/Desktop/administracja/src/default")	
		
		return HttpResponseRedirect('/test/')
		
	else:
		
		print "ELSE:"
		dataNode = virtualHost.data[nodeId]
		nodeId = nodeId + 1
		
	return render_to_response('edit_data.html', locals())
	