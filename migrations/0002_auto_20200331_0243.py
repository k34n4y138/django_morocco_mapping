# Generated by Django 3.0.4 on 2020-03-31 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('morocco_mapping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commune',
            name='center',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter'),
        ),
        migrations.AlterField(
            model_name='country',
            name='center',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter'),
        ),
        migrations.AlterField(
            model_name='region',
            name='center',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter'),
        ),
        migrations.AlterField(
            model_name='subregion',
            name='center',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter'),
        ),
        migrations.AlterField(
            model_name='wilaya',
            name='center',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter'),
        ),
    ]