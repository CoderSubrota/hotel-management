from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings 
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
import logging

User  = get_user_model()
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User )
def send_verification_email(sender, instance, created, **kwargs):
    # Check if the user was created and has an email
    if created and instance.email:
        # Generate a token for the user
        token = default_token_generator.make_token(instance)

        # Construct the activation URL
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{force_str(instance.id)}/{token}/"

        # Prepare the email subject and message
        subject = "Activate Your Account"
        message = (
            f"Hi {instance.username},\n\n"
            "Please activate your account by clicking the link below:\n"
            f"{activation_url}\n\n"
            "Thank you!"
        )
        recipient_list = [instance.email]

        try:
            # Send the email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False  # Set to True to suppress errors in development
            )
            logger.info(f"Verification email sent to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send email to {instance.email}: {str(e)}")