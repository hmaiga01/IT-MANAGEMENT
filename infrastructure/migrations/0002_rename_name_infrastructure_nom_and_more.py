# Generated by Django 4.2.1 on 2023-06-03 00:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('infrastructure', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infrastructure',
            old_name='name',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='infrastructure',
            old_name='responsible',
            new_name='responsable',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='characteristics',
            new_name='caracteristiques',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='created_at',
            new_name='date_de_creation',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='last_update',
            new_name='date_maintenance',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='is_asigned',
            new_name='est_assignee',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='modified_by',
            new_name='modifie_par',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='name',
            new_name='nom',
        ),
        migrations.RenameField(
            model_name='machine',
            old_name='status',
            new_name='statut',
        ),
        migrations.RenameField(
            model_name='update',
            old_name='date_updated',
            new_name='date_modification',
        ),
        migrations.RenameField(
            model_name='update',
            old_name='updated_by',
            new_name='modifie_par',
        ),
        migrations.RemoveField(
            model_name='machine',
            name='owner',
        ),
        migrations.AddField(
            model_name='machine',
            name='date_derniere_modification',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='machine',
            name='proprietaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='machines_proprietaire', to=settings.AUTH_USER_MODEL),
        ),
    ]
