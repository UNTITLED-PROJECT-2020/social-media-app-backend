from django.shortcuts import render

# Create your views here.


def home(request):  # home url
    return render(request, 'home/index.html', {})


def start(request):  # quick start url
    return render(request, 'home/start.html', {})


def components(request):  # components url
    return render(request, 'home/components.html', {})


def charts(request):  # charts url
    return render(request, 'home/charts.html', {})


def faqs(request):  # faqs url
    return render(request, 'home/faqs.html', {})


def showcase(request):  # showcase url
    return render(request, 'home/showcase.html', {})


def license(request):  # license url
    return render(request, 'home/license.html', {})
