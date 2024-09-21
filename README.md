# This is SafeFi!
#### _My humble wifi protection web application_
### Video demo: https://youtu.be/imhKwAO75ZQ
### Description: It's a web application built in Python using Flask and Selenium. It allows you to control the accessibility of your wifi to any device, and detects new intruders.

## Files:
## In the "templates" folder:

### Register.html:
![image](https://github.com/user-attachments/assets/a52df35f-4ca5-4a1f-ade0-4363e500701d)

It's the first page you'll see on opening the application. Inside it, you'll enter the **sole** password for the application. There's only one password for the application because it's assumed that only one person (you, in this case) will have access to the router settings. This is meant to avoid allowing any other user to register and alter anything you've done. 
### getRouter.html:
![image](https://github.com/user-attachments/assets/660515b1-cc84-4053-90e2-f022cd2ab952)

After entering a password, you'll now go on and enter the username and password for your router. Don't worry, these will only be stored on your device after you clone the repository.

### getDevices.html:
This is where all of the action takes place! 

![image](https://github.com/user-attachments/assets/a52ac333-16e1-4aa8-9aad-39e7f242f889)

**Here, you have three sections:**
1. Devices with access to wifi section:
   _you can check any of them to go into the following intruders section_
2. Intruders section:
   Here reside devices that are marked by you as intruders.

   ![image](https://github.com/user-attachments/assets/6c4c2270-0baa-4957-81b5-323784e38e2b)

   ![image](https://github.com/user-attachments/assets/5d9528e1-ef41-4756-854a-246049e65262)


3. New intruders section:
   After you determine which devices are intruders and which aren't, the application undertakes the task of detecting any new devices that may attempt to infiltrate your wifi. These devices, upon detection, appear in the "New intruders" section for you to decide on their fate. If you check any device of them, it'll be grouped with intruders. If you don't, it'll be considered an innocent device.

### Login.html:
![image](https://github.com/user-attachments/assets/47662354-47a6-4fda-88aa-ed0393d23cc5)
After you finish all of your device interrogations and would like to open the app another time, you won't need to register again. The app will remember you and greet you with the Login.html page. Enter the password and you'll start just where you left off! 


### changePassword.html:

![image](https://github.com/user-attachments/assets/c1dc1c76-c5b3-4e2b-b07e-8523fb322705)
If you would like to change the app password for any reason, you can do it right away by clicking "change password" from the navbar. Just ensure you remember the old password, though!

### changeRouter.html:
If you have changed your router's password (or entered a wrong one), you can change the router's username and/or password by clicking "Change password" from the navbar. But this privilege requires your password, as well.
![image](https://github.com/user-attachments/assets/9a2e8b52-51ee-421c-80e3-969bfbf93b04)


### clearDevices.html:
If, for any reason, you want to reset all the device setting and start over or feel like you've broken something, you can clear all the stored devices in the database and go and let the app detect all connected devices once again and start over. Very simple.
![image](https://github.com/user-attachments/assets/a60c88da-b31d-418c-bd51-d7b463c37b87)

### Layout.html:
Oh, this is just the base html template that is expanded to create all of the aforementioned html pages. Neat trick, isn't it?

## In the "Static" folder:
   ### "js" folder:
   
   It contains two files:
   
   ### 1. getDevices.js:
   This javascript file contains the code by which getDevices.html functions. It allows it to show connected devices, intruders and submit these devices to the server correctly. It also gives the application the ability to contact the server to check for new intruders, display them in the "New intruders" section in getDevices.html, and even make the page icon flicker so as to warn the user against new intruders!!
      
   ### 2. jquery-3.7.1.js:
   This javascript file basically includes the code for jQuery, a code that helps a lot in dealing with document objects.
   
   ### favicon.icon, alert1.icon, and alert2.icon:
   These are the deafult icon of the web application, and the two warning icons that flicker when a new intruder is detected, respectively.
   
## app.py:

This is the file where the majority of the action took place, and the largest file in the entire web application! It contains all of the code that's responsible for:
- Initializing the Flask application properly.
- Configuring sqlite for further operations.
- Setting up Selenium and configuring it for further operations.
- Getting your password when you register and store its hash in the database using sqlite.
- Changing your password (if you want) and committing the new one to the database.
- Storing the router credentials in the database.
- Changing the router credentials (if you want) and storing the new ones in the database.
- Going to the router's website, fetching the devices, taking your preferences regarding the devices (who has access and who's an intruder) and storing them in the databse, and passing your preferences again to getDevices.html to be shown.
- Logging you in when you want to open the application any time after registering or closing the application.
- Clearing the database from all identified devices (and the router's website from the time rule that prevents devices from accessing wifi), if you want.
- Managing all of the redirects inside each route such that you get directed to the correct following page, or not if you've entered something wrong.
- Ensuring the innocent devices, intruders and time rule are set every time correctly and don't have duplicates or missing values or crash the app!
- Scanning for new intruders and informing getDevices.html to warn you whenever one tries to access your wifi.
- Ensuring you restore your data successfully from the database and resume from where you last left the application without any change.
## routerData.db:
It's the database file that sqlite interacts with. It contains the following tables:
   ### mainPassword:
   It's only one column called "password" and one row (i.e.: one cell only. Remember you're the **only** one that can access the application).
   ### routerData:
   It contains a "name" cloumn and a "password" column for the router's name and password.
   ### verifiedDevices:
   It has a "name" column containing the innocent devices (devices that you let access the wifi).
   ### intruderDevices:
   It has a "name" column containing all the intruders (devices you marked as intruders and don't want to access the wifi network).

# How to use:
1. Ensure you have VS code with both Flask and Selenium installed.
2. clone the repository into a git repository in vs code.
3. Go into app.py, and (without selecting any text or using Ctrl + F to search for any text!), click run (Ctrl + Alt + N).
4. Ctrl + click on the server's url in the terminal.
5. Use the application :D
6. Commiting without selecting any devices stores the current devices with their categories in the database and lets the application scan for new intruders. **Don't close** the get LAN devices tab if you want the app to warn you whenever there's a new intruder!
7. If you want to close the application, simply close any open webpages, and go into the terminal where you ran app.py and press Ctrl + C to stop the server.

### Notes:
- If the app ever crashes or you can't find any devices in Get LAN devices (getDevices.html) just refersh the page, or go back and submit the last data you submitted again.
- If the previous option doesn't work (less probable) and you feel something has messed up blatantly, you can always reset the devices from Clear devices. You'll be able to restore your previous configuration in a moment (it's a simple app), no worries!
- If anything seems unclear, I hope the video demo can treat any confusion.
- If you wonder why the "static" folder is repeated outside of templates, that's because I noticed the server could find those files when I placed them their. I tried to change that but haven't been able to do so for some reason.
- This app is designed to run on a device connected to a "we" router. it may or may not work for other internet providers in Egypt.
