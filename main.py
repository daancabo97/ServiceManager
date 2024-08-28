from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from inicio_sesion import iniciar_sesion
from extraer_datos import extraer_datos
import pandas as pd
import time
import os

def main():

        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')

        chromedriver_path = os.path.join('chromedriver-win64', 'chromedriver.exe')
        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        url = 'https://bac033lnx052.bancoagrario.gov.co/smbac/index.do?2FC89408-C4F6-46CE-9CC1-44B31B9B6295_kes_cup_C6FA3ED5_6D17_47D1_B6E2_F4B02CC905E0_=&lang=es'
        driver.get(url)

        usuario = 'Sangutie'
        contrasena = 'Banco202708*'
        iniciar_sesion(driver, url, usuario, contrasena)

        datos_consolidados = extraer_datos(driver, 'sangutie')

        if datos_consolidados:
            df_consolidados = pd.DataFrame(datos_consolidados)
            with pd.ExcelWriter('reporte.xlsx', engine='openpyxl') as writer:
                df_consolidados.to_excel(writer, sheet_name='Consolidado', index=False)
                formatear_columnas(writer.sheets['Consolidado'])
            print("Casos extraídos y guardados en reporte.xlsx")
        else:
            print("No se ha extraído información")

        time.sleep(5)
        driver.quit()

def formatear_columnas(worksheet):

        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:    
                        pass
            adjust_width = (max_length + 2)
            worksheet.column_dimensions[column].width = adjust_width

if __name__ == "__main__":
    main()