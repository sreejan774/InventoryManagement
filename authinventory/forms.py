from django import forms 

class LoginForm(forms.Form):
    username = forms.CharField(
                max_length=256 ,
                widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'User Name','id':'floatingInput'})
            ) 
    password = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'floatingPassword'})
            )

class SignUpForm(forms.Form):
    username = forms.CharField(
                max_length=256,
                widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'User Name','id':'floatingInput'})
            )
    password = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'floatingPassword'})
            )
    confirmPassword = forms.CharField(
                widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','id':'floatingConfirmPassword'})
            )