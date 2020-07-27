from django.shortcuts import render
from django.http import HttpResponse
from django.views.defaults import page_not_found


def index(request):
    return render(request, "index.html")


# handling 404 Error
def handler404(request, exception):
    template_name = '404.html'
    if request.path.startswith('/shop/'):
        template_name = '404_shop.html'
    elif request.path.startswith('/blog/'):
        template_name = '404_blog.html'
    return page_not_found(request, exception, template_name=template_name)
