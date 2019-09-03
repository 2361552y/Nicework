from django.db import models
from django.contrib.auth.models import User
from PIL import Image


def file_upload_to(instance, filename):
    return '/'.join(['static/dist/files/', instance.entry.title, 'image/', filename])


def avatar_upload_to(instance, filename):
    return '/'.join(['static/dist/files/', instance.user.username, 'avatar/', filename])


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    detail = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    major = models.CharField(max_length=64)

    def __str__(self):
        return self.detail.name


class Lecturer(models.Model):
    detail = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    office = models.CharField(max_length=128)

    def __str__(self):
        return self.detail.name


class Mentor(models.Model):
    detail = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    company = models.CharField(max_length=64)

    def __str__(self):
        return self.detail.name


class Activity(models.Model):
    topic = models.CharField(max_length=128, null=False)
    date = models.DateTimeField(null=False)
    address = models.CharField(max_length=128, null=False)
    description = models.TextField(null=False)
    holder = models.ForeignKey(Mentor)
    actor = models.ManyToManyField(Student)

    class Meta:
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.topic


class Journal(models.Model):
    title = models.CharField(max_length=128)
    lastModifyTime = models.DateTimeField(auto_now_add=True)
    createTime = models.DateTimeField(auto_created=True)
    activity = models.ForeignKey(Activity)
    owner = models.ForeignKey(Student)

    def __str__(self):
        return self.title


class Entry(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=False)
    lastModifyTime = models.DateTimeField(auto_now_add=True)
    createTime = models.DateTimeField(auto_created=True)
    content = models.TextField()
    isPlanOrReflection = models.BooleanField(default=False)
    mentorPass = models.NullBooleanField(default=None)
    lecturerPass = models.NullBooleanField(default=None)
    likes = models.IntegerField(default=0)
    version = models.IntegerField(default=0)
    preEntryID = models.IntegerField(default=-1)

    class Meta:
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.title


class EntryImage(models.Model):
    attachedImage = models.ImageField(upload_to=file_upload_to, blank=True)
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET("Deleted_User"))
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=False)
    isPassed = models.BooleanField(default=False)
    competencies = models.TextField(blank=True)
