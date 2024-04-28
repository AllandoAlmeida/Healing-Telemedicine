from django.contrib import admin

from patient.models import Document, Query

# Register your models here.

admin.site.register(Query)
admin.site.register(Document)
