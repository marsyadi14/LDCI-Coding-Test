import re
from django import forms

from .models import User, Post

class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput, label="Email", error_messages={
                "invalid": "Please provide a proper email format like user@example.com",
                "required": "Email is required",
            })
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirmed_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", error_messages={
                "required": "Please confirm the password",
            },)
    
    class Meta:
        model = User
        fields = [
            "username", "email", "display_name", "password"
        ]
        error_messages = {
            "username": {
                "required": "You must choose a username",
            },
            "display_name": {
                "required": "Display name is required",
            },
            "password": {
                "required": "Password is required",
            },
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})
            
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 3:
            raise forms.ValidationError("Username must be atleast 3 characters long")
        elif not re.match(r'^[a-zA-Z0-9._-]{3,32}$', username):
            raise forms.ValidationError("Please use acceptable character (A-Za-z0-9_-.)")
        elif User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Sorry, "{username}" already taken. Please try another one')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if not re.match(r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise forms.ValidationError("Please provide a proper email format like user@example.com")
        
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password and len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")
        return password
    
    def clean_confirmed_password(self):
        password = self.cleaned_data.get("password")
        confirmed_password = self.cleaned_data.get("confirmed_password")

        if password != confirmed_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match"
            )

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update({"autocomplete": "off"})
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})
    
            
class PostForm(forms.ModelForm):
    post_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=True)
    repost_val = forms.CharField(widget=forms.HiddenInput(), required=False)
    loc_lon = forms.FloatField(widget=forms.HiddenInput(), required=False)
    loc_lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["post_content"].widget.attrs.update({"class": "form-control", "placeholder": "What's happening?"})
    
    class Meta:
        model = Post
        fields = ["post_content", "loc_lon", "loc_lat"]