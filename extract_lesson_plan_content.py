import csv  # Module for reading/writing CSV files
import json  # Module for handling JSON data
import os  # Module for interacting with the operating system (e.g., file existence check)
import re  # Module for working with regular expressions

from bs4 import BeautifulSoup  # Library for parsing HTML content
from selenium import webdriver  # Selenium WebDriver for browser automation
from selenium.webdriver.common.by import By  # For locating elements on the page
from selenium.webdriver.support import expected_conditions as EC  # Predefined conditions for WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait  # Explicit wait for dynamic content loading


def clean_text(text):
	"""
	Cleans the input text by removing extra whitespaces and special characters.

	:param text: The raw string to clean
	:return: Cleaned string with no extra spaces or special characters
	"""
	# Replace multiple whitespaces (including non-breaking spaces) with a single space and strip leading/trailing spaces
	return re.sub(r'\s+', ' ', text).strip()


def scrape_lesson_plan(lesson_url):
	"""
	Scrapes a lesson plan from the given lesson URL and saves the result in a CSV file.

	:param lesson_url: The URL of the lesson plan to scrape
	"""
	# Initialize the Chrome WebDriver
	driver = webdriver.Chrome()
	
	# Load the webpage
	driver.get(lesson_url)
	
	try:
		# Wait for the dynamic content to load (up to 10 seconds)
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
		
		# Get the HTML source of the loaded page
		page_source = driver.page_source
		
		# Parse the page source with BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")
		
		# Find key information such as class, subject, and topic using regex to match text patterns
		class_tag = soup.find("p", string=lambda t: t and re.search(r'class\s*:', t, re.IGNORECASE))
		subject_tag = soup.find("p", string=lambda t: t and re.search(r'subject\s*:', t, re.IGNORECASE))
		topic_tag = soup.find("p", string=lambda t: t and re.search(r'topic\s*:', t, re.IGNORECASE))
		
		# Extract and clean the class, subject, and topic information from the matched tags
		class_info = clean_text(class_tag.text.split(":")[1]) if class_tag else ""
		subject_info = clean_text(subject_tag.text.split(":")[1]) if subject_tag else ""
		topic_info = clean_text(topic_tag.text.split(":", 1)[1]) if topic_tag else ""
		
		# Locate the section containing the lesson plan and its table structure
		lesson_plan_section = soup.find("div", class_="container mt-5").find_next("div", class_="col-sm-12")
		lesson_plan_table = lesson_plan_section.find_all("table", class_="table")
		
		# If no table is found, log the error and write the URL to an error log
		if lesson_plan_table is None or len(lesson_plan_table) == 0:
			print(f"No lesson plan table found for {lesson_url}")
			
			# Append the URL to the error log CSV file
			with open("lesson_plan_error_urls.csv", "a", newline="", encoding="utf-8") as csvfile:
				file_exists = os.path.isfile("lesson_plan_error_urls.csv")
				fieldnames = ["url"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				
				# Write the header if the file is being created for the first time
				if not file_exists or os.stat("lesson_plan_error_urls.csv").st_size == 0:
					writer.writeheader()
				
				writer.writerow({"url": lesson_url})
		else:
			print(f"Lesson plan table found for {lesson_url}")
			
			# Extract the content of the lesson plan up to the table and clean it
			lesson_plan_content = lesson_plan_section.get_text(separator="\n", strip=True).split(
				lesson_plan_table[0].get_text(strip=True))[0].strip()
			lesson_plan_cleaned = clean_text(lesson_plan_content)
			
			# Append the scraped lesson plan data to a CSV file
			with open("lesson_plan_pri.csv", "a", newline="", encoding="utf-8") as csvfile:
				file_exists = os.path.isfile("lesson_plan_pri.csv")
				fieldnames = ["instruction", "input", "output"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				
				# Write the header if the file is being created for the first time
				if not file_exists or os.stat("lesson_plan_pri.csv").st_size == 0:
					writer.writeheader()
				
				# Write the cleaned lesson plan data
				writer.writerow({
					"instruction": f"Create a lesson plan for teaching {topic_info} in {subject_info} to {class_info} students.",
					"input": f"Subject: {subject_info}, Topic: {topic_info}, Class: {class_info}",
					"output": lesson_plan_cleaned,
				})
	
	# Handle exceptions during scraping and log failed URLs
	except Exception as e:
		print(f"An error occurred while scraping {lesson_url}: {e}")
		
		# Log error URLs to the CSV file
		with open("lesson_plan_error_urls.csv", "a", newline="", encoding="utf-8") as csvfile:
			file_exists = os.path.isfile("lesson_plan_error_urls.csv")
			fieldnames = ["url"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			
			# Write the header if the file is being created for the first time
			if not file_exists or os.stat("lesson_plan_error_urls.csv").st_size == 0:
				writer.writeheader()
			
			writer.writerow({"url": lesson_url})
	
	# Ensure the browser instance is closed
	finally:
		driver.quit()


def extra_lesson_plan():
	"""
	Reads lesson data from a JSON file and scrapes each lesson plan URL.
	Skips URLs that contain 'french-language'.
	"""
	with open('primary1.json', 'r') as file:
		lesson_data = json.load(file)  # Load JSON data
		
		# Loop through each lesson's URL in the JSON file
		for lesson in lesson_data:
			s_url = lesson.get("URL")
			
			# Skip URLs that contain 'french-language'
			if "french-language" in s_url:
				print(f"Skipping URL: {s_url} (contains 'french-language')")
				continue  # Skip the current iteration
			
			# Call the function to scrape the lesson plan for the current URL
			scrape_lesson_plan(s_url)


if __name__ == "__main__":
	# Main entry point of the script
	extra_lesson_plan()  # Initiates scraping of lesson plans
