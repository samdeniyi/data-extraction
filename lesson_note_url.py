import csv

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

base_url = 'https://lessonotes.com/v2/'


def scrape_links(sch_detail):
	# Create a new instance of the Chrome driver
	driver = webdriver.Chrome()
	
	# Load the webpage
	url = sch_detail.get('url')
	driver.get(url)
	try:
		# Wait for the dynamic content to load (adjust the timeout as needed)
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-success"))
		)
		
		# Get the page source after dynamic content is loaded
		page_source = driver.page_source
		
		# Parse the page source with BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")
		
		# Find all the anchor tags with the class 'link-success'
		links = soup.select("a.link-success")
		
		# Initialize a list to store link details
		link_data = []
		
		# Extract the subject and URL from each link
		for link in links:
			url = link['href']
			subject = link.text.strip()
			
			link_info = {
				"subject": subject,
				"URL": f'{base_url}{url}'
			}
			
			# Append link details to the list
			link_data.append(link_info)
		
		# Write link details to a CSV file
		with open("ss2.csv", "w", newline="", encoding="utf-8") as csvfile:
			fieldnames = ['subject', 'URL']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for link in link_data:
				writer.writerow(link)
	
	finally:
		# Close the browser
		driver.quit()


if __name__ == "__main__":
	school_detail = {
		"url": 'https://lessonotes.com/v2/senior-secondary-school-2.html'  # Replace with your actual URL
	}
	scrape_links(school_detail)
