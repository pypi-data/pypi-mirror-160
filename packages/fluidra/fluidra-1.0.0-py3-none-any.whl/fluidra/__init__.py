import time
import numpy
import selenium
import cv2
import gspread
import csv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from fluidra.elements import *
#from fluidra.elements import lights
#from fluidra.elements import abbreviations

global driver
driver = webdriver.Chrome(r'C:\chromedriver.exe')

print('Input -> fluidra.help() for some directions on how to use this library')

def help():

    print('How to use: ')
    print('To access functions type -> fluidra.funcName()')
    print('\nAvailable Functions:')
    print('.use(element): Allows you to use all menu elements.  To look at the available elemenets available for use, visit elements.py page')
    print('.openOwnersCenter(username, password, environment): Log into desired environment with employee credentials')
    print('.openDevice(deviceName): Checks the status of your device, searches for that device in the owners center, and opens up WebTouch window for that device')
    print('.scheduleDevice(device): Choose device to schedule')
    print('.setScheduleStartTime(startTime): Set the start time for your schedule -> IN MILITARY TIME')
    print('.setScheduleEndTime(endTime): Set the end time for your schedule -> IN MILITARY TIME')
    print('.colorLightSetup(lightName, auxNumber): Choses the light name to put on the correct auxillary port')
    print('.turnOffAux(lightName, auxNumber): Turns off correct auxillary port for different lights')
    print('.onOffDevices(device): Turn on and off available devices in the Other Devices menu. Just type in the device name as it is displayed in the menu' )
    print('.lightTest(lightName, auxNumber): Starts testing desired light on specific aux port.  Goes through all light sequences for desired light')
    print('\nHope this helps! Feel free to improve')

def openOwnersCenter(username, password, environment):

    if environment == 'Staging' or environment == 'staging':
        driver.get('https://site.zodiac-staging.com/?lang=en')
    elif environment == 'Development' or environment == 'development':
        driver.get('https://site.zodiac-dev.com/?lang=en')
    elif environment == 'Test' or environment == 'test':
        driver.get('https://site.zodiac-test.com/?lang=en')
    elif environment == 'Production' or environment == 'production':
        driver.get('https://site.iaqualink.net/index.html#/owners-center')
    else:
        print('Invalid Environment')

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userID')))
        idBox = driver.find_element(By.ID, 'userID') #Access the Username text box
        idBox.send_keys(username) #Enter my username into the text box
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userID')))
        idBox = driver.find_element(By.ID, 'userID') #Access the Username text box
        idBox.send_keys(username) #Enter my username into the text box
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userPassword')))
        pwdBox = driver.find_element(By.ID, 'userPassword')
        pwdBox.send_keys(password)
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'userPassword')))
        pwdBox = driver.find_element(By.ID, 'userPassword')
        pwdBox.send_keys(password)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'signinBottom')))
        loginButton = driver.find_element(By.CLASS_NAME, 'signinBottom')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.CLASS_NAME, 'signinBottom')))
        loginButton = driver.find_element(By.CLASS_NAME, 'signinBottom')


    time.sleep(3) #Have to wait for the sign in boxes to be filled before you can click login
    loginButton.click()

def openDevice(deviceName):

    WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div[4]/div[1]/div[1]/a/span/span')))
    compDeviceName = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div[4]/div[1]/div[1]/a/span/span')
    i = 4
    while compDeviceName.text != deviceName:
        i += 1
        compDeviceName = compDeviceName = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) + ']/div[1]/div[1]/a/span/span')


    checkDeviceStatus(i)

    device = compDeviceName
    WebDriverWait(driver,25).until(EC.element_to_be_clickable((device)))
    device.click()


def checkDeviceStatus(i):

    WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[1]/div[2]/div')))
    checkDeviceStatusButton = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[1]/div[2]/div')
    checkDeviceStatusButton.click()

    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]')))
        deviceStatus = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]').text
        print(deviceStatus)
    except:
        print('Could not find device status')

    while deviceStatus == 'Offline':
        checkDeviceStatusButton.click()
        time.sleep(1)
        checkDeviceStatusButton.click()
        time.sleep(1)
        try:
            deviceStatus = driver.find_element(By.XPATH, '//*[@id="homeTab"]/div['+ str(i) +']/div[2]/div[2]/div[1]/div[2]/div/p[1]/span[2]').text
            print(deviceStatus)
        except NoSuchElementException:
            print('Cannot find Status')


