from stories.models import Article
from stories.models import Source

import json
import datetime 

from django.http import *
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.db.models import Q, Count
from django.contrib.csrf.middleware import csrf_exempt
from django.core.context_processors import csrf


from django.contrib.auth.models import User
from django.contrib.auth import *
import django.contrib.auth.views
from django.contrib.auth.decorators import login_required

status_dict = {'': 'To start', 'to_start':'To start', 'in_progress':'In progress', 'almost_done':'Almost done','completed':'Completed'}  
category_dict = {'': 'News', 'news':'News', 'feature':'Feature', 'opinion':'Opinion','analysis':'Analysis'}  


#**************************************************************     DUMMIES    ****************************************************************************
#**************************************************************     DUMMIES    ****************************************************************************
#**************************************************************     DUMMIES    ****************************************************************************

@login_required(login_url='/login_page')
def test(request):
	username = request.user.username
	return render_to_response('dummies/test.html',{'User':username})
	
def users(request):
	user_list = User.objects.all()
	return render_to_response('dummies/users.html',{'user_list':user_list})
	
#**************************************************************     WELCOME PAGE   ****************************************************************************
#**************************************************************     WELCOME PAGE   ****************************************************************************
#**************************************************************     WELCOME PAGE   ****************************************************************************

def index(request):
	return render_to_response('index.html',
		context_instance=RequestContext(request))
	
#**************************************************************     USERS    ****************************************************************************
#**************************************************************     USERS    ****************************************************************************
#**************************************************************     USERS    ****************************************************************************
		
def login_page(request):
	return render_to_response('login_page.html',
		context_instance=RequestContext(request))

def register(request):
	u = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
	u.first_name = request.POST['first_name']
	u.last_name = request.POST['last_name']
	u.save()
	user = authenticate(username=u.username, password=request.POST['password'])
	login(request, user)
	return render_to_response('register.html',{'User':u},
		context_instance=RequestContext(request))
#register=csrf_exempt(register)

def login_submit(request):
	user = authenticate(username=request.POST['username'], password=request.POST['password'])
	if user is not None:
		if user.is_active:
			login(request, user)
			message = "You are now logged in as %s." %user.username
			return HttpResponseRedirect('/stories')
		else:
			message = "Your account has been disabled."
		return HttpResponseRedirect('/account_disabled')
	else:
		message = "Your username and password were incorrect." 
		return HttpResponseRedirect('/login_error')
#login_submit=csrf_exempt(login_submit)

def login_error(request):
	return render_to_response('login_error.html',
		context_instance=RequestContext(request))

def account_disabled(request):
	return render_to_response('account_disabled.html',
		context_instance=RequestContext(request))

def logout_view(request):
	logout(request)
	return render_to_response('logout_view.html',
		context_instance=RequestContext(request))

#**************************************************************     ARTICLES    ****************************************************************************
#**************************************************************     ARTICLES    ****************************************************************************
#**************************************************************     ARTICLES    ****************************************************************************

'''@login_required(login_url='/login_page')
def stories(request):
	article_list = Article.objects.annotate(number_of_sources=Count('sources')).order_by('-pub_date')
	order_by='-pub_date'
	sort_by='desc'
	if 'order_by' in request.GET and request.GET['order_by'] and request.GET['sort_by']:	
		order_by = request.GET['order_by']
		sort_by = request.GET['sort_by']
		if request.GET['sort_by']=='desc':
			article_list = article_list.order_by(order_by).reverse()
		else:
			article_list = article_list.order_by(order_by)
	return render_to_response('stories.html', {'article_list':article_list,'order_by':order_by,'sort_by':sort_by,'status_dict':status_dict,'category_dict':category_dict})
'''
@login_required(login_url='/login_page')
def stories(request):
	if request.user.is_authenticated():
		article_list = request.user.articles.annotate(number_of_sources=Count('sources')).order_by('-pub_date')
		#article_list = Article.objects.filter(user=request.user).annotate(number_of_sources=Count('sources')).order_by('-pub_date')
		order_by='-pub_date'
		sort_by='desc'
		if 'order_by' in request.GET and request.GET['order_by'] and request.GET['sort_by']:	
			order_by = request.GET['order_by']
			sort_by = request.GET['sort_by']
			if request.GET['sort_by']=='desc':
				article_list = article_list.order_by(order_by).reverse()
			else:
				article_list = article_list.order_by(order_by)
		return render_to_response('stories.html', {'article_list':article_list,'order_by':order_by,'sort_by':sort_by,'status_dict':status_dict,'category_dict':category_dict},
			context_instance=RequestContext(request))
		
		
