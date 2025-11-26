# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='datasets/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CleaningJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('RUNNING', 'Running'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('logs', models.TextField(default='[]')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agent_core.dataset')),
            ],
        ),
        migrations.CreateModel(
            name='AnalysisReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_quality_score', models.FloatField(default=0.0)),
                ('final_quality_score', models.FloatField(default=0.0)),
                ('issues_found', models.JSONField(default=dict)),
                ('actions_taken', models.JSONField(default=list)),
                ('cleaned_file_path', models.CharField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='agent_core.cleaningjob')),
            ],
        ),
    ]
