from django.contrib import admin

from core.models import User, TitledImage, Like

class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # Override this to set the password to the value in the field if it's
        # changed.
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)
admin.site.register(TitledImage)
admin.site.register(Like)
