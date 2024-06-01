Certainly! Here's the updated `README.md` with the instructions on how to use the `search_poster.py` script:

---

# Manga4Life-cli-Downloader

**Download manga chapters from Manga4Life easily with this script.**

## Prerequisites

- **Python 3.x**
- Required Python libraries:
  - `aiohttp`
  - `concurrent.futures`
  - `pathlib`
  - `argparse`

Install the required libraries using:

```sh
pip install aiohttp concurrent.futures pathlib argparse
```

## Usage

1. **Clone or Download the Repository**:
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

### Command-Line Options

You can also use command-line arguments to specify the manga name and chapters to download:

#### Download Manga Chapters

```sh
python manga_downloader.py -d 'MANGA_NAME' -c 'CHAPTERS'
```

- **Manga Name**: The name of the manga.
  - Example: `Jujutsu Kaisen` is different from `JujutsuKaisen`.
  - If the English name doesn't work, try using the Japanese name.
  - Example: Instead of `My Hero Academia`, use `Boku No Hero Academia`.
- **Chapter Numbers**: The chapter number(s) separated by commas.
  - Example: `14, 15, 14.5`

#### Use Uppercase for Manga Name

If the manga name is in all uppercase, use the `-U` flag:

```sh
python manga_downloader.py -U -d 'TSUYOKI' -c '1,2,3'
```

#### View Download History

```sh
python manga_downloader.py -H
```

### Interactive Mode

If you don't use the `-d` or `-c` options, the script will run in interactive mode, prompting you to enter the manga name and chapter numbers:

```sh
python manga_downloader.py
```

- **Manga Name**: `One Piece`
- **Chapter Numbers**: `001, 002, 0014.5`

The script will download the specified manga chapters and save them in separate folders within a directory named after the manga title.

## Search Poster Script

Additionally, a script named `search_poster.py` is provided to search for posters related to manga titles. This script utilizes the `requests` library to fetch search results from various sources and processes the results to extract relevant information about posters.

To use the `search_poster.py` script, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the folder where the `search_poster.py` script is located.
3. Run the script using the following command:

```sh
python search_poster.py 'MANGA_NAME'
```

Replace `'MANGA_NAME'` with the name of the manga for which you want to search for posters.

The script will search for posters related to the specified manga name and provide relevant information about the posters found.

## Features

- Supports chapters with decimals, e.g., `14.5`.
- Saves your download history in a file (`download_history.txt`) for successful downloads only.
- Automatically formats manga names and chapter numbers.
- Option to use uppercase for manga names with the `-U` flag.

## Notes

- Ensure you have a stable internet connection while running the script.
- The downloaded manga chapters will be saved in a folder named after the manga title.
- Each chapter will be saved in a separate folder named `Chapter-XXXX` (where XXXX is the chapter number).

## Troubleshooting

- If you encounter an issue where `vm.CurPathName` is not found, this might be due to an incorrect manga name or chapter number. Please verify that the manga name and chapter number are correct.
- For network-related issues, ensure you have a stable internet connection.
- You can use https://github.com/ollm/OpenComic to read the manga chapters. I recommend it. :)
---

This updated README now includes instructions on how to use the `search_poster.py` script, providing users with a clear understanding of how to search for posters related to manga titles. Let me know if there's anything else you'd like to add or modify!
