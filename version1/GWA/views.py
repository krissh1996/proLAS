# -*- coding: utf-8 -*-

import base64
import smtplib
import binascii
import os
from Crypto.Cipher import XOR
from django.contrib import messages
from django.urls import reverse
from random import randint
from django.conf import settings
#from django.conf.settings import MEDIA_ROOT


from .forms import RegistrationForm, LoginForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# for uploading projects and files
from django.core.files.storage import FileSystemStorage

# main script
import plotly
from plotly import tools
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='udayu1111', api_key='Fp3Qsz4JNIEV8R37PD6N')
import lasio
import os


# for creating the window output
#import webkit
#import gtk, gobject

# encryption key for creating activation key
secret_key = "965874113"
# sender's email address in account verification email
email_address = "uday.u1111@gmail.com"
# sender;s email password
email_password = "therisingsun"

def custom_save(user):
    user.is_active = False
    user.save()

def encrypt(key, plaintext):
    cipher = XOR.new(key)
    return base64.b64encode(cipher.encrypt(plaintext))

# encrypt a string and return :param key:param plaintext: :return: unicode(encryptedtext)


def decrypt(key, ciphertext):
    cipher = XOR.new(key)
    return cipher.decrypt(base64.b64decode(ciphertext))

def send_verification_mail(email, activation_key, msg):
    print("send verificaion mail")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()

    server.starttls()
    #print "Helo"
    server.login(email_address, email_password)
    #print "world"
    server.sendmail(email_address, email, msg)
    #print "hey"
    server.quit()

@login_required(login_url="login/")
def simple_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        #request.session['filename'] = filename
        uploaded_file_url = fs.url(filename)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })


    return render(request, 'simple_upload.html')

@login_required(login_url="login/")
def welcome(request):
    return render(request, "WelcomePage.html")

@login_required(login_url="login/")
def home(request):
    filelist = [x for x in os.listdir("media/") if x.endswith('.las')]
    # print(filelist)
    # for file in filelist:
    #     #print "hello"
    #     print file
    return render(request, "home.html", {'filelist': filelist})


@login_required(login_url="login/")
def submit(request):

    filename = request.session.get('filename', '')
    if filename:
        #l = lasio.read(str(filename))
        l = lasio.read(str(os.path.join('media/', str(filename))))
        curve_mnemonic = []
        curve_descr = []
        for curve in l.curves:
            curve_mnemonic.append(curve.mnemonic)
            curve_descr.append(curve.descr)
            # print("[%s]" % (curve.mnemonic))
            # print("%s\t%s" % (curve.unit, curve.descr))

        # getting the input from the user

        First_Track = request.POST.get('First_Track')
        Second_Track = request.POST.get('Second_Track')
        Third_Track = request.POST.get('Third_Track')

        # converting the input to uppercase
        #first_plot = First_Plot.upper()
        #second_plot = Second_Plot.upper()
        #third_plot = Third_Plot.upper()
        #print first_plot
        #print second_plot
        #print third_plot
        #print(" for Checking purpose",First_Plot)

        # the subplots of the file
        trace0 = go.Scatter(
            x=l[str(First_Track)],
            y=l["DEPT"],
            name=str(First_Track),
        )

        trace1 = go.Scatter(
            x=l[str(Second_Track)],
            y=l["DEPT"],
            name=str(Second_Track)
        )

        trace2 = go.Scatter(
            x=l[str(Third_Track)],
            y=l["DEPT"],
            name=str(Third_Track)
        )

        # n = int(input("Enter the no. of subplots :"))
        fig = tools.make_subplots(rows=1, cols=3, shared_yaxes=True)

        fig.append_trace(trace0, 1, 1)
        fig.append_trace(trace1, 1, 2)
        fig.append_trace(trace2, 1, 3)

        fig['layout']['xaxis3'].update(title=str(Third_Track))
        fig['layout']['xaxis2'].update(title=str(Second_Track)+' OHMM', type='log')
        fig['layout']['xaxis1'].update(title=str(First_Track))
        fig['layout']['yaxis1'].update(title='DEPTH')

        fig['layout'].update(height=2000, width=1300,
                             title='Multiple Subplots with Shared DEPTH(Y-Axis)', plot_bgcolor='#E0E0E0')

        plotly.offline.plot(fig)
         # window output
        '''gobject.threads_init()
        win = gtk.Window()
        view = webkit.WebView()
        view.open(plotly.offline.plot(fig))
        win.add(view)
        win.show_all()
        gtk.main()'''
        return render(request, "submit.html", {'curve_descr': curve_descr, 'curve_mnemonic': curve_mnemonic})

    else:
        return redirect('simple_upload')

@login_required(login_url="login/")
def plot(request):
    filename = request.POST['file']
    request.session['filename'] = filename
    print filename
    curve_mnemonic = []
    curve_descr = []
    if filename:
        print "hello"
        #print os.path.join('media/', str(filename))
        l = lasio.read("media/" + str(filename))
        print "heyey"
        for curve in l.curves:
            curve_mnemonic.append(curve.mnemonic)
            curve_descr.append(curve.descr)
            # print("[%s]" % (curve.mnemonic))
            # print("%s\t%s" % (curve.unit, curve.descr))

    return render(request, "plot.html", {'curve_descr': curve_descr, 'curve_mnemonic': curve_mnemonic})

