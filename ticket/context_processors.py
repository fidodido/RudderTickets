
from ticket.forms import TicketForm

def user_processors(request):

    context = {}
    context['app_title'] = 'Rudder Tickets'
    context['ticket_form'] = TicketForm()
    context['active_user'] = request.user
    return context
