from django.contrib import admin
#always import include 
from django.urls import path, include 
from django.conf import settings 
from django.conf.urls.static import static 



urlpatterns = [
    path('admin/', admin.site.urls),
    # the include function literally connects the urls from the app level to the urls on the project level 
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)