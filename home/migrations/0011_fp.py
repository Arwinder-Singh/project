# Generated by Django 4.2.1 on 2023-07-29 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_fpgrowth_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('support', models.FloatField()),
                ('itemsets', models.BinaryField()),
                ('key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recordKey', to='home.fprecord')),
            ],
        ),
    ]
