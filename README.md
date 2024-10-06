# README

This repository contains data extraction scripts designed to retrieve data in text file format for use with LLMs (e.g., Notebook LLM). It provides scripts to extract text data from websites or repositories, outputting the data for ingestion by large language models (LLMs).

This repository contains two Python scripts designed for different tasks:

1. **get_data_from_url.py** - A recursive web crawler with a Streamlit-based user interface.
2. **repository_to_text_file.py** - A script to combine all files from a directory into a single text file.

## Requirements

Before running the scripts, ensure you have the required Python packages installed. You can install the dependencies by running:

```bash
pip install streamlit requests beautifulsoup4 tqdm
```

## Scripts Overview

### 1. `get_data_from_url.py`

This script is designed to crawl a website recursively and extract the text content from the pages. It uses `requests` and `BeautifulSoup` for web scraping, and the user can configure the crawl depth and specify URL patterns to filter the links. The results are displayed in a Streamlit web interface, and the output is saved as a text file in the `output` folder.

#### Features:
- **Recursive Crawling**: You can specify how deep the crawler should go when exploring links.
- **Streamlit User Interface**: A simple interface to enter the target URL, set parameters, and view progress in real time.
- **Export Results**: The crawled text data can be exported to a text file.

#### How to Use:
1. Run the script with:
   ```bash
   streamlit run get_data_from_url.py
   ```
2. Enter the target URL, set the maximum depth, and optionally add a URL pattern.
3. Start the crawling process, and the results will be saved in the `output` directory.

### 2. `repository_to_text_file.py`

This script is designed to traverse a directory and combine the contents of all files into a single text file. It walks through the directory, opens each file, and writes the content along with the file name into a text file (`repository.txt`). The script uses the `tqdm` library to display the progress of file processing.

#### Features:
- **Directory Traversal**: Combines all files from a given directory and its subdirectories.
- **Encoding Handling**: Supports multiple encodings (`utf-8`, `latin-1`, `cp1252`) to ensure compatibility with various text files.
- **Progress Bar**: Uses `tqdm` to display a progress bar for file processing.

#### How to Use:
1. Set the `INPUT_DIRECTORY` variable in the script to the directory you want to process.
2. Run the script with:
   ```bash
   python repository_to_text_file.py
   ```
3. The script will generate a `repository.txt` file in the `output` directory, containing all the file contents.

---

## Output

- The crawled web pages' text from `get_data_from_url.py` will be saved in the `output` directory as a text file.
- The combined repository text from `repository_to_text_file.py` will also be saved in the `output` directory as `repository.txt`.

## License

This project is licensed under the MIT License.
