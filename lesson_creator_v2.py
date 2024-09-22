import csv
import json
import os
import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def clean_text(text):
	# Remove non-breaking spaces and other special characters
	return re.sub(r'\s+', ' ', text).strip()


def convert_to_lower(text):
	return text.lower()


def log_error(lesson_url, error):
	with open("lesson_plan_error_urls.csv", "a", newline="", encoding="utf-8") as csvfile:
		file_exists = os.path.isfile("lesson_plan_error_urls.csv")
		fieldnames = ["url", "error"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		if not file_exists or os.stat("lesson_plan_error_urls.csv").st_size == 0:
			writer.writeheader()
		writer.writerow({
			"url": lesson_url,
			"error": error,
		})


def scrape_lesson_plan(lesson_url):
	driver: WebDriver = webdriver.Chrome()
	driver.get(lesson_url)
	time.sleep(3)
	
	try:
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "col-sm-12")))
		page_source = driver.page_source
		
		# Parse the page source with BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")
		
		# Extract the class, subject, and topic information
		class_tag = soup.find('p', string=lambda text: text and 'Class:' in text)
		subject_tag = soup.find('p', string=lambda text: text and 'Subject:' in text)
		topic_tag = soup.find('p', string=lambda text: text and 'Topic:' in text)
		specific_objectives_tag = soup.find('p', string=lambda text: text and 'SPECIFIC OBJECTIVES' in text)
		instructional_techniques_tag = soup.find('p', string=lambda text: text and 'INSTRUCTIONAL TECHNIQUES' in text)
		instructional_materials_tag = soup.find('p', string=lambda text: text and 'INSTRUCTIONAL MATERIALS' in text)
		
		class_info = clean_text(class_tag.get_text(strip=True).split(":")[1].strip()) if class_tag else ""
		subject_info = clean_text(subject_tag.get_text(strip=True).split(":")[1].strip()) if subject_tag else ""
		topic_info = clean_text(topic_tag.get_text(strip=True).split(":", 1)[1].strip()) if topic_tag else ""
		specific_objectives_info = clean_text(specific_objectives_tag.find_next('ol').get_text(separator='. ',
		                                                                                       strip=True)) if specific_objectives_tag else ""
		instructional_techniques_info = clean_text(instructional_techniques_tag.get_text(strip=True).split(":")[
			                                           1].strip()) if instructional_techniques_tag else ""
		instructional_materials_info = clean_text(instructional_materials_tag.get_text(strip=True).split(":")[
			                                          1].strip()) if instructional_materials_tag else ""
		
		specific_objectives_info = f"at the end of the lesson, the students should be able to: {specific_objectives_info}"
		instructional_techniques_info = f"the instructional techniques used include: {instructional_techniques_info}"
		instructional_materials_info = f"the materials required for this lesson are: {instructional_materials_info}"
		
		table = soup.find("table", class_="table") or soup.find("table")
		instructional_procedures = []
		if table is None:
			print(f"No table found for {lesson_url}")
			log_error(lesson_url, "No table found")
			pass
		else:
			# Extract the instructional procedures from the table
			for row in table.find_all("tr")[1:]:
				cells = row.find_all("td")
				step = cells[0].get_text(strip=True)
				teacher_activity = cells[1].get_text(strip=True)
				learner_activity = cells[2].get_text(strip=True)
				instructional_procedures.append(
					f"Step {step}: {teacher_activity}, {learner_activity}"
				)
			instructional_procedures_cleaned = " ".join(instructional_procedures)
			
			note_section = []
			
			note_element = table.find_next("p", string="NOTE" or "Note")
			
			while note_element:
				note_section.append(note_element.get_text(strip=True))
				note_element = note_element.find_next_sibling()
			
			note_section_cleaned = " ".join(note_section)
			
			lesson_plan_content = f"Class:{class_info} Subject:{subject_info} Topic:{topic_info} Specific Objectives:{specific_objectives_info} Instructional Techniques:{instructional_techniques_info} Instructional Materials:{instructional_materials_info} Instructional Procedures:{instructional_procedures_cleaned} Note Section:{note_section_cleaned}"
			print(f"Lesson Plan generated for {lesson_url}")
			
			with open("lesson_plan.csv", "a", newline="", encoding="utf-8") as csvfile:
				file_exists = os.path.isfile("lesson_plan.csv")
				fieldnames = ["instruction", "input", "output"]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
				if not file_exists or os.stat("lesson_plan.csv").st_size == 0:
					writer.writeheader()
				writer.writerow({
					"instruction": f"Create a lesson plan for teaching {topic_info} in {subject_info} to {class_info} students.",
					"input": f"Subject: {subject_info}, Topic: {topic_info}, Class: {class_info}",
					"output": lesson_plan_content,
				})
	
	except Exception as e:
		print(f"Error: {e}")
		log_error(lesson_url, e)
	
	finally:
		# Close the WebDriver
		driver.quit()


def extra_lesson_plan():
	with open('primary.json', 'r') as file:
		lesson_data = json.load(file)
		for lesson in lesson_data:
			s_url = lesson.get("URL")
			
			scrape_lesson_plan(s_url)


if __name__ == "__main__":
	extra_lesson_plan()
