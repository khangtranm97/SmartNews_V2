from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import sys
from selenium import webdriver
from datetime import datetime,timedelta
import glob
import json
import time
import os
import msvcrt
import pandas as pd
import shutil
from datetime import date

#Get date time
start_time = time.time()
now = datetime.now()
current_date = str(date.today())
year_month, split_part, day = current_date.rpartition('-')
years,plit,month=year_month.rpartition('-')
today  =years+month+day

#Path folder define
if getattr(sys, 'frozen', False):  # Check if running as compiled executable
        script_path = sys.executable  # Path of the executable
else:
        script_path = os.path.abspath(__file__) 
file_contain_folder = os.path.dirname(script_path)

#Create raw folder
raw_folder=file_contain_folder+'\\Raw'
if not os.path.exists(raw_folder):
        os.mkdir(raw_folder)

#Create download folder
download_folder=file_contain_folder+'\\Download'
if not os.path.exists(download_folder):
        os.mkdir(download_folder)

final_folder =download_folder+'\\'+today
if not os.path.exists(final_folder):
        os.mkdir(final_folder)
        
#Define and get config file
config_path=file_contain_folder+'\\config.json'
with open(config_path, 'r') as file:
    data = json.load(file)
url=data['url']
timestamp_file = file_contain_folder+'/timestamp.txt'

#Set chrome options
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    'download.default_directory': raw_folder,  # Set download directory
    'download.prompt_for_download': False,              # Disable download prompt
    'download.directory_upgrade': True,                 # Upgrade the directory
    'safebrowsing.enabled': True,                        # Enable safe browsing
    'plugins.always_open_pdf_externally': True          # Open PDF files externally
})

# Running
print(f" ,-----.  ,---.  ,------.,--.   ,--.,-----.    ,---.  ,------.   ,---.        ")
print(f"'  .--./ /  O  \\ |  .--. '\\  `.'  / |  |) /_  /  O  \\ |  .--. ' /  O  \\  ")
print(f"|  |    |  .-.  ||  '--' | '.    /  |  .-.  \\|  .-.  ||  '--'.'|  .-.  |      ")
print(f"'  '--'\\|  | |  ||  | --'    |  |   |  '--' /|  | |  ||  |\\  \\ |  | |  |      ")
print(f" `-----'`--' `--'`--'        `--'   `------' `--' `--'`--' '--'`--' `--'      ")
print('------------------------------------------------------------------------')
print('RUN')
print('Get chrome options.')
driver = webdriver.Chrome(options=options)
print('Set chrome options completed.')
driver.get(data['work_link']) 
print('Loading cookies')
#Load cookie
with open('cookies.json', 'r') as file:
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.refresh()

#Define total raw delete function
def total_delete(import_path,export_path,delete_condition):
    data=pd.read_csv(import_path)
    df_cleaned = data[data[delete_condition].notna() & (data[delete_condition] != '')]
    df_cleaned.to_csv(export_path, index=False)
    return print('Total row deleted')

