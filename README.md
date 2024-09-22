
# Lesson Plan Web Scraper

## Project Overview

This project is designed to scrape lesson plans from a website and store them in a structured format (CSV/JSON). The scraping is done using Python libraries such as **BeautifulSoup** and **Selenium** to handle dynamic content loading. This tool can be used to automate the extraction of lesson plans, process the content, and handle various scenarios like dynamic content or missing data. 

The project contains two main scripts:
1. **Link Scraper**: Scrapes lesson links from a web page.
2. **Lesson Plan Scraper**: Scrapes the actual lesson plans from each lesson link.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Example Output](#example-output)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

## Features

1. **Scrape Lesson Links**: Extracts all links related to lesson plans on a webpage.
2. **Scrape Lesson Plans**: For each link, scrapes relevant lesson information like subject, topic, and class.
3. **Data Storage**: Saves the scraped data into CSV and JSON formats for further use.
4. **Error Logging**: Logs URLs with missing or incomplete data into an error log for easy review.
5. **Exclusion Filter**: Filters out lesson plans with certain criteria (e.g., "french-language").

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- [Google Chrome](https://www.google.com/chrome/) (as the web browser)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (to interact with Chrome through Selenium)
- Required Python libraries:
  - BeautifulSoup (`bs4`)
  - Selenium
  - Regular Expressions (`re` for text cleaning)
  - JSON
  - CSV
  - OS

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/lesson-plan-scraper.git
   cd lesson-plan-scraper
   ```

2. **Install the required Python libraries:**

   Use the following command to install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file should contain:

   ```txt
   beautifulsoup4
   selenium
   ```

3. **Set up ChromeDriver:**

   - Download the correct version of ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
   - Ensure the version of ChromeDriver matches your version of Chrome.
   - Add the ChromeDriver to your system's PATH or place it in the project directory.

## Usage

### 1. Scrape Lesson Links

The script `scrape_links.py` is used to scrape links related to lesson plans from the provided webpage.

#### Run the link scraper:

```bash
python scrape_links.py
```

This script will:
- Open the specified webpage.
- Scrape all lesson plan links with the class `link-success`.
- Store the scraped links in `primary1.json` in the following format:
  
  ```json
  [
    {
      "subject": "English",
      "URL": "https://lessonotes.com/v2/..."
    },
    ...
  ]
  ```

### 2. Scrape Lesson Plans

The script `scrape_lesson_plan.py` is used to extract lesson plans from the URLs provided in the `primary1.json` file.

#### Run the lesson plan scraper:

```bash
python scrape_lesson_plan.py
```

This script will:
- Read lesson URLs from `primary1.json`.
- Scrape lesson details (subject, topic, class, and lesson plan).
- Store the lesson details in `lesson_plan_pri.csv`.

#### Sample lesson plan entry in CSV format:

| instruction                                                      | input                                           | output           |
|------------------------------------------------------------------|------------------------------------------------|------------------|
| Create a lesson plan for teaching Addition in Mathematics to Primary 1 students. | Subject: Mathematics, Topic: Addition, Class: Primary 1 | Lesson plan content... |

#### Log error URLs:

Any URLs that do not contain valid lesson plan data will be logged in `lesson_plan_error_urls.csv`.

## File Structure

```bash
lesson-plan-scraper/
│
├── scrape_links.py                  # Script to scrape lesson links
├── scrape_lesson_plan.py             # Script to scrape lesson plan details
├── primary1.json                     # JSON file with scraped lesson links
├── lesson_plan_pri.csv               # CSV file with scraped lesson plan data
├── lesson_plan_error_urls.csv        # CSV file with URLs that failed to be scraped
├── requirements.txt                  # Python package requirements
├── README.md                         # Project documentation
```

## Example Output

- **Link Scraping**: `primary1.json`
  
  ```json
  [
    {
      "subject": "Mathematics",
      "URL": "https://lessonotes.com/v2/primary1/mathematics.html"
    },
    {
      "subject": "English",
      "URL": "https://lessonotes.com/v2/primary1/english.html"
    }
  ]
  ```

- **Lesson Plan Scraping**: `lesson_plan_pri.csv`

  ```csv
  instruction,input,output
  "Create a lesson plan for teaching Addition in Mathematics to Primary 1 students.", "Subject: Mathematics, Topic: Addition, Class: Primary 1", "Lesson plan content..."
  ```

- **Error Handling**: `lesson_plan_error_urls.csv`

  ```csv
  url
  "https://lessonotes.com/v2/primary1/missing-page.html"
  ```

## Error Handling

If a lesson plan cannot be scraped (e.g., missing content or table), the `lesson_plan_error_urls.csv` file will be updated with the problematic URLs. These URLs can be reviewed later for troubleshooting.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
