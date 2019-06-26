from django.http import HttpResponse

def index(request):
    '''Landing page'''
    return HttpResponse(
        '<p>Welcome to Airtech Flights API. Documentation can be found <a href="https://documenter.getpostman.com/view/3400181/S1Zw9B8Q">here</a>.</p>'
    )
