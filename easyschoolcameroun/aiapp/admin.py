from django.contrib import admin
from .models import AISettings, Conversation, AIMessage, AIModel, Pack

@admin.register(AISettings)
class AISettingsAdmin(admin.ModelAdmin):
    list_display = ('default_daily_credits', 'file_upload_cost', 'openai_api_key_status', 'gemini_api_key_status')
    
    def openai_api_key_status(self, obj):
        return "Configuré" if obj.openai_api_key else "Non configuré"
    openai_api_key_status.short_description = "Clé OpenAI"

    def gemini_api_key_status(self, obj):
        return "Configuré" if obj.gemini_api_key else "Non configuré"
    gemini_api_key_status.short_description = "Clé Gemini"

    def has_add_permission(self, request):
        # Allow adding if no settings exist yet
        return AISettings.objects.count() == 0
        
    def has_change_permission(self, request, obj=None):
        return True
        
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    search_fields = ('user__email', 'title')

@admin.register(AIMessage)
class AIMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'mode', 'created_at']
    list_filter = ['mode', 'created_at']
    search_fields = ['user__email', 'user_message', 'ai_response']

@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'provider', 'cost', 'is_active')
    list_filter = ('model_type', 'provider', 'is_active')
    search_fields = ('name', 'api_value')

@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'credit', 'popular')
    search_fields = ('name',)
