from django.contrib import admin
from voting.models import VotingQuestion, Votes

# # Register your models here.
admin.site.register(VotingQuestion)
admin.site.register(Votes)
