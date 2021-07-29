from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import AdvUser

from .apps import user_registered

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required=True, label='Адрес электронной почты')
	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')

class RegisterUserForm(forms.ModelForm):
	email = forms.EmailField(required=True, label='Адрес электронной почты')
	#password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validation_help_text_html())
	#password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text='puk')
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput,
      help_text=password_validation.password_validators_help_text_html())
	password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Введите еще раз тот же самый пароль для проверки')
	def clean(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False
		user.is_activated = False
		if commit:
			user.save()
		user_registered.send(RegisterUserForm, insrance=user)
		return user
	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')
		