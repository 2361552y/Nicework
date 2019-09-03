from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from nicework.models import Activity, Journal, Entry, UserProfile, Student, EntryImage, Lecturer, Mentor, Comment
from nicework.forms import EntryForm, JournalForm, UserForm, UserProfileForm, ActivityForm, EntryImageForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User


def get_context(request):
    student = None;
    lecturer = None;
    mentor = None;
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        students = Student.objects.all()
    except UserProfile.DoesNotExist:
        user_profile = None
    if request.user.username[0] == 's' or request.user.username[0] == 'S':
        activities = Activity.objects.filter(
            actor=Student.objects.filter(detail__user=request.user)).order_by('date')
        journals = Journal.objects.filter(
            owner=Student.objects.filter(detail__user=request.user)).order_by('createTime')
        entries = Entry.objects.filter(
            journal__owner=Student.objects.filter(detail__user=request.user)).filter(version=0).order_by('createTime')
        student = Student.objects.get(detail__user=request.user)
    elif request.user.username[0] == 'l' or request.user.username[0] == 'L':
        activities = Activity.objects.order_by('date')
        journals = Journal.objects.order_by('createTime')
        entries = Entry.objects.filter(mentorPass=True).filter(lecturerPass=None).filter(version=0).order_by(
            'createTime')
        lecturer = Lecturer.objects.get(detail__user=request.user)
    elif request.user.username[0] == 'm' or request.user.username[0] == 'M':
        activities = Activity.objects.order_by('date')
        journals = Journal.objects.order_by('createTime')
        entries = Entry.objects.filter(mentorPass=None).filter(version=0).order_by('createTime')
        mentor = Mentor.objects.get(detail__user=request.user)
    else:
        return HttpResponse("Invalid login details supplied.")
    context_dict = {'user_profile': user_profile, 'activities': activities, 'journals': journals, 'entries': entries,
                    'students': students, 'student': student, 'lecturer': lecturer, 'mentor': mentor}
    return context_dict


def welcome(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'welcome.html')


def contact(request):
    return render(request, 'contact.html')


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     return render(request,
#                   'rango/register.html',
#                   {'user_form': user_form,
#                    'profile_form': profile_form,
#                    'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'welcome.html', context={'login_error': "Your account is not active!"})
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'welcome.html', context={'login_error': "Invalid login information supplied!"})
    else:
        return render(request, 'welcome.html', context={'login_error': "Invalid login information supplied!"})


def index(request):
    # if request.user.username[0] == 's' or request.user.username[0] == 'S':
    #     return HttpResponseRedirect(reverse('student_index'))
    # elif request.user.username[0] == 'l' or request.user.username[0] == 'L':
    #     return HttpResponseRedirect(reverse('staff_index'))
    # elif request.user.username[0] == 'm' or request.user.username[0] == 'M':
    #     return HttpResponseRedirect(reverse('staff_index'))
    # else:
    # return render(request, 'index.html', context={'login_error': "Invalid login information supplied!"})
    return render(request, 'index.html', context=get_context(request))


def edit_profile(request):
    context_dict = get_context(request)
    profile_form = UserProfileForm()
    if request.method == 'POST':
        # user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST)
        # if user_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            # user = user_form
            user_profile = profile_form.save(commit=False)
            user_profile.user = request.user
            if 'avatar' in request.FILES:
                user_profile.avatar = request.FILES['avatar']
            # user.save(commit=False)
            user_profile.save()
            # print(user_profile, user_profile)
            context_dict = get_context(request)
            context_dict['success_log'] = "Successfully updated!"
        else:
            # print(user_form.errors, profile_form.errors)
            print(profile_form.errors)
            # context_dict['error_log'] = user_form.errors + profile_form.errors
            context_dict['error_log'] = profile_form.errors
    context_dict['form'] = profile_form
    return render(request, 'profile.html', context_dict)


# @login_required
# def user_logout(request):
#     logout(request)
#     return render(request, 'rango/logout.html', {})
#
#
# @login_required
# def restricted(request):
#     # return render("Since you're logged in, you can see this text!")
#     return render(request, 'rango/restricted.html', {})

def base(request):
    return render(request, 'base.html')


# @login_required
def student_index(request):
    context_dict = get_context(request)
    return render(request, 'student_index.html', context=context_dict)


# @login_required
def staff_index(request):
    context_dict = get_context(request)
    return render(request, 'staff_index.html', context=context_dict)


# @login_required
# def mentor_index(request):
#     context_dict = get_context(request)
#     return render(request, 'staff_index.html', context=context_dict)


# @login_required
def show_activity(request, activity_id):
    context_dict = get_context(request)
    try:
        activity = Activity.objects.get(id=activity_id)
        context_dict['activity'] = activity
    except Activity.DoesNotExist:
        context_dict['activity'] = None
    return render(request, 'activity.html', context=context_dict)


