from django.contrib import admin
from .models import (
    MessageTemplate, Prospect, ProspectNote, ProspectMessage
)


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'usage_type', 'language', 'stage', 'is_default', 'created_at']
    list_filter = ['usage_type', 'language', 'stage', 'is_default']
    search_fields = ['name', 'subject', 'body']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'usage_type', 'language', 'stage', 'is_default')
        }),
        ('Contenu Email', {
            'fields': ('subject', 'body')
        }),
        ('Lettre de Motivation (Stage uniquement)', {
            'fields': ('cover_letter_html',),
            'classes': ('collapse',)  # Section repliable
        }),
    )


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_name', 'status', 'estimated_value', 'source', 'created_at']
    list_filter = ['status', 'source', 'has_website', 'has_facebook']
    search_fields = ['company_name', 'contact_name', 'email', 'city']
    date_hierarchy = 'created_at'


@admin.register(ProspectNote)
class ProspectNoteAdmin(admin.ModelAdmin):
    list_display = ['prospect', 'created_at']
    search_fields = ['prospect__company_name', 'content']


@admin.register(ProspectMessage)
class ProspectMessageAdmin(admin.ModelAdmin):
    list_display = ['prospect', 'subject', 'status', 'sent_at', 'created_at']
    list_filter = ['status']
    search_fields = ['prospect__company_name', 'subject']
