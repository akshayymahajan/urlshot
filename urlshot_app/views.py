from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urlshot.urlshot_app.models import URL
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json

# Create your views here.

CHARSET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
base = 62
code_length = 6
def convert(a):
    code = ''
    while(a > 0):
        code = code + CHARSET[a % base]
        a = a/base
    return code[::-1]

def url_exist(url):
    url_obj = URL.objects.filter(long_url=url)
    try:
        url = url_obj.get()
        return url.short_url
    except URL.DoesNotExist:
        return ''

def get(request):
        site = 'urlshot.co.nr/'
        if request.method == 'GET':
            return render_to_response('main.html', {'url_value':'','response_text':""}, context_instance=RequestContext(request))
        else:
            url = 'http://' + request.POST.get('tf')
            validate = URLValidator()
            try:
                validate(url)
            except ValidationError:
                return render_to_response('main.html',{'url_value':'', 'response_text':'Enter a valid URL'}, context_instance=RequestContext(request))

            check = url_exist(url)
            if check:
                return render_to_response('main.html',{'url_value':url, 'short':check, 'response_text':site + check}, context_instance=RequestContext(request))

            a = URL(short_url = 'short', long_url = url)
            a.save()
            short = convert(a.id+10000)
            a.short_url = short
            a.save()
            return render_to_response('main.html',{'url_value':url, 'short':short, 'response_text':site + short}, context_instance=RequestContext(request))

def invalid_url(request):
    return HttpResponseRedirect('/')

def redirect_url(request):
    short = request.path
    if short[-1] == '/':
        short = short[:-1]
    short = short[1:]
    url_obj = URL.objects.filter(short_url=short)
    try:
        url = url_obj.get()
        res_string = '''<!DOCTYPE html>
                        <html>
                        <head>
                        <title>urlshot</title>
                        <script type="text/javascript">window.top.location="%s"</script>
                        </head>
                        </html>''' % url.long_url
        #return render_to_response('error.html',{'response_text':res_string}, context_instance=RequestContext(request))
        return HttpResponse(res_string)
    except URL.DoesNotExist:
        return render_to_response('error.html',{'response_text':'That did not match any url in the DB'}, context_instance=RequestContext(request))

def getJSON(request, long_url):
    long_url = 'http://'+long_url
    #return render_to_response('error.html',{'response_text':long_url}, context_instance=RequestContext(request))
    short = url_exist(long_url)
    url = {}
    if short:
        url['short'] = short
        url['long'] = long_url
        url['error'] = 0
        res = json.dumps(url)
        return HttpResponse(res)
    else:
        validate = URLValidator()
        try:
            validate(long_url)
        except ValidationError:
            url['short'] = ''
            url['long'] = ''
            url['error'] = 1
            res = json.dumps(url)
            return HttpResponse(res)

        a = URL(short_url = 'short', long_url = long_url)
        a.save()
        short = convert(a.id+10000)
        a.short_url = short
        a.save()
        url['short'] = short
        url['long'] = long_url
        url['error'] = 0
        res = json.dumps(url)
        return HttpResponse(res)