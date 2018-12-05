# Write functions for sending email here.
from django.core.mail import send_mail
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required

from core.models import Bibtex
#from .const import address


@login_required
def send_email_test():
    # 件名
    subject = "Please update the registration information."

    # 本文
    message = "The following papers have missing items.\n\n\n"

    not_published_list = Bibtex.objects.filter(is_published=False)
    mail_template = get_template('notification/mail_templates/mail_basic.txt')
    for bib in not_published_list:
        book = Bibtex.objects.get(id=bib.id).book
        context = {
            "bib": bib,
            "book": book,
        }
        message = message + mail_template.render(context) + "\n"

    # 送信元
    #from_email = "test@test.com"

    from_email = "settings.EMAIL_HOST_USER"

    # あて先
    recipient_list = address

    return send_mail(subject, message, from_email, recipient_list)


def send_email_to_appointed_address(address, bibtex):
    # 件名
    subject = "Please update the registration information."

    # 本文
    message = "The following papers have missing items.\n\n\n"

    mail_template = get_template('notification/mail_templates/mail_basic.txt')

    context = {
            "bib": bibtex,
            "book": bibtex.book,
    }
    
    message = message + mail_template.render(context) + "\n"

    # 送信元
    #from_email = "test@test.com"

    from_email = "settings.EMAIL_HOST_USER"

    # あて先
    recipient_list = [address]

    return send_mail(subject, message, from_email, recipient_list)


def send_email_to_all():
    # 件名
    subject = "Please update the registration information."

    # 本文

    from_email = "settings.EMAIL_HOST_USER"

    not_published_list = Bibtex.objects.filter(is_published=False)
    bad_status = []

    for bib in not_published_list:
        message = "The following papers have missing items.\n\n\n"
        mail_template = get_template('notification/mail_templates/mail_basic.txt')
        book = bib.book
        if len(bib.authors.all()) == 0:
            continue

        address = bib.authors.all()[0].mail

        if address == None:
            continue

        context = {
            "bib": bib,
            "book": book,
        }

        message = message + mail_template.render(context) + "\n"
        status = send_mail(subject, message, from_email, [address])
        if status == False:
            bad_status.append((address, book))

    if len(bad_status) == 0:
        status = "Success"
    else:
        status = bad_status
    return status, not_published_list