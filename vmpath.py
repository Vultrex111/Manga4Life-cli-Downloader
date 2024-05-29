import re
import requests
import subprocess

def extract_text_from_html(html_content):
    awk_command = ["awk", "-F=", '/vm\.CurPathName/ {gsub(/"/, "", $2); if ($2 !~ /^https/) print $2}']
    result = subprocess.run(awk_command, input=html_content, capture_output=True, text=True)

    if result.returncode == 0:
        extracted_text = result.stdout.strip()
        print(extracted_text)
    else:
        print("No text between quotation marks found.")

def extract_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            extract_text_from_html(html_content)
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Prompt the user to enter a URL
url = input("Enter the URL: ")
extract_text_from_url(url)

