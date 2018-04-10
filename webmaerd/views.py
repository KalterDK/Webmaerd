from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import *


def render_tamplate(tpl, dt, request):
    """

    :param tpl: html template
    :param dt: dictionary to send
    :param request: HTTP request
    :return: HTML with base
    """
    dct = {}
    dct.update(dt)
    return render(request, tpl, dct)


def contact(request):
    if request.method == 'POST':
        cform = ContactForm(request.POST)

        if request.method == 'POST' and cform.is_valid():

            name = cform.cleaned_data['name']
            email = cform.cleaned_data['email']
            phone = cform.cleaned_data['phone']
            subject = cform.cleaned_data['subject']
            message = cform.cleaned_data['message']
            recipients = ['info@webmaerd.com']

            try:
                send_mail("[WEBMAERD] Contact From Message",
                          "Subject: %s \n\nName: %s \nEmail: %s \nPhone: %s \n\nMessage: %s"
                          "\n\nPlease don't reply to this message. "
                          "For the answer use the e-mail specified by the client."
                          % (subject, name, email, phone, message), 'info@webmaerd.com', recipients)
                send_mail(
                    '[WEBMAERD] Thank you for contacting',
                    'Thank you for contacting us.\nWe will contact with you shortly.\nRegards,\nWEBMAERD Team.',
                    'info@webmaerd.com',
                    [cform.cleaned_data['email']],
                )

            except BadHeaderError:
                return HttpResponse('Invalid header found')

            return redirect('/success_page')

    else:
        cform = ContactForm()

        return render_tamplate('contact.html', {'cform': cform}, request)