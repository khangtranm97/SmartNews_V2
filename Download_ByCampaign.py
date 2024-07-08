from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json

#Xpath
acc_id_xpath='//*[@id="root"]/div/div/div/div[3]/div[1]/div/div/div/span[2]'
time_picker_xpath='//*[@id="root"]/div/div/main/div[1]/div[2]/div[2]/div/div[1]'
start_time_xpath='//*[@id="root"]/div/div/main/div[1]/div[2]/div[2]/div/div[1]/div[1]/input'
end_time_xpath=''
template_select_xpath='//*[@id="rc-tabs-0-panel-campaigns"]/div/div[1]/div[3]/div[2]/button'
template_xpath='//*[@id="rc-tabs-0-panel-campaigns"]/div/div[1]/div[3]/div[2]/div/div/ul/li[4]/ul/li[2]/span'
export_report_xpath='//*[@id="rc-tabs-0-panel-campaigns"]/div/div[1]/div[3]/div[3]/button/span[2]'
bydate_xpath='//*[@id="body"]/div[4]/div/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/div/div[3]/label'
report_export_xpath='//*[@id="body"]/div[4]/div/div[2]/div/div[2]/div[3]/button[2]/span'
#Id
cpn_address_id='input.send_keys(start_time)'

#Get information from json file
with open('get_something.json') as f:
    data = json.load(f)
acc_id=data['acc_id']
start_time=data['start_time']
end_time=data['end_time']
time.sleep(2)


def download_campaign():    
    work_url='https://ads.smartnews.com/am/ad_accounts/1001502/campaigns'
    driver = webdriver.Chrome()
    driver.get(work_url)
    time.sleep(3)
    controller = driver.find_element(By.XPATH, acc_id_xpath)
    controller.click()
    input.send_keys(acc_id)
    time.sleep(3)
    controller = driver.find_element(By.XPATH, time_picker_xpath)
    input.clear()
    input.send_keys(start_time)
    input.send_keys(end_time)
    time.sleep(5)
    controller=driver.find_element(By.ID,cpn_address_id)
    controller.click()
    time.sleep(3)
    controller=driver.find_element(By.XPATH,template_select_xpath)
    controller.click()
    controller=driver.find.element(By.XPATH, template_xpath)
    controller.click()
    controller=driver.find_element(By.XPATH, export_report_xpath)
    controller.click()
    controller=driver.find_element(By.XPATH,bydate_xpath)
    controller.click()
    controller=driver.find_element(By.XPATH,report_export_xpath)
    controller.click()
    time.sleep(10)
download_campaign()