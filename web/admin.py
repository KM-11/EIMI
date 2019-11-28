from .models import Vmachine, Sample, Architecture, Family
from django.contrib import admin

# Register your models here.
admin.site.register(Vmachine)
admin.site.register(Sample)
admin.site.register(Architecture)
admin.site.register(Family)