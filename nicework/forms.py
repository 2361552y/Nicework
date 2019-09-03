from django import forms
from django.contrib.auth.models import User
from nicework.models import Journal, Activity, Entry, UserProfile, Student, Mentor, EntryImage, Comment


class ActivityForm(forms.ModelForm):
    topic = forms.CharField(max_length=128)
    date = forms.DateTimeField(widget=forms.SelectDateWidget)
    address = forms.CharField(max_length=128)
    description = forms.CharField(widget=forms.Textarea)
    # holder = forms.ChoiceField(widget=forms.RadioSelect)
    # actor = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Activity
        exclude = ('',)


class JournalForm(forms.ModelForm):
    # title = forms.CharField(max_length=128,
    #                         help_text="Please enter the journal title.")
    # # activity = forms.ChoiceField(help_text="Choose the related activity.")

    class Meta:
        model = Journal
        exclude = ('lastModifyTime', 'createTime', 'owner')


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        # exclude = ('lastModifyTime', 'createTime', 'mentorPass', 'lecturerPass', 'journal', 'likes', 'preEntryID')
        fields = ('title', 'content', 'isPlanOrReflection',)


class EntryImageForm(forms.ModelForm):
    class Meta:
        model = EntryImage
        fields = ('attachedImage',)
        # fields = ('attaches',)


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password', 'email',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'competencies')


class EditEntryForm(forms.ModelForm):
    # title = forms.CharField(max_length=128,
    #                         help_text="Please enter the title of the entry.", label="Title:")
    # content = forms.CharField(widget=forms.Textarea)
    #
    # # isPlanOrReflection = forms.ChoiceField(choices=[True, False], label="Whether a plan")

    class Meta:
        model = Entry
        fields = ('content',)
