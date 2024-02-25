from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from Users.models import UserProfile
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, "Users/index.html")

@login_required
def home(request):
    
    return render(request, "Users/home.html",{'user':request.user.username})
    
    
    
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        current_weight =  request.POST.get('current_weight')
        height = request.POST.get('height') 
        activity_level = request.POST.get('activity_level')  
        goal = request.POST.get('goal')    
        
        myuser = User.objects.create_user(username=username,password=password, email=email,first_name=fname,last_name=lname)
        myuser.save()
        
        myuserprofile = UserProfile(user=myuser,age=age,gender=gender,current_weight=current_weight,
                                    height=height,activity_level=activity_level,goal=goal)
        myuserprofile.save()
        messages.success(request, "User added successfully")
        return redirect('signin')

    return render(request, 'Users/signup.html')
    
    
    
def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        
        if user is not None:
            username = user.get_username
            login(request,user)
            return redirect('home')
            
        else:
            messages.error(request,"Invalid Username or Password")
            
       
    return render(request, 'Users/signin.html')
    
@login_required
def modifyuser(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        new_weight = request.POST.get('weight')
        new_height = request.POST.get('height')
        new_activity_level = request.POST.get('activity_level')
        new_goal = request.POST.get('goal')
        updated_weight = user_profile.current_weight
        updated_height = user_profile.height
        updated_activity_level = user_profile.activity_level
        updated_goal = user_profile.goal
        if new_weight != 0:
            updated_weight = new_weight
        if new_height != 0:
            updated_height = new_height
        if new_activity_level is not None:
            updated_activity_level = new_activity_level
        if new_goal is not None:
            goal = new_goal
        UserProfile.objects.filter(user=request.user).update(
            current_weight=updated_weight,
            height=updated_height,
            activity_level=updated_activity_level,
            goal=updated_goal
        )
      
        messages.success(request, "User updated successfully")
        #to make the updated values appear in html
        user_profile.current_weight = updated_weight
        user_profile.height = updated_height
        user_profile.activity_level = updated_activity_level
        user_profile.goal = updated_goal
        
    return render(request, 'Users/modifyuser.html',{'user_profile': user_profile})
    
    
def signout(request):
    logout(request)
    return redirect("index")

