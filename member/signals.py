from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from .models import Member

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        try:
            # 소셜 계정 확인
            social_account = SocialAccount.objects.filter(user=instance).first()
            if social_account:
                # 이미 존재하는지 확인
                existing_member = Member.objects.filter(user=instance).exists()
                if not existing_member:
                    Member.objects.create(
                        user=instance,
                        member_id=instance.username,
                        name=instance.first_name or instance.username,
                        email=instance.email,
                        member_password=User.objects.make_random_password(),
                        phone_num='',
                        member_type='normal'
                    )
        except Exception as e:
            print(f"Error creating member profile: {e}")