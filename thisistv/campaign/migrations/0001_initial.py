# Generated by Django 3.2.18 on 2023-04-11 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('priority', models.IntegerField(default=5, max_length=1, verbose_name='Prioridade da Campanha')),
                ('regularity', models.CharField(choices=[('D', 'Diária'), ('S', 'Semanal'), ('M', 'Mensal')], default='D', max_length=1, verbose_name='Regularidade da Campanha')),
                ('initial_datetime', models.DateTimeField(verbose_name='Data e Hora Inicial')),
                ('final_datetime', models.DateTimeField(verbose_name='Data e Hora Final')),
                ('approval', models.IntegerField(blank=True, choices=[(2, 'Aprovado'), (1, 'Pendente'), (0, 'Rejeitado')], max_length=1, null=True, verbose_name='Aprovação da Campanha')),
                ('status', models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A', max_length=1, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='VisualContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('type_content', models.CharField(choices=[('IE', 'Imagem Estática'), ('ID', 'Imagem Dinâmica')], default='IE', max_length=2, verbose_name='Tipo de Conteúdo Visual')),
                ('content', models.FileField(upload_to='%Y/%m/%d')),
                ('status', models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A', max_length=1, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='ContentCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration_visibility', models.IntegerField()),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.campaign', verbose_name='')),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.visualcontent', verbose_name='')),
            ],
        ),
    ]
