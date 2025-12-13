from django import forms
from .models import Student, Faculty

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['code', 'faculty']

    code = forms.CharField(max_length=10, required=True, label="کد دانشجویی")
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), required=True, empty_label="انتخاب کنید", label="دانشکده")

    def clean_code(self):
        code = self.cleaned_data.get('code')

        student_exists = Student.objects.filter(code=code).exists()

        if student_exists:
            raise forms.ValidationError(
                """
                کد دانشجویی از قبل در دیتابیس ما ثبت شده است.
                اگر این کد برای شماست و نمی‌توانید وارد شوید، لطفاً از طریق ارتباط با ما مشکل خود را به اشتراک بگذارید.
                """
            )
            
        if len(code) < 9:
            raise forms.ValidationError("کد دانشجویی باید یا 9 یا 10 کاراکتر باشد.")
        else:
            return code