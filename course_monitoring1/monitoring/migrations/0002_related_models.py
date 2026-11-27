import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [("monitoring", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='passport', to='monitoring.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='devices', to='monitoring.tag'),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(-80), django.core.validators.MaxValueValidator(150)])),
                ('measured_at', models.DateTimeField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='measurements', to='monitoring.device')),
            ],
            options={
                'ordering': ['-measured_at', '-pk'],
                'constraints': [models.CheckConstraint(condition=models.Q(('temperature__gte', -80), ('temperature__lte', 150)), name='temperature_in_range')],
            },
        ),
    ]
