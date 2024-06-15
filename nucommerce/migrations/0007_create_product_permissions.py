# Generated by Django 5.0.6 on 2024-06-15 15:58

from django.db import migrations
from django.contrib.auth.models import Group, Permission

class Migration(migrations.Migration):

    def apply_migration(apps, schema_editor):
        admin_group = Group.objects.get(name='admin')

        all_product_permissions = Permission.objects.filter(content_type__app_label='nucommerce',
                                                            content_type__model='product')
        for permission in all_product_permissions:
            admin_group.permissions.add(permission)

    def revert_migration(apps, schema_editor):
        admin_group = Group.objects.get(name='admin')

        all_product_permissions = Permission.objects.filter(content_type__app_label='nucommerce',
                                                             content_type__model='product')
        for permission in all_product_permissions:
            admin_group.permissions.remove(permission)
        pass

    dependencies = [
        ('nucommerce', '0006_product_category'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
