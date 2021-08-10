from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from core.Schema import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=Schema))),
    path('editorjs/', include('django_editorjs_fields.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)