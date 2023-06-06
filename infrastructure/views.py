from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Infrastructure, Machine
from .forms import MachineForm, UserForm
from django.contrib import messages
from django.views import View

from django.contrib.auth import get_user_model

User = get_user_model()

from django.contrib.auth.hashers import make_password
from .forms import UserForm

def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = request.POST.get('password')
            hashed_password = make_password(password)
            user.password = hashed_password
            machine_id = request.POST.get('machine')
            user.save()
            if machine_id:
                machine = Machine.objects.get(id=machine_id)
                machine.proprietaire = user
                machine.est_assignee = True
                machine.save()
            
            messages.success(request, "Utilisateur créé avec succès")
            return redirect('administration')
    else:
        user_form = UserForm()
    return render(request, 'create_user.html', {'form': user_form})

def homepage(request):
    """ page d'acceuil """
    return render(request, 'home.html')

@login_required 
def personnel(request):
    machines = Machine.objects.filter(proprietaire=request.user)
    admin = False
    if machines:
        machine = machines.first()
        return render(request, 'personel.html', {"machine": machine, 'admin': admin})
    return render(request, 'personel.html', {'admin': admin})


@login_required 
def administration(request):
    user = request.user
    infras= Infrastructure.objects.filter(responsable=user)
    admin=True
    if infras:
        infra = infras.first()
        machines = Machine.objects.filter(infrastructure=infra)    
        return render(request, 'administration.html', {'machines': machines, 'admin': admin})
    return render(request, 'administration.html', {'admin': admin})


class Utilisateur(LoginRequiredMixin, View):
    template_name = 'infrastructure/liste_users.html'
    
    def get(self, request):
        user = request.user
        infras= Infrastructure.objects.filter(responsable=user)
        if infras:
            infra = infras.first()
            machines = Machine.objects.filter(infrastructure=infra)
            personnels = User.objects.filter(id__in=[machine.proprietaire.id for machine in machines])
            return render(request, self.template_name, {'personnels':personnels})
        return render(request, self.template_name)



@login_required
def machine_create(request):
    """
    Permet à l'utilisateur connecté de créer une nouvelle machine
    """
    user = request.user
    
    infrastructure =  Infrastructure.objects.filter(responsable=user)
    
    if infrastructure:
    
        
        infrastructure = infrastructure.first()

        if request.method == 'POST':
            form = MachineForm(request.POST, request.FILES)
            if form.is_valid():
                machine = form.save(commit=False)
                machine.infrastructure = infrastructure
                machine.save()
                messages.success(request, 'Machine creee avec success.')
                return redirect('administration')
        else:
            form = MachineForm()

        context = {
            'form': form,
        }
    else:
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette d'action.")    
        

    return render(request, 'infrastructure/machine_create.html', context)

@login_required
def machine_update(request, machine_id):
    """
    Permet à l'utilisateur connecté de mettre à jour une machine existante
    """
    user = request.user
    infrastructure = Infrastructure.objects.filter(responsable=user).first()

    if infrastructure:
        machine = Machine.objects.get(id=machine_id)

        if request.method == 'POST':
            form = MachineForm(request.POST, request.FILES, instance=machine)
            if form.is_valid():
                machine = form.save(commit=False)
                machine.modifie_par = user  # Ajout du champ "modified_by"
                machine.save()
                return redirect('administration')
        else:
            form = MachineForm(instance=machine)

        context = {
            'form': form,
        }
    else:
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette action.")
        return redirect('dashboard')

    return render(request, 'infrastructure/machine_update.html', context)


@login_required
def machine_delete(request, machine_id):
    """
    Permet à l'utilisateur connecté de supprimer une machine existante
    """
    machine = Machine.objects.get(id=machine_id)
    if machine.infrastructure.responsable == request.user:
        machine.delete()
        messages.success(request, f"{machine.name} a ete supprimee avec success ")
    else:
        messages.error(request, "Vous n'avez pas la permission d'effectuer cette action. ")    
    return redirect('dashboard')

@login_required
def machine_detail(request, machine_id):
    machine = Machine.objects.get(id=machine_id)
    return render(request, 'infrastructure/machine_detail.html', {'machine':machine})