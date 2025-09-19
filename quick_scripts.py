from PIL import Image, ImageEnhance

# Path to your image
image_path = 'static/bg.png'

try:
    # Open the image
    img = Image.open(image_path)

    # To make the image less vivid, we can reduce its color saturation.
    # A factor of 0.0 will make it completely grayscale.
    # A factor of 1.0 is the original image's saturation.
    # We'll use a value in between to create a desaturated look.
    enhancer = ImageEnhance.Color(img)
    img_desaturated = enhancer.enhance(0.2)  # Adjust this value between 0.0 and 1.0

    # Save the modified image, overwriting the original
    img_desaturated.save(image_path)

    print(f"Successfully desaturated the image: {image_path}")

except FileNotFoundError:
    print(f"Error: The file could not be found at {image_path}")
except Exception as e:
    print(f"An error occurred: {e}")
