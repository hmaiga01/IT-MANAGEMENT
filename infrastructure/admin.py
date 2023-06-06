from django.contrib import admin
from .models import Infrastructure, Machine, Update

admin.site.site_header = 'Management' # Modifier le nom affiché dans l'en-tête du site
admin.site.site_title = 'Management' # Modifier le titre de l'onglet du navigateur

@admin.register(Infrastructure)
class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('nom', 'responsable')
    search_fields = ('nom', 'responsable__username')  # Recherche par nom d'infrastructure et nom d'utilisateur du responsable

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('nom', 'proprietaire', 'infrastructure', 'date_maintenance', 'type', 'date_de_creation', 'modifie_par', 'statut')
    search_fields = ('nom', 'proprietaire__username', 'infrastructure__nom')  # Recherche par nom de machine, nom d'utilisateur du propriétaire et nom d'infrastructure

@admin.register(Update)
class UpdateAdmin(admin.ModelAdmin):
    list_display = ('machine', 'modifie_par', 'date_modification')
    search_fields = ('machine__nom', 'modifie_par__username')  # Recherche par nom de machine et nom d'utilisateur ayant effectué la mise à jour
 