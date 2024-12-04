from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import StickyNote, Attachment
from .forms import StickyNoteForm, AttachmentForm

@login_required
def sticky_notes_list(request):
    # Get all sticky notes created by the current user
    sticky_notes = StickyNote.objects.filter(user=request.user)
    
    context = {
        'sticky_notes': sticky_notes,
    }
    return render(request, 'notes/sticky_notes_list.html', context)


@login_required
def add_edit_sticky_note(request, note_id=None):
    # Retrieve or initialize the sticky note
    note = get_object_or_404(StickyNote, id=note_id, user=request.user) if note_id else None

    if request.method == "POST":
        # Handle sticky note form
        form = StickyNoteForm(request.POST, instance=note)

        # Only process the attachment if a file is uploaded
        attachment_form = AttachmentForm(request.POST, request.FILES) if 'file' in request.FILES else None

        if form.is_valid():
            # Save the sticky note
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            # Save the attachment if provided
            if attachment_form and attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.sticky_note = new_note
                attachment.save()

            return redirect('sticky_notes_list')

    else:
        form = StickyNoteForm(instance=note)
        attachment_form = AttachmentForm()  # Empty form for new attachments

    context = {
        'form': form,
        'attachment_form': attachment_form,
        'note': note,
    }
    return render(request, 'notes/add_edit_sticky_note.html', context)

@login_required
def add_attachment(request, note_id):
    note = get_object_or_404(StickyNote, id=note_id, user=request.user)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.sticky_note = note
            attachment.save()
            return redirect('view_attachments', note_id=note.id)

    else:
        form = AttachmentForm()

    context = {
        'form': form,
        'note': note,
    }
    return render(request, 'notes/add_attachment.html', context)


@login_required
def delete_sticky_note(request, note_id):
    note = get_object_or_404(StickyNote, id=note_id, user=request.user)

    if request.method == 'POST':
        # Delete the attachments associated with the note
        note.attachments.all().delete()
        note.delete()
        return redirect('sticky_notes_list')

    context = {
        'note': note,
    }
    return render(request, 'users/delete_sticky_note.html', context)


@login_required
def view_attachments(request, note_id):
    note = get_object_or_404(StickyNote, id=note_id, user=request.user)
    attachments = Attachment.objects.filter(sticky_note=note)

    context = {
        'note': note,
        'attachments': attachments,
    }
    return render(request, 'notes/view_attachments.html', context)

@login_required
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    
    # Check if the current user is the one who uploaded the attachment or the user who owns the sticky note
    if attachment.sticky_note.user != request.user:
        return redirect('sticky_notes_list')  # Redirect if user is not authorized to delete this attachment

    if request.method == 'POST':
        # Delete the attachment
        attachment.delete()
        return redirect('view_attachments', note_id=attachment.sticky_note.id)  # Redirect to the note's attachments page

    # In case it's not a POST request, show a confirmation message or redirect
    return redirect('view_attachments', note_id=attachment.sticky_note.id)







from django.shortcuts import render, redirect, get_object_or_404
from .models import LectureNote, LectureAttachment
from .forms import LectureNoteForm, LectureAttachmentForm
from django.contrib.auth.decorators import login_required

@login_required
def add_edit_lecture_note(request, pk=None):
    lecture_note = None
    if pk:
        lecture_note = get_object_or_404(LectureNote, pk=pk, user=request.user)

    if request.method == "POST":
        note_form = LectureNoteForm(request.POST, instance=lecture_note)
        attachment_form = LectureAttachmentForm(request.POST, request.FILES)

        if note_form.is_valid():
            # Save the lecture note and assign the current user
            lecture_note_instance = note_form.save(commit=False)
            lecture_note_instance.user = request.user  # Assign the logged-in user
            lecture_note_instance.save()

            # Handle attachments only if there is a file uploaded
            if 'file' in request.FILES:
                if attachment_form.is_valid():
                    attachment = attachment_form.save(commit=False)
                    attachment.lecture_note = lecture_note_instance
                    attachment.save()

            return redirect('lecture_notes_list')

    else:
        note_form = LectureNoteForm(instance=lecture_note)
        attachment_form = LectureAttachmentForm()

    return render(
        request,
        'lecture_note/add_edit_lecture_note.html',
        {'note_form': note_form, 'attachment_form': attachment_form, 'lecture_note': lecture_note}
    )





def lecture_notes_list(request):
    notes = LectureNote.objects.all().order_by('-created_at')  # Adjust filtering as needed
    context = {'notes': notes}
    return render(request, 'lecture_note/lecture_notes_list.html', context)


def lecture_note_detail(request, note_id):
    note = get_object_or_404(LectureNote, id=note_id)
    context = {'note': note}
    return render(request, 'lecture_note/lecture_note_detail.html', context)


@login_required
def delete_attachment(request, pk, attachment_id):
    # Fetch the attachment and ensure the user owns the lecture note
    attachment = get_object_or_404(LectureAttachment, pk=attachment_id, lecture_note__pk=pk, lecture_note__user=request.user)

    # Delete the attachment
    attachment.delete()

    return redirect('lecture_note_detail', note_id=pk)

@login_required
def delete_lecture_note(request, pk):
    # Fetch the lecture note and ensure the user owns it
    lecture_note = get_object_or_404(LectureNote, pk=pk, user=request.user)

    # Delete the lecture note and its attachments
    lecture_note.delete()

    return redirect('lecture_notes_list')





