


from django.shortcuts import render, redirect
from .forms import PUAdmissionForm, DegreeAdmissionForm
from .models import PUAdmission, DegreeAdmission, Enquiry


# ---------- PU Admission Form View ----------
def admission_form(request):
    success = False

    if request.method == 'POST':
        form = PUAdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission_no = form.cleaned_data.get('admission_no')
            sslc_percentage = form.cleaned_data.get('sslc_percentage')
            quota_type = form.cleaned_data.get('quota_type')
            student_name = form.cleaned_data.get('student_name')

            # Auto-generate admission_no
            if not admission_no:
                last_admission = PUAdmission.objects.order_by('id').last()
                if last_admission and last_admission.admission_no.startswith("PUA-"):
                    try:
                        last_number = int(last_admission.admission_no.split('-')[1])
                    except (IndexError, ValueError):
                        last_number = 0
                    admission_no = f"PUA-{last_number + 1:02d}"
                else:
                    admission_no = "PUA-01"

            # Fetch enquiry_no by student name
            enquiry_obj = Enquiry.objects.filter(student_name=student_name).first()
            enquiry_no = enquiry_obj.enquiry_no if enquiry_obj else 'None'

            # ATS Screening Logic
            if quota_type == 'Regular':
                application_status = 'Shortlisted' if sslc_percentage >= 60 else 'Rejected'
            elif quota_type == 'Management':
                application_status = 'Shortlisted Management' if sslc_percentage >= 60 else 'Rejected'
            else:
                application_status = 'Pending'

            # Save form data
            pu_admission = form.save(commit=False)
            pu_admission.admission_no = admission_no
            pu_admission.application_status = application_status
            pu_admission.enquiry_no = enquiry_no
            pu_admission.save()

            success = True
            form = PUAdmissionForm()
        else:
            print("Form Errors:", form.errors)
    else:
        form = PUAdmissionForm()

    return render(request, 'admission/admission_form.html', {
        'form': form,
        'success': success
    })


