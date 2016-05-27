
def user_processors(request):

    context = {}
    context['app_title'] = 'Rudder Tickets'
    context['active_user'] = request.user
    return context
