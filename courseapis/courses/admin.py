from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse

from courses.models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    readonly_fields = ['image_view']

    def image_view(self, course):
        if course:
            return mark_safe(
                f'<img src="/static/{course.image.name}" width="100/>'
            )

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'

class LessonAmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_at', 'course']
    list_filter = ['subject', 'created_at']
    search_fields = ['subject', 'course__subject']
    form = LessonForm
class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khóa học trực tuyến'
    def stats_view(self, request):
        count = Course.objects.filter(activate=True).count()
        stats = Course.objects.annotate(lesson_count=Count('lesson__id')).values('id', 'subject', 'lesson_count')

admin_site = CourseAppAdminSite(name='Admin')
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAmin)
admin_site.register(Tag)