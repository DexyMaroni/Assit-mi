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
    # If note_id is provided, retrieve the sticky note; otherwise, set it to None
    if note_id:
        note = get_object_or_404(StickyNote, id=note_id, user=request.user)
    else:
        note = None

    if request.method == "POST":
        form = StickyNoteForm(request.POST, instance=note)
        attachment_form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()

            # Handle attachment if provided
            if attachment_form.is_valid() and 'file' in request.FILES:
                attachment = attachment_form.save(commit=False)
                attachment.sticky_note = new_note
                attachment.save()

            return redirect('sticky_notes_list')

    else:
        form = StickyNoteForm(instance=note)
        attachment_form = AttachmentForm()

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
