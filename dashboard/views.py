

from pyexpat.errors import messages

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import ParentProfile

@login_required
def student_dashboard(request):

    parents = ParentProfile.objects.filter(is_approved=True)

    # 🔥 FILTER VALUES
    city = request.GET.get('city')
    service_type = request.GET.get('service_type')
    parent_type = request.GET.get('parent_type')
    max_price = request.GET.get('max_price')

    # 🔥 APPLY FILTERS
    if city:
        parents = parents.filter(city__icontains=city)

    if service_type:
        parents = parents.filter(service_type=service_type)

    if parent_type:
        parents = parents.filter(parent_type=parent_type)

    if max_price:
        parents = parents.filter(price__lte=max_price)

    # 🔥 REQUEST STATUS LOGIC
    requests = Request.objects.filter(student=request.user)

    request_dict = {}

    for req in requests:
        request_dict[req.parent.id] = req.status

    return render(request, 'student_dashboard.html', {
        'parents': parents,
        'request_dict': request_dict
    })

from .models import ParentProfile, Request

@login_required
def parent_dashboard(request):

    try:
        profile = request.user.parentprofile
    except:
        profile = None

    requests = []

    if profile:
        requests = Request.objects.filter(parent=profile)

    return render(request, 'parent_dashboard.html', {
        'profile': profile,
        'requests': requests
    })

from django.shortcuts import render, redirect
from .models import ParentProfile

from django.shortcuts import render, redirect
from .models import ParentProfile

@login_required
def create_parent_profile(request):

    try:
        profile = request.user.parentprofile
    except:
        profile = None

    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        city = request.POST['city']
        parent_type = request.POST['parent_type']
        service_type = request.POST['service_type']
        price = request.POST['price']
        description = request.POST['description']

        photo = request.FILES.get('photo')
        aadhar = request.FILES.get('aadhar')

        if not profile and not aadhar:
            return render(request, 'create_parent_profile.html', {
                'error': 'Aadhar required 🚨',
                'profile': profile
            })

        if profile:
            # UPDATE
            profile.name = name
            profile.age = age
            profile.city = city
            profile.parent_type = parent_type
            profile.service_type = service_type
            profile.price = price
            profile.description = description

            if photo:
                profile.photo = photo
            if aadhar:
                profile.aadhar = aadhar

            profile.save()

        else:
            # CREATE
            ParentProfile.objects.create(
                user=request.user,
                name=name,
                age=age,
                city=city,
                parent_type=parent_type,
                service_type=service_type,
                price=price,
                description=description,
                photo=photo,
                aadhar=aadhar
            )

        return redirect('parent_dashboard')

    return render(request, 'create_parent_profile.html', {
        'profile': profile
    })

from .models import Request, ParentProfile
from django.shortcuts import get_object_or_404

from django.contrib import messages

@login_required
def send_request(request, parent_id):

    parent = get_object_or_404(ParentProfile, id=parent_id)

    if Request.objects.filter(student=request.user, parent=parent).exists():
        messages.warning(request, "You have already sent a request.")
        return redirect('student_dashboard')

    Request.objects.create(
        student=request.user,
        parent=parent
    )

    messages.success(request, "Request sent successfully. The parent may contact you soon.")

    return redirect('student_dashboard')

from django.shortcuts import get_object_or_404

@login_required
def accept_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    req.status = 'accepted'
    req.save()

    return redirect('parent_dashboard')


@login_required
def reject_request(request, request_id):
    req = get_object_or_404(Request, id=request_id)

    req.status = 'rejected'
    req.save()

    return redirect('parent_dashboard')