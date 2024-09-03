from django.shortcuts import render,redirect
from newresume.forms import UserForm,SigninForm,LoginForm
from django.http import HttpResponse
from newresume.models import SignIn,LogIn
from reportlab.pdfgen import canvas
from django.contrib.auth import authenticate, login
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


# Create your views here.

def newResume(request):
    form=UserForm
    values={'form':form}
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            return homepage(request)

    return render(request,'newresume/newresume.html',values)


def signin(request):
    form1=SigninForm
    dict1={'form1':form1}
    if request.method=='POST':
        form1=SigninForm(request.POST)
        if form1.is_valid():
            na=form1.cleaned_data['name1']
            mail=form1.cleaned_data['mail']
            password3 = form1.cleaned_data['password']
            password4= form1.cleaned_data['password1']
            if SignIn.objects.filter(mail=mail).exists():
                return HttpResponse("Email already exists.Please click on log in to continue")
                
            if password3==password4:
                form1.save()
                return redirect('/newresume')

            else:
                return HttpResponse("password didnt match")
    return render(request,'newresume/signin.html',dict1)

def login(request):
    form2=LoginForm
    dict2={'form2':form2}
    if request.method=='POST':
        form2=LoginForm(request.POST)
        if form2.is_valid():
            username=request.POST['user_mail']
            password3=request.POST['user_password']
            user = authenticate(request, username=username, password=password3)
            a=f"Email: {username}"
            b=f"Password: {password3}"
            print(a,b)
            print(user)
            if user is  not None:
                form2.save()
                return redirect('/newresume')
            else:
                return HttpResponse('You did not have any account in Resume Bilder.Please Sign In to continue')
            
    return render(request,'newresume/login.html',dict2)



def homepage(request):
    return render(request,"index.html")

def generatepdf(request):
     # Extract data from the POST request
    name = request.POST.get('name')
    email = request.POST.get('email')
    contact = request.POST.get('contact')
    school = request.POST.get('school')
    degree = request.POST.get('degree')
    skills = request.POST.get('skills')
    about_you = request.POST.get('about_you')
    experience = request.POST.get('experience')

    # Context data for rendering the HTML template
    context = {
        'name': name,
        'email': email,
        'contact': contact,
        'school': school,
        'degree': degree,
        'skills': skills,
        'about_you': about_you,
        'experience': experience,
    }

    # Render the HTML template
    template = get_template('resume_template.html')  # Replace 'your_default_template.html' with the actual template name
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    # Generate PDF from the HTML content
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    # If PDF generation failed, return an error
    if pisa_status.err:
        return HttpResponse('PDF generation failed!')

    return response        
