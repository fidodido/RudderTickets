from django.contrib import admin

# Register your models here.
# Register your models here.
from ticket.models import Project, Type, Status, Ticket, UserDetail, Reply, Action, Workflow

# Register your models here.
# Register your models here.
admin.site.register(Project)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Ticket)
admin.site.register(UserDetail)
admin.site.register(Reply)
admin.site.register(Action)
admin.site.register(Workflow)