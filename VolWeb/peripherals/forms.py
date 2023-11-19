from django import forms
from .models import Peripheral

class PeripheralForm(forms.ModelForm):
    class Meta:
        model = Peripheral
        fields = ['name', 'description', 'os_version', 'source_system', 'bash_bunny_device', 'storage_device']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 500px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'os_version': forms.Select(attrs={'class': 'form-control'}),
            'source_system': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        bash_bunny_devices = kwargs.pop('bash_bunny_devices', [])
        storage_devices = kwargs.pop('storage_devices', [])
        super().__init__(*args, **kwargs)
        bash_bunny_device_choices = [(device, device) for device in bash_bunny_devices]
        storage_device_choices = [(device, device) for device in storage_devices]
        self.fields['bash_bunny_device'] = forms.ChoiceField(choices=bash_bunny_device_choices, widget=forms.RadioSelect)
        self.fields['storage_device'] = forms.ChoiceField(choices=storage_device_choices, widget=forms.RadioSelect)

    def clean_bash_bunny_device(self):
        data = self.cleaned_data['bash_bunny_device']
        return data.split(" : ")[-1] if " : " in data else data

    def clean_storage_device(self):
        data = self.cleaned_data['storage_device']
        return data.split(" : ")[-1] if " : " in data else data