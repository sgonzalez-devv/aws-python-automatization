import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import csv

# Configurar WebDriver (Asegúrate de tener el ChromeDriver correcto)
driver = webdriver.Chrome()

# URL de inicio de sesión de AWS
aws_login_url = "https://YOUR_IAM_USER_ID.signin.aws.amazon.com/console"
lambda_console_url = "https://console.aws.amazon.com/lambda/home"

# Abrir la página de AWS
driver.get(aws_login_url)
time.sleep(3)  # Esperar a que la página cargue completamente

# Llenar el campo de IAM Username
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("YOUR_IAM_USERNAME")

# Llenar el campo de Password
password_field = driver.find_element(By.ID, "password")
password_field.send_keys("YOUR_PASSWORD")  # Evita almacenar credenciales en código real

# Hacer clic en el botón "Sign In"
sign_in_button = driver.find_element(By.ID, "signin_button")
sign_in_button.click()


print("🔵 Se ha enviado la información de inicio de sesión.")
print("🔵 Por favor, ingresa el código MFA en AWS y presiona Enter aquí para continuar...")

# 🚀 Pausar el programa hasta que el usuario presione Enter en la consola
input("🔵 Esperando confirmación después de ingresar MFA... Presiona Enter para continuar.")

print("✅ Continuando con el flujo después del MFA...")

# Esperar a que la página de AWS Lambda cargue después de MFA
time.sleep(5)

# 📌 Navegar a la consola de AWS Lambda
driver.get(lambda_console_url)
time.sleep(5) 

# Inicializar lista de datos
lambda_data = []

# 📌 Definir la ruta del archivo CSV
csv_directory = "C:/Users/samue/Desktop/AWS_QA"
csv_path = os.path.join(csv_directory, "lambda_functions.csv")

# 📌 Crear la carpeta si no existe
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
    print(f"📂 Carpeta creada: {csv_directory}")
    
try:
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Lambda Name", "Last Modified", "Description", "Runtime", "Layers", "API Endpoint", "Method"])

        while True:
            print("🔄 Revisando página de Lambdas...")

            # Esperar carga de la lista de Lambdas
            WebDriverWait(driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[id^='link-self']"))
            )

            # Obtener enlaces de Lambdas
            lambda_links = driver.find_elements(By.CSS_SELECTOR, "a[id^='link-self']")
            lambda_urls = [(link.text.strip(), link.get_attribute("href")) for link in lambda_links]

            # 🔄 **Recorrer cada Lambda de la página actual**
            for lambda_name, lambda_url in lambda_urls:
                driver.get(lambda_url)
                time.sleep(3)

                print(f"🔍 Procesando Lambda: {lambda_name}")

                # 🏷️ **Nombre de la Lambda**
                try:
                    lambda_name = driver.find_element(By.XPATH, "//span[contains(@class, 'awsui_heading-text_')]").text.strip()
                except:
                    lambda_name = "N/A"

                # 🕒 **Fecha de última modificación**
                try:
                    last_modified = driver.find_element(By.XPATH, "//div[contains(text(),'Last modified')]/following-sibling::div//button").text.strip()
                except:
                    last_modified = "N/A"

                # 📝 **Descripción**
                try:
                    description = driver.find_element(By.XPATH, "//div[contains(text(),'Description')]/following-sibling::div/span").text.strip()
                except:
                    description = "No description"

                # ⚙️ **Runtime**
                try:
                    runtime = driver.find_element(By.XPATH, "//div[contains(text(),'Runtime')]/following-sibling::div").text.strip()
                except:
                    runtime = "N/A"

                # 📂 **Layers**
                try:
                    layers = [
                        f"{row.find_elements(By.TAG_NAME, 'td')[1].text.strip()} (v{row.find_elements(By.TAG_NAME, 'td')[2].text.strip()})"
                        for row in driver.find_elements(By.XPATH, "//table[contains(@class,'awsui_table')]//tr")[1:]
                    ]
                    layers = ", ".join(layers) if layers else "No layers"
                except:
                    layers = "No layers"

                # 👉 Navegar a "Configuration"
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Configuration"))).click()
                    time.sleep(2)
                except:
                    print(f"⚠️ No se encontró la pestaña de Configuration en {lambda_name}")

                # 👉 Click en "Triggers"
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Triggers"))).click()
                    time.sleep(3)
                except:
                    print(f"⚠️ No se encontró la pestaña de Triggers en {lambda_name}")

                # 🔗 **API Endpoint**
                try:
                    api_endpoint = driver.find_element(By.XPATH, "//span[contains(text(),'API endpoint:')]/strong/a").text.strip()
                except:
                    api_endpoint = "No API Endpoint"

                # 🔄 **Abrir el dropdown "Details" si está cerrado**
                try:
                    details_button = driver.find_element(By.XPATH, "//span[contains(@class,'awsui_expand-button_')]")
                    if details_button.get_attribute("aria-expanded") == "false":
                        details_button.click()
                        time.sleep(2)  # Esperar que se despliegue
                except:
                    print(f"⚠️ No se encontró el botón 'Details' en {lambda_name}")

                # 🔄 **Extraer el Método (GET, POST, etc.)**
                try:
                    method = driver.find_element(By.XPATH, "//div[contains(text(),'Method:')]/following-sibling::strong/span").text.strip()
                except:
                    method = "No Method"

                # 📌 Guardar datos en la lista
                lambda_data.append([lambda_name, last_modified, description, runtime, layers, api_endpoint, method])
                writer.writerow([lambda_name, last_modified, description, runtime, layers, api_endpoint, method])
                file.flush()  # 🔥 Guarda los datos en tiempo real

                # 🔙 **Volver a la lista de Lambdas**
                driver.get(lambda_console_url)
                time.sleep(5)

            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-awsui-analytics*='next'] > button"))
                )

                if next_button.is_enabled():
                    print("➡️ Moving to the next page...")
                    driver.execute_script("arguments[0].click();", next_button)  # More reliable than .click()
                    time.sleep(5)  # Allow the page to load
                else:
                    print("✅ No more pages available.")
                    break  # Exit the loop if there's no next page

            except NoSuchElementException:
                print("✅ 'Next' button not found, exiting pagination.")
                break  # Exit loop if the button doesn’t exist
            except StaleElementReferenceException:
                print("⚠️ 'Next' button went stale, retrying...")
                time.sleep(2)
                continue  # Retry finding the button

except KeyboardInterrupt:
    print("\n🚨 **Proceso interrumpido por el usuario (Ctrl + C). Guardando datos antes de salir...**")

finally:
    print(f"✅ Información guardada en: {csv_path}")
    driver.quit()
    print("🛑 **Proceso terminado.**")