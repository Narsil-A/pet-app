from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from .models import Chat
from userprofile.models import User
from django.conf import settings
 

import openai

openai.api_key=settings.OPENAI_API_KEY

def ask_openai(message, role):
    
    system_message_content = {
        'pet_owner': "You are an assistant helping pet owners with their queries.",
        'vet_staff': "You are a knowledgeable vet staff assistant ready to support veterinary professionals."
    }
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message_content.get(role, "You are an assistant.")},
            {"role": "user", "content": message}
        ],
            max_tokens=250,
            temperature=0.7,
            # Additional parameters for chat-like context may go here
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except Exception as e:
        print(f"Error while calling OpenAI API: {e}")
        return "There was an error processing your request."
    


def chatbot(request):

    if request.user.is_vetstaff:
        role = 'vet_staff'
    elif request.user.is_petowner:
        role = 'pet_owner'
    else:
        role = 'general' 

    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message, role)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone)
        chat.save()

        return JsonResponse({'message': message, 'response': response})
    else:
        return render(request, 'chatbot/chatbot.html', {'chats':chats})



