import os
import re
import requests
import subprocess

def generate_image_url(manga_name, chapter_number, png_number, manga_address):
    base_url = f"https://{manga_address}/manga/{{}}/{{}}-{{:03d}}.png"
    formatted_manga_name = manga_name.replace(" ", "-")
    url = base_url.format(formatted_manga_name, str(chapter_number).zfill(4), png_number)
    return url

def download_image(url, path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {url}")
            return True
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_text_from_html(html_content):
    awk_command = ["awk", "-F=", '/vm\\.CurPathName/ {gsub(/"/, "", $2); if ($2 !~ /^https/) print $2}']
    result = subprocess.run(awk_command, input=html_content, capture_output=True, text=True)

    if result.returncode == 0:
        extracted_text = result.stdout.strip()
        lines_with_us = [line for line in extracted_text.split('\n') if 'us' in line]
        if lines_with_us:
            manga_address = lines_with_us[0].rstrip(';')
            return manga_address
        else:
            print("No line containing 'us' found.")
            return None
    else:
        print("No text between quotation marks found.")
        return None

def extract_text_from_url(manga_name, manga_chapter):
    # Replace spaces with hyphens in the manga_name
    manga_name = manga_name.replace(" ", "-")
    
    url = f"https://manga4life.com/read-online/{manga_name}-chapter-{manga_chapter}.html"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            return extract_text_from_html(html_content)
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def convert_to_pdf(images_folder, output_pdf):
    # List all the image files in the folder
    image_files = [f for f in os.listdir(images_folder) if f.endswith('.png')]
    
    # Sort the image files numerically
    image_files.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    # Create a list of image paths
    image_paths = [os.path.join(images_folder, f) for f in image_files]
    
    # Use ImageMagick's convert command to convert images to PDF
    convert_command = ['convert'] + image_paths + [output_pdf]
    try:
        subprocess.run(convert_command, check=True)
        print(f"PDF generated: {output_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PDF: {e}")

# Example usage
manga_name = input("Enter the manga name: ")
chapter_number = int(input("Enter the chapter number: "))

# Create manga folder
formatted_manga_name = manga_name.replace(" ", "-")
manga_folder = os.path.join(os.getcwd(), formatted_manga_name)
os.makedirs(manga_folder, exist_ok=True)

# Create chapter folder with "Chapter : " prefix
chapter_folder_name = f"Chapter : {str(chapter_number).zfill(4)}"
chapter_folder = os.path.join(manga_folder, chapter_folder_name)
os.makedirs(chapter_folder, exist_ok=True)

# Get the manga address from the HTML
manga_address = extract_text_from_url(manga_name, chapter_number)
if manga_address:
    png_number = 1
    while True:
        url = generate_image_url(manga_name, chapter_number, png_number, manga_address)
        image_filename = "{:03d}.png".format(png_number)
        image_path = os.path.join(chapter_folder, image_filename)

        # Download the image
        if not download_image(url, image_path):
            print("Download Complete")
            break  # Exit the loop if the image download fails

        png_number += 1

    # After downloading all images, rename them
    for i, filename in enumerate(os.listdir(chapter_folder)):
        os.rename(os.path.join(chapter_folder, filename), os.path.join(chapter_folder, f"{formatted_manga_name}_{chapter_number}_{i+1}.png"))

    # Convert images to PDF
    output_pdf = os.path.join(manga_folder, f"{manga_name}: Chapter: {chapter_number}.pdf")
    convert_to_pdf(chapter_folder, output_pdf)
else:
    print("Failed to extract manga address.")

