# Generated by Django 2.1.3 on 2019-03-17 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_benefit_searchable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='benefit',
            options={'ordering': ('condition', 'ordering', 'name'), 'verbose_name': 'Dávka', 'verbose_name_plural': 'Dávky'},
        ),
        migrations.AddField(
            model_name='benefit',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=1, help_text='Čím vyšší číslo, tím později ve výpisu.', verbose_name='Pořadí'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Název'),
        ),
        migrations.AlterField(
            model_name='lifecondition',
            name='ordering',
            field=models.PositiveSmallIntegerField(db_index=True, default=1, help_text='Čím vyšší číslo, tím později ve výpisu.', verbose_name='Pořadí'),
        ),
        migrations.AlterField(
            model_name='lifecondition',
            name='title',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Název'),
        ),
    ]
