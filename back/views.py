from rest_framework import generics, filters, viewsets, mixins
from .models import Painel
from .serializers import PainelSerializer, ExtractKeywordsSerializer
from django.http import JsonResponse
from django.views import View
import requests
import json
from django.conf import settings

filters.OrderingFilter

class FilterPainelBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        offset = request.query_params.get('offset') or 0
        chunk = request.query_params.get('chunk') or 20
        filtered_queryset = queryset.order_by('id').filter(id__gte=str(offset))

        isFav = request.query_params.get('isFav')
        if (isFav):
            isFav = True if isFav == 'true' else False
            filtered_queryset = filtered_queryset.filter(isFav=isFav)

        tags = request.query_params.get('tags')
        if (tags):
            tagsToFilter = tags.split(';')
            findIds = []
            for item in filtered_queryset:
                for tag in tagsToFilter:
                    if tag.lower() in (t.lower() for t in item.tags.split(';')):
                        findIds.append(item.id)
            filtered_queryset = filtered_queryset.filter(id__in=findIds)

        return filtered_queryset[:int(chunk)]

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "offset",
                "in": "query",
                "required": False,
                "description": "A partir de qual ID sequencial retornar. Default: 0",
                "schema": {"type": "int"}
            },
            {
                "name": "chunk",
                "in": "query",
                "required": False,
                "description": "Quantidade de itens a serem retornados. Default: 20",
                "schema": {"type": "int"}
            },
            {
                "name": "isFav",
                "in": "query",
                "required": False,
                "description": "Retorna apenas items favoritados.",
                "schema": {"type": "boolean"}
            },
            {
                "name": "tags",
                "in": "query",
                "required": False,
                "description": "Retorna apenas items que contém uma das tags. Para mais de uma tag utilizar ponto e vírgula (;).",
                "schema": {"type": "string"}
            },
        ]


class PainelList(generics.ListCreateAPIView):

    queryset = Painel.objects.all()
    serializer_class = PainelSerializer 
    filter_backends = (filters.SearchFilter, FilterPainelBackend,)
    search_fields = ['titulo', 'url', 'tags', 'descricao']


class PainelEdit(generics.RetrieveUpdateDestroyAPIView):

    queryset = Painel.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = PainelSerializer 


class UniqueTags(generics.RetrieveAPIView):
    def get(self, *args, **kwargs):
        queryset = Painel.objects.all()
        tags = set(';'.join(set(item.tags for item in queryset)).split(';'))
        return JsonResponse(';'.join(tags), safe=False)


class ExtractKeywords(viewsets.GenericViewSet, mixins.CreateModelMixin):

    serializer_class = ExtractKeywordsSerializer

    def post(self, request):

        parsed_body = request.data['text']
        
        resp = requests.post(
            'http://api.textrazor.com/',
            headers={
                'x-textrazor-key': settings.API_KEY
            },
            data={
                "extractors": "entities,entailments",
                "text": parsed_body
            }
        )

        resp_json = json.loads(resp.content)
        entities = resp_json['response'].get('entities')

        if (not entities):
            return JsonResponse({'found': False})
        
        return JsonResponse({
            'found': True,
            'tags': [entitie['entityEnglishId'] for entitie in entities]
        })