from django.contrib import admin
from finflo.models import Action, States, Temp, TransitionManager, workflowitems, workevents
# Register your models here.
from django.conf import settings




admin.site.register(TransitionManager)
admin.site.register(Action )
admin.site.register(States)