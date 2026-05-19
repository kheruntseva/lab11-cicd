import os
import subprocess
import sys
import time
import urllib.request

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = os.environ.get("APP_URL", "http://127.0.0.1:8000")
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session", autouse=True)
def start_local_server():
    """Запускает локальный HTTP-сервер для статических файлов."""
    if os.environ.get("SKIP_SERVER") == "1":
        yield
        return

    process = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8000", "--directory", PROJECT_ROOT],
        cwd=PROJECT_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    for _ in range(30):
        try:
            urllib.request.urlopen(f"{BASE_URL}/index.html", timeout=1)
            break
        except Exception:
            time.sleep(0.2)
    else:
        process.terminate()
        pytest.fail("Не удалось запустить локальный сервер")

    yield
    process.terminate()


@pytest.fixture
def driver():
    options = Options()
    if os.environ.get("CI") == "true":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()


def open_page(driver):
    driver.get(f"{BASE_URL}/index.html")


def test_page_title_and_heading(driver):
    """Страница загружается, заголовок отображается корректно."""
    open_page(driver)
    assert "Форма обратной связи" in driver.title

    heading = driver.find_element(By.ID, "page-title")
    assert heading.text == "Форма обратной связи"


def test_form_fields_exist(driver):
    """Все обязательные поля формы присутствуют на странице."""
    open_page(driver)

    assert driver.find_element(By.ID, "name").is_displayed()
    assert driver.find_element(By.ID, "email").is_displayed()
    assert driver.find_element(By.ID, "message").is_displayed()
    assert driver.find_element(By.ID, "submit-btn").is_displayed()


def test_submit_button_text(driver):
    """Текст кнопки отправки соответствует ожидаемому."""
    open_page(driver)
    button = driver.find_element(By.ID, "submit-btn")
    assert button.text == "Отправить"


def test_successful_form_submission(driver):
    """При корректном заполнении формы показывается сообщение об успехе."""
    open_page(driver)

    driver.find_element(By.ID, "name").send_keys("Иван Тестов")
    driver.find_element(By.ID, "email").send_keys("ivan@test.ru")
    driver.find_element(By.ID, "message").send_keys("Тестовое сообщение")
    driver.find_element(By.ID, "submit-btn").click()

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "result-message"))
    )
    assert "успешно отправлено" in result.text
    assert "success" in result.get_attribute("class")


def test_empty_form_shows_error(driver):
    """Пустая форма не отправляется и показывает ошибку."""
    open_page(driver)
    driver.find_element(By.ID, "submit-btn").click()

    result = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "result-message"))
    )
    assert "Заполните все поля" in result.text
    assert "error" in result.get_attribute("class")