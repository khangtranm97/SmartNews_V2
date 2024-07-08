#Login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import Get_Login_Token

login_code_input_xpath='//*[@id="app"]/div/section/div/div/div/div/div[2]/div[1]/div/form/div[1]/div/input'
login_xpath='//*[@id="app"]/div/section/div/div/div/div/div[2]/div[1]/div/form/div[2]/button'

print('SmartNews V2 Downloader is running. Please wait')
#Login with code select
def login_with_code():
    mailaddress ='ca_smartnews@ext.cyberagent.co.jp'
    work_url="https://ads.smartnews.com/login#"
    page_address="//html/body/div/form/div/div[1]/div[2]/div/div[3]/button"
    driver = webdriver.Chrome()
    driver.get(work_url)
    time.sleep(2)
    controller = driver.find_element(By.XPATH, page_address)
    controller.click()


    #Login email input
    input=driver.find_element(By.CLASS_NAME,'input')
    time.sleep(1)
    input.send_keys(mailaddress)

    #Send code
    codesender=driver.find_element(By.CLASS_NAME,'button.is-dark.is-fullwidth')
    time.sleep(1)
    codesender.click()
    time.sleep(10)
    print('Login by code selected. Code sended to your email address !')
    #Get login token
    login_token=Get_Login_Token.get_token()
    controller=driver.find_element(By.XPATH,login_code_input_xpath)
    controller.send_keys(login_token)
    controller=driver.find_element(By.XPATH,login_xpath)
    controller.click()
    print('Login Completed')
    time.sleep(5)
    driver.quit()
    #Download_ByCampaign.download_campaign()
login_with_code()


#status=driver.current_url
#print(status)
#time.sleep(10)