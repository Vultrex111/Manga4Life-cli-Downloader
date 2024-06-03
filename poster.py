import requests
import argparse
from pathlib import Path

def search_and_download_manga_poster(manga_name):
    # Remove quotes if they surround the manga name
    if manga_name.startswith('"') and manga_name.endswith('"'):
        formatted_manga_name = manga_name.strip('"')
    else:
        # Format the manga name to have the first letter of each word in uppercase and replace spaces with "-"
        formatted_manga_name = manga_name.title().replace(" ", "-")
    
    # Construct the poster URL using the formatted manga name
    poster_url = f"https://temp.compsci88.com/cover/{formatted_manga_name}.jpg"
    
    # Path for the downloaded poster
    poster_path = Path(f"{formatted_manga_name}_poster.jpg")
    
    # Check if the poster already exists
    if poster_path.exists():
        print(f"Poster already exists: {poster_path}")
        return
    
    try:
        # Send a GET request to the poster URL
        response = requests.get(poster_url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Save the downloaded image to a file
        with poster_path.open("wb") as file:
            file.write(response.content)
        print("Manga poster downloaded successfully!")
        
        # Save the entered manga name to a history file for successful downloads
        history_path = Path("manga_history.txt")
        with history_path.open("a") as history_file:
            history_file.write(formatted_manga_name + "\n")
        print("Manga name added to history.")
        
    except requests.RequestException as e:
        print(f"Failed to download the manga poster: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download manga posters by name.")
    parser.add_argument('manga_name', type=str, help="Name of the manga")
    args = parser.parse_args()
    
    search_and_download_manga_poster(args.manga_name)

if __name__ == "__main__":
    main()
