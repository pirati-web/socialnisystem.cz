# Generated by Django 2.1.3 on 2019-01-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20181127_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lifecondition',
            options={'ordering': ('ordering', 'title'), 'verbose_name': 'Źivotní situace', 'verbose_name_plural': 'Životní situace'},
        ),
        migrations.AddField(
            model_name='lifecondition',
            name='ordering',
            field=models.PositiveSmallIntegerField(default=1, help_text='Čím vyšší číslo, tím později ve výpisu.', verbose_name='Pořadí'),
        ),
    ]
