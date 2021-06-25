from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from account.models import User, Role, UserRole, Family, Profile


# in admin panel creating user
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        # check that the two passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords didn't match")
        return password2

    def save(self, commit=True):
        # save the password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# in admin panel updating user
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_superuser')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    # the created forms to create and change the user
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'family', 'is_superuser', 'id')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        ('Personal info', {'fields': ('first_name', "last_name", 'family')}),
        ('Permissions', {'fields': ('is_superuser', 'is_admin', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'family', 'password1', 'password2', 'role')
        }),
    )
    search_fields = ('first_name', 'last_name', 'email',)
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('last_name', )
    filter_horizontal = ()


admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Family)
admin.site.register(Profile)
