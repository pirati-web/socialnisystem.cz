# Generated by Django 2.1.3 on 2018-11-24 14:10

import bitfield.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20181122_1549'),
    ]

    operations = [
        migrations.CreateModel(
            name='BenefitManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='BenefitRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flags', bitfield.models.BitField([('svobodny_rozvedeny_samozivitel', 'Jsem svobodný/rozvedený, samoživitel'), ('svobodna_rozvedena_samozivitelka', 'Jsem svobodná/rozvedená samoživitelka'), ('jsme_rodina', 'Jsme rodina'), ('cekam_dite', 'Čekám dítě'), ('mam_dite_do_4', 'Mám dítě do 4 let'), ('mam_dite_do_6', 'Mám dítě do 6 let'), ('mam_dite_do_18', 'Mám dítě do 18 let'), ('mam_studenta_do_26', 'Máme doma studenta do 26 let'), ('jsem_senior', 'Jsem senior'), ('jsem_vdova_vdovec', 'Jsem vdova/vdovec'), ('osamele_dite', 'Situace osamělého dítěte'), ('ohrozene_dite', 'Situace ohroženého dítěte'), ('jsem_pestoun', 'Jsem pěstoun'), ('jsem_nezamestnany', 'Jsem nezaměstnaný'), ('chybi_mi_penize', 'Chybí mi peníze na živobytí'), ('prijem_pod_hranici_minima', 'Příjem mojí domácnosti je nižší než 2,7 násobek životního minima'), ('nemam_na_najem', 'Nemám prostředky na placení nájmu'), ('nemam_na_kauci_na_najem', 'Nemám prostředky na kauci na nájem'), ('obtizna_zivotni_situace', 'Jsem v obtížné životní situaci'), ('jsem_nemocny', 'Jsem nemocný'), ('jsem_po_urazu', 'Jsem po úrazu'), ('zdravotni_hendikep', 'Mám zdravotní hendikep'), ('pecuji_o_nemocneho', 'Pečuji o blízkou osobu, která je nemocná'), ('pecuji_o_osobu_po_urazu', 'Pečuji o blízkou osobu, která je po úrazu'), ('pecuji_o_zdravotne_znevyhodneneho', 'Pečuji o blízkou osobu, která je zdravotně znevýhodněná'), ('umrti_v_rodince', 'V rodině došlo k úmrtí')], default=0, verbose_name='Požadavky')),
            ],
            options={
                'verbose_name': 'Požadavek na získání dávky',
                'verbose_name_plural': 'Požadavky na získání dávky',
            },
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='requirements',
        ),
        migrations.AddField(
            model_name='benefitrequirement',
            name='benefit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Benefit', verbose_name='Dávka'),
        ),
    ]
