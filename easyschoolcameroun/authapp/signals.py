from allauth.account.signals import email_confirmed
from django.contrib import messages
from django.db import transaction
from django.dispatch import receiver

from .models import UserRegistration

BONUS_FCFA = 1000
BONUS_CREDITS_IA = 500


@receiver(email_confirmed)
def award_onboarding_bonus(request, email_address, **kwargs):
    """Offre le bonus de bienvenue UNE SEULE FOIS par compte.

    Avant : le bonus dépendait de is_first_login, si bien qu'un utilisateur
    pouvait le recevoir plusieurs fois en ajoutant puis confirmant d'autres
    adresses e-mail avant de terminer l'accueil.
    """
    with transaction.atomic():
        user = UserRegistration.objects.select_for_update().get(pk=email_address.user_id)
        if user.bonus_bienvenue_recu:
            return
        user.somme += BONUS_FCFA
        user.wallet_credits += BONUS_CREDITS_IA
        user.bonus_bienvenue_recu = True
        user.save(update_fields=["somme", "wallet_credits", "bonus_bienvenue_recu"])
    if request is not None:
        messages.success(
            request,
            f"Félicitations ! Vous avez reçu {BONUS_FCFA} FCFA et {BONUS_CREDITS_IA} crédits IA pour commencer.",
            fail_silently=True,
        )
