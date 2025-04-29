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

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("Start date must be before end date.")

        return cleaned_data