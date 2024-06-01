Here's a revised and formatted version of your README for your GitHub page, providing clear instructions for users on how to use the script:

---

# Manga4Life-cli-Downloader

**Download manga chapters from Manga4Life easily with this script.**

## Prerequisites

- **Python 3.x**
- Required Python libraries:
  - `requests` 
  - `concurrent.futures`
  - `pathlib`

Install the required libraries using:

```sh
pip install requests concurrent.futures pathlib
```

## Usage

1. **Clone or Download the Repository**:
   - Only download the latest commit.
   - Clone the repository using:
     ```sh
     git clone <repository_url>
     ```

2. **Navigate to the Downloaded Folder**:
   - Open a terminal or command prompt and navigate to the folder where the repository is downloaded.

3. **Run the Script**:
   - Execute the script using the following command:
     ```sh
     python manga_downloader.py
     ```

4. **Enter the Manga Details**:
   - **Manga Name**: Type the correct name of the manga.
     - Example: `Jujutsu Kaisen` is different from `JujutsuKaisen`.
     - If the English name doesn't work, try using the Japanese name.
     - Example: Instead of `My Hero Academia`, use `Boku No Hero Academia`.
   - **Chapter Numbers**: Enter the chapter number(s) separated by commas.
     - Example: `14, 15, 14.5`

## Example

```sh
python manga_downloader.py
```

- **Manga Name**: `One Piece`
- **Chapter Numbers**: `001, 002, 0014.5`

The script will download the specified manga chapters and save them in separate folders within a directory named after the manga title.

## Features

- Supports chapters with decimals, e.g., `14.5`.
- Saves your download history in a file (`download_history.txt`).

## Notes

- Ensure you have a stable internet connection while running the script.
- The downloaded manga chapters will be saved in a folder named after the manga title.
- Each chapter will be saved in a separate folder named `Chapter-XXXX` (where XXXX is the chapter number).

## Troubleshooting

- If you encounter an issue where `vm.CurPathName` is not found, this might be due to an incorrect manga name or chapter number. Please verify that the manga name and chapter number are correct.
- For network-related issues, ensure you have a stable internet connection.

---

