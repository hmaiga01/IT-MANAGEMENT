from django import forms
from .models import Infrastructure, Machine
from django.contrib.auth.models import User
 
class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        exclude = ['infrastructure', 'modifie_par', 'date_de_creation', 'date_derniere_modification']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietaire': forms.Select(attrs={'class': 'form-control'}),
            'date_maintenance': forms.DateInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'caracteristiques': forms.Textarea(attrs={'class': 'form-control'}),
            
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class UserForm(forms.ModelForm):
    machine = forms.ModelChoiceField(required=False, queryset=Machine.objects.filter(est_assignee=False), widget=forms.Select(attrs={'class': 'form-control'}))

    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'machine']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
