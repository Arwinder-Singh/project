from django.contrib import admin

from .models import User,Product,Fp,Billing,fpRecord,associationRecord,association


# Register your models here.

admin.site.register(User) 
admin.site.register(Product) 
admin.site.register(Fp) 
admin.site.register(Billing) 
admin.site.register(fpRecord) 
admin.site.register(associationRecord) 
admin.site.register(association) 