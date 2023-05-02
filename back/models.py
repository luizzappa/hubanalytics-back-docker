import os
from django.db import models

class Painel(models.Model):

    class Meta:
        db_table = 'painel'

    titulo = models.TextField()
    url = models.TextField()
    visitas = models.IntegerField()
    likes = models.IntegerField()
    tags = models.TextField()
    descricao = models.TextField()
    isLiked = models.BooleanField()
    isFav = models.BooleanField()


class Images(models.Model):

    painel = models.ForeignKey(Painel, on_delete=models.CASCADE, related_name='painel_set')
    image = models.ImageField(upload_to='')


    class Meta:
        db_table = 'images'
