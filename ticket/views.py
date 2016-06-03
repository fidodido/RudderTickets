from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from ticket.forms import TicketForm, AssignToForm, CancelForm, SolveForm, ReplyForm, ReopenForm
from django.contrib import messages
from ticket.models import Ticket, Action, Status, Workflow, Reply, UserDetail, Attachment
import pprint
from django.http import HttpResponse, JsonResponse
import os

PENDING = 1
WORKING_IN = 2
CANCELED = 3
RESOLVED = 4


@login_required
def index(request):

    tickets = Ticket.objects.filter(
        status__in=[PENDING, WORKING_IN]
    ).order_by('-status', '-high_priority', '-created')
    
    template = 'ticket/index.html'
    return render(request, template, { 'tickets' : tickets})


@login_required
def resolved(request):

    tickets = Ticket.objects.filter(status=RESOLVED).order_by('status', '-high_priority', '-created')
    template = 'ticket/index.html'
    return render(request, template, { 'tickets' : tickets})



@login_required
def canceled(request):

    tickets = Ticket.objects.filter(status=CANCELED).order_by('status', '-high_priority', '-created')
    template = 'ticket/index.html'
    return render(request, template, { 'tickets' : tickets})


@login_required
def view(request, ticket_slug):
    
    ticket = Ticket.objects.get(slug=ticket_slug)
    actions = Action.objects.filter(current_status=ticket.status)
    workflow = Workflow.objects.filter(ticket=ticket)
    replies = Reply.objects.filter(ticket=ticket).order_by('created')
    
    user_detail = UserDetail.objects.filter(ticket=ticket, user=request.user)

    if not user_detail:
        new_detail = UserDetail()
        new_detail.user = request.user
        new_detail.ticket = ticket
        new_detail.viewed = True
        new_detail.save()

    replyForm = ReplyForm(initial={
        'user': request.user,
        'ticket': ticket
    })

    template = 'ticket/view.html'
    return render(request, template, {'ticket': ticket, 'replies': replies, 'actions': actions, 'workflow': workflow, 'replyForm': replyForm})


@login_required
def add(request):

    template = 'ticket/add.html'
    form = TicketForm()
    
    if request.method == 'POST':

        form = TicketForm(request.POST)

        if form.is_valid():
            
            new_ticket = form.save()

            # ademas se debe crear una reply.
            reply = Reply()
            reply.user = request.user
            reply.ticket = new_ticket
            reply.comment = request.POST.get('description')
            reply.save()

            # ademas se debe procesar los archivos subidos.
            filenames = request.POST.getlist('filename')
            filehashes = request.POST.getlist('filehash')

            print filehashes

            i = 0
            for myfile in filenames:
                attachment = Attachment()
                attachment.reply = reply
                attachment.name = myfile
                attachment.hash = filehashes[i]
                attachment.save()
                i = i + 1

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', new_ticket.slug)
        else:
            return render(request, template, {'form': form})

    return render(request, template, {'form': form})


@login_required
def upload(request):
    """
    Sube un archivo al servidor
    """

    from time import time

    # por ahora, los archivos quedaran en el directorio temporal dentro del proyecto.
    upload_file = request.FILES['file']

    # creamos un nombre unico para guardar en el disco.
    unique_name = hex(int(time()*10000000))[2:]

    # especificamos el path
    path = 'temp/' + unique_name

    # Escribimos en el servidor.
    with open(path, 'wb+') as destination:
        for chunk in upload_file.chunks():
            destination.write(chunk)

    return JsonResponse({'status':'success', 'hash': unique_name, 'name': upload_file.name})


@login_required
def download(request, hash):

    from django.utils.encoding import smart_str
    from wsgiref.util import FileWrapper
    attachment = Attachment.objects.get(hash=hash)

    filename = "temp/" + attachment.hash
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(attachment.name)
    response['Content-Length'] = os.path.getsize(filename)
    return response


@login_required
def comment(request, ticket_slug):

    if request.method == 'POST':

        form = ReplyForm(request.POST)

        if form.is_valid():

            new_reply = form.save()

            filenames = request.POST.getlist('filename')
            filehashes = request.POST.getlist('filehash')

            print filehashes

            i = 0
            for myfile in filenames:
                attachment = Attachment()
                attachment.reply = new_reply
                attachment.name = myfile
                attachment.hash = filehashes[i]
                attachment.save()
                i = i + 1

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', new_reply.ticket.slug)


