from django.template.loader import render_to_string
from django.core.signing import Signer
from django.core.mail import EmailMessage, get_connection

from big_web_view.settings import ALLOWED_HOSTS

signer = Signer()

def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    con = get_connection()
    con.open()
    context = {'user': user, 'host': host, 'sign': signer.sign(user.username)}
    subject = 'Регистрация пользователя'
    body_text = render_to_string('email/activation_letter_body.txt', context)
    #user.email_user(subject, body_text)
    em = EmailMessage(subject = subject, body = body_text,to = [f'{user.email}',])
    con.send_messages([em,])
    con.close()
