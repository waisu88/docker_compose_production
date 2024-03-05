from django.contrib import admin
from .models import Language, Word, WordsPair

# Register your models here.
admin.site.register((Language, Word, WordsPair,))