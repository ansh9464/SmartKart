from django.shortcuts import render , redirect
from django.http import HttpResponse
from . models import Blogpost , Contactus
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User


# HTML pages.
def index(request):
    blogs = Blogpost.objects.all()
    return render(request,'blog/index.html',{'blogs':blogs})

def blogpost(request,id):
    blog = Blogpost.objects.filter(post_id=id)
   # print(blog)
    return render(request,'blog/blogpost.html',{'blog':blog[0]})

def contactus(request):
    if request.method =='POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        if len(name)<=2 or len(email)<=12 or len(phone)<=9 or len(desc)<=3:
            messages.error(request, 'Please Fill the form with correct details')
        else:
            messages.success(request, 'Thanks Our team will contact you soon')
            contact = Contactus(name=name,email=email,phone=phone,desc=desc)
            contact.save()
            thank=True
            return render(request,'blog/contactus.html',{'thank':thank})
    return render(request,'blog/contactus.html')

def aboutus(request):
    return render(request,'blog/about.html')

def searchmatch(query,item):
    if query in item.title.lower():
        return True
    else:
        return False

#APIs for verification
def search(request):
    query = request.GET.get('search')
    if len(query)>90:
        messages.error(request,'Enter correct search keyword to get results')
        blogs = Blogpost.objects.none()
    else:
        blogstitle = Blogpost.objects.filter(title__icontains=query)
        blogscontent = Blogpost.objects.filter(chead0__icontains=query)
        blogs = blogstitle.union(blogscontent)
    #blog_item = [item for item in blogs if searchmatch(query.lower(),item)]
    return render(request,'blog/search.html',{'blogs':blogs,'query':query})

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')

        #creating checks
        if not username.isalnum():
            messages.error(request,'Username can only contains alphabets and numbers')
            return redirect('BlogHome')

        if  len(username)>10:
            messages.error(request,"Username can't exceed 10 characters")
            return redirect('BlogHome')

        if pass1!=pass2:
            messages.error(request,'Please enter password correctly')
            return redirect('BlogHome')

        #creating user
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = name
        myuser.save()
        messages.success(request,'Your account is succesfully created')
        return redirect('BlogHome')

    else:
        return HttpResponse('Error-404 page not found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername', '')
        loginpassword = request.POST.get('loginpass', '')
        user = authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Succesfully Loged In')
            return redirect('BlogHome')
        else:
            messages.error(request,"Invalid Login credentials")
            return redirect('BlogHome')
    return HttpResponse('Error-404 page not found')

def handleLogout(request):
    logout(request)
    messages.success(request,"Succesfully logged out")
    return redirect('BlogHome')