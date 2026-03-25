from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

User = get_user_model()



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        role = request.POST['role']

        
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username already taken 😅'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            phone=phone
        )

        return redirect('login')

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            
            if user.role == 'student':
                return redirect('student_dashboard')
            else:
                return redirect('parent_dashboard')

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

from django.contrib.auth import logout
from django.shortcuts import redirect
def logout_view(request):
    logout(request)
    return redirect('login')
