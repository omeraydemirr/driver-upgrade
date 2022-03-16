    
#################################################################################
############################################################################################################
###################### CREATED BY OMER AYDEMIR https://github.com/omeraydemirr #############################
############################################################################################################
#################################################################################


from django import forms
from firmware.models import *

class FirmwareForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super (FirmwareForm, self).__init__ (*args, **kwargs)
        self.fields['vendor'] = forms.CharField(label = 'Add New Vendor',widget=forms.TextInput(attrs={'placeholder': 'Vendor'}),max_length=17)
        self.fields['device'] = forms.CharField(label = 'Add New Device',widget=forms.TextInput(attrs={'placeholder': 'Device'}))
        self.fields['model'] = forms.CharField(label = 'Add New Model',widget=forms.TextInput(attrs={'placeholder': 'Model'}))
        self.fields['series'] = forms.CharField(label = 'Add New Series',widget=forms.TextInput(attrs={'placeholder': 'Series'}))
        self.fields['operating_system'] = forms.CharField(label = 'Add New OS',widget=forms.TextInput(attrs={'placeholder': 'System'}))


    class Meta:
        model = Firmware

        fields =('vendor','device','model', 'series','operating_system','file')




