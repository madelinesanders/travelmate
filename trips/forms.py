from django import forms
from .models import Trip, Activity

class TripForm(forms.ModelForm):
    location = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'activity-select'}),
        required=False,
        label="Planned Activities"
    )

    class Meta:
        model = Trip
        fields = ['location', 'start_date', 'end_date', 'activities']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
