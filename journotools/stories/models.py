from django.db import models
from django.contrib.auth.models import User
import datetime 
		
# class Tag (models.Model):
	# tag = models.CharField ("Tag", max_length=50)
	# def __unicode__(self):
		# return u'%s %s' % (self.tag)
				
class Source (models.Model):
	user = models.ForeignKey (User, related_name="sources")
	first_name = models.CharField ("First name", max_length=100)
	last_name = models.CharField ("Last name", max_length=300) 
	job_title = models.CharField ("Job title", max_length=300) 
	company = models.CharField ("Company", max_length=300) 
	pub_date = models.DateTimeField("Date added", auto_now=True)
	comments = models.CharField ("Comments", max_length=300) 	
	def __unicode__(self):
		return u'%s %s' % (self.first_name, self.last_name) 
				
				
class Article (models.Model):
	user = models.ForeignKey (User, related_name="articles")
	title = models.CharField ("Title", max_length=100)
	lead = models.CharField ("Lead", max_length=300) # Needed? Maybe erase. 
	content = models.TextField()
	pub_date = models.DateTimeField("Last modified", auto_now=True)
	status = models.CharField ("Status", max_length=400)
	notes = models.CharField ("Notes", max_length=400)
	category = models.CharField ("Category", max_length=100)
	sources = models.ManyToManyField(Source, related_name='articles') 
	#tags = models.ManyToManyField(Tag, related_name='articles')
	#quotes = models.ManyToManyField(Quote, related_name='articles')# related name means you can search by that term in the Quote table
	def __unicode__(self):
		return self.title	
	def was_published_today(self):
		return self.pub_date.date() == datetime.date.today()
	was_published_today.short_description = 'Published today?'

#********************** WILL HAVE TO RENAME TO TRANSCRIPT. AND ADD DATE TO MODEL!!!*************************************
'''class Quote (models.Model):
	content = models.TextField()
	source = models.ForeignKey(Source, related_name='quotes') # related name means you can search by that term in the Source table
	def __unicode__(self):
		return self.content # WILL HAVE TO ADD DATE THERE.'''
		
	
#many-to-many: each object can relate to several objects, and vice versa. ForeignKey=one-to-many. So each quote can only have one source, but one source can have many quotes. 
#I chose manytomany relationship between quotes and articles, as sometimes quotes can be used across more than one article. 
