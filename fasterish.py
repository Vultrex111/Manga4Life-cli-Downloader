import re
import requests
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def generate_image_url(manga_name, chapter_number, png_number, manga_address):
    base_url = f"https://{manga_address}/manga/{{}}/{{}}-{{:03d}}.png"
    formatted_manga_name = manga_name.replace(" ", "-")
    url = base_url.format(formatted_manga_name, str(chapter_number).zfill(4), png_number)
    return url

def download_image(session, url, path):
    try:
        response = session.get(url, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {url}")
            return True
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_text_from_html(html_content):
    pattern = re.compile(r'vm\.CurPathName\s*=\s*"([^"]+)"')
    matches = pattern.findall(html_content)
    if matches:
        for match in matches:
            if 'us' in match:
                return match
    print("No line containing 'us' found.")
    return None

def extract_text_from_url(session, manga_name, manga_chapter):
    manga_name = manga_name.replace(" ", "-")
    url = f"https://manga4life.com/read-online/{manga_name}-chapter-{manga_chapter}.html"
    response = session.get(url)
    if response.status_code == 200:
        html_content = response.text
        return extract_text_from_html(html_content)
    else:
        print(f"Error: {response.status_code}")
        return None

def download_chapter_images(session, args):
    manga_name, chapter_number, manga_address, chapter_folder = args
    png_number = 1
    while True:
        url = generate_image_url(manga_name, chapter_number, png_number, manga_address)
        image_filename = "{:03d}.png".format(png_number)
        image_path = chapter_folder / image_filename
        if not download_image(session, url, image_path):
            print(f"Download of Chapter {chapter_number} Complete")
            break
        png_number += 1

def main():
    manga_name = input("Enter the manga name: ").title()
    input_chapters = input("Enter the chapter number(s) separated by commas: ")
    chapters_to_download = [int(chapter.strip()) for chapter in input_chapters.split(",")]

    formatted_manga_name = manga_name.replace(" ", "-")
    manga_folder = Path(formatted_manga_name)
    manga_folder.mkdir(exist_ok=True)

    with requests.Session() as session:
        with ThreadPoolExecutor() as executor:
            for chapter_number in chapters_to_download:
                chapter_folder_name = f"Chapter: {str(chapter_number).zfill(4)}"
                chapter_folder = manga_folder / chapter_folder_name
                chapter_folder.mkdir(exist_ok=True)

                manga_address = extract_text_from_url(session, manga_name, chapter_number)
                if manga_address:
                    executor.submit(download_chapter_images, session, (manga_name, chapter_number, manga_address, chapter_folder))

if __name__ == "__main__":
    main()
