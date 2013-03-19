#!/usr/bin/python
from flask import Flask, request, render_template
from flask.ext.wtf import Form, TextField, html5, Required
from optparse import OptionParser
from email.mime.text import MIMEText
import smtplib
import settings

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", default=5000, 
    help="Port to listen on", type="int")
parser.add_option("-l", "--listen", dest="listen", default="127.0.0.1", 
    help="Address to listen on", type="string")

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY

class ContactForm(Form):
  email = html5.EmailField(validators=[Required()])
  message = TextField(validators=[Required()]) 

@app.route('/', methods=['POST'])
def send():
  form = ContactForm(request.form)
  if form.validate():
    print "ALL OK, SEND EMAIL"
    message = "Email: %s -- Message: %s" % (form.email.data, form.message.data)
    msg = MIMEText(message, 'text')
    msg['Subject'] = settings.EMAIL_SUBJECT
    msg['From'] = settings.SMTP_USER
    msg['To'] = settings.SMTP_USER
    smtp = None
    if settings.SMTP_TLS:
      smtp = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
    else:
      smtp = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
    smtp.sendmail(settings.SMTP_USER, [settings.SMTP_USER], msg.as_string())
    smtp.quit()
  return render_template('index.html', settings=settings, form=form)
  
@app.route('/')
def index():
  form = ContactForm()
  return render_template('index.html', settings=settings, form=form)

if __name__ == "__main__":
    (options, args) = parser.parse_args()
    app.debug = True
    app.run(host=options.listen, port=options.port)
