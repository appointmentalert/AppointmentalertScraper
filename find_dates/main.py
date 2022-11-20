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


def excerpt_data(tables: list):
    all_free_slots = dict()
    for table in tables:
        month = MONTHS[table.text.split('\n')[0].split(' ')[0]]
        buttons = table.find_by_tag('button')
        monthly_free_slots = []
        for button in buttons:
            date, free = button.text.split('\n')
            free = int(free.removesuffix(' frei'))
            if free:
                monthly_free_slots.append((int(date), free))

        if monthly_free_slots:
            all_free_slots.update({int(month): monthly_free_slots})
    return all_free_slots


def all_time_clicking_wrapper(special_clicking_func):
    def wrapper(browser, url, tag):
        browser.visit(url)
        browser.driver.switch_to.frame(0)

        browser.find_by_name('AGREEMENT_ACCEPT').click()
        browser.find_by_name('ACTION_INFOPAGE_NEXT').click()

        special_clicking_func(browser)

        browser.find_by_name("ACTION_CONCERNSELECT_NEXT").click()
        optional = browser.find_by_name("ACTION_CONCERNCOMMENTS_NEXT")
        if optional:
            optional.click()
        data = excerpt_data(browser.find_by_css('table[class=ekolCalendarMonthTable]'))

        return {tag: data}

    return wrapper


@all_time_clicking_wrapper
def retrieve_kfzzulassung(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[2]/td[2]/div/button').click()
    browser.find_by_id("action_officeselect_termnew_prefix1222936509").click()
    browser.find_by_id("id_1224593434").find_by_xpath("//option[. = '1']").click()


@all_time_clicking_wrapper
def retrieve_reisegewerbe(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[8]/td[2]/div/button').click()
    browser.find_by_id("action_officeselect_termnew_prefix1595996623129").click()
    browser.find_by_id("id_1595996623151").find_by_xpath("//option[. = '1']").click()


@all_time_clicking_wrapper
def retrieve_fundbuero(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[3]/td[2]/div/button').click()
    browser.find_by_id('action_officeselect_termnew_prefix1459326045557').click()
    browser.find_by_id('id_1459327477898').find_by_xpath("//option[. = '1']").click()


@all_time_clicking_wrapper
def retrieve_aufenthaltstitel(browser):
    browser.find_by_css(".buttonTreeviewExpand").click()
    browser.find_by_id("action_officeselect_termnew_prefix1600340740349").click()
    browser.find_by_id("id_1600340740368").click()
    browser.find_by_id("id_1600340740368").find_by_xpath("//option[. = '1']").click()


@all_time_clicking_wrapper
def retrieve_pflichtumtausch(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[4]/td[2]/div/button').click()  # expand option list
    browser.find_by_id('action_officeselect_termnew_prefix1317888915').click()  # click button
    browser.find_by_id('id_1563449415908').find_by_xpath("//option[. = '1']").click()  # select dropdown


@all_time_clicking_wrapper
def retrieve_fahrerlaubnisangelegenheiten(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[5]/td[2]/div/button').click()  # expand option list
    browser.find_by_id('action_officeselect_termnew_prefix1586953390193').click()  # click button
    browser.find_by_id('id_1586953390210').find_by_xpath("//option[. = '1']").click()  # select dropdown


@all_time_clicking_wrapper
def retrieve_gewerbebehoerde(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[6]/td[2]/div/button').click()  # expand option list
    browser.find_by_id('action_officeselect_termnew_prefix1373375283').click()  # click button
    browser.find_by_id('id_1560944759741').find_by_xpath("//option[. = '1']").click()  # select dropdown


@all_time_clicking_wrapper
def retrieve_erlaubnispflichtiges_gewerbe(browser):
    browser.find_by_xpath('//*[@id="id_buergerauswahldienststelle_tree-office"]/tbody/tr[7]/td[2]/div/button').click()  # expand option list
    browser.find_by_id('action_officeselect_termnew_prefix1595996515007').click()  # click button
    browser.find_by_id('id_1595996515028').find_by_xpath("//option[. = '1']").click()  # select dropdown


@all_time_clicking_wrapper
def retrieve_TEMPLATE(browser):
    browser.find_by_xpath('FILL_ME').click()  # expand option list
    browser.find_by_id('FILL_ME').click()  # click button
    browser.find_by_id('FILL_ME').find_by_xpath("//option[. = '1']").click()  # select dropdown


def retrieve_all(browser, todos):
    all_data = {}
    for todo in todos:
        func, url, tag = todo[0], todo[1], todo[2]
        all_data.update(func(browser, url, tag))
    return all_data


def post_free_slots(data):
    http = urllib3.PoolManager()
    http.urlopen('POST', 'http://localhost:8080/assets',
                 headers={'Content-Type': 'application/json'},
                 body=json.dumps(data)
                 )


if __name__ == '__main__':
    url1 = 'https://www.leipzig.de/fachanwendungen/termine/index.html'
    url2 = 'https://www.leipzig.de/fachanwendungen/termine/abholung-aufenthaltstitel.html'
    todos = [(retrieve_kfzzulassung, url1, 'kfz_zulassung'),
             (retrieve_reisegewerbe, url1, 'reisegewerbe'),
             (retrieve_fundbuero, url1, 'fundbüro'),
             (retrieve_pflichtumtausch, url1, 'pflichtumtausch_führerschein'),
             (retrieve_fahrerlaubnisangelegenheiten, url1, 'fahrerlaubnisangelegenheiten'),
             (retrieve_gewerbebehoerde, url1, 'gewerbebehörde'),
             (retrieve_erlaubnispflichtiges_gewerbe, url1, 'erlaubnispflichtiges_gewerbe'),
             (retrieve_aufenthaltstitel, url2, 'aufenthaltstitel')]

    browser = Browser(driver_name='remote',
                      browser='Chrome',
                      command_executor='http://standalone-chrome:4444'
                      )
    post_free_slots(retrieve_all(browser, todos))
    browser.quit()
