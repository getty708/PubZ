# Write functions for sending email here.
from django.core.mail import send_mail
from django.template.loader import get_template
from core.models import Bibtex

def send_email_test():
    # 件名
    subject = "Please update the registration information."

    # 本文
    message = "The following papers have missing items.\n"

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
    from_email = "test@test.com"

    #from_email = "settings.EMAIL_HOST_USER"

    # あて先
    recipient_list = [
        "test@test.com"
    ]

    return send_mail(subject, message, from_email, recipient_list)
