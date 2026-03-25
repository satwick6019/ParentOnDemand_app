from django.urls import path
from .views import send_request, student_dashboard,parent_dashboard
from .views import create_parent_profile
from .views import accept_request,reject_request

urlpatterns = [
    path('student/',student_dashboard,name='student_dashboard'),
    path('parent/',parent_dashboard,name='parent_dashboard'),
    path('parent/create-profile/', create_parent_profile, name='create_parent_profile'),
    path('send-request/<int:parent_id>/', send_request,name='send_request'),
    path('accept/<int:request_id>/',accept_request,name='accept_request'),
    path('reject/<int:request_id>/',reject_request,name='reject_request')

]