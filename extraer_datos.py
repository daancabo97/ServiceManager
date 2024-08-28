from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time

def extraer_datos(driver, usuario):
   
        datos = []
        pagina_actual = 1

        # Cambiar al iframe
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe")))

        while True:
            try:
                WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x-grid3-row'))
                )
                print(f"Evidencias encontradas en la página {pagina_actual}")
            except TimeoutException as e:
                print(f"Error al encontrar incidencias en la tabla: {e}")
                break

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            filas = soup.select('div.x-grid3-row')

            for fila in filas:
                columnas = fila.select('td')
                if len(columnas) >= 6 and usuario.lower() in columnas[4].text.strip().lower():
                    datos.append({
                        'ID': columnas[0].text.strip(),
                        'Fecha/hora de apertura': columnas[1].text.strip(),
                        'Módulo': columnas[2].text.strip(),
                        'Estado': columnas[3].text.strip(),
                        'Asignado': columnas[4].text.strip(),
                        'Descripción': columnas[5].text.strip()
                    })

            try:
                siguiente_pagina = driver.find_element(By.CSS_SELECTOR, '.next-page-button')  # Ajusta el selector
                siguiente_pagina.click()
                time.sleep(5)
                pagina_actual += 1
            except NoSuchElementException:
                print("No hay más páginas.")
                break

        # Volver al contenido principal si es necesario
        driver.switch_to.default_content()

        return datos