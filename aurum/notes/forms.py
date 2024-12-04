from django import forms
from .models import StickyNote, Attachment, LectureNote, LectureAttachment
class StickyNoteForm(forms.ModelForm):
    class Meta:
        model = StickyNote
        fields = ['title', 'body', 'category']
        
    # Additional validation can be added here if needed



class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].required = False 


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

