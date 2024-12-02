from django import forms
from .models import StickyNote, Attachment

class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        fields = ['title', 'body', 'category']
        
    # Additional validation can be added here if needed



class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        
    # Additional validations to added here if required (e.g., file size, type)
