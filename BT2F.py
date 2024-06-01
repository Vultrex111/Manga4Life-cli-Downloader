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
        self.executor = ThreadPoolExecutor()
        self.history_file = Path("download_history.txt")

    def format_chapter_number(self, chapter_number):
        if '.' in chapter_number:
            integer_part, decimal_part = chapter_number.split('.')
            formatted_chapter_number = f"{int(integer_part):04d}.{decimal_part}"
        else:
            formatted_chapter_number = f"{int(chapter_number):04d}"
        return formatted_chapter_number

    async def generate_image_url(self, chapter_number, png_number, manga_address):
        base_url = f"https://{manga_address}/manga/{{}}/{{}}-{{:03d}}.png"
        url = base_url.format(self.formatted_manga_name, chapter_number, png_number)
        return url

    async def download_image(self, session, url, path):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(path, 'wb') as file:
                        file.write(await response.read())
                    print(f"Downloaded: {url}")
                    return True
                else:
                    print(f"Failed to download {url}: {response.status}")
                    return False
        except aiohttp.ClientError as e:
            print(f"Error downloading {url}: {e}")
            return False

    def extract_text_from_html(self, html_content):
        pattern = re.compile(r'vm\.CurPathName\s*=\s*"([^"]+)"')
        matches = pattern.findall(html_content)
        if matches:
            return matches[0]
        print("No line containing 'vm.CurPathName =' found.")
        return None

    async def extract_text_from_url(self, session, chapter_number):
        formatted_chapter_number = self.format_chapter_number(chapter_number)
        url = f"https://manga4life.com/read-online/{self.formatted_manga_name}-chapter-{formatted_chapter_number}.html"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html_content = await response.text()
                return self.extract_text_from_html(html_content)
        except aiohttp.ClientError as e:
            print(f"Error accessing {url}: {e}")
            return None

    async def download_chapter_images(self, session, chapter_number, chapter_folder):
        formatted_chapter_number = self.format_chapter_number(chapter_number)
        manga_address = await self.extract_text_from_url(session, formatted_chapter_number)
        if manga_address:
            png_number = 1
            while True:
                url = await self.generate_image_url(formatted_chapter_number, png_number, manga_address)
                image_filename = "{:03d}.png".format(png_number)
                image_path = chapter_folder / image_filename
                if await self.download_image(session, url, image_path):
                    png_number += 1
                else:
                    break

    async def download_chapters(self, chapters_to_download):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for chapter_number in chapters_to_download:
                chapter_folder_name = f"Chapter-{self.format_chapter_number(chapter_number)}"
                chapter_folder = self.manga_folder / chapter_folder_name
                chapter_folder.mkdir(exist_ok=True)
                task = self.download_chapter_images(session, chapter_number, chapter_folder)
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            if all(result is not None for result in results):
                self.save_history(self.manga_name)

    def save_history(self, manga_name):
        if not self.history_file.exists():
            self.history_file.touch()
        with open(self.history_file, 'r+') as file:
            history = file.read().splitlines()
            if manga_name not in history:
                file.write(manga_name + '\n')
                print(f"Saved {manga_name} to history.")

    def load_history(self):
        if self.history_file.exists():
            with open(self.history_file, 'r') as file:
                history = file.read().splitlines()
                print("Download History:")
                for manga in history:
                    print(manga)
        else:
            print("No download history found.")

def main():
    downloader = None
    while True:
        choice = input("Enter 'd' to download manga, 'h' to view history, 'q' to quit: ").strip().lower()
        if choice == 'd':
            manga_name = input("Enter the manga name: ")
            input_chapters = input("Enter the chapter number(s) separated by commas: ")
            chapters_to_download = [chapter.strip() for chapter in input_chapters.split(",")]
            downloader = MangaDownloader(manga_name)
            asyncio.run(downloader.download_chapters(chapters_to_download))
        elif choice == 'h':
            if downloader is None:
                downloader = MangaDownloader("dummy")  # Use a dummy name to access history functionality
            downloader.load_history()
        elif choice == 'q':
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
