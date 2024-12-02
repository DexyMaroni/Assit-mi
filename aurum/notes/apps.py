from django.apps import AppConfig


class NotesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notes'
    
    
class SpeechAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'speech_app'
