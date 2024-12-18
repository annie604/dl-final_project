from google.cloud import vision
from dotenv import load_dotenv
import os



# Path to the image you want to analyze
image_path = 'image.png'

# Load environment variables
load_dotenv()
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(f"Credentials path: {credentials_path}")

if credentials_path is None:
    raise ValueError("The GOOGLE_APPLICATION_CREDENTIALS environment variable is not set correctly.")


# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

# Open the image file
with open(image_path, 'rb') as image_file:
    content = image_file.read()

# Prepare the image for analysis
image = vision.Image(content=content)

# Perform label detection on the image
response = client.label_detection(image=image)
labels = response.label_annotations

# Print out the labels detected in the image
for label in labels:
    print(label.description)
