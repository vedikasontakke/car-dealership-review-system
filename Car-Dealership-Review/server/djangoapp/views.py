from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import (
    login,
    logout,
    authenticate
)
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapis import (
    get_dealers_from_cf,
    get_dealer_reviews_from_cf,
    post_request,
)

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request


def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("djangoapp:index")

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username,
                                            first_name=first_name,
                                            last_name=last_name,
                                            password=password)
            # Login the user and redirect to index
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "http://localhost:3000/dealerships/get"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        context["dealers"] = dealerships

        return render(request, 'djangoapp/index.html', context)


# render the reviews of a dealer
def get_dealer_details(request, id):
    if request.method == "GET":
        url = "http://localhost:5000/api/get_reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, id)
        context = {
            "reviews": dealer_reviews
        }

        return render(request, 'djangoapp/dealer_details.html', context)



# submit a review
def add_review(request):

    if request.method == "GET":
        url = "http://localhost:3000/dealerships/get"
        cars = get_dealers_from_cf(url)
        context = {
            "cars": cars
        }
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        csrf_token = get_token(request)

        url = "http://localhost:5000/api/post_review"
        review = {
            "id": 1114,
            "name": "Upkar Lidder",
            "dealership": 15,
            "review": "Great service!",
            "purchase": False,
            "another": "field",
            "purchase_date": "02/16/2021",
            "car_make": "Audi",
            "car_model": "Car",
            "car_year": 2021
        }

        headers = {
            "X-CSRFToken": csrf_token
        }

        status = post_request(url, json_payload=review, headers=headers)
        if status:
            return HttpResponse("Review added successfully")
        else:
            return HttpResponse("Failed to add review")
    else:
        return HttpResponse("Failed to add review")
