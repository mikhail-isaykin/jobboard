from .models import Complaint
from django import forms


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Опишите причину жалобы...',
                    'rows': 4      
                }
            )
        }
        labels = {
            'reason': 'Причина жалобы'
        }
        help_texts = {
            'reason': 'Укажите, что именно нарушает данная вакансия.'
            }
