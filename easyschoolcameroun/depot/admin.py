from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html

from .models import EpreuveSoumise, MouvementSolde
from .services import rejeter_epreuve, valider_epreuve


@admin.register(EpreuveSoumise)
class EpreuveSoumiseAdmin(admin.ModelAdmin):
    list_display = ("titre", "eleve", "niveau", "matiere", "etablissement", "annee_scolaire", "statut", "recompense", "date_envoi", "voir")
    list_filter = ("statut", "niveau", "type_evaluation", "annee_scolaire")
    search_fields = ("titre", "etablissement", "eleve__email", "eleve__last_name")
    readonly_fields = (
        "eleve", "fichier", "nom_original", "type_fichier", "taille", "nombre_pages", "empreinte_fichier",
        "empreinte_texte", "empreinte_visuelle", "cle_epreuve", "recompense", "adresse_ip", "date_envoi",
        "date_traitement", "statut", "voir",
    )
    actions = ["action_valider", "action_rejeter"]
    date_hierarchy = "date_envoi"

    def has_add_permission(self, request):
        return False  # les épreuves arrivent uniquement par le formulaire de dépôt

    def has_delete_permission(self, request, obj=None):
        return False  # un rejet reprend la récompense ; la suppression casserait le journal

    @admin.display(description="Fichier")
    def voir(self, obj):
        return format_html('<a href="{}" target="_blank" rel="noopener">Ouvrir</a>', reverse("depot:fichier", args=[obj.pk]))

    @admin.action(description="Valider les épreuves sélectionnées")
    def action_valider(self, request, queryset):
        for epreuve in queryset:
            valider_epreuve(epreuve)
        self.message_user(request, "Épreuves validées.", messages.SUCCESS)

    @admin.action(description="Rejeter (reprend les 25 F de récompense)")
    def action_rejeter(self, request, queryset):
        n = 0
        for epreuve in queryset.exclude(statut=EpreuveSoumise.Statut.REJETEE):
            rejeter_epreuve(epreuve, "Document non conforme")
            n += 1
        self.message_user(request, f"{n} épreuve(s) rejetée(s), récompenses reprises.", messages.WARNING)


@admin.register(MouvementSolde)
class MouvementSoldeAdmin(admin.ModelAdmin):
    list_display = ("eleve", "montant", "solde_apres", "motif", "date")
    search_fields = ("eleve__email", "motif")
    readonly_fields = [f.name for f in MouvementSolde._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
