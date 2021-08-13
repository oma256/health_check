from django import forms
from django.utils.translation import gettext_lazy as _

from apps.users.models import User, Patient


class UserForm(forms.ModelForm):
    new_password = forms.CharField(required=False, label=_('Новый пароль'))

    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        new_password = self.cleaned_data.get('new_password', None)
        if new_password:
            self.instance.set_password(new_password)
        return super(UserForm, self).save(commit)


class AdminPatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = '__all__'


class PatientPatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ('doctor',)
