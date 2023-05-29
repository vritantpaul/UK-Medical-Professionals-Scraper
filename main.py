from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re
import csv

# creating a csv
with open("professionals.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)

csv_writer.writerow(["Name", "Address", "Phone Number", "Email", "Website"])

# configuring driver
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# opening the site
driver.get("https://www.jccp.org.uk/MemberSearch")
driver.maximize_window()

# capturing the dropdown box
dropdown_list = driver.find_element(By.XPATH, "//select[@id='Modality']")
# making a Select object
dropdown = Select(dropdown_list)
# selecting "Botulinum toxins"
dropdown.select_by_visible_text("Botulinum toxins")
driver.find_element(By.XPATH, "//button[@id='btn_submit']").click()

# using driver.page_source to get the page html and using BeautifulSoup to parse it
soup = BeautifulSoup(driver.page_source, "lxml")

# function to get only addresses
only_address = lambda text: re.search("^\s+[\w\d]+", text) if "@" not in text else None

# all the members
members = soup.select("div.result-item")

# writing rows into the csv file with required fields
for member in members:
    name = member.select_one("ul.status").select("li")[0].text.strip()
    address = (
        a.strip()
        if (a := member.select_one("ul.address-info").find(text=only_address))
        is not None
        else None
    )
    tel = (
        member.select_one("ul.address-info")
        .find(text=re.compile("(\(\d{3}\))"))
        .strip()
    )
    mail = member.select_one("ul.address-info").find(text=re.compile("@")).strip()
    website = (
        w.strip()
        if "@"
        not in (
            w := member.select_one("ul.address-info").select_one("li:last-child").text
        )
        else None
    )
    # writing rows
    csv_writer.writerow([name, address, tel, mail, website])

# closing the csv file
csv_file.close()
