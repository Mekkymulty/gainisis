from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(Crypto)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Team)

