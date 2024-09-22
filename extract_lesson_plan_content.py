import csv
import json
import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def clean_text(text):
	# Remove non-breaking spaces and other special characters
	return re.sub(r'\s+', ' ', text).strip()


def scrape_lesson_plan(lesson_url):
	driver = webdriver.Chrome()
	driver.get(lesson_url)
	
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "container")))
		
		page_source = driver.page_source
		
		# Parse the page source with BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")
		
		class_tag = soup.find("p", string=lambda t: t and re.search(r'class\s*:', t, re.IGNORECASE))
		subject_tag = soup.find("p", string=lambda t: t and re.search(r'subject\s*:', t, re.IGNORECASE))
		topic_tag = soup.find("p", string=lambda t: t and re.search(r'topic\s*:', t, re.IGNORECASE))
		
		class_info = clean_text(class_tag.text.split(":")[1]) if class_tag else ""
		subject_info = clean_text(subject_tag.text.split(":")[1]) if subject_tag else ""
		topic_info = clean_text(topic_tag.text.split(":", 1)[1]) if topic_tag else ""
		
		lesson_plan_section = soup.find("div", class_="container mt-5").find_next("div", class_="col-sm-12")
		lesson_plan_table = lesson_plan_section.find_all("table", class_="table")
		
		
		# Extract the lesson plan section up to the table
		if lesson_plan_table is None or len(lesson_plan_table) == 0:
			print(f"No lesson plan table found for {lesson_url}")
			with open("lesson_plan_error_urls.csv", "a", newline="", encoding="utf-8") as csvfile:
				file_exists = os.path.isfile("lesson_plan_error_urls.csv")
				fieldnames = ["url"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				if not file_exists or os.stat("lesson_plan_error_urls.csv").st_size == 0:
					writer.writeheader()
				writer.writerow({
					"url": lesson_url,
				})
		else:
			print(f"There is lesson plan table found for {lesson_url}")
			# lesson_plan_content = lesson_plan_table.get_text(strip=True).strip()
			lesson_plan_content = lesson_plan_section.get_text(separator="\n", strip=True).split(
				lesson_plan_table[0].get_text(strip=True))[0].strip()
			
			# Remove special characters from the lesson plan content
			lesson_plan_cleaned = clean_text(lesson_plan_content)
			
			with open("lesson_plan_pri.csv", "a", newline="", encoding="utf-8") as csvfile:
				file_exists = os.path.isfile("lesson_plan_pri.csv")
				fieldnames = ["instruction", "input", "output"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				if not file_exists or os.stat("lesson_plan_pri.csv").st_size == 0:
					writer.writeheader()
				writer.writerow({
					"instruction": f"Create a lesson plan for teaching {topic_info} in {subject_info} to {class_info} students.",
					"input": f"Subject: {subject_info}, Topic: {topic_info}, Class: {class_info}",
					"output": lesson_plan_cleaned,
				})
	except Exception as e:
		print(f"An error occurred while scraping {lesson_url}: {e}")
		with open("lesson_plan_error_urls.csv", "a", newline="", encoding="utf-8") as csvfile:
			file_exists = os.path.isfile("lesson_plan_error_urls.csv")
			fieldnames = ["url"]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			if not file_exists or os.stat("lesson_plan_error_urls.csv").st_size == 0:
				writer.writeheader()
			writer.writerow({
				"url": lesson_url,
			})
	finally:
		driver.quit()


def extra_lesson_plan():
	with open('primary1.json', 'r') as file:
		lesson_data = json.load(file)
		for lesson in lesson_data:
			s_url = lesson.get("URL")
			
			# Skip URLs containing "french-language"
			if "french-language" in s_url:
				print(f"Skipping URL: {s_url} (contains 'french-language')")
				continue  # Skip to the next iteration if the URL contains "french-language"
			
			# Call the function to scrape the lesson plan for other URLs
			scrape_lesson_plan(s_url)


if __name__ == "__main__":
	extra_lesson_plan()
