import json  # Module for handling JSON data
from bs4 import BeautifulSoup  # Library for parsing HTML content
from selenium import webdriver  # Selenium WebDriver for controlling a browser
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.support import expected_conditions as EC  # Predefined conditions for WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait  # Explicit wait to handle dynamic content loading

# Base URL for appending scraped URLs
base_url = 'https://lessonotes.com/v2/'


def scrape_links(sch_detail):
	"""
	This function scrapes the dynamic links from the given webpage
	and stores them in a JSON file.

	:param sch_detail: Dictionary containing details about the school including the URL to scrape
	"""
	
	# Create a new instance of the Chrome WebDriver
	driver = webdriver.Chrome()
	
	# Extract URL from the school details
	url = sch_detail.get('url')
	
	# Load the webpage using the URL
	driver.get(url)
	
	try:
		# Wait until the dynamic content (links) loads on the page (up to 10 seconds)
		WebDriverWait(driver, 10).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, "a.link-success"))
		)
		
		# After content loads, get the HTML source of the loaded page
		page_source = driver.page_source
		
		# Parse the HTML content using BeautifulSoup
		soup = BeautifulSoup(page_source, "html.parser")
		
		# Select all anchor tags with class 'link-success' (dynamic links)
		links = soup.select("a.link-success")
		
		# Initialize an empty list to store the scraped link details
		link_data = []
		
		# Iterate through the links found on the page
		for link in links:
			# Extract the href attribute (URL) of the link
			url = link['href']
			
			# Extract the text content (subject) of the link
			subject = link.text.strip()
			
			# Construct a dictionary with subject and full URL details
			link_info = {
				"subject": subject,
				"URL": f'{base_url}{url}'  # Combine base URL with the relative link
			}
			
			# Append the link details to the list
			link_data.append(link_info)
		
		# Save the link details into a JSON file named 'primary1.json'
		with open("primary1.json", "w", encoding="utf-8") as jsonfile:
			json.dump(link_data, jsonfile, indent=4)  # Save with indentation for better readability
	
	finally:
		# Close the WebDriver browser instance
		driver.quit()


if __name__ == "__main__":
	# Define the school detail with the URL to be scraped
	school_detail = {
		"url": "https://lessonotes.com/v2/primary1.html"
	}
	
	# Call the scrape_links function with the provided school details
	scrape_links(school_detail)
