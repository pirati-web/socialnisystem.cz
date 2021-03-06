# Generated by Django 2.1.3 on 2019-02-20 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190120_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='related_law',
            field=models.TextField(blank=True, null=True, verbose_name='Související zákon(y)'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='responsible_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.StateOffice', verbose_name='Žádost se podává na'),
        ),
    ]