@login_required
def edit(request, ticket_slug):

    template = 'ticket/edit.html'
    ticket = Ticket.objects.get(slug=ticket_slug)

    form = TicketForm(instance=ticket)
    
    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            new_ticket = form.save()
            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', new_ticket.slug)
        else:
            return render(request, template, {'form': form})

    return render(request, template, {'form': form, 'ticket': ticket})


@login_required
def assign_to(request, ticket_slug):

    template = 'ticket/assign-to.html'
    ticket = Ticket.objects.get(slug=ticket_slug)
    action = Action.objects.get(current_status=ticket.status, post_status=WORKING_IN)

    form = AssignToForm(initial={
        'ticket': ticket,
        'current_status': ticket.status,
        'post_status': action.post_status,
        'user': request.user
    })

    if request.method == 'POST':

        form = AssignToForm(request.POST)

        if form.is_valid():
            new_workflow = form.save()
            ticket.status = new_workflow.post_status
            ticket.assigned_to = new_workflow.user
            ticket.save()

            #new reply
            reply = Reply()
            reply.user = request.user
            reply.ticket = ticket
            reply.comment = '<span style="color: orange; font-weight: bolder;">The ticket has been re-assigned to: ' + new_workflow.user.username + '.</span><br>' + request.POST.get('comment')
            reply.save()

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', ticket.slug)
    
    return render(request, template, {'form': form, 'action': action, 'ticket': ticket})


@login_required
def cancel(request, ticket_slug):

    template = 'ticket/cancel.html'
    ticket = Ticket.objects.get(slug=ticket_slug)
    action = Action.objects.get(current_status=ticket.status, post_status=CANCELED)

    form = CancelForm(initial={
        'ticket': ticket,
        'current_status': ticket.status,
        'post_status': action.post_status,
        'user': request.user
    })

    if request.method == 'POST':

        form = CancelForm(request.POST)

        if form.is_valid():
            new_workflow = form.save()
            ticket.status = new_workflow.post_status
            ticket.assigned_to = new_workflow.user
            ticket.save()

            #new reply
            reply = Reply()
            reply.user = request.user
            reply.ticket = ticket
            reply.comment = '<span style="color: red; font-weight: bolder;">The ticket has been canceled.</span><br>' + request.POST.get('comment')
            reply.save()

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', ticket.slug)
    
    return render(request, template, {'form': form, 'action': action, 'ticket': ticket})


@login_required
def re_open(request, ticket_slug):

    template = 'ticket/re-open.html'
    ticket = Ticket.objects.get(slug=ticket_slug)
    action = Action.objects.get(current_status=ticket.status, post_status=PENDING)

    form = ReopenForm(initial={
        'ticket': ticket,
        'current_status': ticket.status,
        'post_status': action.post_status,
        'user': request.user
    })

    if request.method == 'POST':

        form = ReopenForm(request.POST)

        if form.is_valid():
            new_workflow = form.save()
            ticket.status = new_workflow.post_status
            ticket.assigned_to = new_workflow.user
            ticket.save()

            #new reply
            reply = Reply()
            reply.user = request.user
            reply.ticket = ticket
            reply.comment = '<span style="color: orange; font-weight: bolder;">The ticket has been re-opened.</span><br>' + request.POST.get('comment')
            reply.save()

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', ticket.slug)
    
    return render(request, template, {'form': form, 'action': action, 'ticket': ticket})


@login_required
def solve(request, ticket_slug):

    template = 'ticket/solve.html'
    ticket = Ticket.objects.get(slug=ticket_slug)
    action = Action.objects.get(current_status=ticket.status, post_status=RESOLVED)

    form = SolveForm(initial={
        'ticket': ticket,
        'current_status': ticket.status,
        'post_status': action.post_status,
        'user': request.user
    })

    if request.method == 'POST':

        form = SolveForm(request.POST)

        if form.is_valid():
            new_workflow = form.save()
            ticket.status = new_workflow.post_status
            ticket.assigned_to = new_workflow.user
            ticket.resolution = request.POST.get('comment')
            ticket.save()

            #new reply
            reply = Reply()
            reply.user = request.user
            reply.ticket = ticket
            reply.comment = '<span style="color: green; font-weight: bolder;">The ticket has been resolved.</span><br>' + request.POST.get('comment')

            reply.save()

            messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
            return redirect('tickets_view', ticket.slug)
    
    return render(request, template, {'form': form, 'action': action, 'ticket': ticket})


@login_required
def delete_comment(request, ticket_slug, comment_id):

    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    messages.add_message(request, messages.SUCCESS, 'Your data has been successfully saved')
    return redirect('tickets_view', ticket_slug)