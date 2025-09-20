from django.contrib import admin
from django.urls import path
from core.views import (
    login_page, register_page, logout_view,
    employee_view, employer_view, create_job,
    apply_job, view_applicants,home_page
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_page, name='register_page'),
    path('employee/', employee_view, name='employee_page'),
    path('employer/', employer_view, name='employer_page'),
    path('create_job/', create_job, name='create_job'),
    path('', home_page, name='home_page'),
    
    path('job/<int:job_id>/applicants/', view_applicants, name='view_applicants'),
    path("apply/<int:job_id>/", apply_job, name="apply_job"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
