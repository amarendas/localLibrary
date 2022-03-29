
import datetime
from django import forms

class RenewBookForm(forms.Form):
    renewal_Date=forms.DateField(help_text='Enter new date (Default 3 weeks)')
    
    
    def clean_renewal_Date(self):
        data=self.cleaned_data['renewal_Date']
        if data<datetime.date.today():
            raise forms.ValidationError('Invalid date- date in the past')
        if data> (datetime.date.today()+datetime.timedelta(weeks=4)):
            raise forms.ValidationError('Invalid date -> Date more than 4 weeks')
        return data