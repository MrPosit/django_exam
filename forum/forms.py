from django import forms
from .models import Thread, Message

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'content', 'category']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']