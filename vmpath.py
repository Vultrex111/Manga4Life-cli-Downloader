import re
import requests
import subprocess

def extract_text_from_html(html_content):
    awk_command = ["awk", "-F=", '/vm\.CurPathName/ {gsub(/"/, "", $2); if ($2 !~ /^https/) print $2}']
    result = subprocess.run(awk_command, input=html_content, capture_output=True, text=True)

    if result.returncode == 0:
        extracted_text = result.stdout.strip()
        lines_with_us = [line for line in extracted_text.split('\n') if 'us' in line]
        if lines_with_us:
            mangaAddress = lines_with_us[0].rstrip(';')
            print(mangaAddress)
        else:
            print("No line containing 'us' found.")
    else:
        print("No text between quotation marks found.")

def extract_text_from_url(manga_name, manga_chapter):
    # Replace spaces with hyphens in the manga_name
    manga_name = manga_name.replace(" ", "-")
    
    url = f"https://manga4life.com/read-online/{manga_name}-chapter-{manga_chapter}.html"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            extract_text_from_html(html_content)
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Prompt the user to enter the Manga Name and Manga Chapter
manga_name = input("Enter the Manga Name: ")
manga_chapter = input("Enter the Manga Chapter: ")

extract_text_from_url(manga_name, manga_chapter)

