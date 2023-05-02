from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    url(r'^paineis/$', views.PainelList.as_view(), name='painel-list'),
    path('painel/<int:id>', views.PainelEdit.as_view(), name='painel-edit'),
    path('uniquetags/', views.UniqueTags.as_view(), name='unique-tags'),
]

# print(settings.MEDIA_URL, settings.MEDIA_ROOT, 'a')
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.MEDIA_URL)