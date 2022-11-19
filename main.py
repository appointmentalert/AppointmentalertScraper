from splinter import Browser
import urllib3
import json

MONTHS = dict(Januar=1,
              Februar=2,
              März=3,
              April=4,
              Mai=5,
              Juni=6,
              Juli=7,
              August=8,
              September=9,
              Oktober=10,
              November=11,
              Dezember=12)


def retrieve_aufenthaltstitel():
    browser = Browser(driver_name='chrome')
    browser.visit('https://www.leipzig.de/fachanwendungen/termine/abholung-aufenthaltstitel.html')
    browser.driver.switch_to.frame(0)

    browser.find_by_name('AGREEMENT_ACCEPT').click()
    browser.find_by_name('ACTION_INFOPAGE_NEXT').click()
    browser.find_by_css(".buttonTreeviewExpand").click()
    browser.find_by_id("action_officeselect_termnew_prefix1600340740349").click()
    browser.find_by_id("id_1600340740368").click()
    browser.find_by_id("id_1600340740368").find_by_xpath("//option[. = '1']").click()
    browser.find_by_id("action_concernselect_next").click()
    browser.find_by_id("action_concerncomments_next").click()

    tables = browser.find_by_css('table[class=ekolCalendarMonthTable]')
    all_free_slots = dict()
    for table in tables:
        month = MONTHS[table.text.split('\n')[0].split(' ')[0]]
        buttons = table.find_by_tag('button')
        monthly_free_slots = []
        for button in buttons:
            date, free = button.text.split('\n')
            free = int(free.removesuffix(' frei'))
            if free:
                monthly_free_slots.append((date, free))

        if monthly_free_slots:
            all_free_slots.update({month: monthly_free_slots})

    return all_free_slots


def post_free_slots(data):
    http = urllib3.PoolManager()
    http.urlopen('POST', 'http://localhost:8080/assets',
                 headers={'Content-Type': 'application/json'},
                 body=json.dumps(data))


if __name__ == '__main__':
    post_free_slots(retrieve_aufenthaltstitel())
