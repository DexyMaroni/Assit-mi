from django import forms

class ToDoForm(forms.Form):
    task = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your task',
            'class': 'form-control'
        })
    )
