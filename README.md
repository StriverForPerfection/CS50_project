# This is SafeFi!
#### _My humble wifi protection web application_
### Video demo: (https://youtu.be/imhKwAO75ZQ)[https://youtu.be/imhKwAO75ZQ]
### Description: It's a web application built in Python using Flask and Selenium. It allows you to control the accessibility of your wifi to any device, and detects new intruders.

## Files:
## In the "templates" folder:

###Register.html:
![image](https://github.com/user-attachments/assets/39287582-6498-46c1-9e9d-d358560cedbd)

It's the first page you'll see on opening the application. Inside it, you'll enter the **sole** password for the application. There's only one password for the application because it's assumed that only one person (you, in this case) will have access to the router settings. This is meant to avoid allwing any other user to register and alter anything you've done. 
###getRouter.html:

![image](https://github.com/user-attachments/assets/04d8f7be-139f-435d-afef-94209e4346a2)
After entering a password, you'll now go on and enter the username and password for your router. Don't worry, these will only be stored on your device after you clone the repository.

###getDevices.html:
This is where all of the action takes place! 

![image](https://github.com/user-attachments/assets/a52ac333-16e1-4aa8-9aad-39e7f242f889)

Here, you have three sections:
1. A section for devices with access to wifi.
   _you can check any of them to go into the following intruders section_
2. Intruders section.
   Here reside devices that are marked by you as intruders.

   ![image](https://github.com/user-attachments/assets/6c4c2270-0baa-4957-81b5-323784e38e2b)

   ![image](https://github.com/user-attachments/assets/5d9528e1-ef41-4756-854a-246049e65262)


4. New intruders section:
   After you determine which devices are intruders and which aren't, the application undertakes the task of detecting any new devices that may attempt to infiltrate your wifi. These devices, upon detection, appear in the "New intruders" section for you to decide on their fate. If you check any device of them, it'll be grouped with intruders. If you don't, it'll be considered an innocent device.

###Login.html:
After you finish all of your device interrogations and would like toopen the app another time, you won't need to register again. The app will remember you and greet you with the Login.html page. Enter the password and you'll start just where you left off! 

![image](https://github.com/user-attachments/assets/47662354-47a6-4fda-88aa-ed0393d23cc5)

###changePassword.html:

If you would like to change the app password for any reason, you can do it right away by clicking "change password" from the navbar. Just ensure you remember the old password, though!
![image](https://github.com/user-attachments/assets/c1dc1c76-c5b3-4e2b-b07e-8523fb322705)

###changeRouter.html:
If you have changed your router's password (or entered a wrong one), you can change the router's username and/or password by clicking "Change password" from the navbar. But this privilege requires your password, as well.
![image](https://github.com/user-attachments/assets/9a2e8b52-51ee-421c-80e3-969bfbf93b04)


###clearDevices.html:
If, for any reason, you want to reset all the device setting and start over or feel like you've broken something, you can clear all the stored devices in the database and go and let the app detect all connected devices once again and start over. Very simple.
![image](https://github.com/user-attachments/assets/a60c88da-b31d-418c-bd51-d7b463c37b87)

###Layout.html:
Oh, this is just the base html template that is expanded to create all of the aforementioned html pages. Neat trick, isn't it?

##In the "Static" folder:
### "js" folder:

It contains two files:

### 1.getDevices.js:
This javascript file contains the code by which getDevices.html functions. It allows it to show connected devices, intruders and submit these devices to the server correctly. It also gives the application the ability to contact the server to check for new intruders, display in getDevices.html any new intruders, and even make the page icon flicker so as to warn the user against new intruders!!


