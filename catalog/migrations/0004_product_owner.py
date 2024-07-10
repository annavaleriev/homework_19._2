# Generated by Django 4.2.2 on 2024-07-10 09:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0003_alter_version_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="owner",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец",
            ),
            preserve_default=False,
        ),
    ]
