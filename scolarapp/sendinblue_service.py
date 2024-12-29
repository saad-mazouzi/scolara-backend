import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse

def send_verification_email(user):
    # Générer un token JWT pour l'utilisateur
    token = RefreshToken.for_user(user).access_token
    # Construire le lien de vérification
    verification_url = f"{settings.FRONTEND_URL}/verify-email/?token={str(token)}"
    
    # Configurer le client Brevo
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Contenu de l'email
    subject = "Vérification de votre adresse email"
    html_content = f"""
    <p>Bonjour {user.get_full_name()},</p>
    <p>Merci de vous être inscrit. Veuillez vérifier votre adresse email en cliquant sur le lien ci-dessous :</p>
    <a href="{verification_url}">Vérifier mon email</a>
    """
    sender = {"name": "Scolara Support", "email": "saadmaazouzi580@gmail.com"}
    to = [{"email": user.email, "name": user.get_full_name()}]

    email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, html_content=html_content)

    try:
        api_instance.send_transac_email(email)
        print("Email de vérification envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")

def send_reset_password_email(user, token):
    reset_url = f"{settings.FRONTEND_URL}/reset-password/?token={token}"
    
    # Configuration de Brevo (Sendinblue)
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Contenu de l'email
    subject = "Réinitialisation de votre mot de passe"
    html_content = f"""
    <p>Bonjour {user.get_full_name()},</p>
    <p>Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien ci-dessous :</p>
    <a href="{reset_url}">Réinitialiser mon mot de passe</a>
    """
    sender = {"name": "Scolara Support", "email": "saadmaazouzi580@gmail.com"}
    to = [{"email": user.email, "name": user.get_full_name()}]

    email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, html_content=html_content)

    try:
        api_instance.send_transac_email(email)
        print("Email de réinitialisation envoyé avec succès")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email : {str(e)}")

def send_sms(user, phone_number, message):
    # Configuration de Brevo (Sendinblue) pour les SMS
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.SENDINBLUE_API_KEY
    api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))

    # Contenu du SMS
    sms_data = sib_api_v3_sdk.SendTransacSms(
        sender="Scolara",  # Nom d'expéditeur (max 11 caractères)
        recipient=phone_number,  # Numéro du destinataire au format international
        content=message  # Message à envoyer
    )

    try:
        api_instance.send_transac_sms(sms_data)
        print("SMS envoyé avec succès")
    except ApiException as e:
        print(f"Erreur lors de l'envoi du SMS : {str(e)}")