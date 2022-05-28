from django.shortcuts import render, get_object_or_404 ,redirect,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
 
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = Order.objects.filter(user=request.user.id)
    # print(orders)

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)


@login_required
@csrf_exempt
def add_NewsLetter(request):
    if request.method == 'POST':
        # print("called")
        form = NewsLetterForm(request.POST, request.FILES)
        if form.is_valid():
            newsLetter = form.save()
            print("saved")
            messages.success(request, 'Successfully Subscribed to newsletter!')
            # return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add Email. Please ensure the form is valid.')        
    return redirect("/")



@csrf_exempt
def add_ContactUs(request):
    if request.method == 'POST':
        ContactUs.objects.create(name=request.POST['name'],message=request.POST['message'],email=request.POST['email'],subject=request.POST['subject'])
        messages.success(request, 'Successfully added product!')
        return redirect("/")
              
    template = 'profiles/ContactUsForm.html'

    return render(request, template)