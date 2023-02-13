from django.contrib import admin
from .models import Meeting,Minutes,Annotation,Rsvp,AgendaAction,MinutesAgenda,AgendaItem

# Register your models here.
admin.site.register(Meeting)
admin.site.register(Minutes)
admin.site.register(Annotation)
admin.site.register(Rsvp)
admin.site.register(AgendaAction)
admin.site.register(MinutesAgenda)
admin.site.register(AgendaItem)