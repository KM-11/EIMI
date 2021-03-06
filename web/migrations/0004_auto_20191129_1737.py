# Generated by Django 2.2.7 on 2019-11-29 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20191129_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muestra',
            name='analisis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='muestra',
            name='architecture',
            field=models.CharField(default='arm_32', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='muestra',
            name='familia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='web.Familia'),
        ),
        migrations.AlterField(
            model_name='muestra',
            name='static_anal',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vmachine',
            name='instancePath',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
