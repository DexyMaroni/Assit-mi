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






from django import forms
from .models import LectureNote, LectureAttachment

class LectureNoteForm(forms.ModelForm):
    class Meta:
        model = LectureNote
        fields = ['title', 'course', 'subject', 'instructor_name', 'content']
        
class LectureAttachmentForm(forms.ModelForm):
    class Meta:
        model = LectureAttachment
        fields = ['file']

def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False

