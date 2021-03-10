from django.contrib import admin
from dresser import models
import inspect

# Register your models here.
for cls_ in inspect.getmembers(models, inspect.isclass):
    exec(f"admin.site.register(models.{cls_[0]})")