@login_required(login_url='/login_page')
def status_edit(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	status = request.raw_post_data
	if status in status_dict:
		a.status = status
		a.save()
		return HttpResponseRedirect(reverse('stories.views.index'))
	else:
		return HttpResponseBadRequest("This status selection is invalid.")

@login_required(login_url='/login_page')
def category_edit(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	category = request.raw_post_data
	if category in category_dict:
		a.category = category
		a.save()
		return HttpResponseRedirect(reverse('stories.views.index'))
	else:
		return HttpResponseBadRequest("This category selection is invalid.")

@login_required(login_url='/login_page')
def detail(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	list = a.sources.all()
	return render_to_response('detail.html', {'Article': a, 'list':list, 'status_dict':status_dict,'category_dict':category_dict},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def delete(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	return render_to_response('delete.html', {'Article': a},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def delete_submit(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	if request.POST['choice'] == "Yes":
		a.delete()
		return render_to_response('delete_submit.html',
			context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect(reverse('stories.views.stories', args=()))	

@login_required(login_url='/login_page')
def add(request):
	return render_to_response('add.html',
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def add_submit(request):
	next = request.GET.get('next', '') 
	a = Article()
	a.user = request.user
	a.title = request.POST['title']
	a.lead = request.POST['lead']
	a.content = request.POST['content']
	a.pub_date = datetime.datetime.today()
	a.notes = request.POST['notes']
	a.category = request.POST['category']
	a.status = request.POST['status']
	#a.tags = request.POST['tags']
	a.save()
	b = request.POST['sources'].rsplit(',') #this takes the string and returns a list of the results in the string separated by the separator given -- here, the comma
	list = []
	for i in range (0,len(b)-1):
		if b[i] not in list:
			list.append(b[i])
	for j in a.sources.all():
		a.sources.remove(j)
	for i in list:
		s = get_object_or_404(Source, pk = i)
		a.sources.add(s)
	a.save()
	article_id=a.id
	#return HttpResponseRedirect(reverse('stories.views.stories', args=()))
	if next == "stories":
		return HttpResponseRedirect(reverse('stories.views.stories'))
	else:
		return HttpResponseRedirect(reverse('stories.views.%s' %next, kwargs={'article_id':article_id}))#return HttpResponseRedirect(reverse('stories.views.detail', kwargs={'article_id':article_id})) # the reverse tells the program to go to views.detail, tell it what url it is, then go back
		
	
@login_required(login_url='/login_page')
def add_source_api(request):
	sources=json.loads(request.raw_post_data) # the json converter turns it from string to object. 
	a = Source()
	#q = Quote()
	a.user = request.user
	a.first_name = sources["first_name"]
	a.last_name = sources["last_name"]
	a.job_title = sources["job_title"]
	a.company = sources["company"]
	a.comments = sources["comments"]
	# q.quote = sources["quotes"]
	# q.save()
	# a.quotes = q
	a.save()
	result = {}
	result["id"] = a.id
	result["first_name"]=a.first_name	
	result["last_name"]=a.last_name
	return HttpResponse(json.dumps(result,separators=(',',':')))

@login_required(login_url='/login_page')
def edit(request, article_id):
	a = get_object_or_404(Article, pk=article_id)
	return render_to_response('edit.html', {'Article': a},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def edit_submit(request, article_id):
	next = request.GET.get('next', '') 
	a = get_object_or_404(Article, pk=article_id)
	a.title = request.POST['title']
	a.lead = request.POST['lead']
	a.content = request.POST['content']
	a.status = request.POST['status']
	a.notes = request.POST['notes']
	a.category = request.POST['category']
	#a.tags = request.POST['tags']
	b = request.POST['sources'].rsplit(',') #this takes the string and returns a list of the results in the string separates by the separator given -- here, the comma
	list = []
	for i in range (0,len(b)-1):
		if b[i] not in list:
			list.append(b[i])
	for j in a.sources.all():
		a.sources.remove(j)
	for i in list:
		s = get_object_or_404(Source, pk = i)
		a.sources.add(s)
	a.save()
	if next == "stories":
		return HttpResponseRedirect(reverse('stories.views.stories'))
	else:
		return HttpResponseRedirect(reverse('stories.views.%s' %next, kwargs={'article_id':article_id}))#return HttpResponseRedirect(reverse('stories.views.detail', kwargs={'article_id':article_id})) # the reverse tells the program to go to views.detail, tell it what url it is, then go back
						#to this program with the URL. If you skipped the reverse, it would go straight to the URL, which would make it go wonky if your URL changes. 
						
#**************************************************************     SOURCES  ****************************************************************************
#**************************************************************     SOURCES  ****************************************************************************
#**************************************************************     SOURCES  ****************************************************************************

@login_required(login_url='/login_page')
def sources_index(request):
	source_list = request.user.sources.annotate(number_of_articles=Count('articles')).order_by('first_name')
	#source_list = Source.objects.annotate(number_of_articles=Count('articles')).order_by('first_name')
	order_by='first_name'
	sort_by='desc'
	if 'order_by' in request.GET and request.GET['order_by'] and request.GET['sort_by']:	
		order_by = request.GET['order_by']
		sort_by = request.GET['sort_by']
		if request.GET['sort_by']=='desc':
			source_list = source_list.order_by(order_by).reverse()
		else:
			source_list = source_list.order_by(order_by)
	return render_to_response('sources_index.html',{'source_list': source_list,'order_by':order_by,'sort_by':sort_by},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def sources_detail(request, source_id):
	s = get_object_or_404(Source, pk=source_id)
	article_list = s.articles.all()
	#quote_list = s.quotes.all()
	#short_quote_list = s.quotes.all()
	#for quote in short_quote_list:
	#	quote.content = quote.content[0:100]
	return render_to_response('sources_detail.html', {'Source':s,'article_list':article_list},
		context_instance=RequestContext(request)) # ,short_quote_list':short_quote_list
		
@login_required(login_url='/login_page')
def sources_delete(request, source_id):
	s = get_object_or_404(Source, pk=source_id)
	number_of_articles = s.articles.count()
	return render_to_response('sources_delete.html', {'Source': s, 'number_of_articles':number_of_articles},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def sources_delete_submit(request, source_id):
	s = get_object_or_404(Source, pk=source_id)
	if request.POST['choice'] == "Yes":
		s.delete()
	return HttpResponseRedirect(reverse('stories.views.sources_index', args=()))
	
@login_required(login_url='/login_page')
def sources_edit(request, source_id):
	s = get_object_or_404(Source, pk=source_id)
	return render_to_response('sources_edit.html', {'Source': s},
		context_instance=RequestContext(request))

@login_required(login_url='/login_page')
def sources_edit_submit(request, source_id):
	s = get_object_or_404(Source, pk=source_id)
	s.first_name = request.POST['first_name']
	s.last_name = request.POST['last_name']
	s.job_title = request.POST['job_title']
	s.company = request.POST['company']
	s.comments = request.POST['comments']
	s.save()
	return HttpResponseRedirect(reverse('stories.views.sources_index', args=()))
	
@login_required(login_url='/login_page')
def sources_add(request):
	return render_to_response('sources_add.html',
		context_instance=RequestContext(request))

def sources_add_submit(request):
	s = Source()
	s.user = request.user
	s.first_name = request.POST['first_name']
	s.last_name = request.POST['last_name']
	s.job_title = request.POST['job_title']
	s.company = request.POST['company']
	s.comments = request.POST['comments']
	s.save()
	return HttpResponseRedirect(reverse('stories.views.sources_index', args=()))
	
@login_required(login_url='/login_page')
def source_query(request): 
	query = request.GET['q']
	source_list = request.user.sources.filter( # this is a python query to the database
		Q(first_name__istartswith=query) | Q(last_name__istartswith=query)
	)
	return render_to_response('source_query.json',{'source_list':source_list},
		context_instance=RequestContext(request))

#**************************************************************     TRANSCRIPTS  *****************************************************************************
#**************************************************************     TRANSCRIPTS  *****************************************************************************
#**************************************************************     TRANSCRIPTS  *****************************************************************************

'''def quotes(request):
	quote_list = Quote.objects.all()
	short_quote_list = Quote.objects.all()
	for quote in short_quote_list:
		quote.content = quote.content[0:20]
	return render_to_response('quotes.html', {'quote_list':quote_list,'short_quote_list':short_quote_list})

def quote_detail(request, quote_id):
	q = get_object_or_404(Quote, pk=quote_id)
	return render_to_response('quote_detail.html', {'Quote':q})

def quote_edit (request, quote_id):
	q = get_object_or_404(Quote, pk=quote_id)
	q.content = request.POST['transcript']
	q.save()
	return HttpResponseRedirect(reverse('stories.views.quote_detail', args=[quote_id]))

quote_edit = csrf_exempt(quote_edit)
	
def new_quote(request):
	return render_to_response('new_quote.html',
		context_instance=RequestContext(request))
	
def submit_new_quote(request):
	q = Quote()
	q.content = request.POST['content']
	source = request.POST['sources'][0]#this takes the string and returns a list of the results in the string separates by the separator given -- here, the comma
	q.source = get_object_or_404(Source, pk = source)
	q.save()
	return HttpResponseRedirect(reverse('stories.views.quotes', args=()))	

submit_new_quote = csrf_exempt(submit_new_quote)

def submit_new_transcript(request): #this is used in the source detail template. 
	q = Quote()
	q.content = request.POST['transcript']
	source = get_object_or_404(Source, pk=int(request.POST['source_id']))
	q.source = source
	q.save()
	return HttpResponseRedirect(reverse('stories.views.sources_detail', args=[source.id]))
	
submit_new_transcript = csrf_exempt(submit_new_transcript)'''
		