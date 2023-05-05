############################## Changeable Variables ##############################
DEBUG = True
HEADLESS = False
PATH = "chromedriver.exe" # chrome driver's path
MAX_NUM_TRIALS = 30
SLEEP_BTWN_TRIALS = 0.5
###################################################################################
groupTxts = []
importSuccess = False
print("Importing libraries...")
from msvcrt import getch
try:
    # Other Libraries
    from time import sleep
    import getpass 
    import warnings
    import ctypes
    import datetime

    # Selenium Components   
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By

    importSuccess = True

except ImportError:
    print("It seems that some libraries has not beeen installed yet.")
    print("Did you installed all libraries in the 'requirements.txt' ?")

ctypes.windll.kernel32.SetConsoleTitleW("EE361 Group finder")

#################################################################################################
"""Scraping"""

def isLoaded(myBrowser):
    pageState = myBrowser.execute_script('return document.readyState;')
    return pageState == 'complete'

def waitUntilLoaded(myBrowser):
    while not isLoaded(myBrowser):
        print("Waiting page to load")
        sleep(SLEEP_BTWN_TRIALS)
    return

def getPart(marketBrowser, xpathTbox, partNo):
        textbox = marketBrowser.find_element(By.XPATH, xpathTbox)
        textbox.send_keys(partNo)
        textbox.send_keys(Keys.ENTER)

def getDigikey(partNo):
    textbox = browser_digikey.find_element(By.XPATH, "/html/body/header/div/div[1]/div/div[2]/div[2]/input")
    textbox.send_keys(partNo)
    textbox.send_keys(Keys.ENTER)
    link = browser_digikey.find_element(By.XPATH, "/html/body/div[2]/main/div/div/div[1]/div[2]/div[2]/section/div[2]/div/a").get_attribute('href')
    return link
       
if importSuccess:
    partArray = []
    with open("input.txt", "r", encoding="UTF-8") as fptr:
        partArray = fptr.readlines()
    # get rid of \n
    partArray = [part.strip() for part in partArray]
    try:
        print("Initalizing browser(s)...")
        myOptions = Options()
        if HEADLESS:
            myOptions.add_argument("--headless") # get rid of window
        myOptions.add_argument("--start-maximized")
        myOptions.add_argument("--no-sandbox")
        myOptions.add_argument("--log-level=3") # avoid boring log messages
        
        warnings.filterwarnings("ignore", category=DeprecationWarning) # get rid of deprecation warnings printed on console
        
        browser_digikey = webdriver.Chrome(PATH, chrome_options=myOptions)
        browser_mouser= webdriver.Chrome(PATH, chrome_options=myOptions)
        browser_ozdisan = webdriver.Chrome(PATH, chrome_options=myOptions)

        print("Loading ODTUCLASS...")
        browser_digikey.get("https://www.digikey.com")
        browser_mouser.get("https://www.mouser.com.tr")
        browser_ozdisan.get("https://ozdisan.com")
        
        waitUntilLoaded(browser_digikey)
        waitUntilLoaded(browser_mouser)
        waitUntilLoaded(browser_ozdisan)

        print(partArray)

        # getPart(browser_digikey, "/html/body/header/div/div[1]/div/div[2]/div[2]/input", partArray[0])
        print(getDigikey(partArray[0]))

    except (Exception, OSError, RuntimeError, ImportError, ValueError, IOError, IndexError, OverflowError, TypeError, ArithmeticError) as ex:
        print("An error occured:")
        print(ex)

#################################################################################################

print("Writing completed. Press any key to exit...")
getch()
try:
    print("Closing browser, please wait...")
    browser_digikey.quit()
    browser_mouser.quit()
    browser_ozdisan.quit()
except:
    print("Browser never has been launched")