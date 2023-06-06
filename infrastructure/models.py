from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()
    
    

class Infrastructure(models.Model):
    nom = models.CharField(max_length=100)  # Nom de l'infrastructure
    responsable = models.OneToOneField(User, on_delete=models.CASCADE, related_name='respo')  # Responsable de l'infrastructure (relation OneToOne avec le modèle User)

    def __str__(self):
        return self.nom

class Machine(models.Model):
    STATUS_CHOICES = (
        ('defaillant', 'Défaillance'),
        ('bien_portant', 'Fonctionnel'),
        ('en_maintenance', 'En maintenance'),
    )

    TYPE_MACHINE_CHOICES = (
        ('pc_windows', 'PC Windows'),
        ('pc_linux', 'PC Linux'),
        ('desktop_windows', 'Ordinateur de bureau Windows'),
        ('desktop_linux', 'Ordinateur de bureau Linux'),
        ('routeur', 'Routeur'),
        ('serveur', 'Serveur'),
        ('unite_centrale', 'Unité centrale'),
    )

    nom = models.CharField(max_length=100)  # Nom de la machine
    proprietaire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='machines_proprietaire', null=True)  # Propriétaire de la machine (relation OneToOne avec le modèle User)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)  # Infrastructure à laquelle la machine appartient (relation ForeignKey avec le modèle Infrastructure)
    date_maintenance = models.DateTimeField(null=True, blank=True)  # Date de la dernière maintenance de la machine (peut être nulle ou vide)
    date_de_creation = models.DateTimeField(auto_now_add=True)
    date_derniere_modification = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=15, choices=STATUS_CHOICES, default='bien_portant')  # Statut de la machine
    type = models.CharField(max_length=15, choices=TYPE_MACHINE_CHOICES, default='pc_windows')  # type de la machine
    image = models.ImageField(upload_to='machine_images/', blank=True, null=True)  # Image de la machine
    caracteristiques = models.TextField(blank=True, null=True)  # Caractéristiques de la machine
    est_assignee = models.BooleanField(default=True)  # Indique si la machine est assignée ou non à cet utilisateur
    modifie_par = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nom
    
    def get_image_url(self):
        if self.image:
            return self.image.url 
        return 


class Update(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)  # Machine concernée par la mise à jour (relation ForeignKey avec le modèle Machine)
    modifie_par = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upates_users')  # Utilisateur ayant effectué la mise à jour (relation ForeignKey avec le modèle User)
    date_modification = models.DateTimeField(auto_now_add=True)  # Date de la mise à jour (définie automatiquement lors de la création de l'objet)

    def __str__(self):
        return f"Mise a jour de {self.machine.nom} par {self.modifie_par} a {self.date_modification}"




@receiver(post_save, sender=Machine)
def create_machine_update(sender, instance, created, **kwargs):
    """
    Crée une nouvelle entrée dans la table Update lorsque la machine est modifiée.
    """
    if not created:
        Update.objects.create(
            machine=instance,
            modifie_par=instance.modifie_par,
            date_modification=timezone.now()
        )

