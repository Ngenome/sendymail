import json
from django.http import HttpResponse
from django.shortcuts import render

from django.conf import settings
from django.core.mail import send_mail

from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend



@csrf_exempt
def index(request):
    # default recipient is in settings.py
    if request.method == 'GET':
        return HttpResponse("GET is not allowed")
    if request.method == 'OPTIONS':
        return HttpResponse('''
        <h1>SendyMail</h1>
        <p>SendyMail is an API that allows you to send emails from your application. 
        It is built using Django and Django Rest Framework</p>
        <h2>How to use</h2>
        <p>SendyMail uses a POST request to send emails. The request body must be in JSON format</p>
        <h3>Request Body</h3>
        <ul>
            <li>recipients: This is a list of recipients. If you want to use the default recipient, leave this field blank</li>
            <li>mode: This is the mode of sending the email. It can either be default or custom. If you choose custom, you must provide the following fields: host, port, username, password, use_tls and fail_silently</li>
            <li>subject: This is the subject of the email</li>
            <li>message: This is the message of the email</li>
            <li>host: This is the host of the email server</li>
            <li>port: This is the port of the email server</li>
            <li>username: This is the username of the email server</li>
            <li>password: This is the password of the email server</li>
            <li>use_tls: This is a boolean that specifies if TLS should be used or not</li>
            <li>fail_silently: This is a boolean that specifies if the email should fail silently or not</li>
        </ul>
<h3>Example Request Body</h3>
{
    "recipients": [],
    "mode": "default",
    "subject": "Test Email",
    "message": "This is a test message",
    "host": "",
    "port": "",
    "username": "",
    "password": "",
    "use_tls": True,
    "fail_silently": False,

}


        

        ''')

    body = json.loads(request.body)
    email_from = settings.EMAIL_HOST_USER
    custom_recipients = body["recipients"]
    recipient_list = ["ngenondumia@gmail.com", ]
    recipient = body["recipient"]
    mode = body["mode"]
    # check if the recipient is not none

    if custom_recipients is not None:
        if custom_recipients == True:
            recipient_list = []
            for recipient in body["recipients"]:
                recipient_list.append(recipient)
        else:
            pass

    # check if the mode is default or custom
    if mode not in ["default", "custom"]:
        return HttpResponse("<h1>500 Internal Server Error</h1> <p>Mode must be either default or custom. Please check your request body and try again</p>", status=500)
    
    if mode=="default":
        pass
    elif mode=="custom":
        host = body["host"]
        port = body["port"]
        username = body["username"]
        password = body["password"]
        use_tls = body["use_tls"]
        fail_silently = body["fail_silently"]
        # check if all the fields are not none and if any is none, return an 500 error
        if host is None or port is None or username is None or password is None or use_tls is None or fail_silently is None:
            return HttpResponse("<h1>500 Internal Server Error</h1> <p>One or more fields are missing. Please check your request body and try again</p>", status=500)
        # check if the port is an integer
        try:
            port = int(port)
        except:
            return HttpResponse("<h1>500 Internal Server Error</h1> <p>Port must be an integer. Please check your request body and try again</p>", status=500)
        # check if the use_tls and fail_silently are boolean
        if use_tls not in [True, False] or fail_silently not in [True, False]:
            return HttpResponse("<h1>500 Internal Server Error</h1> <p>use_tls and fail_silently must be boolean. Please check your request body and try again</p>", status=500)
        # send email using the custom settings
        email = EmailMessage(body["subject"], body["message"], email_from, recipient_list)
        email.send(fail_silently=fail_silently, auth_user=username, auth_password=password, connection=EmailBackend(host=host, port=port, use_tls=use_tls, username=username, password=password))
        return HttpResponse("Hello, world. successfully sent the email.")
    
    


    if request.method == 'GET':
        return HttpResponse("GET is not allowed")
    elif request.method == 'POST':
        try:
            send_mail(body["subject"], body["message"],
                      email_from, recipient_list)
            return HttpResponse("Hello, world. successfully sent the email.")
        except Exception as e:
            print(e)
            return HttpResponse(f"<h1>An exception occurred</h1> {e}")