# ---------- Degree Admission Form View ----------
def degree_admission_form(request):
    form_submission_success = False

    if request.method == 'POST':
        form = DegreeAdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission_no = form.cleaned_data.get('admission_no')
            pu_percentage = form.cleaned_data.get('pu_percentage')
            quota_type = form.cleaned_data.get('quota_type')
            student_name = form.cleaned_data.get('student_name')

            # Auto-generate admission_no
            if not admission_no:
                last_admission = DegreeAdmission.objects.order_by('id').last()
                if last_admission and last_admission.admission_no.startswith("PEA-"):
                    try:
                        last_number = int(last_admission.admission_no.split('-')[1])
                    except (IndexError, ValueError):
                        last_number = 0
                    admission_no = f"PEA-{last_number + 1:02d}"
                else:
                    admission_no = "PEA-01"

            # Fetch enquiry_no by student name (if exists)
            enquiry_obj = Enquiry.objects.filter(student_name=student_name).first()
            enquiry_no = enquiry_obj.enquiry_no if enquiry_obj else 'None'

            # ATS Screening Logic
            if quota_type == 'Regular':
                application_status = 'Shortlisted' if pu_percentage >= 60 else 'Rejected'
            elif quota_type == 'Management':
                application_status = 'Shortlisted Management' if pu_percentage >= 60 else 'Rejected'
            else:
                application_status = 'Pending'

            # Save the form data
            degree_admission = form.save(commit=False)
            degree_admission.admission_no = admission_no
            degree_admission.application_status = application_status
            degree_admission.enquiry_no = enquiry_no
            degree_admission.save()

            form_submission_success = True
            form = DegreeAdmissionForm()
        else:
            print("Form Errors:", form.errors)
    else:
        form = DegreeAdmissionForm()

    return render(request, 'admission/degree_admission_form.html', {
        'form': form,
        'form_submission_success': form_submission_success,
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PUAdmission, DegreeAdmission, PUAdmissionshortlist, DegreeAdmissionshortlist
import json


def shortlisted_students_view(request):
    stream = request.GET.get('stream', 'PU')

    if stream == 'PU':
        students = PUAdmission.objects.filter(
            Q(application_status__iexact='Shortlisted') |
            Q(application_status__iexact='Shortlisted Management') |
            Q(application_status__iexact='Shortlisted for Management')
        )
        approved_ids = list(
            PUAdmissionshortlist.objects.filter(admin_approved=True).values_list('admission_no', flat=True)
        )
        not_approved_ids = list(
            PUAdmissionshortlist.objects.filter(admin_approved=False).values_list('admission_no', flat=True)
        )

    elif stream == 'Degree':
        students = DegreeAdmission.objects.filter(
            Q(application_status__iexact='Shortlisted') |
            Q(application_status__iexact='Shortlisted Management') |
            Q(application_status__iexact='Shortlisted for Management')
        )
        approved_ids = list(
            DegreeAdmissionshortlist.objects.filter(admin_approved=True).values_list('admission_no', flat=True)
        )
        not_approved_ids = list(
            DegreeAdmissionshortlist.objects.filter(admin_approved=False).values_list('admission_no', flat=True)
        )

    else:
        students = []
        approved_ids = []
        not_approved_ids = []

    context = {
        'stream': stream,
        'students': students,
        'approved_ids': approved_ids,
        'not_approved_ids': not_approved_ids,
    }
    return render(request, 'admission/shortlisted_students.html', context)


@csrf_exempt
def approve_student(request, stream, student_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            approved = bool(int(data.get('approved', 0)))

            if stream == 'PU':
                student = get_object_or_404(PUAdmission, id=student_id)
                shortlist, created = PUAdmissionshortlist.objects.get_or_create(
                    admission_no=student.admission_no,
                    defaults={'quota_type': student.quota_type,
                              'student_name': student.student_name  # Add this
                              }

                )
                shortlist.admin_approved = approved
                shortlist.save()

            elif stream == 'Degree':
                student = get_object_or_404(DegreeAdmission, id=student_id)
                shortlist, created = DegreeAdmissionshortlist.objects.get_or_create(
                    admission_no=student.admission_no,
                    defaults={'quota_type': student.quota_type,
                              'student_name': student.student_name  # Add this
                              }
                )
                shortlist.admin_approved = approved
                shortlist.save()

            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid stream'}, status=400)

            return JsonResponse({'status': 'success', 'approved': shortlist.admin_approved})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


from django.shortcuts import render, redirect
from .forms import EnquiryForm
from .models import Enquiry

from .models import Enquiry
from .forms import EnquiryForm

def enquiry_form_view(request):
    success = False

    if request.method == 'POST':
        # Fetch the latest enquiry again at the time of POST
        last_enquiry = Enquiry.objects.order_by('id').last()
        if last_enquiry and last_enquiry.enquiry_no and last_enquiry.enquiry_no.startswith("ENQ-"):
            try:
                last_number = int(last_enquiry.enquiry_no.split('-')[1])
            except (IndexError, ValueError):
                last_number = 0
            next_enquiry_no = f"ENQ-{last_number + 1:03d}"
        else:
            next_enquiry_no = "ENQ-001"

        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.enquiry_no = next_enquiry_no
            enquiry.save()
            success = True

            # Now prepare next enquiry no for fresh form
            next_number = int(next_enquiry_no.split('-')[1]) + 1
            next_enquiry_no = f"ENQ-{next_number:03d}"
            form = EnquiryForm(initial={'enquiry_no': next_enquiry_no})
    else:
        # For GET method only
        last_enquiry = Enquiry.objects.order_by('id').last()
        if last_enquiry and last_enquiry.enquiry_no and last_enquiry.enquiry_no.startswith("ENQ-"):
            try:
                last_number = int(last_enquiry.enquiry_no.split('-')[1])
            except (IndexError, ValueError):
                last_number = 0
            next_enquiry_no = f"ENQ-{last_number + 1:03d}"
        else:
            next_enquiry_no = "ENQ-001"

        form = EnquiryForm(initial={'enquiry_no': next_enquiry_no})

    return render(request, 'admission/enquiry_form.html', {
        'form': form,
        'success': success
    })


from .models import PUAdmissionshortlist, DegreeAdmissionshortlist, PUAdmission, DegreeAdmission

from .models import PUAdmissionshortlist, DegreeAdmissionshortlist
from django.shortcuts import render

def shortlist_display(request):
    selection = request.GET.get('type', 'PU')  # Default to PU
    shortlisted = []

    if selection == 'PU':
        shortlisted = PUAdmissionshortlist.objects.all()
    elif selection == 'Degree':
        shortlisted = DegreeAdmissionshortlist.objects.all()

    return render(request, 'admission/shortlist_display.html', {
        'shortlisted': shortlisted,
        'selection': selection
    })


# views.py
from django.shortcuts import render, get_object_or_404
from .models import PUFeeDetail, PUAdmission, PUAdmissionshortlist
from .forms import PUFeeDetailForm

def pu_fee_detail_form(request, shortlist_id):
    shortlist = get_object_or_404(PUAdmissionshortlist, pk=shortlist_id)
    admission = get_object_or_404(PUAdmission, admission_no=shortlist.admission_no)
    fee = PUFeeDetail.objects.filter(student=admission).first()
    form = PUFeeDetailForm(instance=fee) if fee else PUFeeDetailForm()

    if request.method == 'POST':
        form = PUFeeDetailForm(request.POST, instance=fee)
        if form.is_valid():
            fee_detail = form.save(commit=False)
            fee_detail.student = admission
            fee_detail.final_fee = fee_detail.base_fee - fee_detail.scholarship

            if fee_detail.payment_mode == 'Installment':
                balance = fee_detail.final_fee - fee_detail.advance_amount
                fee_detail.emi_amount = balance / 2 if balance > 0 else 0
            else:
                fee_detail.emi_amount = None
                fee_detail.due_date_1 = None
                fee_detail.due_date_2 = None

            fee_detail.save()

            return render(request, 'admission/fee_detail_form.html', {
                'form': PUFeeDetailForm(instance=fee_detail),
                'fee': fee_detail,
                'success_message': "PU Fee details saved successfully.",
                'admission': admission,
                'type': 'PU',
                'form_title': 'PU Fee Detail Form',
            })

    return render(request, 'admission/fee_detail_form.html', {
        'form': form,
        'admission': admission,
        'type': 'PU',
        'form_title': 'PU Fee Detail Form',
    })
# views.py
from .models import DegreeFeeDetail, DegreeAdmission, DegreeAdmissionshortlist
from .forms import DegreeFeeDetailForm

def degree_fee_detail_form(request, shortlist_id):
    shortlist = get_object_or_404(DegreeAdmissionshortlist, pk=shortlist_id)
    admission = get_object_or_404(DegreeAdmission, admission_no=shortlist.admission_no)

    fee = DegreeFeeDetail.objects.filter(student=admission).first()
    form = DegreeFeeDetailForm(instance=fee) if fee else DegreeFeeDetailForm()

    if request.method == 'POST':
        form = DegreeFeeDetailForm(request.POST, instance=fee)
        if form.is_valid():
            fee_detail = form.save(commit=False)
            fee_detail.student = admission
            fee_detail.final_fee = fee_detail.base_fee - fee_detail.scholarship

            if fee_detail.payment_mode == 'Installment':
                balance = fee_detail.final_fee - fee_detail.advance_amount
                fee_detail.emi_amount = balance / 2 if balance > 0 else 0
            else:
                fee_detail.emi_amount = None
                fee_detail.due_date_1 = None
                fee_detail.due_date_2 = None

            fee_detail.save()

            return render(request, 'admission/fee_detail_form.html', {
                'form': DegreeFeeDetailForm(instance=fee_detail),
                'fee': fee_detail,
                'success_message': "Fee details saved successfully.",
                'admission': admission,
                'type': 'Degree',
                'form_title': 'Degree Fee Detail Form',
            })

    return render(request, 'admission/fee_detail_form.html', {
        'form': form,
        'admission': admission,
        'type': 'Degree',
        'form_title': 'Degree Fee Detail Form',
    })


from django.shortcuts import render, redirect
from .forms import EnquiryForm
from .models import Enquiry

from .models import Enquiry
from .forms import EnquiryForm

def enquiry_form_view(request):
    success = False

    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            enquiry.enquiry_no = None  # Let model auto-generate it
            enquiry.save()
            success = True

            # Get next enquiry number to show again in new form
            last_enquiry = Enquiry.objects.order_by('id').last()
            if last_enquiry and last_enquiry.enquiry_no.startswith("ENQ-"):
                try:
                    last_number = int(last_enquiry.enquiry_no.split('-')[1])
                except (IndexError, ValueError):
                    last_number = 0
                next_enquiry_no = f"ENQ-{last_number + 1:03d}"
            else:
                next_enquiry_no = "ENQ-001"

            form = EnquiryForm(initial={'enquiry_no': next_enquiry_no})
    else:
        # First load - prepare next enquiry number
        last_enquiry = Enquiry.objects.order_by('id').last()
        if last_enquiry and last_enquiry.enquiry_no.startswith("ENQ-"):
            try:
                last_number = int(last_enquiry.enquiry_no.split('-')[1])
            except (IndexError, ValueError):
                last_number = 0
            next_enquiry_no = f"ENQ-{last_number + 1:03d}"
        else:
            next_enquiry_no = "ENQ-001"

        form = EnquiryForm(initial={'enquiry_no': next_enquiry_no})

    return render(request, 'admission/enquiry_form.html', {
        'form': form,
        'success': success
    })