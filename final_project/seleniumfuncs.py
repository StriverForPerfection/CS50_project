from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium import webdriver

# Optimization for selenium. Credit: https://stackoverflow.com/questions/55072731/selenium-using-too-much-ram-with-firefox
options = webdriver.EdgeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Edge(options=options)  # Initiate a driver object (instance of a browser, perhaps)
driver.get("https://192.168.1.1")  # Let the browser go this link
import time


def passPrivacy():

    # Skip privacy error page:
    buttonAdvanced = driver.find_element(By.ID, "details-button")  # Click the advanced button to display the hyperlink
    buttonAdvanced.click()

    hyperlink1 = driver.find_element(By.ID, "proceed-link")  # Click the proceed to xyz hyperlink (must be made not
    # hidden first).
    hyperlink1.click()


def goToDevices(cursor):
    
    # LogIn page:
    # Get the name and password input fields on the login page
    name = driver.find_element(By.ID, "index_username")
    password = driver.find_element(By.ID, "password")

    # Get the stored router name and password

    cursor.execute("SELECT name FROM routerData")
    Rname = (cursor.fetchone())["name"]

    cursor.execute("SELECT password FROM routerData")
    Rpassword = cursor.fetchone()["password"]

    name.clear()
    name.send_keys(Rname)

    password.clear()
    password.send_keys(Rpassword)

    loginbtn = driver.find_element(By.ID, "loginbtn")
    loginbtn.click()

    print(driver.title)
    # _ = WebDriverWait(driver, 10).until(lambda element: driver.find_element(By.ID, "homenetwork_settings_menu"))
    time.sleep(0.5)

    #  Go to LAN devices:
    driver.get("https://192.168.1.1/html/advance.html#landevices")

    time.sleep(2) # Ensure the devices have loaded

def getDeviceNames():
    # Get the device names and their delete buttons
    deviceNames = driver.find_elements(By.CSS_SELECTOR, "div[id^='landev_ip_view_data_list_InternetGatewayDevice_LANDevice']")
    deviceDeletes = driver.find_elements(By.CSS_SELECTOR, "span[class^='ember-view controls-pad-right change_del text_left pull-left']")

    devices = []

    # Populate the devices array with LAN devices and their corresponding delete buttons
    for i in range(0, len(deviceNames), 2):
        device = {}
        device["name"] = (deviceNames[i].text).split()[0]
        device["deleter"] = deviceDeletes[i]
        devices.append(device)
    return devices