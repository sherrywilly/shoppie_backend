from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from core.webhooks import  RazorHookView

from core.Schema import Schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=Schema)),name="graph"),
    path('editorjs/', include('django_editorjs_fields.urls')),
    path('hook/api/payment/',RazorHookView.as_view(),name="razorpayhook")

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)