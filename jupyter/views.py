import glob
import json
import os
import subprocess

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# A global variable to cache the Jupyter URL.
JUPYTER_URL = None


def get_jupyter_url():
    """
    Finds the URL of the running Jupyter server.
    It does this by finding the latest jupyter server connection file.
    """
    global JUPYTER_URL
    # Return from cache if we already found it.
    if JUPYTER_URL:
        return JUPYTER_URL

    try:
        # Get the jupyter runtime directory
        runtime_dir = subprocess.check_output(['jupyter', '--runtime-dir']).strip().decode('utf-8')
        # Find all server files
        server_files = glob.glob(os.path.join(runtime_dir, 'jpserver-*.json'))
        if not server_files:
            return None  # No server running

        # Get the latest server file
        latest_server_file = max(server_files, key=os.path.getctime)

        # Read the server file and extract the URL
        with open(latest_server_file, 'r') as f:
            server_info = json.load(f)

        url = server_info.get('url')
        if url:
            # Cache the URL
            JUPYTER_URL = url
            return JUPYTER_URL

    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        # This can happen if jupyter is not installed, not in PATH, or if the
        # server file is corrupted.
        return None

    return None

@login_required
def notebook_view(request):
    """
    Renders the Jupyter notebooks in an iframe.
    It dynamically finds the jupyter server URL.
    """
    jupyter_url = get_jupyter_url()
    if not jupyter_url:
        # If we can't find the jupyter server, render an error page.
        return render(request, 'jupyter/jupyter_error.html')

    context = {'jupyter_url': jupyter_url}
    return render(request, 'jupyter/jupyter.html', context)

