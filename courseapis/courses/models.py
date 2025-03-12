from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.transaction import mark_for_rollback_on_error


# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='users/%Y/%m', null=True)


class BaseModel(models.Model):
    activate = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    subject = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='courses/%Y/%m')

    class Meta:
        unique_together = ('subject', 'category')

    def __str__(self):
        return self.subject


class Lesson(BaseModel):
    subject = models.CharField(max_length=255, unique=True)
    content = RichTextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses/%Y/%m', null=True)
    tags = models.ManyToManyField('Tag')
    class Meta:
        unique_together = ('subject', 'course')

    def __str__(self):
        return self.subject

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.CharField(max_length=255)

class Like(Interaction):
    class Meta:
        unique_together = ('user', 'lesson')