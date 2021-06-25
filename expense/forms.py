from django import forms
from account.models import UserRole
from .models import UserExpense
from account.models import User, Profile


class UserRoleCreationForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ('role', 'user2')


class AddExpenseForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))

    class Meta:
        model = UserExpense
        fields = ('items', 'cost', 'category', 'description')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)


class EditUserForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(EditUserForm, self).__init__(*args, **kwargs)
    #
    #     # for example change class for integerPolje1
    #     # self.fields['integerPolje1'].widget.attrs['class'] = 'SOMECLASS'
    #
    #     # you can iterate all fields here
    #     for fname, f in self.fields.items():
    #         f.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('email', 'username', 'role', 'first_name', 'last_name', 'is_superuser', 'is_admin')







