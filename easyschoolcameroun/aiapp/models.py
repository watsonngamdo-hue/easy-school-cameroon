from django.db import models
from django.conf import settings
import uuid

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=200, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.email})"

class AIMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_messages')
    user_message = models.TextField()
    ai_response = models.TextField(blank=True, null=True)
    mode = models.CharField(max_length=10, default='chat', choices=[('chat', 'Chat'), ('image', 'Image')])
    image = models.ImageField(upload_to='ai_images/', blank=True, null=True)
    file = models.FileField(upload_to='ai_files/', blank=True, null=True)
    file_type = models.CharField(max_length=100, blank=True, null=True)  # Store content type
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Chat by {self.user.email} at {self.created_at}"

class AISettings(models.Model):
    default_daily_credits = models.IntegerField(default=100, verbose_name="Crédits journaliers par défaut")
    file_upload_cost = models.IntegerField(default=20, verbose_name="Coût par upload de fichier")
    
    openai_api_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="Clé API OpenAI")
    gemini_api_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="Clé API Gemini")
    
    class Meta:
        verbose_name = "Paramètres IA"
        verbose_name_plural = "Paramètres IA"


    def __str__(self):
        return "Paramètres IA Globaux"

class AIModel(models.Model):
    PROVIDER_CHOICES = [
        ('openai', 'OpenAI'),
        ('deepseek', 'DeepSeek'),
        ('gemini', 'Google Gemini'),
    ]
    TYPE_CHOICES = [
        ('chat', 'Chat'),
        ('image', 'Image Generation'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom affiché")
    api_value = models.CharField(max_length=100, verbose_name="Valeur API (ID Modèle)")
    model_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='chat')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='openai')
    cost = models.IntegerField(default=10, verbose_name="Coût en crédits")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    def __str__(self):
        return f"{self.name} ({self.get_provider_display()}) - {self.cost} Cr"

class Pack(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    credit = models.IntegerField()
    icon = models.CharField(max_length=50, default='bolt')
    popular = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.credit} Credits - {self.price} FCFA)"
