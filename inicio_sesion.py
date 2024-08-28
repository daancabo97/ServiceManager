from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time

def configurar_navegador():
    
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        chromedriver_path = os.path.join('chromedriver-win64', 'chromedriver.exe')
        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)
        return driver

def iniciar_sesion(driver, url, usuario, contrasena):
    
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'user.id')))
        
        campo_usuario = driver.find_element(By.NAME, 'user.id')
        campo_contrasena = driver.find_element(By.ID, 'LoginPassword')
        
        campo_usuario.send_keys(usuario)
        campo_contrasena.send_keys(contrasena)
        campo_contrasena.send_keys(Keys.RETURN)
        

        time.sleep(5)