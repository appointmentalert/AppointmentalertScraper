# Use selenium functionality on the page below to get available dates
# https://www.leipzig.de/fachanwendungen/termine/abholung-aufenthaltstitel.html

import pandas as pd
from selenium import webdriver  
from selenium.webdriver.common.by import By

def get_available_days():
    """
    Get the available days for the appointment.
    """

    driver = webdriver.Chrome() # webdriver.Chrome() webdriver.Firefox()
    # driver.maximize_window()

    driver.get("https://www.leipzig.de/fachanwendungen/termine/abholung-aufenthaltstitel.html")

    driver.switch_to.frame(0) # focus on frame 0

    # Click on checkbox "Einwilligung zur elektronischen Datenverarbeitung / Consent to the electronic processing of data*"
    driver.find_element(By.ID, 'agreement_accept').click()
    # Click on Weiter button
    driver.find_element(By.ID, 'action_infopage_next').click()
    # Expand the tree "Ausländerbehörde Leipzig"
    driver.find_element(By.XPATH, '//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[2]/td[2]/div/button').click()
    # Click on 'Termin vereinbaren' button
    driver.find_element(By.ID, 'action_officeselect_termnew_prefix1600340740349').click()
    # Select 1 for the dropdown 'Abholung Dokument für 1 Person bzw. 1 Ehepaar
    driver.find_element(By.ID, 'id_1600340740368').click() # select the dropdown
    driver.find_element(By.XPATH, '//*[@id="id_1600340740368"]/option[2]').click() # select option "1"
    driver.find_element(By.ID, 'action_concernselect_next').click() # Click Next / Weiter

    # Warning: This doesn't work on Firefox though. Some waiting time might be needed for Firefox.
    driver.find_element(By.ID, 'action_concerncomments_next').click() # Click Next / Weiter

    # Read the tables with month and days
    monthTables = driver.find_elements(By.CLASS_NAME, 'ekolCalendarMonthTable')

    # For each table, get the month, days and slots.
    # Put the information in a list of data frames (one per month).
    dfList = []

    # Helper dictionary to convert the month name to a number format (01-12)
    monthDict = {
                'Januar': '01', 
                'Februar': '02', 
                'März': '03', 
                'April': '04', 
                'Mai': '05', 
                'Juni': '06', 
                'Juli': '07', 
                'August': '08', 
                'September': '09', 
                'Oktober': '10', 
                'November': '11', 
                'Dezember': '12'
                }

    for monthTable in monthTables:
        monthText = monthTable.text.split('\n')
        month_year = monthText[0]
        month = month_year.split(' ')[0]

        # Transform the month name to month index
        month = monthDict[month]

        year = month_year.split(' ')[1]

        days = monthTable.find_elements(By.CLASS_NAME, 'ekolCalendarDayNumberInRange')
        days = [day.text for day in days]

        slots = monthTable.find_elements(By.CLASS_NAME, 'ekolCalendarFreeTimeContainer')
        slots = [slot.text for slot in slots]

        df = pd.DataFrame({'year': year, 'month': month, 'day': days, 'slots': slots})

        dfList.append(df)

    # Concatenate the data frames into one
    df = pd.concat(dfList)
    # Concate the month and day columns into a date column
    df['yyyy-mm-dd'] = df['year'] + '-' + df['month'] + '-' + df['day']
    # Filter out the rows with no free slots
    mask = df['slots'] != '0 frei'
    # Get the available days as a list of dates
    availabeDays = df[mask]['yyyy-mm-dd'].tolist()
    return availabeDays

if __name__ == '__main__':
    get_available_days()
