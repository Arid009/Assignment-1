from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        print(instance,'this is instance from signals')
        activation_url = f'{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/'

        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!\nFrom Event Management'
        recipient_list = [instance.email]

        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,recipient_list)
        except Exception as e:
            print(f'Failed to send email to {instance.email}: {str(e)}')

@receiver(post_save, sender=User)
def assign_role(sender, instance, created, **kwargs):
    if created:
        particpant_group, created = Group.objects.get_or_create(name='Participant')
        instance.groups.add(particpant_group)
        instance.save()

