from datetime import date


def user_logged(request):
    if request.user.is_authenticated:
        logged = request.user.username
        return {'logged': logged}
    else:
        return {'logged': 'Unknown'}


def footer_data(request):
    return {'date': date.today()}
