from django.contrib import admin
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

admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAmin)
admin.site.register(Tag)