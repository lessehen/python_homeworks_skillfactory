import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import driver, login_url, valid_email, valid_password, my_pets_url


@pytest.fixture(scope="session", autouse=True)
def authorization():
    # Переходим на страницу авторизации
    driver.get(login_url)
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    yield

    driver.quit()


@pytest.fixture(scope="class")
def my_pets():
    # Открываем нужную страницу. Делаем прямой переход по урлу, а не ищем кнопку на странице, потому что цель тестов -
    # проверить страницу my_pets, а не наличие и корректность работы ссылки.
    driver.get(my_pets_url)


@pytest.fixture(scope="class")
def table_amount():
    # Считаем количество питомцев в таблице - для этого находим количество строк (tr) в теле таблицы (tbody).
    # По-хорошему нужно ещё посмотреть, умещаются ли все питомцы на страницу или потом делятся пагинацией,
    # но пока оставим так.
    t_amount = len(WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//tbody/tr'))))
    return t_amount


@pytest.fixture(scope="class")
def names():
    names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td:nth-child(2)')))
    return names
