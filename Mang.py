import os
import subprocess
import chapter_parser

def generate_image_url(manga_name, chapter_number, png_number):
    base_url = chapter_parser.vm_cur_path_name + "/manga/{}/{}-{:03d}.png"
    formatted_manga_name = manga_name.replace(" ", "-")
    url = base_url.format(formatted_manga_name, str(chapter_number).zfill(4), png_number)
    return url

# Example usage
manga_name = input("Enter the manga name: ")
chapter_number = int(input("Enter the chapter number: "))
start_png = 1
end_png = 30
max_failed_attempts = 2

# Create manga folder
formatted_manga_name = manga_name.replace(" ", "-")
manga_folder = os.path.join(os.getcwd(), formatted_manga_name)
os.makedirs(manga_folder, exist_ok=True)

# Create chapter folder
chapter_folder = os.path.join(manga_folder, "Chapter: " + str(chapter_number).zfill(4))
os.makedirs(chapter_folder, exist_ok=True)

# Generate and save the URLs
downloaded_images = 0
failed_attempts = 0
consecutive_404_errors = 0  # Variable to keep track of consecutive 404 errors

# Check if the original vm.CurPathName works
original_vm_cur_path_name = "https://scans.lastation.us"
original_vm_cur_path_name_valid = True

for png_number in range(start_png, end_png + 1):
    url = generate_image_url(manga_name, chapter_number, png_number)
    image_filename = "{:03d}.png".format(png_number)
    image_path = os.path.join(chapter_folder, image_filename)  # Add the prefix here

    # Download the image using wget
    subprocess.run(["wget", "-O", image_path, url])

    # Check if the download was successful
    if os.path.exists(image_path):
        downloaded_images += 1
        print("Downloaded:", url)
        failed_attempts = 0
        consecutive_404_errors = 0  # Reset the consecutive 404 errors count
    else:
        print("Failed to download:", url)
        failed_attempts += 1
        if failed_attempts == max_failed_attempts:
            print("Downloads Complete")
            break
        if failed_attempts > 1 and consecutive_404_errors == failed_attempts - 1:
            print("Downloads Complete")
            break
        consecutive_404_errors = failed_attempts  # Update the consecutive 404 errors count

        # If the original vm.CurPathName doesn't work, prompt the user to input the chapter URL
        if original_vm_cur_path_name_valid:
            print("The original vm.CurPathName doesn't work. Please input the chapter URL.")
            chapter_url = input("Chapter URL: ")
            new_vm_cur_path_name = chapter_parser.parse_chapter_url(chapter_url)

            if new_vm_cur_path_name:
                # Replace the original vm.CurPathName with the new one
                chapter_parser.replace_vm_cur_path_name("Mang.py", new_vm_cur_path_name)
                original_vm_cur_path_name_valid = False
            else:
                print("Invalid chapter URL. Downloads cannot continue.")
                break

# Check if all images were downloaded
if downloaded_images == end_png - start_png + 1:
    print("Download Complete")

