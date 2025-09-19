from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.templatetags.static import static
# from .models import BridgePhoto # We don't need the model for this temporary solution

@login_required
def photo_gallery(request):
    # --- TEMPORARY SOLUTION ---
    # This is a temporary setup to display hardcoded static images.
    # The correct, long-term solution is to use the BridgePhoto model to manage photos.

    photo_files = ["1.JPG", "2.JPG", "3.JPG", "4.JPG", "5.JPG"] # Displaying 5 as requested

    # Create a list of dictionaries that mimics the structure of a BridgePhoto object
    photos_context = []
    for i, filename in enumerate(photo_files):
        photos_context.append({
            'sfn': f'STATIC-0{i+1}',
            'inspection_id': f'INSP-STATIC-0{i+1}',
            'photo_url': static(filename),
            # For this temporary view, we'll use the main image as the thumbnail
            'thumbnail_url': static(filename),
        })

    # The old database query is commented out below
    # photos = BridgePhoto.objects.order_by('-id')[:5]

    return render(request, 'inspections/photo_gallery.html', {'photos': photos_context})


@login_required
def inspection_list(request):
    """
    Placeholder view for the main inspections list page.
    """
    # This view can be expanded later to show a list of actual inspections.
    return render(request, 'inspections/inspection_list.html')