@login_required(login_url="login/")
def crossplot(request):
    filename = request.POST['file']
    request.session['filename'] = filename
    print filename
    curve_mnemonic = []
    curve_descr = []
    if filename:
        print "hello"
        #print os.path.join('media/', str(filename))
        l = lasio.read("media/" + str(filename))
        print "heyey"
        for curve in l.curves:
            curve_mnemonic.append(curve.mnemonic)
            curve_descr.append(curve.descr)
            # print("[%s]" % (curve.mnemonic))
            # print("%s\t%s" % (curve.unit, curve.descr))

    return render(request, "crossplot.html", {'curve_descr': curve_descr, 'curve_mnemonic': curve_mnemonic})

@login_required(login_url="login/")
def any(request):
    filelist = [x for x in os.listdir("media/") if x.endswith('.las')]
    # print(filelist)
    # for file in filelist:
    #     #print "hello"
    #     print file
    return render(request, "any.html", {'filelist': filelist})



@login_required(login_url="login/")
def doublesubmit(request):

    filename = request.session.get('filename', '')
    if filename:
        #l = lasio.read(str(filename))
        l = lasio.read(str(os.path.join('media/', str(filename))))
        curve_mnemonic = []
        curve_descr = []
        for curve in l.curves:
            curve_mnemonic.append(curve.mnemonic)
            curve_descr.append(curve.descr)
            # print("[%s]" % (curve.mnemonic))
            # print("%s\t%s" % (curve.unit, curve.descr))

        # getting the input from the user

        First_Track = request.POST.get('First_Track')
        Second_Track = request.POST.get('Second_Track')


        # converting the input to uppercase
        #first_plot = First_Plot.upper()
        #second_plot = Second_Plot.upper()
        #third_plot = Third_Plot.upper()
        #print first_plot
        #print second_plot
        #print third_plot
        #print(" for Checking purpose",First_Plot)

        # the subplots of the file
        trace0 = go.Scatter(
            x=l[str(First_Track)],
            y=l[str(Second_Track)],
            mode='markers',
            name='Gamma Ray'
        )

        # n = int(input("Enter the no. of subplots :"))
        fig = tools.make_subplots(rows=1, cols=1, shared_yaxes=True)

        fig.append_trace(trace0, 1, 1)


        fig['layout']['xaxis1'].update(title=str(First_Track))
        fig['layout']['yaxis1'].update(title=str(Second_Track))

        fig['layout'].update(height=700, width=700,
                             title='Cross PLOT', plot_bgcolor='#F5F5F5')

        plotly.offline.plot(fig)
         # window output
        '''gobject.threads_init()
        win = gtk.Window()
        view = webkit.WebView()
        view.open(plotly.offline.plot(fig))
        win.add(view)
        win.show_all()
        gtk.main()'''
        return render(request, "submit.html", {'curve_descr': curve_descr, 'curve_mnemonic': curve_mnemonic})

    else:
        return redirect('simple_upload')

def index(request):
    return render(request, "index.html")

def user_login(request):
    return render(request, 'user_login.html',{'form': form})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) #This will be used in POST request
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            custom_save(user)

            activation_key = encrypt(secret_key, user.email)
            # sending account verification mail
            #activation_key =
            message = "Your email address is" + user.email + "activation key is " + activation_key.decode("utf-8")
            # message = "Reset link is  Emahere"
            send_verification_mail(user.email, activation_key, message)
            return HttpResponseRedirect(reverse("activate"))

    else:

        form = RegistrationForm()
    return render(request, 'user_reg.html', {'form': form})

def activate(request):
    # handle for user account activation:param request::return: httpresponseredirect or rendered html

    if request.method == "POST":
        email = request.POST.get("email")
        activation_key = request.POST.get("activation-key")
        # verifying thw activation key
        try:
            decoded = decrypt(secret_key, activation_key)
            decoded = decoded.decode("utf-8")
        except binascii.Error:
            decoded = None

        if email == decoded:
            user = User.objects.get(email=email)
            if user is None:
                messages.error(request, "This email id is not valid")
                return render(request, 'activation_form.html')
            # activating the user
            else:
                user.is_active = True
                user.save()
                login(request, user)

                messages.success(request, "Your Account Has been Activated..")
                return render(request, 'successfull_activation.html', {})

        else:
            messages.error(request, "Wrong activation key")

    return render(request, 'activation_form.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = randint(10000000,99999999)

        message = "Your new password is " + str(new_password)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            user.set_password(new_password)
            user.save()
            send_verification_mail(email, new_password, message)
            return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, 'Sorry no user exist with this email address')
            return render(request, "reset_password.html")

    else:
        return render(request, "reset_password.html")

@login_required(login_url="login/")
def change_password(request):
    user = request.user
    if request.method == 'POST':
        username = user.username
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_again = request.POST.get("new_password_again")
        user = authenticate(username=username, password=old_password)
        if user is not None:
            if new_password == new_password_again:
                user.set_password(new_password)
                user.save()
                login(request,user)
                return HttpResponseRedirect(reverse("home"))
            else:
                messages.error(request, "both passwords you entered did not match")
                return render(request, 'change_password.html', {'user': user})
        else:
            messages.error(request, "sorry the password you entered is not correct")
            return render(request, 'change_password.html', {'user': user})
    else:
        return render(request, 'change_password.html', {'user': user})

