import os
import environ
from pathlib import Path
import openai
from openai.error import RateLimitError

from .models import Chat
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 

openai_api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = openai_api_key

def ask_openai(message):
    """
    Uses the OpenAI API to generate a response to the given message.

    Args:
        message (str): The message to generate a response for.

    Returns:
        str: The generated response.
    """
    response = openai.ChatCompletion.create(
        model ="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer =  response.choices[0].message.content.strip()
    return answer

def homepage(request):
    """
    Renders the homepage template.

    Args:
        request: The HTTP request object.

    Returns:
        A rendered homepage template.
    """
    return render(request, 'homepage.html')

@login_required
def chatbot(request):
    """
    View function for the chatbot page.

    Retrieves the last 10 chat messages for the logged-in user and displays them on the page.
    If a POST request is received, it processes the user's message, generates a response using the ask_openai function,
    and saves the chat message and response in the database.
    Returns a JSON response with the user's message and the generated response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered chatbot.html template and the chat messages.
        JsonResponse: The JSON response object containing the user's message and the generated response.

    Raises:
        RateLimitError: If the user has exceeded their current quota for OpenAI API requests.
    """
    chats = Chat.objects.filter(user=request.user).order_by('-created_at')[:10]

    if request.method == 'POST':
        message = request.POST.get('message')
        try:
            response = ask_openai(message) 
        except RateLimitError as e:
            return JsonResponse({'error': 'You exceeded your current quota, please contact support and check your plan and billing details.', 'exception': str(e)}, safe=False, status=400)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})

    return render(request, 'chatbot.html', {'chats': chats})

def login(request):
    """
    Authenticates the user and logs them in.

    If a POST request is received, it retrieves the username and password from the request,
    authenticates the user, and logs them in if the credentials are valid.
    If the credentials are invalid, it renders the login page with an error message.
    If a GET request is received, it renders the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered login.html template.

    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = "Invalid Credentials"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    """
    Registers a new user.

    If a POST request is received, it retrieves the username, email, first name, and passwords from the request,
    checks if the username is already taken, and if not, creates a new user with the provided information.
    If the passwords do not match, it renders the register page with an error message.
    If an error occurs during user registration, it renders the register page with an error message.
    If a GET request is received, it renders the register page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object containing the rendered register.html template.

    """
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already taken"
            return render(request, 'register.html', {'error_message': error_message})

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:    
                error_message = "An error occurred during user registration"
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Password not matching"
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    """
    Logs out the user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object redirecting to the login page.

    """
    auth.logout(request)
    return redirect('login')
    


