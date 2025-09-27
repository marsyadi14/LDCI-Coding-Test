from django import forms

from .models import User, Post

class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirmed_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = [
            "username", "email", "display_name", "password"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})
            
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirmed_password = cleaned_data.get("confirmed_password")

        if password != confirmed_password:
            raise forms.ValidationError(
                "Password and Confirm Password does not match"
            )

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control", "placeholder": field.label})
            
class PostForm(forms.ModelForm):
    post_content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), required=True)
    repost_val = forms.CharField(widget=forms.HiddenInput(), required=False)
    loc_lon = forms.FloatField(widget=forms.HiddenInput(), required=False)
    loc_lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["post_content"].widget.attrs.update({"placeholder": "What's happening?"})
    
    class Meta:
        model = Post
        fields = ["post_content", "loc_lon", "loc_lat"]