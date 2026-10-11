from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UserRegistration
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'somme')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('classe', 'numero_telephone', 'ville', 'avater')
        })
    )    

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name',)
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('classe', 'numero_telephone', 'ville')
        })
    )

    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ('numero_telephone',)
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "last_login",
        'somme',
        'numero_telephone',
       
    )
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(UserRegistration, CustomUserAdmin)


admin.site.site_title = "Easy School Cameroon"
admin.site.site_header = "Easy School Cameroon"
admin.site.index_title = "Easy School Cameroon"