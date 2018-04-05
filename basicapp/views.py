from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd
from . import forms
import rpyc
import os
conn = None

@login_required
def index(request):
    return render(request,'basicapp/index.html')

@login_required
def ping_view(request):
    form = forms.PingForm(request.POST)
    if request.method == 'POST':
        try:
            ping_ip = request.POST['ping_ip']
            cmd = "ping "+ping_ip+" -c 3"
            conn.modules.os.system(cmd)
            conn.close()
            return render(request,'basicapp/result.html',{'output':'Ping Success','reasons':' '})
        except:
            return render(request,'basicapp/result.html',{'output':'Ping Failed','reasons':'Unable to ping to target IP'})
    return render(request,'basicapp/form_page.html',{'form':form})

@login_required
def update_view(request):
    try:
        x = conn.modules.platform.system()
        if x == 'Linux':
            cmd = "apt-get update -y"
            conn.modules.os.system(cmd)
        elif x == 'Windows':
            cmd = "xxxxxxx"
            conn.modules.os.system(cmd)
        return render(request,'basicapp/result.html',{'output':'Update Successful'})
    except:
        return render(request,'basicapp/result.html',{'output':'Update Failed'})

@login_required
def operations_menu(request):
    if request.method == 'POST':
        ip_addr = request.POST['ip_address']
        request.session['ip_addr'] = ip_addr
        try:
            global conn
            conn = rpyc.classic.connect(ip_addr)
            rsys = conn.modules.sys
            if 'ping' in request.POST:
                return redirect('/ping/')
            if 'update' in request.POST:
                return redirect('/update/')
        except:
            return render(request,'basicapp/result.html',{'output':'Connection Failure','reasons':'Check the IP again. Make sure that you are inside the network.'})
    return render(request,'basicapp/operations.html')

@login_required
def exec_file(file_name,file_parameters):
    if file_name.endswith('.py'):
        conn.modules.os.system("python "+file_name+" "+file_parameters)
    elif file_name.endswith('.sh'):
        conn.modules.os.system("./"+file_name+" "+file_parameters)

@login_required
def param_form(request):
    ip_addr = request.session['ip_addr']
    l = request.session['l']
    parameters = request.session['param']
    a, b = zip(*parameters)
    a = list(a)
    b = list(b)
    list_fields = zip(a,b)
    file_name = request.session['file_name']
    file_parameters = []
    if request.method == 'POST':
        for i in range(l):
            file_parameters.append(request.POST[a[i]])
        file_parameters = ' '.join(file_parameters)
        try:
            global conn
            try:
                conn = rpyc.classic.connect(ip_addr)
                rsys = conn.modules.sys
            except:
                return render(request,'basicapp/result.html',{'output':'Connection Failure','reasons':'Check the IP again. Make sure that you are inside the network.'})
            f = open("scripts/"+file_name,"r")
            x = conn.modules.platform.system()
            if x == 'Windows':
                # Yet to test working on Windows
                if file_name.endswith('.sh'):
                    return render(request,'basicapp/result.html',{'output':'Invalid Script','reasons':'.sh files can only be run on POSIX type operating systems'})
                else:
                    conn.modules.os.chdir("C:\Windows\Temp")
                    conn.modules.os.mknod(file_name)
                    fh = conn.modules.os.open(file_name,os.O_RDWR)
                    for line in f:
                        conn.modules.os.write(fh,line)
                    conn.modules.os.fdatasync(fh)
                    conn.modules.os.close(fh)
                    exec_file(file_name,file_parameters)
            else:
                if file_name.endswith('.bat'):
                    return render(request,'basicapp/result.html',{'output':'Invalid Script','reasons':'.bat files can be run only on Windows machines. Target system evironment does not support execution of .bat files.'})
                else:
                    conn.modules.os.chdir("/scripts")
                    conn.modules.os.system("pwd")
                    try:
                        conn.modules.os.mknod(file_name)
                    except:
                        conn.modules.os.remove(file_name)
                        conn.modules.os.mknod(file_name)
                    fh = conn.modules.os.open(file_name,os.O_RDWR)
                    for line in f:
                        conn.modules.os.write(fh,line)
                    conn.modules.os.fdatasync(fh)
                    conn.modules.os.close(fh)
                    try:
                        exec_file(file_name,file_parameters)
                    except:
                        return render(request,'basicapp/result.html',{'output':'Execution Failed','reasons':'Check log for more information.'})
            return render(request,'basicapp/result.html',{'output':'Script Execution Complete','reasons':'Check log for more information'})
        except:
            return render(request,'basicapp/result.html',{'output':'Script Execution Failed','reasons':'Check error logs.'})

    return render(request,'basicapp/parameter_form.html',{'ip_addr':ip_addr,'file_name':file_name.split('.')[0],'list_fields':list_fields,'range':range(l)})

@login_required
def file_select(request):
    base_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    script_directory = os.path.join(base_directory,'scripts')
    file_list = sorted(os.listdir(script_directory))
    file_list.remove('scripts.csv')
    target_file_path = None
    local_file_path = None
    param_data = pd.read_csv('scripts/scripts.csv',sep=",",names=['filename','parameters'])
    param_data = param_data.set_index("filename")
    if request.method == 'POST':
        request.session['ip_addr'] = request.POST['ip_address']
        file_name = request.POST['file_radio']
        request.session['file_name'] = file_name
        parameters = param_data.loc[file_name,'parameters']
        parameters = parameters.split(';')
        request.session['param'] = [item.split(':') for item in parameters]
        request.session['l'] = len(parameters)
        return redirect('/param_form/')

    return render(request,'basicapp/file.html',{'file_list':file_list})

@login_required
def add_file(request):
    if request.method == 'POST' and request.FILES['scriptFile']:
        scriptFile = request.FILES['scriptFile']
        fs = FileSystemStorage()
        filename = fs.save(scriptFile.name,scriptFile)
        uploaded_file_url = fs.url(filename)
        request.session['uploaded_filename'] = filename
        n = request.POST['num']
        if n == '0':
            f = open("scripts/scripts.csv","a")
            f.write("{},\n".format(filename))
            f.close()
            return render(request,'basicapp/result.html',{'output':'File upload successful','reasons':'The file was successfully uploaded to the script repository. Now users can run the uploaded script on any machine.'})

        request.session['num'] = n
        return redirect('/add_file/form')
    return render(request,'basicapp/add_file.html')

@login_required
def add_file_form(request):
    n = int(request.session['num'])
    print n
    filename = request.session['uploaded_filename']
    p = []
    if request.method == 'POST':
        for i in range(n):
            p.append(request.POST["label"+str(i)]+":"+request.POST["select"+str(i)])
        parameters = ';'.join(p)
        f = open("scripts/scripts.csv","a")
        f.write(filename+","+parameters+"\n")
        f.close()
    return render(request,'basicapp/add_file_form.html',{'range':range(n),'filename':filename})
