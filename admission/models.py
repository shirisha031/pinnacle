from django.db import models
from master.models import CourseType, Course  # adjust if your app name is different

class Enquiry(models.Model):
    enquiry_no = models.CharField(max_length=10, unique=True)
    student_name = models.CharField(max_length=100)
    dob = models.DateField()
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)

    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )

    percentage_10th = models.FloatField()
    percentage_12th = models.FloatField(null=True, blank=True)
    address = models.TextField()
    email = models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.enquiry_no} - {self.student_name}"



    def save(self, *args, **kwargs):
        if not self.enquiry_no:
            last_enquiry = Enquiry.objects.order_by('id').last()
            if last_enquiry and last_enquiry.enquiry_no.startswith("ENQ-"):
                try:
                    last_number = int(last_enquiry.enquiry_no.split('-')[1])
                except (IndexError, ValueError):
                    last_number = 0
                self.enquiry_no = f"ENQ-{last_number + 1:03d}"
            else:
                self.enquiry_no = "ENQ-001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enquiry_no} - {self.student_name}"

 

from master.models import CourseType, Course  # adjust import as per your app structure

class PUAdmission(models.Model):
    enquiry_no = models.CharField(max_length=10, blank=True, null=True)
    admission_no = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=100)
    parent_mobile_no = models.CharField(max_length=15)
    aadhar_no = models.CharField(max_length=12)
    caste = models.CharField(max_length=50)
    sslc_reg_no = models.CharField(max_length=30)
    sslc_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    admission_date = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='uploads/photos/', blank=True, null=True)

    # ✅ Add foreign key fields
    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pu_admissions'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pu_admissions'
    )

    year_of_passing = models.PositiveIntegerField(null=True, blank=True)

    quota_type = models.CharField(
        max_length=20,
        choices=[('Regular', 'Regular'), ('Management', 'Management')],
        default='Regular'
    )
    application_status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Shortlisted Management', 'Shortlisted for Management'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.student_name} - {self.admission_no}"


from django.db import models

class DegreeAdmission(models.Model):
    enquiry_no = models.CharField(max_length=10, blank=True, null=True)
    admission_no = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    caste = models.CharField(max_length=50)
    student_phone_no = models.CharField(max_length=15)
    parent_phone_no = models.CharField(max_length=15)
    pu_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    pu_reg_no = models.CharField(max_length=30)
    year_of_passing = models.PositiveIntegerField()
    dob = models.DateField()
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)

    course_type = models.ForeignKey(
        CourseType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='degree_admissions'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='degree_admissions'
    )

   
    quota_type = models.CharField(
        max_length=20,
        choices=[('Regular', 'Regular'), ('Management', 'Management')],
        default='Regular'
    )

    application_status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Shortlisted Management', 'Shortlisted for Management'),
        ],
        default='Pending'
    )

    def __str__(self):
        return self.student_name
# For PUAdmission
from django.db import models
class PUAdmissionshortlist(models.Model):
    admission_no = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    quota_type = models.CharField(
        max_length=20,
        choices=[
            ('Regular', 'Regular'),
            ('Management', 'Management'),
        ]
    )
    application_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Shortlisted(M)', 'Shortlisted Management'),  # Short code stored, label shown
        ],
        default='Pending'
    )
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name


class DegreeAdmissionshortlist(models.Model):
    admission_no = models.CharField(max_length=20)
    student_name = models.CharField(max_length=100)
    quota_type = models.CharField(
        max_length=20,
        choices=[
            ('Regular', 'Regular'),
            ('Management', 'Management'),
        ]
    )
    application_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Shortlisted', 'Shortlisted'),
            ('Rejected', 'Rejected'),
            ('Shortlisted(M)', 'Shortlisted Management'),  # Short code stored, label shown
        ],
        default='Pending'
    )
    admin_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name
    from django.db import models

class PUFeeDetail(models.Model):
    student = models.OneToOneField(PUAdmission, on_delete=models.CASCADE)

    base_fee = models.DecimalField(max_digits=10, decimal_places=2)
    scholarship = models.DecimalField(max_digits=10, decimal_places=2)
    final_fee = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_mode = models.CharField(max_length=20, choices=[('Full', 'Full Payment'), ('Installment', 'Installment')])
    due_date_1 = models.DateField(null=True, blank=True)
    due_date_2 = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from .models import DegreeAdmission  # Ensure this is imported

class DegreeFeeDetail(models.Model):
    student = models.OneToOneField(DegreeAdmission, on_delete=models.CASCADE)

    base_fee = models.DecimalField(max_digits=10, decimal_places=2)
    scholarship = models.DecimalField(max_digits=10, decimal_places=2)
    final_fee = models.DecimalField(max_digits=10, decimal_places=2)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    payment_mode = models.CharField(max_length=20, choices=[('Full', 'Full Payment'), ('Installment', 'Installment')])
    due_date_1 = models.DateField(null=True, blank=True)
    due_date_2 = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
