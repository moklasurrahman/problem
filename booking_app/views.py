import json
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from air.forms import SearchFlightForm, SearchMultiFlightForm
from air.models import OrderDetail, Traveler, FlightOffer
from .forms import ProfileChangeForm, ReSendCode, VerifyForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
# from air.flight import Flight
from allauth.account.forms import LoginForm, SignupForm
from allauth.account.utils import get_request_param

from amadeus import Client, ResponseError, Location

from django.core.exceptions import SuspiciousOperation

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

U = get_user_model()

from air.utils import (
    get_currency_code_by_request,
    form_traveler_parameters,
    get_country_by_request,
    get_recommended_airport_from_country,
)
from air.flight import Flight

from .phoneVerification import check, send
from .decorators import phone_verification_not_required, phone_verification_required


def home_page(request):
    # return render(request, 'home.html', {"search_form": SearchFlightForm()})
    return render(request, 'home.html', {"search_form": SearchFlightForm()})


def home_page2(request):
    country = get_country_by_request(request)
    from_airport = ''
    if country:
        from_airport = get_recommended_airport_from_country(country) or ''
    form = SearchFlightForm(initial={'departure_at': from_airport })
    multi_form = SearchMultiFlightForm(initial={'multi_departure_at_0': from_airport})
    
    return render(request, 'home-new.html', {"form": form, "multi_form": multi_form})


def taj(request):
    country = get_country_by_request(request)
    from_airport = ''
    if country:
        from_airport = get_recommended_airport_from_country(country) or ''
    form = SearchFlightForm(initial={'departure_at': from_airport })
    multi_form = SearchMultiFlightForm(initial={'multi_departure_at_0': from_airport})
    
    return render(request, 'taj.html', {"form": form, "multi_form": multi_form})




def terms(request):
    return render(request, 'terms.html', {})

def cookie_policy(request):
    return render(request, 'cookie_policy.html', {})

def privacy_policy(request):
    return render(request, 'privacy_policy.html', {})

def fqa_page(request):
    return render(request, 'fqa.html', {})

def guest_login(request):
    redirect_field_value = get_request_param(request, 'next')
    if request.user.is_authenticated:
        return redirect(redirect_field_value)
    return render(request, 'account/guest.html', {
        "signup_form": SignupForm(),
        "login_form": LoginForm(),
        "redirect_field_value": redirect_field_value or '',
        "redirect_field_name": "next"
    })

def contact_page(request):
    return render(request, 'contact_us.html', {})

def about_us(request):
    return render(request, 'about_us.html', {})

def payment_policy(request):
    return render(request, 'payment_policy.html', {})


def user_profile(request):
    return render(request, 'account/profile.html')


#----------------------------------------------
@login_required
# @phone_verification_required
def my_account(request):
    orders = OrderDetail.objects.filter(user=request.user)
    # flight_offer = FlightOffer.objects.filter(user=request.user).first()
    # traveler = Traveler.objects.filter(flight_offer=flight_offer)
   
    
    books = []
    for order in orders:
        books.append({
            "order_id": order.pk,
            "order_reference_id": order.reference_id,
            "has_paid": order.has_paid,
            "amount": str(order.flight_offer.price) + " " + order.flight_offer.currency,
            "created_on": order.created_on,
            "updated_on": order.updated_on,
            "submited": True if order.reference_id else False
            # "offer": Flight(order.flight_offer.flight).construct_flights()
        })
    return render(request, 'account/account.html', {"books": books})

@login_required
def change_profile(request):
    form = ProfileChangeForm(request.POST)
    user = request.user
    if form.is_valid():
        for key in form.cleaned_data:
            if form.cleaned_data[key]:
                setattr(user, key, form.cleaned_data[key])
        user.save()
        messages.add_message(
            request, messages.SUCCESS, "Updated successfully"
        )
    else:
        messages.add_message(
            request, messages.ERROR, form.errors.as_text()
        )

    return redirect('my_account')

@login_required
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        messages.success(request, 'Your password was successfully updated!')
        return redirect('my_account')
    else:
        for error in form.errors:
            messages.add_message(
                request, messages.ERROR, error + form.errors[error].as_text()
            )
    return redirect('my_account')

@login_required
@phone_verification_not_required
def verify_phone_code_error(request):
    if request.method == 'POST':
        form = ReSendCode(request.POST)
        if form.is_valid():
            send(request.user.username)
            return redirect('verify_phone_code')
    else:
        form = ReSendCode()
    return render(request, 'verify.html', {'form': form, 'phone': request.user.username })

@login_required
@phone_verification_not_required
def verify_phone_code(request):
    context = {
        'phone': request.user.username,
        'resent': False
    }
    if request.method == 'POST':
        if request.POST.get('resend_code', False):
            send(request.user.username)
            context['resent'] = True

        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if check(request.user.username, code):
                request.user.is_phone_verified = True
                request.user.save()
                return redirect('my_account')
            else:
                form.add_error('code', 'Verification code does not match')

        context['form'] = form
    elif request.method == 'GET':
        if request.user.is_phone_verified:
            return redirect('my_account')

        form = VerifyForm()
        context['form'] = form

    return render(request, 'verify.html', context)

def verify_phone_code_ajax(request):
    if not request.user.is_authenticated and request.is_ajax():
        form = VerifyForm(json.loads(request.body))
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if check(request.session['phone'], code):
                try:
                    user = U.objects.get(username=request.session['phone'])
                    if not user.is_phone_verified:
                        user.is_phone_verified = True
                        user.save()
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                except U.DoesNotExist:
                    pass

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False})

    return JsonResponse({'success': False})

def phone_code_ajax(request):
    if not request.user.is_authenticated and request.is_ajax():
        json_data = None
        try:
            json_data = json.loads(request.body)
        except json.JSONDecodeError as e:
            pass

        if json_data and 'login' in json_data and json_data['login']:
            if U.objects.filter(username=json_data['login'].strip()).exists():
                send(json_data['login'].strip())
                request.session['phone'] = json_data['login'].strip()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Phone number does not have an account'})

    return JsonResponse({'success': False})


def verify_phone_code_error_ajax(request):
    if request.method == 'POST':
        send(request.user.username)
    return HttpResponse('')
