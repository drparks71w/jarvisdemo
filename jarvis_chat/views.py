from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
import json
import os
import google.generativeai as genai
import markdown  # Add this import

# A simple function to find relevant context from your sources
def find_relevant_context(message):
    """
    Searches through files in the 'sources' directory for the message content.
    Returns the content of the first file that contains the message as context.
    This is a very basic implementation for demonstration purposes.
    """
    sources_dir = os.path.join(settings.BASE_DIR, 'sources')
    if not os.path.exists(sources_dir):
        return "" # Return empty if sources directory doesn't exist

    try:
        # A simple keyword search
        keywords = message.lower().split()
        for filename in os.listdir(sources_dir):
            if filename.endswith(".txt"): # Assuming .txt files
                filepath = os.path.join(sources_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(keyword in content.lower() for keyword in keywords):
                        # Return the first 4000 characters of the relevant file as context
                        return content[:4000]
    except Exception as e:
        print(f"Error reading sources: {e}")

    return "" # Return empty string if no context is found

@login_required
def jarvis_view(request):
    """
    Renders the Jarvis chat page.
    """
    return render(request, 'jarvis_chat/jarvis.html')


@login_required
def ask_notebook(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message')

        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

        try:
            # Configure the Gemini API key
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            # Use the latest model as you suggested
            model = genai.GenerativeModel('gemini-2.5-pro')

            # 1. Retrieve: Find context from your local files
            context = find_relevant_context(user_message)

            # 2. Augment: Create a prompt with the context
            if context:
                prompt = f"Based on the following context, please answer the user's question.\n\nContext:\n---\n{context}\n---\n\nUser Question: {user_message}"
            else:
                prompt = user_message # Fallback to just the user message if no context is found

            # 3. Generate: Call the Gemini API
            response = model.generate_content(prompt)

            # Convert the markdown response to HTML
            html_reply = markdown.markdown(response.text)

            return JsonResponse({'reply': html_reply})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
