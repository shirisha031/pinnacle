from django.urls import path
from . import views

urlpatterns = [
    path('admission/form/', views.admission_form, name='admission_form'),
    path('admission/degree/', views.degree_admission_form, name='degree_admission_form'),
     path('shortlisted/', views.shortlisted_students_view, name='shortlisted_students_view'),
    path('approve/<str:stream>/<int:student_id>/', views.approve_student, name='approve_student'),
     path('enquiry/', views.enquiry_form_view, name='enquiry_form'),
    path('shortlist/', views.shortlist_display, name='shortlist_display'),
    path('pu-fee/<int:shortlist_id>/', views.pu_fee_detail_form, name='pu_fee_detail_form'),
    path('degree-fee/<int:shortlist_id>/', views.degree_fee_detail_form, name='degree_fee_detail_form'),

    # path('fee/view/<int:fee_id>/', views.view_fee_detail, name='view_fee_detail'),

]
