from django.db import models

# Create your models here.

TYPE_CONTENT_CHOICES = (
    ('IE', 'Imagem Estática'),
    ('ID', 'Imagem Dinâmica'),
)

ACTIVE_INACTIVE_CHOICES = (
    ('A', 'Ativo'),
    ('I', 'Inativo'),
)

REGULARITY_CAMPAIGN = (
    ('D', 'Diária'),
    ('S', 'Semanal'),
    ('M', 'Mensal'),
)

APPROVAL_CHOICES = (
    (2, 'Aprovado'),
    (1, 'Pendente'),
    (0, 'Rejeitado'),
)


class VisualContent(models.Model):
    name = models.CharField("Nome", max_length=255)
    type_content = models.CharField("Tipo de Conteúdo Visual", max_length=2,
                             choices=TYPE_CONTENT_CHOICES, default='IE')
    content = models.FileField(upload_to="%Y/%m/%d")
    status = models.CharField("Status", max_length=1,
                             choices=ACTIVE_INACTIVE_CHOICES, default='A')

    def __str__(self):
        return self.name


class Campaign(models.Model):
    name = models.CharField("Nome", max_length=255)
    priority = models.IntegerField("Prioridade da Campanha", max_length=1, default=5)
    regularity = models.CharField("Regularidade da Campanha", max_length=1,
                             choices=REGULARITY_CAMPAIGN, default='D')
    initial_datetime = models.DateTimeField("Data e Hora Inicial", auto_now=False, auto_now_add=False)
    final_datetime = models.DateTimeField("Data e Hora Final", auto_now=False, auto_now_add=False)
    approval = models.IntegerField("Aprovação da Campanha", max_length=1, choices=APPROVAL_CHOICES, default=1)
    status = models.CharField("Status", max_length=1,
                             choices=ACTIVE_INACTIVE_CHOICES, default='A')
    justify = models.CharField("Justificativa campanha", max_length=255, null=True, blank=True)


class ContentCampaign(models.Model):
    campaign = models.ForeignKey(
        Campaign, on_delete=models.CASCADE, verbose_name="")
    content = models.ForeignKey(
        VisualContent, on_delete=models.CASCADE, verbose_name="")
    duration_visibility = models.IntegerField()
