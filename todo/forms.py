from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'category'] #only these fields will be there in the form.
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Task Title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Task Description', 'rows':2}),
            'due_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'priority': forms.Select(attrs={'class':'form-select'}),
            'category': forms.Select(attrs={'class':'form-select'}),
        }