from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from authapp.models import BlogUser


class BlogUserLoginForm(AuthenticationForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogUserRegisterForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'about_me', 'gender', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(BlogUserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class BlogUserEditForm(UserChangeForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'email', 'first_name', 'age', 'avatar', 'about_me', 'gender', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = forms.HiddenInput()


class BannedForm(forms.Form):
    banned_time = forms.IntegerField(min_value=1, required='True')