#Define download function
def download(url,acc_id,download_type,download_start,download_end,template_id,delete,delete_condition,wait,breakdown,audience):
    #Check and delete all file in raw folder
    if os.path.exists(raw_folder) and os.path.isdir(raw_folder):
        files = glob.glob(os.path.join(raw_folder, '*'))
        for file in files:
            os.remove(file)
        print(f"All files in raw folder have been deleted.\n")
    else:
        print(f"Raw folder does not exist.\n")
        
    #Access to download url
    print('Access url success')
    parse_work_url=url+acc_id+'/'+download_type+'?start_date='+str(download_start)+'&end_date='+str(download_end)+'&report='+template_id
    controller=driver.get(parse_work_url)
    
    #Wait for page loading and download button display to donwload
    time.sleep(10)
    download_button_class='/html/body/div[1]/div/div/main/div[2]/div[2]/div/div/div/div[1]/div[3]/div[3]'
    controller=driver.find_element(By.XPATH,download_button_class).click()

    #Choose by day or by time and wait for fully loaded
    print('Checking download required')
    time.sleep(5)
    
    #Time breakdown
    by_age='input[type="radio"][value="age"]'
    by_gender='input[type="radio"][value="gender"]'
    by_age_gender='input[type="radio"][value="age_and_gender"]'
    by_connection_type='input[type="radio"][value="connection_type"]'
    by_prefecture='input[type="radio"][value="prefecture"]'
    by_carrier_type='input[type="radio"][value="carrier_type"]'
    by_city='input[type="radio"][value="city"]'
    by_device_type='input[type="radio"][value="device_type"]'
    by_os='input[type="radio"][value="os"]'
    by_day='input[type="radio"][value="day"]'
    by_time='input[type="radio"][value="hour"]'
    
    #controller=driver.find_element(By.CSS_SELECTOR, by_day).click()
    #time.sleep(2)
    if breakdown=='時間帯別':
        controller=driver.find_element(By.CSS_SELECTOR, by_time).click()
        time.sleep(1)
        print('Downloading !')
        #Download and wait for donwload completed
        controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
    elif breakdown=='なし':
        match audience:
            case 'なし':
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '年齢':
                controller=driver.find_element(By.CSS_SELECTOR, by_age).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '性別':
                controller=driver.find_element(By.CSS_SELECTOR, by_gender).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '年齢・性別':
                controller=driver.find_element(By.CSS_SELECTOR, by_age_gender).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '回線':
                controller=driver.find_element(By.CSS_SELECTOR, by_connection_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '都道府県':
                controller=driver.find_element(By.CSS_SELECTOR, by_prefecture).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '通信キャリア':
                controller=driver.find_element(By.CSS_SELECTOR, by_carrier_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '市':
                controller=driver.find_element(By.CSS_SELECTOR, by_city).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case 'デバイス':
                controller=driver.find_element(By.CSS_SELECTOR, by_device_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case 'OS':
                controller=driver.find_element(By.CSS_SELECTOR, by_os).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
    elif breakdown=='日別':
        controller=driver.find_element(By.CSS_SELECTOR, by_day).click()
        time.sleep(1)
        match audience:
            case 'なし':
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '年齢':
                controller=driver.find_element(By.CSS_SELECTOR, by_age).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '性別':
                controller=driver.find_element(By.CSS_SELECTOR, by_gender).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '年齢・性別':
                controller=driver.find_element(By.CSS_SELECTOR, by_age_gender).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '回線':
                controller=driver.find_element(By.CSS_SELECTOR, by_connection_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '都道府県':
                controller=driver.find_element(By.CSS_SELECTOR, by_prefecture).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '通信キャリア':
                controller=driver.find_element(By.CSS_SELECTOR, by_carrier_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case '市':
                controller=driver.find_element(By.CSS_SELECTOR, by_city).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case 'デバイス':
                controller=driver.find_element(By.CSS_SELECTOR, by_device_type).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
            case 'OS':
                controller=driver.find_element(By.CSS_SELECTOR, by_os).click()
                time.sleep(1)
                print('Downloading !')
                controller=driver.find_element(By.XPATH,'//*[@id="body"]/div[2]/div/div[2]/div/div[2]/div/div[3]/button[2]').click()
    #Get the last download file、rename and relocate to Download Folder
    raw_files=os.listdir(raw_folder)
    print('Wait for downloading !')
    check=len(raw_files)
    check_count=0
    while check==0 and check_count<5:
        time.sleep(wait)
        raw_files=os.listdir(raw_folder)
        if len(raw_files)>0 and os.path.splitext(raw_files[0])[1]=='.csv':
            print('Download completed\n')
            delete_status='FALSE'
            if str(delete)=='ON':
                delete_status='TRUE'
            print('Is total row delete :',delete_status)
            latest_file = max([os.path.join(raw_folder, f) for f in raw_files], key=os.path.getctime)
            if delete=='TRUE':
                total_delete(latest_file,latest_file,delete_condition)
            final_folder_files=os.listdir(final_folder)
            new_file_name = acc_id+'_'+download_type+'_'+str(download_start).replace('-', '')+'_'+str(download_end).replace('-', '')+'.csv'
            new_file_path = os.path.join(os.path.abspath(file_contain_folder)+'\\Download\\'+today, new_file_name)
            count=0
            name_count=0
            options_out=''
            if breakdown=='なし' and audience=='なし':
                options_out=''
            if breakdown=='なし' and audience!='なし':
                options_out='_'+audience
            if breakdown!='なし' and audience=='なし':
                options_out='_'+breakdown
            if breakdown!='なし' and audience!='なし':
                options_out='_'+breakdown+'_'+audience
            new_file_name = acc_id+'_'+download_type+'_'+str(download_start).replace('-', '')+'_'+str(download_end).replace('-', '')+(options_out)+'.csv'
            while count<len(final_folder_files):
                exist_file_name=str(final_folder_files[count])
                if str(new_file_name)!=exist_file_name:
                #print('File name is not exist')
                #print('Set file name: ',new_file_name)
                    count+=1
                else:
                #print('File name existed')
                    name_count+=1
                    new_file_name = acc_id+'_'+download_type+'_'+str(download_start).replace('-', '')+'_'+str(download_end).replace('-', '')+(options_out)+'_('+str(name_count)+').csv'                      
                    #print('Set file name: ',new_file_name+'\n')
                    count+=1
            new_file_path = os.path.join(os.path.abspath(final_folder)+'\\'+ new_file_name)
            print('Final file name :',new_file_name)
            #print('Last file is: ',latest_file)
            shutil.move(latest_file, new_file_path)
            print('DOWNLOAD COMPLETED WITH DATA IN ROW: '+str(count+1))
            print('Account ID: ',acc_id)
            print('Download Level: ',download_type)
            print('Download start: ',download_start)
            print('Donwload End: ',download_end)
            print('Template ID: ',template_id)
            delete_status=''
            if delete=='ON':
                delete_status='TRUE'
            else: delete_status='FALSE'
            print('Total Raw Delete: ',delete_status)
            print('時間別の内訳: ',breakdown)
            print('オーディエンス別の内訳: ',audience)
            print('\n')
            break
        else:
            if len(raw_files)==0 and check_count==4: 
                print('Download fail after 5 attemp ! Wait too long')
                check_count+=1
            elif len(raw_files)==0 and check_count<5:
                check_count+=1
                print('Wait time ',check_count)
    
#Get download data from setting's file and convert to dataframe
print('Get download info from setting file !\n')
download_setting = pd.read_excel('Download_Setting.xlsx', sheet_name='Run')
row_count=len(download_setting)
for count in range(row_count):
    run_status=download_setting.at[count,'Status']
    if run_status =='ON':
        print('\nDownload with data in row :',count+1)
        run_element={'status':'',
                     'account_id':'',
                     'download_type':'',
                     'download_start':'',
                     'download_end':'',
                     'template_id':'',
                     'delete':'',
                     'delete_condition':'',
                     'wait':'',
                     '時間別の内訳':'',
                     'オーディエンス別の内訳':''
                     }
       
        run_element['status']=download_setting.at[count,'Status']
        run_element['account_id']=str(download_setting.at[count,'Acc ID'])
        run_element['download_type']=download_setting.at[count,'Download Type']
        run_element['download_time']=download_setting.at[count,'Download Time']
        run_element['template_id']=download_setting.at[count,'Template Id']
        delete_status=''
        if download_setting.at[count,'Total Row Delete']=='ON':
            delete_status='TRUE'
        else: delete_status='FALSE'
        run_element['delete']=delete_status
        run_element['delete_condition']=download_setting.at[count,'Delete Condition']
        run_element['wait']=str(int(download_setting.at[count,'Wait']))
        run_element['時間別の内訳']=str((download_setting.at[count,'時間別の内訳']))
        run_element['オーディエンス別の内訳']=str((download_setting.at[count,'オーディエンス別の内訳']))
         #Parse download time:
        this_month_day1=now.replace(day=1).date()
        yesterday=(now-timedelta(days=1)).date()
        lastmonth_end=this_month_day1- timedelta(days=1)
        lastmonth_day1=lastmonth_end.replace(day=1)
        if run_element['download_time']=='This month':
            run_element['download_start']=str(this_month_day1)
            run_element['download_end']=str(yesterday)
        elif run_element['download_time']=='Last month':
            run_element['download_start']=str(lastmonth_day1)
            run_element['download_end']=str(lastmonth_end)
        else:
            if run_element['download_time'].find(': ')>-1:
                 date=run_element['download_time'].replace('Custom: ','')
            else:
                date=run_element['download_time'].replace('Custom:','')
            date_arr=date.split(';')
            date_format = "%Y%m%d"
            run_element['download_start'] = (datetime.strptime((date_arr[0]), date_format)).date()
            run_element['download_end']=(datetime.strptime((date_arr[1]), date_format)).date()
        print('Get download info completed')
        print(run_element)
        print('Downloading !\n')
        #parse_work_url=url+run_element['account_id']+'/'+run_element['download_type']+'?start_date='+str(run_element['download_start'])+'&end_date='+str(run_element['download_end'])+'&report='+run_element['template_id']
        download(url,run_element['account_id'],run_element['download_type'],run_element['download_start'],run_element['download_end'],run_element['template_id'],run_element['delete'],str(run_element['delete_condition']),int(run_element['wait']),run_element['時間別の内訳'],run_element['オーディエンス別の内訳']) 
driver.quit()
end_time = time.time()
elapsed_time = end_time - start_time
print(f"All task completed in: {elapsed_time:.0f}s")
print("Press any key to continue...")
msvcrt.getch()