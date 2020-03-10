from threading import Thread

from flask import current_app, render_template
from flask_mail import Mail, Message


def thread_task(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, filename, **kwargs):
    app = current_app._get_current_object()
    mail = Mail(app)
    msg = Message(subject=subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to])

    msg.html = render_template(filename + '.html', **kwargs)
    thread = Thread(target=thread_task, args=(app, mail, msg))
    thread.start()
    return thread