def switchWindow(window):

    nextWindow = driver.window_handles
    driver.switch_to.window(nextWindow[window])

def scheduleDevice(device):

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_26_0_1"]/table/tbody/tr/td')))
        compDevice = driver.find_element(By.XPATH, '//*[@id="56_26_0_1"]/table/tbody/tr/td')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_26_0_1"]/table/tbody/tr/td')))
        compDevice = driver.find_element(By.XPATH, '//*[@id="56_26_0_1"]/table/tbody/tr/td')

    i = 0

    while device != compDevice.text:
        if i < 8:
            i += 1
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_26_0_'+ str(i) +'"]/table/tbody/tr/td')))
            compDevice = driver.find_element(By.XPATH, '//*[@id="56_26_0_'+ str(i) +'"]/table/tbody/tr/td')
        else:
            i = 0
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_24_1"]')))
            pageDown = driver.find_element(By.XPATH, '//*[@id="56_24_1"]')
            pageDown.click()

    WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_26_0_'+ str(i) +'"]/table/tbody/tr/td')))
    compDevice.click()
    time.sleep(0.2)
    WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="56_24_2"]')))
    selectDevice = driver.find_element(By.XPATH, '//*[@id="56_24_2"]')
    selectDevice.click()


def setScheduleStartTime(startTime):

    AMPM = ''
    startTime = startTime.replace(':','', len(startTime))

    use("Start Time Schedule")

    if(int(startTime) > 1259):
        adjustedTime = int(startTime) % 1200
        numList = [int(a) for a in str(adjustedTime)]
        AMPM = 'PM'
    else:
        numList = [int(a) for a in startTime]
        AMPM = 'AM'

    i = 0
    while i < len(numList):
        use(str(numList[i]))
        i += 1

    if AMPM == 'AM':
        use('AM/PM')

    use('timeEnter')




def setScheduleEndTime(endTime):

    AMPM = ''
    endTime = endTime.replace(':','', len(endTime))

    use("Stop Time Schedule")

    if(int(endTime) > 1259):
        adjustedTime = int(endTime) % 1200
        numList = [int(a) for a in str(adjustedTime)]
        AMPM = 'PM'
    else:
        numList = [int(a) for a in startTime]
        AMPM = 'AM'

    i = 0
    while i < len(numList):
        use(str(numList[i]))
        i += 1

    if AMPM == 'AM':
        use('AM/PM')

    use('timeEnter')


def use(element):

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, elem[element])))
        newElem = driver.find_element(By.XPATH, elem[element])
        time.sleep(0.5)
        newElem.click()
    except TimeoutException:
        time.sleep(5)
        use(element)

def colorLightSetup(lightName, auxNum):

    time.sleep(0.5)

    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, '61_24_0')))
        light = driver.find_element(By.ID, '61_24_0')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, '61_24_0')))
        light = driver.find_element(By.ID, '61_24_0')

    i = 1
    while light.text != lights[lightName]:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i))))
            light = driver.find_element(By.ID, '61_24_'+str(i))
            i += 1
        except TimeoutException:
            time.sleep(5)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i))))
            light = driver.find_element(By.ID, '61_24_'+str(i))
            i += 1

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((light)))
        light.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((light)))
        light.click()

    time.sleep(0.5)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '62_26_0_1')))
        auxNumber = driver.find_element(By.ID, '62_26_0_1')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '62_26_0_1')))
        auxNumber = driver.find_element(By.ID, '62_26_0_1')

    i = 2
    while auxNumber.text != 'Aux'+ str(auxNum):
        time.sleep(0.5)
        if i < 7:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i))))
                auxNumber = driver.find_element(By.ID, '62_26_0_'+str(i))
                i+=1
            except TimeoutException:
                time.sleep(5)
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '62_26_0_'+str(i))))
                auxNumber = driver.find_element(By.ID, '62_26_0_'+str(i))
                i+=1
        else:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '61_24_1')))
                downPage = driver.find_element(By.ID, '62_24_1')
                downPage.click()
                i = 1
            except TimeoutException:
                time.sleep(5)
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '61_24_1')))
                downPage = driver.find_element(By.ID, '62_24_1')
                downPage.click()
                i = 1

    time.sleep(2)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
        auxNumber.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
        auxNumber.click()

    time.sleep(3)

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2')))
        saveLightConfig = driver.find_element(By.ID, '62_24_2')
        saveLightConfig.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2')))
        saveLightConfig = driver.find_element(By.ID, '62_24_2')
        saveLightConfig.click()

    print(lightName + ' to Aux' + str(auxNum))




