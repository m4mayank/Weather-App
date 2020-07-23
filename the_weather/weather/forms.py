from django import forms
from .models import City, Country, SelectedCity
from django.contrib.auth import get_user_model

class CityForm(forms.ModelForm):
    country = forms.ModelChoiceField(queryset=Country.objects.all())
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        print(self.request)
        super(CityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = SelectedCity
        fields = ['country','city']
    
    def clean(self):
        cleaned_data = super(CityForm, self).clean()
        city = cleaned_data.get('city')
        cities = SelectedCity.objects.prefetch_related('user').filter(user_id__exact = self.request.user.id)
        for c in cities:
            if city == c.city:
                raise forms.ValidationError(f'{city} is already added. Please select another city.')
        
            