# forms.py
from django import forms

class NoteGenerationForm(forms.Form):
    prompt = forms.CharField(
        label="Enter a prompt for note generation",
        widget=forms.Textarea(attrs={"placeholder": "Type keywords or a brief description..."}),
        required=True,
    )
