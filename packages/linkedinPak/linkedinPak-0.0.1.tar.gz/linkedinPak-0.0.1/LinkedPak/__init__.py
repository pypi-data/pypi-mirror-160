
# import webdriver from selenium
from selenium import webdriver
import sys
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import warnings 
warnings.filterwarnings('ignore')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.linkedin.com/')
input("Press enter after login")

def follow_activities():
        
    # https://docs.google.com/spreadsheets/d/1qvQ3Fc35EEcq0AIrw8tvF62L5xBmHcPiKCmDZ-nqVgk/edit?usp=sharing
    sheet_id = "1qvQ3Fc35EEcq0AIrw8tvF62L5xBmHcPiKCmDZ-nqVgk" #update ID here
    df_sheet_base= "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet=".format(sheet_id)
    sheet_name = "Sheet1"
    df = pd.read_csv(df_sheet_base + sheet_name)
    # df

    for i in range(len(df)):
    # for i in range():

        try:    
            link = df["LinkedIn Profile URL"][i]
            driver.get(link)
            # to follow Activity
            follow_button = driver.find_element("xpath",'//div[@class="p2"]')
            sleep(2)
            follow_button.click()
            sleep(2)
        except:
            print(sys.exc_info()[0])

# follow_activities()

