from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile , ProjectPost , notify_user
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
User = get_user_model()

@receiver(post_save , sender = ProjectPost)
def create_notify(sender, instance, created, **kwargs):
    if created:
        notify_user.objects.create(notify_post = instance , user = instance.user , 
                                   text = 'a new post added by : ' + str(instance.user.username))
        

        async_to_sync(channel_layer.group_send)(
            'notify',     # Group name
            {
                'type': 'send_notification',    #function send notification in consumer.py
                 'notification': {      #the parameter in json.dumps
                    'message': f'New post added by : {instance.user.username}',
                    'post_id': instance.id,
                    'user': instance.user.id,
                    'footer': 'powered by zkzk',
                }
            },
        )

# @receiver(post_save , sender = ProjectPost)
# def save_notify(sender , instance , **kwargs):
#     instance.notify_user.save()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance , f_name = instance.first_name 
                               , l_name = instance.last_name , email = instance.email)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()