def turnOffAuxLight(lightName, auxNum):

    time.sleep(0.5)

    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_0')))
        light = driver.find_element(By.ID, '61_24_0')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_0')))
        light = driver.find_element(By.ID, '61_24_0')

    time.sleep(0.5)

    i = 1
    while light.text != lights[lightName]:
        try:
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i))))
            light = driver.find_element(By.ID, '61_24_'+str(i))
            i += 1
        except TimeoutException:
            time.sleep(5)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, '61_24_'+str(i))))
            light = driver.find_element(By.ID, '61_24_'+str(i))
            i += 1

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((light)))
        light.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((light)))
        light.click()

    time.sleep(0.5)

    auxNumber = driver.find_element(By.ID, '62_26_0_1')

    i = 2
    while auxNumber.text != 'Aux' + str(auxNum) + ' ' + abbreviations[lightName]:
        if i < 7:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
                auxNumber = driver.find_element(By.ID, '62_26_0_'+str(i))
                i+=1
            except TimeoutException:
                time.sleep(5)
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
                auxNumber = driver.find_element(By.ID, '62_26_0_'+str(i))
                i+=1
        else:
            try:
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_1')))
                downPage = driver.find_element(By.ID, '62_24_1')
                downPage.click()
                i = 1
            except TimeoutException:
                time.sleep(5)
                WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_1')))
                downPage = driver.find_element(By.ID, '62_24_1')
                downPage.click()
                i = 1


    print(auxNumber.text + ' Found')
    time.sleep(2)

    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
        auxNumber.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((auxNumber)))
        auxNumber.click()

    time.sleep(3)
    try:
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2')))
        saveLightConfig = driver.find_element(By.ID, '62_24_2')
        saveLightConfig.click()
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.ID, '62_24_2')))
        saveLightConfig = driver.find_element(By.ID, '62_24_2')
        saveLightConfig.click()

    print(lightName + ' off Aux' + str(auxNum))


def onOffDevices(device):

    time.sleep(0.5)

    try:
        WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="54_24_0"]/table/tbody/tr/td[1]')))
        deviceName = driver.find_element(By.XPATH, '//*[@id="54_24_0"]/table/tbody/tr/td[1]')
    except TimeoutException:
        time.sleep(5)
        WebDriverWait(driver,25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="54_24_0"]/table/tbody/tr/td[1]')))
        deviceName = driver.find_element(By.XPATH, '//*[@id="54_24_0"]/table/tbody/tr/td[1]')

    time.sleep(0.5)

    i = 0
    while deviceName.text != device:
        i +=1
        try:
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="54_24_' + str(i) +'"]/table/tbody/tr/td[1]')))
            deviceName = driver.find_element(By.XPATH, '//*[@id="54_24_' + str(i) +'"]/table/tbody/tr/td[1]')
        except TimeoutException:
            time.sleep(5)
            WebDriverWait(driver,25).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="54_24_' + str(i) +'"]/table/tbody/tr/td[1]')))
            deviceName = driver.find_element(By.XPATH, '//*[@id="54_24_' + str(i) +'"]/table/tbody/tr/td[1]')


    deviceName.click()


