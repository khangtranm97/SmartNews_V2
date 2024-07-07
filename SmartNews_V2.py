import time
import Get_Login_Token


print('SmartNews V2 Downloader is running. Please wait')
#Login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import Get_Login_Token




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
    return print('Login by code selected. Code sended to your email address !')
login_with_code()
#Get login token
login_token=Get_Login_Token.get_token()
#login

print('Completed')
time.sleep(5)
#status=driver.current_url
#print(status)
#time.sleep(10)