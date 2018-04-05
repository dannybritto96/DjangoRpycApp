from django import forms
from django.core import validators

# class IP_form(forms.Form):
#     ip_address = forms.CharField(max_length=20, label="")

class PingForm(forms.Form):
    ping_ip = forms.CharField(max_length=20,label="Ping IP")
    # myfile = forms.FileField(required=False,label="File to Upload")

    def clean_data(self):
        ip_address = self.cleaned_data['ip_address']
        operation = self.cleaned_data['operation']
        ping_ip = self.cleaned_data['ping_ip']
        text_area = self.cleaned_data['text_area']
        return ip_address, operation, ping_ip, text_area