# @login_required
# def show_journal(request, journal_id):
#     context_dict = get_context(request)
#     try:
#         journal = Journal.objects.get(id=journal_id)
#         context_dict['journal'] = journal
#     except Journal.DoesNotExist:
#         context_dict['journal'] = None
#     return render(request, 'journal.html', context_dict)


# @login_required
def get_folios(context_dict, entry_id):
    folios = {}
    version = 1
    try:
        entry = Entry.objects.get(id=entry_id)
        context_dict['entry'] = entry
    except Entry.DoesNotExist:
        context_dict['entry'] = None
    try:
        entry_files = EntryImage.objects.get(entry=entry)
        context_dict['entry_files'] = entry_files
    except EntryImage.DoesNotExist:
        context_dict['entry_files'] = None
    try:
        comments = Comment.objects.filter(entry=entry)
        context_dict['comments'] = comments
    except EntryImage.DoesNotExist:
        context_dict['comments'] = None

    while entry.preEntryID != -1:
        entry_id = entry.preEntryID
        folio = {}
        try:
            entry = Entry.objects.get(id=entry_id)
            folio['entry'] = entry
        except Entry.DoesNotExist:
            folio['entry'] = None
        try:
            entry_files = EntryImage.objects.get(entry=entry)
            folio['entry_files'] = entry_files
        except EntryImage.DoesNotExist:
            folio['entry_files'] = None
        try:
            comments = Comment.objects.filter(entry=entry)
            folio['comments'] = comments
        except EntryImage.DoesNotExist:
            folio['comments'] = None
        folio['version'] = version
        folios[version] = folio
        version += 1
    context_dict['latest'] = version - 1
    context_dict['folios'] = folios
    return context_dict


# @login_required
def show_entry(request, entry_id):
    context_dict = get_folios(get_context(request), entry_id)
    return render(request, 'entry.html', context_dict)


def edit_entry(request, entry_id):
    context_dict = get_folios(get_context(request), entry_id)
    entry = get_object_or_404(Entry, pk=int(entry_id))
    try:
        entry_img = EntryImage.objects.get(entry=entry)
    except EntryImage.DoesNotExist:
        entry_img = None
    if request.method == 'POST':
        form1 = EntryForm(data=request.POST, instance=entry)
        if form1.is_valid():
            entry1 = form1.save(commit=False)
            entry1.id = None
            entry1.journal = entry.journal
            entry1.lastModifyTime = timezone.now()
            entry1.preEntryID = entry_id
            entry1.version = 0
            entry1.mentorPass = None
            entry1.lecturerPass = None
            entry1.save()
            entry = Entry.objects.get(id=entry_id)
            entry.version += 1
            entry.save()
            form2 = EntryImageForm(data=request.POST, instance=entry_img)
            if form2.is_valid():
                if 'attachedImage' in request.FILES:
                    entry_img1 = form2.save(commit=False)
                    entry_img1.id = None
                    entry_img1.entry = entry1
                    entry_img1.attachedImage = request.FILES['attachedImage']
                    entry_img1.save()
            context_dict = get_folios(get_context(request), entry1.id)
            context_dict['success_log'] = "Entry Updated!"
            return render(request, 'entry.html', context_dict)
        else:
            print(form1.errors)
            context_dict['error_log'] = 'Error.'
    else:
        form1 = EntryForm(instance=entry)
        form2 = EntryImageForm(instance=entry_img)
    context_dict['form1'] = form1
    context_dict['form2'] = form2
    return render(request, 'edit_entry.html', context_dict)


# @login_required
def add_journal(request):
    context_dict = get_context(request)
    form = JournalForm()
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.createTime = timezone.now()
            journal.owner = Student.objects.get(detail=UserProfile.objects.get(user=request.user))
            journal.save()
            context_dict['success_log'] = "Successfully updated!"
        else:
            print(form.errors)
            context_dict['error_log'] = form.errors
    context_dict['form'] = form
    return render(request, 'add_journal.html', context_dict)


# @login_required
def add_activity(request):
    context_dict = get_context(request)
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=True)
            print(activity, activity.id)
            context_dict['success_log'] = "Successfully updated!"
            return show_activity(request, activity.id)
        else:
            print(form.errors)
            context_dict['error_log'] = form.errors
    context_dict['form'] = form
    return render(request, 'add_activity.html', context_dict)


