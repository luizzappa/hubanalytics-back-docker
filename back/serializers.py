from rest_framework import serializers
from .models import Painel, Images
import os


class PainelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['image']

    def to_representation(self, instance):
        return str(instance.image)


class PainelSerializer(serializers.ModelSerializer):
    images = PainelImageSerializer(many=True, read_only=True, source='painel_set')
    uploaded_images = serializers.ListField(child=serializers.FileField(allow_empty_file=False, use_url=False), write_only=True)


    class Meta:
        model = Painel
        depth = 1
        fields = ['id', 'titulo', 'url', 'visitas', 'likes', 'tags', 'descricao', 'isLiked', 'isFav', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        painel = Painel.objects.create(**validated_data)

        for image in uploaded_images:
            Images.objects.create(painel=painel, image=image)

        return painel

    def update(self, instance, validated_data):
        if not validated_data.get("uploaded_images") is None:
            uploaded_images = validated_data.pop("uploaded_images")

            # Deleta imagens atuais
            foundImgs = Images.objects.filter(painel=instance.id)
            for img in foundImgs:
                if os.path.isfile(img.image.path):
                    os.remove(img.image.path)
            foundImgs.delete()

            for image in uploaded_images:
                Images.objects.create(painel=instance, image=image)

        return super().update(instance=instance, validated_data=validated_data)


