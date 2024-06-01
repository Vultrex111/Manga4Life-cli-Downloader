import requests

def download_manga_poster(manga_name):
    if manga_name.startswith('"') and manga_name.endswith('"'):
        # Remove the quotes and use the input as is
        formatted_manga_name = manga_name.strip('"')
    else:
        # Format the manga name to have the first letter of each word in uppercase and replace spaces with "-"
        formatted_manga_name = manga_name.title().replace(" ", "-")
    
    # Construct the poster URL using the formatted manga name
    poster_url = f"https://temp.compsci88.com/cover/{formatted_manga_name}.jpg"
    
    # Send a GET request to the poster URL
    response = requests.get(poster_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the downloaded image to a file
        with open(f"{formatted_manga_name}_poster.jpg", "wb") as file:
            file.write(response.content)
        print("Manga poster downloaded successfully!")
        
        # Save the entered manga name to a history file for successful downloads
        with open("manga_history.txt", "a") as history_file:
            history_file.write(formatted_manga_name + "\n")
        print("Manga name added to history.")
    else:
        print("Failed to download the manga poster.")

# Prompt the user to input the manga name
user_input = input("Enter the name of the manga: ")
formatted_input = user_input.strip()  # Remove leading/trailing white spaces
download_manga_poster(formatted_input)
