from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(ModuleInstance)
admin.site.register(TaughtModule)
admin.site.register(Rating)