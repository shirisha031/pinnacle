from django import forms
from .models import PUAdmission

from django import forms
from .models import PUAdmission

from django import forms
from .models import PUAdmission

class PUAdmissionForm(forms.ModelForm):
    class Meta:
        model = PUAdmission
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'admission_date': forms.DateInput(attrs={'type': 'date'}),
            'admission_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


from django import forms
from .models import DegreeAdmission

from django import forms
from .models import DegreeAdmission

class DegreeAdmissionForm(forms.ModelForm):
    class Meta:
        model = DegreeAdmission
        fields = [
            'enquiry_no',
            'admission_no',
            'student_name',
            'gender',
            'caste',
            'student_phone_no',
            'parent_phone_no',
            'pu_percentage',
            'pu_reg_no',
            'year_of_passing',
            'dob',
            'photo',
            'course_type',
            'course',
            'quota_type',
            'application_status',
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'admission_no': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

from django import forms
from .models import Enquiry
from master.models import CourseType, Course

from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            'enquiry_no',
            'student_name',
            'dob',
            'parent_name',
            'parent_phone',
            'course_type',
            'course',
            'percentage_10th',
            'percentage_12th',
            'address',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        # Make enquiry_no readonly
        self.fields['enquiry_no'].widget.attrs['readonly'] = True
        # Optional: Improve display by adding placeholders or custom widgets
        self.fields['dob'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['percentage_10th'].widget.attrs['placeholder'] = "Enter 10th %"
        self.fields['percentage_12th'].widget.attrs['placeholder'] = "Enter 12th %"
        self.fields['address'].widget.attrs['rows'] = 3

from django import forms
from .models import PUFeeDetail,DegreeFeeDetail

class PUFeeDetailForm(forms.ModelForm):
    class Meta:
        model = PUFeeDetail
        exclude = ['student', 'final_fee', 'emi_amount', 'created_at']
        widgets = {
            'due_date_1': forms.DateInput(attrs={'type': 'date'}),
            'due_date_2': forms.DateInput(attrs={'type': 'date'}),
        }

class DegreeFeeDetailForm(forms.ModelForm):
    class Meta:
        model = DegreeFeeDetail
        exclude = ['student', 'final_fee', 'emi_amount', 'created_at']
        widgets = {
            'due_date_1': forms.DateInput(attrs={'type': 'date'}),
            'due_date_2': forms.DateInput(attrs={'type': 'date'}),
        }

