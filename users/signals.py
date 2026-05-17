from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Role, User


@receiver(post_migrate)
def seed_roles_and_admin(sender, **kwargs):

    # SEED ROLES
    roles = [
        'Administrator',
        'Manager',
        'Staff',
        'Warehouse Staff',
        'Cashier'
    ]

    for role in roles:
        Role.objects.get_or_create(role_type=role)

    # CREATE DEFAULT ADMIN ACCOUNT
    if not User.objects.filter(username='admin').exists():

        admin_role = Role.objects.get(role_type='Administrator')

        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            first_name='System',
            middle_name='',
            last_name='Administrator',
            password='admin123',
            role=admin_role
        )

        print("Default admin account created.")