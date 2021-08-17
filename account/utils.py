from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_activation_code(email, activation_code, status):
    if status == 'register':
        context = {
            'text_detail': 'Thanks for your registration!',
            'email': email,
            'domain': 'http://localhost:8000',
            'activation_code': activation_code
        }
        msg_html = render_to_string('email.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate Your account',
            message,
            'stackoverflow@gmail.com',
            [email, ],
            html_message=msg_html,
            fail_silently=False
        )
    elif status == 'reset_password':
        send_mail(
            'Reset your password',
            f'Code activations: {activation_code}',
            'stackoverflow@gmail.com',
            [email, ],
            fail_silently=False
        )
