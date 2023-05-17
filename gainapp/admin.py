from django.contrib import admin

# Register your models here.
from . models import *

admin.site.register(Profile)
admin.site.register(Crypto)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Support)
admin.site.register(Team)
