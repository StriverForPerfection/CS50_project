from flask import Flask, render_template, redirect, request, url_for, flash, jsonify

# For selenium
import sqlite3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common import actions

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
#  Credits: CS50 problem sets ;) ^_^
import time

# Ensure the database is created successfuly. Credits: Bing Copilot

connection = sqlite3.connect("routerData.db", check_same_thread = False) # Connect to database
connection.row_factory = sqlite3.Row # Credit: https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
# .row_factory makescursor.execute calls return dictionaries in lieu of tuples!
cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS mainPassword(password TEXT NOT NULL DEFAULT 'cat')""")
cursor.execute("""CREATE TABLE IF NOT EXISTS routerData (
                name TEXT NOT NULL DEFAULT 'cat',
                password TEXT NOT NULL DEFAULT 'cat'
                )""")
cursor.execute("CREATE TABLE IF NOT EXISTS verifiedDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")

connection.commit()

 # Optimization for selenium. Credit: https://stackoverflow.com/questions/55072731/selenium-using-too-much-ram-with-firefox
options = webdriver.EdgeOptions()
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox')
options.add_argument('--disable-application-cache')
options.add_argument('--disable-gpu')
options.add_argument("--disable-dev-shm-usage")
### Adding this activates the code without opening a browser tab
# options.add_argument("headless")

driver = None
devices = [] # Array for LAN devices as a global array
allIntruders = [] # Devices with unsolicited access to the Wifi network
innocentDevices = [] # Devices allowed to access this wifi network

app = Flask(__name__, static_folder="static")
app.secret_key = "Very secret"
# static_folder ensures your server can find static files

def createDriver():

    # app.firstTimeOnly_funcs[None].remove(createDriver) (**Not necessary now)
    #This ensures the driver is created only the first time the app is run, credits: https://stackoverflow.com/questions/73570041/flask-deprecated-before-first-request-how-to-update & Bing Copilot
    
    global driver
    if driver is None:
        driver = webdriver.Edge(options=options)  # Initiate a driver object (instance of a browser, perhaps)
        driver.get("https://192.168.1.1")  # Let the browser go this link

        # Skip privacy error page:
        buttonAdvanced = driver.find_element(By.ID, "details-button")  # Click the advanced button to display the hyperlink
        buttonAdvanced.click()

        hyperlink1 = driver.find_element(By.ID, "proceed-link")  # Click the proceed to xyz hyperlink (must be made not
        # hidden first).
        hyperlink1.click()
    else:
        driver.get("https://192.168.1.1")  # Let the browser go this link
        # This ensure the link is reset every time

@app.route("/", methods = ["get", "post"])

def register():
    cursor.execute("SELECT * FROM mainPassword") # Credits: https://docs.python.org/3/library/sqlite3.html
    password = (cursor.fetchone())

    if not password: # If no password, this must be the first time you use the application
        if request.method == "POST":
            if request.form.get("password") != request.form.get("confirm"): # The passwords must be identical
                flash("The password and its confirmation aren't identical!")    
                return render_template("register.html") 
            else:  # If all is well, store the hash of the password in the database
                cursor.execute("INSERT INTO mainPassword (password) VALUES (?)", (generate_password_hash(request.form.get("password")),))
                connection.commit()

                flash("Registered successfully!")
                return render_template("getRouter.html")
        else:
            return render_template("register.html")
    else: # If a password is actually already stored, Log in
         return render_template("Login.html")


@app.route("/storeCred", methods = ["get", "post"])

def storeCred():
    if request.method == "POST":
        # You have to use a tuple to enter multiple variables #Credits: https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
        cursor.execute("DROP TABLE IF EXISTS routerData")
        cursor.execute("CREATE TABLE IF NOT EXISTS routerData (name TEXT NOT NULL DEFAULT 'cat', password TEXT NOT NULL DEFAULT 'cat')")
        cursor.execute("INSERT INTO routerData(name, password) VALUES(?, ?)", (request.form.get("name"), request.form.get("password")))
        connection.commit()
        return redirect("/getDevices")
    else:
        return render_template("getRouter.html")

@app.route("/LogIn", methods = ["Get", "Post"])
def LogIn():
    if request.method == "POST":

        password = request.form.get("password")
        cursor.execute("SELECT * FROM mainPassword")
        storedPassword = (cursor.fetchone())['password']

        if check_password_hash(storedPassword, password): # If the passwords match
            flash("Log in successful!")
            if cursor.execute("SELECT COUNT(*) FROM routerData").fetchone()[0] < 1:
                return redirect("/storeCred")
            return redirect("/getDevices")
        else:
            flash("Incorrect password!")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/getDevices", methods = ["Get", "Post"])

def getDevices():
    global devices

    if request.method == "POST":
        
        tmpIntruders = []
        tmpIntruders.clear()
        tmpIntruders = request.form.get("intruders").strip().split(",") # Get the intruders from getDevices.html
        #tmpIntruders changes on every POST.

        tmpInnocents = []
        tmpInnocents.clear()
        tmpInnocents = request.form.get("innocents").strip().split(",")
        #tmpInnocents changes on every POST.

        for i in tmpIntruders:
            global allIntruders
            if i not in allIntruders:
                allIntruders.append(i) # Store the new intruders with all the intruders

        for i in tmpInnocents:
            if i in allIntruders:
                allIntruders.remove(i) # Remove devices made innocent from the intruder list

        if tmpIntruders[0] != '' or tmpInnocents[0] != '': # On having no tmpintruders or tmpinnocents, it's a list containing "one" empty string
            createDriver()
            driver.get("https://192.168.1.1")
            time.sleep(0.6)

            ### REPEATED:++++++++++++++++++++++++++++++++++++++++
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

            time.sleep(1.25)

            #  Go to LAN devices:
            driver.get("https://192.168.1.1/html/advance.html#parent_control")
        
            time.sleep(4) # Ensure the drop list doesn't refresh

            ###:++++++++++++++++++++++++++++++++++++++++
            
            try: # Delete the old rule so as to create only one rule for all devices
                
                # Click the delete button
                deleteOldRule = driver.find_elements(By.CSS_SELECTOR, "a[id^='macfilter_view_data_list_InternetGatewayDevice_X_FireWall_TimeRule']")
                (deleteOldRule[1]).click()
                
                time.sleep(0.5)
                # Click the confirmation (text = "ok") button:
                deleteRuleConfirm = driver.find_element(By.CSS_SELECTOR, "button[class='atp_button modal-confirm']")
                deleteRuleConfirm.click()
                time.sleep(2.5)

            finally:

                # Get the device names and their checkboxes 

                # Click the "new time rule" link
                newTimeRule = driver.find_element(By.ID, "macfilter_view_data_add_link")
                newTimeRule.click()
                time.sleep(1)
                
                # Get the device names
                deviceNames = driver.find_elements(By.CSS_SELECTOR, "label[class='pull-left third_menu_below_config_font margintop_n3']")
                checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")

                devices.clear()
                for i in range(1, len(deviceNames)):
                    device = {}
                    device["name"] = (deviceNames[i].text).strip()
                    device["checkbox"] = checkboxes[i + 1]
                    devices.append(device)
             
                # Check/select intruders Intruders:

                for i in range(len(allIntruders)):
                    for j in range(len(devices)):
                        if allIntruders[i] == (devices[j])["name"]:
                            ((devices[j])["checkbox"]).click()
                            break # No need for additional iterations
                
                # Set the upper time limit:
                time.sleep(0.15)
                uprTimeLimit = driver.find_element(By.CSS_SELECTOR, "input[class='ember-view ember-text-field time margintop_n3 marginleft_5']")
                uprTimeLimit.clear()
                uprTimeLimit.send_keys("08:01") 
                #   The upper time limit is only one minute larger than the lower limit, practically preventing intruders
                #   from benefiting from this wifi.
                
                # Give a name for this time rule:

                ruleName = driver.find_element(By.CSS_SELECTOR, "input[class='ie6widthbug']")
                ruleName.send_keys("blockIntruders")

                # Save the time rule:
                saveButton = driver.find_element(By.ID, "macfilter_view_data_list_multiedit_submitctrl")
                saveButton.click()

                global innocentDevices
                innocentDevices.clear() # Devices allowed to access this wifi

                for i in range(len(devices)): # Store the devices allowed to access the wifi network
                    if (devices[i])["name"] in allIntruders:
                        continue # Don't store the intruder as an innocent device
                    innocentDevices.append(devices[i])

                return render_template("getDevices.html", devices = innocentDevices, allIntruders = allIntruders)
            

        # You shall go into this branch if you've exitted the application and reopened it to restore stored data.
        elif (len(innocentDevices) == 0 and (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] > 0) or (len(allIntruders) == 0 and (cursor.execute("SELECT COUNT(*) FROM intruderDevices")).fetchone()[0] > 0):
            # This two important if statements ensure the innocentDevices and allIntruders arrays are populated even
            # when the user closes the web application.

            if len(innocentDevices) == 0 and (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] > 0:

                for i in (cursor.execute("SELECT * FROM verifiedDevices")).fetchall():
                    device = {}
                    device["name"] = i["name"]
                    innocentDevices.append(device)

            if len(allIntruders) == 0 and (cursor.execute("SELECT COUNT(*) FROM intruderDevices")).fetchone()[0] > 0:
                for i in (cursor.execute("SELECT * FROM intruderDevices")).fetchall():
                    allIntruders.append(i["name"])


            # Store verified devices in database
            cursor.execute("DROP TABLE IF EXISTS verifiedDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS verifiedDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            for item in innocentDevices:
                cursor.execute("INSERT INTO verifiedDevices (name) VALUES(?)", (item["name"], ))
            connection.commit()

            # Store intruders in database
            cursor.execute("DROP TABLE IF EXISTS intruderDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS intruderDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            for item in allIntruders:
                cursor.execute("INSERT INTO intruderDevices (name) VALUES(?)", (item, ))
            connection.commit()

            return render_template("getDevices.html", devices=innocentDevices, allIntruders=allIntruders, signal = 1)
        
        # If the user doesn't choose any intruders
        elif (len(innocentDevices) == 0 and (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] == 0):
            cursor.execute("DROP TABLE IF EXISTS verifiedDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS verifiedDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            for item in devices:
                cursor.execute("INSERT INTO verifiedDevices (name) VALUES(?)", (item["name"], ))
            connection.commit()

            # Store intruders in database
            cursor.execute("DROP TABLE IF EXISTS intruderDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS intruderDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            return render_template("getDevices.html", devices=devices)

        else:
            # Reset databases on new changes

            # Store verified devices in database
            cursor.execute("DROP TABLE IF EXISTS verifiedDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS verifiedDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            # Store intruders in database
            cursor.execute("DROP TABLE IF EXISTS intruderDevices")
            cursor.execute("CREATE TABLE IF NOT EXISTS intruderDevices(name TEXT NOT NULL DEFAULT 'fillerVeriDev')")
            connection.commit()

            if (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] == 0:
                for item in innocentDevices:
                    cursor.execute("INSERT INTO verifiedDevices (name) VALUES(?)", (item["name"], ))
                connection.commit()

            if (cursor.execute("SELECT COUNT(*) FROM intruderDevices")).fetchone()[0] == 0:
                for item in allIntruders:
                    cursor.execute("INSERT INTO intruderDevices (name) VALUES(?)", (item, ))
                connection.commit()

            if (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] > 0: # If verifiedDevices is not empty
                inno = []
                for i in (cursor.execute("SELECT * FROM verifiedDevices")).fetchall():
                    device = {}
                    device["name"] = i["name"]
                    inno.append(device)
                intr = []
                for i in (cursor.execute("SELECT * FROM intruderDevices")).fetchall():
                    intr.append(i["name"])

            flash("Acknowledged devices stored in database successfully!")
            return render_template("getDevices.html", devices = inno, allIntruders = intr, signal = 1)

    else:
        if (cursor.execute("SELECT COUNT(*) FROM verifiedDevices")).fetchone()[0] > 0: # If verifiedDevices is not empty (will most probably occur after the app is first used)
            inno = []
            for i in (cursor.execute("SELECT * FROM verifiedDevices")).fetchall():
                device = {}
                device["name"] = i["name"]
                inno.append(device)
        
            intr = []
            for i in (cursor.execute("SELECT * FROM intruderDevices")).fetchall():
                intr.append(i["name"])

            
            return render_template("getDevices.html", devices = inno, allIntruders = intr, signal = 1)
        
        createDriver()
        time.sleep(0.25)
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

        time.sleep(0.5)

        #  Go to LAN devices:
        driver.get("https://192.168.1.1/html/advance.html#parent_control")
    
        time.sleep(2.75) # Ensure the devices have loaded 

        # Click the "new time rule" link
        newTimeRule = driver.find_element(By.ID, "macfilter_view_data_add_link")
        newTimeRule.click()
        time.sleep(1)
        
        # Get the device names
        deviceNames = driver.find_elements(By.CSS_SELECTOR, "label[class='pull-left third_menu_below_config_font margintop_n3']")
        
        devices.clear()

        for i in range(1, len(deviceNames)):
            device = {}
            device["name"] = (deviceNames[i].text).strip()
            devices.append(device)
        
        return render_template("getDevices.html", devices = devices)


@app.route("/changeRouter", methods = ["get", "post"])
def changeRouter():
    if request.method == "POST":
        if not check_password_hash(((cursor.execute("SELECT * FROM mainPassword")).fetchone())["password"], request.form.get("app password")):
            flash("The app password is incorrect!")
            return render_template("changeRouter.html")
        else: # Store router credentials in database
            name = request.form.get("router username")
            password = request.form.get("router password")

            cursor.execute("DELETE FROM routerData")
            cursor.execute("INSERT INTO routerData (name, password) VALUES(?, ?)", (name, password))
            connection.commit()
            return redirect("/getDevices")
    else:
        return render_template("changeRouter.html")
    

@app.route("/changePassword", methods = ["get", "post"])
def changePassword():
    
    if request.method == "POST":
        if not check_password_hash(((cursor.execute("SELECT * FROM mainPassword")).fetchone())["password"], request.form.get("old password")):
            flash("This isn't the old password!")
            return render_template("changePassword.html")
        elif request.form.get("new password") != request.form.get("confirmation"): # Passwords must match
            flash("Passwords don't match!")
            return render_template("changePassword.html")
        else: # Store new password in database
            cursor.execute("DELETE FROM mainPassword")
            cursor.execute("INSERT INTO mainPassword VALUES (?)", (generate_password_hash(request.form.get("new password")), ))
            connection.commit()
            return redirect("/getDevices")
    else:
        return render_template("changePassword.html")


@app.route("/detectIntruders", methods = ["get", "post"])
def detectIntruders():
    createDriver()

    currentDevices = []
    currentDevices.clear()
    time.sleep(0.5)

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

    time.sleep(1)

    #  Go to LAN devices:
    driver.get("https://192.168.1.1/html/advance.html#parent_control")

    time.sleep(2.5) # Ensure the devices have loaded


    # Click the "new time rule" link
    newTimeRule = driver.find_element(By.ID, "macfilter_view_data_add_link")
    newTimeRule.click()
    time.sleep(0.5)
    
    # Get the device names
    deviceNames = driver.find_elements(By.CSS_SELECTOR, "label[class='pull-left third_menu_below_config_font margintop_n3']")
    
    devices.clear()

    for i in range(1, len(deviceNames)):
        device = {}
        device["name"] = (deviceNames[i].text).strip()
        currentDevices.append(device["name"])

    newIntruders = []
    tmpInno = []
    for i in cursor.execute("SELECT * FROM verifiedDevices").fetchall():
        tmpInno.append(i["name"])
    tmpIntr = []
    for i in cursor.execute("SELECT * FROM intruderDevices").fetchall():
        tmpIntr.append(i["name"])

    for i in currentDevices:
        if i not in tmpInno and i not in tmpIntr: # If there's a device neither in innocent not intruder devices (never seen before), it's a new intruder
            newIntruders.append(i)
    
    return jsonify(newIntruders) # Jsonify ensures the page needn't refresh

@app.route("/clearDevices" , methods = ["get", "post"])
def clearDevices():
    if request.method == "POST":
        if not check_password_hash(((cursor.execute("SELECT * FROM mainPassword")).fetchone())["password"], request.form.get("app password")):
            flash("The app password is incorrect!")
            return render_template("clearDevices.html")
        else:
            cursor.execute("DELETE FROM verifiedDevices")
            cursor.execute("DELETE FROM intruderDevices")

            createDriver()
            driver.get("https://192.168.1.1")
            time.sleep(0.25)

            ### REPEATED:++++++++++++++++++++++++++++++++++++++++
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

            time.sleep(0.5)

            #  Go to LAN devices:
            driver.get("https://192.168.1.1/html/advance.html#parent_control")
        
            time.sleep(1.2) # Ensure the drop list doesn't refresh

            ###:++++++++++++++++++++++++++++++++++++++++
            
            # Delete the old rule so as to create only one rule for all devices
            try:
                # Click the delete button
                deleteOldRule = driver.find_elements(By.CSS_SELECTOR, "a[id^='macfilter_view_data_list_InternetGatewayDevice_X_FireWall_TimeRule']")
                (deleteOldRule[1]).click()
                
                time.sleep(0.5)
                # Click the confirmation (text = "ok") button:
                deleteRuleConfirm = driver.find_element(By.CSS_SELECTOR, "button[class='atp_button modal-confirm']")
                deleteRuleConfirm.click()
                time.sleep(1)
                connection.commit()

                flash("Database and time rule cleared successfully")
                return redirect("/")
            except:
                flash("Database cleared successfully")
                return redirect("/")
    else:
        return render_template("clearDevices.html")
    
if __name__ == '__main__':
    app.run(debug=True)