# @login_required
def evaluate_entry(request, entry_id):
    context_dict = get_context(request)
    form = CommentForm()
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExsit:
        entry = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = entry
            comment.date = timezone.now()
            comment.user = request.user
            if entry.lecturerPass is False:
                comment.competencies = None
            comment.save()
            context_dict = get_folios(context_dict, entry_id)
            context_dict['success_log'] = "Successfully updated!"
            return render(request, 'entry.html', context_dict)
        else:
            print(form.errors)
            context_dict['error_log'] = form.errors
    context_dict = get_folios(context_dict, entry_id)
    context_dict['form'] = form
    return render(request, 'evaluate_entry.html', context_dict)


def pass_entry(request, entry_id):
    context_dict = get_context(request)
    try:
        entry = Entry.objects.get(id=entry_id)
        if request.user.username[0] == 'l' or request.user.username[0] == 'L':
            entry.lecturerPass = True;
            log = "Lecturer passed!"
        elif request.user.username[0] == 'm' or request.user.username[0] == 'M':
            entry.mentorPass = True;
            log = "Mentor passed!"
        entry.save()
        context_dict = get_folios(get_context(request), entry.id)
        context_dict['mark'] = 1
        context_dict['error_log'] = log
        context_dict['form'] = CommentForm()
        return render(request, 'evaluate_entry.html', context_dict)
    except Entry.DoesNotExist:
        context_dict['entry'] = None
        entry_id = None
    context_dict = get_folios(get_context(request), entry_id)
    context_dict['form'] = CommentForm()
    return render(request, 'evaluate_entry.html', context_dict)


def fail_entry(request, entry_id):
    context_dict = get_context(request)
    try:
        entry = Entry.objects.get(id=entry_id)
        if request.user.username[0] == 'l' or request.user.username[0] == 'L':
            entry.lecturerPass = False;
            log = "Lecturer Failed!"
        elif request.user.username[0] == 'm' or request.user.username[0] == 'M':
            entry.mentorPass = False;
            log = "Mentor Failed!"
        entry.save()
        context_dict = get_folios(context_dict, entry.id)
        context_dict['mark'] = 0
        context_dict['error_log'] = log
        context_dict['form'] = CommentForm()
        return render(request, 'evaluate_entry.html', context_dict)
    except Entry.DoesNotExist:
        context_dict['entry'] = None
        entry_id = None
    context_dict = get_folios(context_dict, entry_id)
    context_dict['form'] = CommentForm()
    return render(request, 'evaluate_entry.html', context_dict)


def like(request, entry_id):
    context_dict = get_context(request)
    try:
        entry = Entry.objects.get(id=entry_id)
        entry.likes += 1;
        entry.save()
        context_dict['entry'] = entry
    except Entry.DoesNotExist:
        context_dict['entry'] = None
        entry_id = None
    context_dict = get_folios(get_context(request), entry_id)
    return render(request, 'evaluate_entry.html', context_dict)


def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id)
    activity.delete()
    context_dict = get_context(request);
    context_dict['log'] = "Updated!"
    return render(request, 'index.html', context_dict)


def delete_journal(request, journal_id):
    journal = Journal.objects.get(id=journal_id)
    journal.delete()
    context_dict = get_context(request);
    context_dict['log'] = "Updated!"
    return render(request, 'index.html', context_dict)


# @login_required
def add_entry(request, journal_id):
    context_dict = get_context(request)
    try:
        journal = Journal.objects.get(id=journal_id)
    except Journal.DoesNotExist:
        journal = None
    if request.method == 'POST':
        form1 = EntryForm(data=request.POST)
        if form1.is_valid():
            if journal:
                entry = form1.save(commit=False)
                entry.journal = journal
                entry.createTime = timezone.now()
                entry.lastModifyTime = timezone.now()
                entry.preEntryID = -1
                entry.version = 0
                entry.likes = 0
                entry.save()
                form2 = EntryImageForm(data=request.POST)
                if form2.is_valid():
                    if 'attachedImage' in request.FILES:
                        entry_img1 = form2.save(commit=False)
                        entry_img1.entry = entry
                        entry_img1.attachedImage = request.FILES['attachedImage']
                        entry_img1.save()
                context_dict = get_folios(context_dict, entry.id)
                context_dict['success_log'] = "Entry Updated!"
                return render(request, 'entry.html', context_dict)
        else:
            print(form1.errors)
            context_dict['error_log'] = 'Error.'
    else:
        form1 = EntryForm()
        form2 = EntryImageForm()
    context_dict['form1'] = form1
    context_dict['form2'] = form2
    context_dict['journal'] = journal
    return render(request, 'add_entry.html', context_dict)
    # return HttpResponseRedirect(reverse('add_entry'))


def view_classmates(request):
    context_dict = get_context(request)
    return render(request, 'view_classmates.html', context=context_dict)


def view(request):
    context_dict = get_context(request)
    return render(request, 'view.html', context=context_dict)