def lightTest(lightName, auxNumber):

    video = cv2.VideoCapture(2)
    print('@video Capture')
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    Results = []

    for i in range(0,len(colors[lightName])):
        #for j in range(0, len(times[colors[lightName][i]])):
            #print(sequences[colors[lightName][i]][j])
        print(colors[lightName][i])
        print(times[colors[lightName][i]])
        onOffDevices('Aux' + str(auxNumber))
        use(colors[lightName][i])

        Sequence = []
        j = 0

        while j < len(times[colors[lightName][i]]):
            time.sleep(times[colors[lightName][i]][j])
            _i = 0
            Colors = []
            while _i < 5:
                _, img = video.read()
                image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                height, width, _ = img.shape

                cx = int(width / 2)
                cy = int(height / 2)

                center = image[cy, cx]
                hue = center[0]
                sat = center[1]
                val = center[2]

                color = "Undefined"

                time.sleep(0.1)


                if hue > 0 and hue <= 32:
                    color = "Orange"
                elif hue > 32 and hue < 90:
                    color = "Green"
                elif hue >= 90 and hue <= 132:
                    if sat <= 100:
                        color = "Light Green"
                    else:
                        color = "Blue"
                elif hue > 132 and hue <= 165:
                    color = "Red"
                elif hue > 165 and hue <= 180 :
                    color = "Violet"


                #print(color)
                Colors.append(color)
                print(center)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), 3)

                cv2.imshow("Frame", img)
                cv2.waitKey(1)
                _i += 1

            print('')
            print(max(set(Colors), key = Colors.count))
            print('')
            j += 1
            Sequence.append(max(set(Colors), key = Colors.count))

        onOffDevices('Aux' + str(auxNumber))
        time.sleep(6)

        if colors[lightName][i] == 'American':
            if Sequence == ['Violet', 'Red', 'Blue', 'Violet']:
                Sequence = ['Orange', 'Red', 'Blue', 'Orange']
        if colors[lightName][i] == 'Cal Sunset':
            if Sequence == ['Violet', 'Orange', 'Red', 'Red', 'Violet']:
                Sequence = ['Orange', 'Orange', 'Red', 'Red', 'Orange']
        if colors[lightName][i] == 'Twilight':
            if Sequence ==['Orange', 'Green', 'Blue', 'Blue', 'Red', 'Red', 'Violet']:
                Sequence = ['Violet', 'Green', 'Blue', 'Blue', 'Red', 'Red', 'Violet']
        if colors[lightName][i] == 'USA Jandy':
            if Sequence == ['Orange', 'Red', 'Blue']:
                Sequence = ['Undefined', 'Red', 'Blue']
        if colors[lightName][i] == 'White':
            if Sequence == ['Green']:
                Sequence = ['Undefined']
        if colors[lightName][i] == 'Fast':
            if Sequence == ['Blue', 'Blue', 'Light Green', 'Green', 'Undefined', 'Light Green', 'Red', 'Red', 'Blue']:
                Sequence = ['Blue', 'Blue', 'Light Green', 'Green', 'Orange', 'Light Green', 'Red', 'Red', 'Blue']

        #print(Sequence)
        if Sequence == sequences[colors[lightName][i]]:
            result = 'P'
            Results.append(result)
            print('Camera Sees ' + colors[lightName][i])
        else:
            result = 'B'
            Results.append(result)
            print('Did not see ' + colors[lightName][i])

    writeToCSV(auxNumber, lightName, Results)



def writeToCSV(auxNumber, lightName, results):
    sa = gspread.service_account(filename=r"C:\Users\anthony.kahley\Documents\fluidra\lightautomation-89ef15bf87ea.json")
    sh = sa.open("PDA GIGA Validation test")
    wks = sh.worksheet("Function Test - Pool Light")

    with open('lightDataForSheet.csv', 'w') as new_file:

        writer = csv.writer(new_file)

        writer.writerow(results)

    with open('lightDataForSheet.csv', 'r') as file:

        content = file.read()

        column = ''
        rowLow = 0
        rowHigh = 0

        if lightName == 'pentair':
            rowLow = 26
            rowHigh = 38
        elif lightName == 'jandy':
            rowLow = 10
            rowHigh = 24
        elif lightName == 'hayward':
            rowLow = 40
            rowHigh = 55
        else:
            print('Do not recognize light name')

        if auxNumber == 2:
            column = 'C'
        elif auxNumber == 4:
            column = 'D'
        elif auxNumber == 7:
            column = 'E'
        else:
            print('Invalid Aux Number')

        j = 0

        print(column + str(rowLow) + ' to ' + column + str(rowHigh))

        while rowLow < rowHigh:
            print(str(j))
            wks.update((column+str(rowLow)), content[j])
            rowLow += 1
            j += 2
