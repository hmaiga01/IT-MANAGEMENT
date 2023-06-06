from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from infrastructure.models import Infrastructure


def user_login(request):
    """ Vue d'authentification des utilisateurs """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(username, password, 'login')
            login(request, user)
            # Connexion réussie, rediriger l'utilisateur vers une page spécifique
            if Infrastructure.objects.filter(responsable=user).exists():
                return redirect('administration')
            return redirect('personnel')
        else:
            # Identifiants invalides, afficher un message d'erreur
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
    # Afficher le formulaire de connexion
    return render(request, 'login.html')



def user_logout(request):
    """ Vue de deconnection """
    logout(request)
    # Déconnexion réussie, rediriger l'utilisateur vers une page spécifique
    return redirect('login')
