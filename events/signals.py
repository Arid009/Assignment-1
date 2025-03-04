from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event
from django.contrib.auth.models import User
from django.conf import settings


@receiver(m2m_changed, sender=Event.participants.through)
def notify_participants_on_rsvp(sender, instance, action,pk_set, **kwargs):
    if action == 'post_add':
        
        for id in pk_set:
            user = User.objects.get(id=id)
            print(user)

            subject = 'Activate Your Account'
            message = f'Hi {user.first_name},\n\nYou have RSVP for this event: {instance.name} \n\nThank You!'
            recipient_list = [user.email]
            print(recipient_list)

            try:
                send_mail(subject, message,settings.EMAIL_HOST_USER, recipient_list)
            except Exception as e:
                print(f"Failed to send email to {user.email}: {str(e)}")