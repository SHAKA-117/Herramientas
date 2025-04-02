from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from pathlib import Path
import time, re, getpass

class Error(Exception):
    def __init__(self,mensaje) -> None:
        self.mensaje = mensaje

    def __str__(self) -> str:
        return f"{self.mensaje}"

def toggle_activo(driver):
    try:
        trigrama = driver.find_elements(By.XPATH, "/html/body/div[2]/app-root/div/app-subnav/nav/div/div[1]/button/mat-icon")
              
        if trigrama:
            trigrama[0].click()
            time.sleep(5)

            driver.find_element(By.XPATH, "/html/body/div[2]/app-root/div/app-subnav/nav/div/div[2]/ul/li[2]/a").click()  
            time.sleep(5)

            return True
    except WebDriverException as WE:
        pass

    return False

def fecha_inicio(wait,fecha_desde,months):
    toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-datepicker-toggle button")))
    toggle.click()
    time.sleep(1) 
    
    # Extraer el día, mes y año
    dia, mes, anio = re.split(r"[/-]", fecha_desde)

    # Seleccion el año     
    seleccion_anio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-calendar-period-button")))
    seleccion_anio.click()
    time.sleep(1)

    elemento_anio = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{anio}')]")))
    elemento_anio.click()
    time.sleep(1)

    # Seleccion de mes
    elemento_mes = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{months[mes]}')]")))
    elemento_mes.click()
    time.sleep(1)

    # Seleccion del día
    elemento_dia = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[not(contains(@class, 'mat-calendar-body-disabled'))]//div[contains(text(), '{dia}')]")))
    elemento_dia.click()
    time.sleep(2)
    return

def fecha_fin(wait, fecha_hasta, months):
    dia, mes, anio = re.split(r"[/-]", fecha_hasta)

    seleccion_anio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mat-calendar-period-button")))
    seleccion_anio.click()
    time.sleep(1)

    elemento_anio = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{anio}')]")))
    elemento_anio.click()
    time.sleep(1)

    elemento_mes = wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{months[mes]}')]")))
    elemento_mes.click()
    time.sleep(1)

    elemento_dia = wait.until(EC.element_to_be_clickable((By.XPATH, f"//td[not(contains(@class, 'mat-calendar-body-disabled'))]//div[contains(text(), '{dia}')]")))
    elemento_dia.click()
    time.sleep(2)
    return

def descargar_zip(driver):
    driver.execute_script("window.scrollBy(0, 350)")
    try:
        boton_descarga = driver.find_elements(By.XPATH, "/html/body/div[2]/app-root/div/app-descarga-ejemplares/div/div[5]/div[1]/div[2]/div/img[1]")
        if boton_descarga:
            boton_descarga[0].click()
            time.sleep(15) #aumentar tiempo si tarda la descaga
            return True
    except TimeoutException as e:
        pass
    return False

def mensaje(driver):
    try:
        mensaje = driver.find_elements(By.XPATH, "//strong[contains(text(), 'No se encontraron resultados')]")
        if mensaje:
            raise Error("No se encontraron resultados")
    except Error as e:
        print(e)
    return 

def manipulacion_formulario(driver, wait,fecha_desde, fecha_hasta, gaceta):
    try: 
        driver.find_element(By.NAME, "areas").click()
        opciones = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "mat-option")))
        opciones[2].click()
        time.sleep(5)

        # Diccionario de meses en español (ajustar si es necesario)
        months = {
            "01": "ENE", "02": "FEB", "03": "MAR", "04": "ABR",
            "05": "MAY", "06": "JUN", "07": "JUL", "08": "AGO",
            "09": "SEP", "10": "OCT", "11": "NOV", "12": "DIC"
        }

        fecha_inicio(wait, fecha_desde, months)
        fecha_fin(wait, fecha_hasta, months)

        #input Gacetas
        gacetas = driver.find_element(By.NAME, "gacetas")#(By.ID, "mat-input-0")
        driver.execute_script("arguments[0].removeAttribute('readonly');", gacetas)
        driver.execute_script("arguments[0].removeAttribute('disabled');", gacetas)
        gacetas.send_keys(gaceta)

        option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "mat-option")))
        option.click()
        time.sleep(5) 

        #Boton buscar
        driver.find_element(By.XPATH,"/html/body/div[2]/app-root/div/app-descarga-ejemplares/div/div[4]/div[2]/button").click()
        wait.until(EC.invisibility_of_element_located((By.XPATH,"//img[contains(@src, 'loading-impi.gif')]")))
        time.sleep(5)
        
        #Seleccion de elementos por pagina
        driver.find_element(By.ID, "mat-select-10").click()
        opcion_elemento = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "mat-option")))
        opcion_elemento[2].click()
        time.sleep(5)

        #iniciar descarga 
        respuesta = descargar_zip(driver)
        if respuesta == False:
            mensaje(driver)
        
        time.sleep(60)
        driver.quit()

    except WebDriverException as WE:
        pass
    return

def buscar_perfil(directorio,extencion):
    return [archivo.name for archivo in Path(directorio).rglob(f"*{extencion}")]

def get_from_cdn(url_base, fecha_desde, fecha_hasta, gaceta):
    service = Service("./geckodriver")
    usuario = getpass.getuser()
    opciones = Options()
    opciones.add_argument("-profile")
    perfil = buscar_perfil(f"/home/{usuario}/.mozilla/firefox/",".pruebas")[0]
    opciones.add_argument(f"/home/{usuario}/.mozilla/firefox/{perfil}")
    driver = webdriver.Firefox(service=service, options=opciones)
    driver.get(url_base)
    wait = WebDriverWait(driver, 20)
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(5)
    
    if toggle_activo(driver) == True:
        manipulacion_formulario(driver,wait,fecha_desde, fecha_hasta, gaceta)
    elif toggle_activo(driver) == False:
        driver.find_element(By.XPATH, "/html/body/div[2]/app-root/div/app-subnav/nav/div/div[2]/ul/li[2]/a").click()  
        time.sleep(5)
        manipulacion_formulario(driver,wait,fecha_desde, fecha_hasta, gaceta)
    return

if __name__ == "__main__":
    fecha_desde = "3-06-2024"
    fecha_hasta = "7-06-2024"
    gaceta = "Solicitudes de Marcas, Avisos y Nombres Comerciales presentadas ante el Instituto" 
    #gaceta = "Notificación de Resoluciones, Requerimientos y demás Actos" 
    get_from_cdn("https://siga.impi.gob.mx/", fecha_desde, fecha_hasta, gaceta)


#Controlador para firefox
#https://github.com/mozilla/geckodriver/releases


