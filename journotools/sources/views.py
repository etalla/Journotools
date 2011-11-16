# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from sources.models import Source
from stories.models import Article
from django.template import RequestContext
from django.db.models import Q
import datetime 


#from django.http import Http404

def index(request):
	source_list = Source.objects.all().order_by('first_name')
	return render_to_response('sources/index.html',{'source_list': source_list})
	
def detail(request, source_id):
	a = get_object_or_404(Source, pk=source_id)
	article_list = a.articles.all()
	return render_to_response('sources/detail.html', {'Source':a,'article_list':article_list})
		
def delete(request, source_id):
	a = get_object_or_404(Source, pk=source_id)
	return render_to_response('sources/delete.html', {'Source': a},
		context_instance=RequestContext(request))

def delete_submit(request, source_id):
	a = get_object_or_404(Source, pk=source_id)
	if request.POST['choice'] == "Yes":
		a.delete()
	return HttpResponseRedirect(reverse('sources.views.index', args=()))	
	
def edit(request, source_id):
	a = get_object_or_404(Source, pk=source_id)
	return render_to_response('sources/edit.html', {'Source': a},
		context_instance=RequestContext(request))

def edit_submit(request, source_id):
	a = get_object_or_404(Source, pk=source_id)
	a.first_name = request.POST['first_name']
	a.last_name = request.POST['last_name']
	a.job_title = request.POST['job_title']
	a.company = request.POST['company']
	a.comments = request.POST['comments']
	a.save()
	return HttpResponseRedirect(reverse('sources.views.index', args=()))
	
def add(request):
	return render_to_response('sources/add.html',
		context_instance=RequestContext(request))

def add_submit(request):
	a = Source()
	a.first_name = request.POST['first_name']
	a.last_name = request.POST['last_name']
	a.job_title = request.POST['job_title']
	a.company = request.POST['company']
	a.comments = request.POST['comments']
	a.save()
	return HttpResponseRedirect(reverse('sources.views.index', args=()))

# class Story_Source (models.Model):
	# article = models.ForeignKey(Article)
	# source = models.ForeignKey(Source)
	
def source_query(request): 
	query = request.GET['q']
	source_list = Source.objects.filter( # this is a python query to the database
		Q(first_name__istartswith=query) | Q(last_name__istartswith=query)
	)
	return render_to_response('sources/source_query.json',{'source_list':source_list},
		context_instance=RequestContext(request))
