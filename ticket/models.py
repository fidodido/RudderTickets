from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Project(models.Model):
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name


class Type(models.Model):
	name = models.CharField(max_length=255, unique=True)
	icon = models.CharField(default='', max_length=255)
	color = models.CharField(default='', max_length=255)

	def __unicode__(self):
		return self.name


class Status(models.Model):

	name = models.CharField(max_length=255, unique=False)
	label_class = models.CharField(max_length=255, default="label label-default")

	def __unicode__(self):
		return self.name


class Ticket(models.Model):

	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField()
	created_by = assigned_to = models.ForeignKey(User, default=1, related_name='created_by')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.ForeignKey(Status, default=1)
	type = models.ForeignKey(Type)
	assigned_to = models.ForeignKey(User, null=True, related_name='assigned_to')
	high_priority = models.BooleanField(default=0)
	user_detail = models.ManyToManyField(User, through='UserDetail')

	def is_priority(self):
		return True if self.high_priority else False


# Un ticket tiene muchas respuestas como un blog/post
class Reply(models.Model):

	comment = models.CharField(max_length=255)
	ticket = models.ForeignKey(Ticket)
	user = models.ForeignKey(User)
	created = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name


class Attachment(models.Model):
	
	name = models.CharField(max_length=255)
	hash = models.CharField(default='', max_length=255)
	reply = models.ForeignKey(Reply)

	def __unicode__(self):
		return self.name
		

class UserDetail(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	viewed = models.BooleanField(default=0)

	def __unicode__(self):
		return self.name


class Action(models.Model):

	name = models.CharField(max_length=255)
	current_status = models.ForeignKey(Status, related_name='current_status')
	post_status = models.ForeignKey(Status, related_name='post_status')
	slug = models.CharField(max_length=255, unique=False, default="-")
	class_name = models.CharField(max_length=255, default="btn btn-md btn-default")
	icon = models.CharField(max_length=255, default="glyphicon glyphicon-remove")

	def __unicode__(self):
		return self.name


class Workflow(models.Model):

	current_status = models.ForeignKey(Status, related_name='wf_current_status')
	post_status = models.ForeignKey(Status, related_name='wf_post_status')
	comment = models.CharField(blank=True, default='', max_length=255)
	ticket = models.ForeignKey(Ticket)
	user = models.ForeignKey(User)
	modified = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name

