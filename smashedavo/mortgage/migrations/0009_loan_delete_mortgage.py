# Generated by Django 4.2.13 on 2024-05-24 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mortgage', '0008_alter_blogpost_pub_date_alter_mortgage_amount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=200000)),
                ('deposit', models.FloatField(default=10000.0)),
                ('interest_rate', models.FloatField(default=5.0)),
                ('paid_principal', models.FloatField(default=0.0)),
                ('paid_interest', models.FloatField(default=0.0)),
                ('loan_type', models.CharField(choices=[('MTG', 'Mortgage'), ('HEQ', 'Home Equity'), ('CAR', 'Car'), ('PSL', 'Personal'), ('STD', 'Student'), ('OTH', 'Other')], default='MTG')),
                ('start_date', models.DateField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Mortgage',
        ),
    ]
