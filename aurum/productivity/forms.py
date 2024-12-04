# forms.py
from django import forms
from .models import ToDo



class TextGenerationForm(forms.Form):
    prompt = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your prompt here...', 'rows': 5, 'cols': 40}),
        label="Prompt",
        required=True,
    )
    max_tokens = forms.IntegerField(
        initial=200,
        min_value=1,
        label="Max Tokens",
    )
    temperature = forms.FloatField(
        initial=0.7,
        min_value=0.0,
        max_value=2.0,
        label="Temperature",
        help_text="Set between 0 (deterministic) and 2 (highly creative)."
    )


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['task', 'completed']
        widgets = {
            'task': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a task'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }