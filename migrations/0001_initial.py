# Generated by Django 3.0.4 on 2020-03-31 02:39

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoundaryCenter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('center', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('center', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('center', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='regions', to='morocco_mapping.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Wilaya',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('osm_id', models.BigIntegerField()),
                ('wilaya_type', models.PositiveSmallIntegerField(choices=[(1, 'Prefecture'), (2, 'Province')], default=2)),
                ('center', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Wilayas', to='morocco_mapping.Region')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subregion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField()),
                ('shape', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('subregion_type', models.PositiveSmallIntegerField(choices=[(1, 'Cercle'), (2, 'Pachalik')], default=2)),
                ('center', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='morocco_mapping.BoundaryCenter')),
                ('wilaya', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subregions', to='morocco_mapping.Wilaya')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('osm_id', models.BigIntegerField()),
                ('wikidata', models.CharField(max_length=50, null=True)),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('place_type', models.CharField(max_length=50)),
                ('commune', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='places', to='morocco_mapping.Commune')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='commune',
            name='subregion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='communes', to='morocco_mapping.Subregion'),
        ),
        migrations.CreateModel(
            name='AlternativeName',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lang', models.CharField(default='und', max_length=5)),
                ('name', models.CharField(max_length=255)),
                ('object_id', models.UUIDField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
