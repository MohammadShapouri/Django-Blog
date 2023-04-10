import email
from operator import contains
import re
from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.core.validators import RegexValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.db.models import Q


customASCIIUsernameValidator = RegexValidator(regex=r"^[\w.]+\Z",
                                            message=("Enter a valid username. This value may contain only English letters, "
                                                    "numbers, and @/./+/-/_ characters."),
                                            flags=re.ASCII)

UserModel = get_user_model()

# class CustomASCIIUsernameValidator(RegexValidator):
#     regex=r"^[\w.]+\Z"
#     message=("Enter a valid username. This value may contain only English letters, "
#             "numbers, and @/./+/-/_ characters.")
#     flags = re.ASCII
# customASCIIUsernameValidator = CustomASCIIUsernameValidator()





class UserAccountForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(UserAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'unique' : "نام کاربری در حال استفاده است."}
        self.fields['email'].error_messages = {'unique' : " ایمیل در حال استفاده است."}
        self.fields['password1'].label = "رمز"
        self.fields['password2'].label = "تکرار رمز"
        self.fields['password1'].help_text = format_html("<ul>  <li>{}</li> <li>{}</li> <li>{}</li>  <ul>".format(
                                                            "دست کم ۸ کاراکتر داشته باشد.",
                                                            "شامل حروف باشد.",
                                                            "مشابه داده های دیگر نباشد."
                                                            )
                                                        )
        self.fields['password2'].help_text = format_html("<ul>  <li>{}</li>  <ul>".format(
                                                            "رمز را تکرار کنید."
                                                            )
                                                        )

    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email']



    def clean_username(self):
        cleaned_data = super(UserAccountForm, self).clean()
        username = cleaned_data.get('username')

        # CustomASCIIUsernameValidator = RegexValidator(regex=r"^[\w.]+\Z",
        #                                             message=("Enter a valid username. This value may contain only English letters, "
        #                                                     "numbers, and @/./+/-/_ characters."),
        #                                             flags=re.ASCII)
        # CustomASCIIUsernameValidator = ASCIIUsernameValidator()

        try:
            customASCIIUsernameValidator(username)
        except forms.ValidationError:
            raise forms.ValidationError([{'username' : "نام کاربری ساختار نامعتبری دارد."}])

        try:
            user = UserModel.objects.get(username__iexact = username)
        except UserModel.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "نام کاربری در حال استفاده است."}])



    def clean_email(self):
        cleaned_data = super(UserAccountForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = UserModel.objects.get(email__iexact = email)
        except UserModel.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : " ایمیل در حال استفاده است."}])





class EditUserAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(EditUserAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = {'unique' : "نام کاربری در حال استفاده است."}
        self.fields['email'].error_messages = {'unique' : " ایمیل در حال استفاده است."}


    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']




    def clean_username(self):
        cleaned_data = super(EditUserAccountForm, self).clean()
        username = cleaned_data.get('username')

        try:
            customASCIIUsernameValidator()
        except forms.ValidationError:
            raise forms.ValidationError([{'username' : "نام کاربری ساختار نامعتبری دارد."}])

        try:
            user = UserModel.objects.get(username__iexact = username)
        except UserModel.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "نام کاربری در حال استفاده است."}])




    def clean_email(self):
        cleaned_data = super(EditUserAccountForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = UserModel.objects.get(email__iexact = email)
        except UserModel.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : " ایمیل در حال استفاده است."}])




class LoginForm(forms.Form):
    # email field (field below this comment.) can also accepts username!!! clean_email will handle it.
    email_username = forms.CharField(required=True, label="ایمیل", error_messages={'required' : "پر کردن این بخش الزامی است."})
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز", error_messages={'password' : "رمز ساختار نادرستی دارد."})


    def clean_email_username(self):
        cleaned_data = super(LoginForm, self).clean()
        email_username = cleaned_data.get('email_username')

        if str(email_username).__contains__('@'):
            email = email_username
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError([{ 'email_username' : "ایمیل وارد شده ساختار نامعتبری دارد" }])
            return email
        else:
            username = email_username
            try:
                customASCIIUsernameValidator(username)
            except forms.ValidationError:
                raise forms.ValidationError([{'email_username' : "نام کاربری ساختار نامعتبری دارد."}])
            return username






class DeleteUserAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز", error_messages={'password' : "رمز ساختار نادرستی دارد."})





class PasswordResetForm(BasePasswordResetForm):
    # email field (field below this comment.) can also accepts username!!! clean_email will handle it.
    email = forms.CharField(max_length=254, label='ایمیل یا نام کاربری')


    def clean_email(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        email = cleaned_data.get('email')

        if str(email).__contains__('@'):
            try:
                validate_email(email)
            except forms.ValidationError:
                raise forms.ValidationError([{ 'email' : "ایمیل وارد شده ساختار نامعتبری دارد" }])
            return email
        else:
            username = email
            try:
                customASCIIUsernameValidator(username)
            except forms.ValidationError:
                raise forms.ValidationError([{'email' : "نام کاربری ساختار نامعتبری دارد."}])
            try:
                user = UserModel.objects.get(username = username)
            except UserModel.DoesNotExist:
                return email
            else:
                email = user.email
                return email



class EditEmailForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['new_email']


    def clean_new_email(self):
        cleaned_data = super(EditEmailForm, self).clean()
        new_email = cleaned_data.get('new_email')

        usersWithThisEmail = UserModel.objects.filter(Q(new_email__iexact = new_email) | Q(email__iexact = new_email)).count()

        if usersWithThisEmail != 0:
            raise forms.ValidationError([{'new_email' : " ایمیل در حال استفاده است."}])
        else:
            return new_email

        # if usersWithThisEmail == 0:
        #     return new_email
        # else:
        #     raise forms.ValidationError([{'new_email' : " ایمیل در حال استفاده است."}])


