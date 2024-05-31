import re
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

class MangaDownloader:
    def __init__(self, manga_name):
        self.manga_name = manga_name.title()
        self.formatted_manga_name = self.manga_name.replace(" ", "-")
        self.manga_folder = Path(self.formatted_manga_name)
        self.manga_folder.mkdir(exist_ok=True)
        self.session_pool = ThreadPoolExecutor()
        self.executor = ThreadPoolExecutor()

    async def generate_image_url(self, chapter_number, png_number, manga_address):
        base_url = f"https://{manga_address}/manga/{{}}/{{}}-{{:03d}}.png"
        url = base_url.format(self.formatted_manga_name, str(chapter_number).zfill(4), png_number)
        return url

    async def download_image(self, url, path):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    with open(path, 'wb') as file:
                        file.write(await response.read())
                    print(f"Downloaded: {url}")
                    return True
        except aiohttp.ClientError as e:
            print(f"Error downloading {url}: {e}")
            return False

    def extract_text_from_html(self, html_content):
        pattern = re.compile(r'vm\.CurPathName\s*=\s*"([^"]+)"')
        matches = pattern.findall(html_content)
        if matches:
            for match in matches:
                return match
        print("No line containing 'vm.CurPathName =' found.")
        return None

    async def extract_text_from_url(self, chapter_number):
        url = f"https://manga4life.com/read-online/{self.formatted_manga_name}-chapter-{chapter_number}.html"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html_content = await response.text()
                    return self.extract_text_from_html(html_content)
        except aiohttp.ClientError as e:
            print(f"Error accessing {url}: {e}")
            return None

    async def download_chapter_images(self, chapter_number, chapter_folder):
        png_number = 1
        while True:
            manga_address = await self.extract_text_from_url(chapter_number)
            if manga_address:
                url = await self.generate_image_url(chapter_number, png_number, manga_address)
                image_filename = "{:03d}.png".format(png_number)
                image_path = chapter_folder / image_filename
                if await self.download_image(url, image_path):
                    png_number += 1
                else:
                    break
            else:
                break

    def download_chapters(self, chapters_to_download):
        loop = asyncio.get_event_loop()
        tasks = []
        for chapter_number in chapters_to_download:
            chapter_folder_name = f"Chapter: {str(chapter_number).zfill(4)}"
            chapter_folder = self.manga_folder / chapter_folder_name
            chapter_folder.mkdir(exist_ok=True)
            task = asyncio.ensure_future(self.download_chapter_images(chapter_number, chapter_folder))
            tasks.append(task)
        loop.run_until_complete(asyncio.wait(tasks))

def main():
    manga_name = input("Enter the manga name: ")
    input_chapters = input("Enter the chapter number(s) separated by commas: ")
    chapters_to_download = [int(chapter.strip()) for chapter in input_chapters.split(",")]

    downloader = MangaDownloader(manga_name)
    downloader.download_chapters(chapters_to_download)

if __name__ == "__main__":
    main()
