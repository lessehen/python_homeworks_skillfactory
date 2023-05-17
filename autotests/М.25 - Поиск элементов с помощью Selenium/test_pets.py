from config import driver, all_pets_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Проверяем множество карточек питомцев на главной странице - внутри каждой из них есть имя питомца, возраст и вид
# (Готовый тест из модуля 25)
def test_cards_all():
    # Убедимся, что внутри каждой карточки есть имя питомца, возраст и вид, используя цикл.
    # Но этот тест в любом случае падает, потому что всегда есть питомцы, не соответствующие условиям.
    driver.get(all_pets_url)
    driver.implicitly_wait(10)  # в интернете пишут, что действует на время сессии
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    driver.implicitly_wait(10)  # но на всякий случай добавила к каждому элементу
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    driver.implicitly_wait(10)
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i].text  # в модуле в этой строке пропущен .text, без него не работает
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


class TestMyPets:
    # 1. Сверяем количество питомцев в сводке пользователя и на странице
    # Количество питомцев, отображаемых списком на странице пользователя, считается фикстурой
    def test_my_pets_amount(self, my_pets, table_amount):
        # Сохраняем текст элемента, содержащего сводку пользователя:
        user_summary = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.\.col-sm-4.left'))).text
        # Делим полученную строку на список по пробелам:
        split_summary = user_summary.split()
        # Сохраняем в переменную значение, следующее в списке за значением "Питомцев:":
        summary_amount = 10
        for i in range(1, len(split_summary)):
            if split_summary[i] == "Питомцев:":
                summary_amount = int(split_summary[i + 1])

        # Здесь сначала идёт условие с выводом информации, а уже потом assert, потому что мне так красивее :)
        if summary_amount == table_amount:
            print("\n✓ — 1. Присутствуют все питомцы\n")
        else:
            print("\n✖ — 1. Количество питомцев на странице и в сводке не совпадает")
            print(f"Питомцев в сводке: *** {summary_amount} ***")
            print(f"Питомцев на странице: *** {table_amount} ***\n")
        assert summary_amount == table_amount

    # 2. Проверяем количество питомцев с фото на странице
    def test_photos_amount(self, my_pets, table_amount):
        # Находим по селектору все элементы, обрамляющие фото питомцев:
        photos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'th > img')))
        # Заводим счётчик, чтобы посчитать питомцев с непустым фото:
        pets_photos = 0
        for i in range(table_amount):  # В подобные циклы подставляю table_amount, чтобы не вычислять каждый раз len(x)
            if photos[i].get_attribute('src') != '':
                pets_photos += 1
        # Проверяем, что фото есть более, чем у половины питомцев:
        if table_amount/2 <= pets_photos:
            print("\n✓ — 2. У половины или более питомцев есть фото\n")
        else:
            print("\n✖ — 2. Фото загружены менее, чем у половины питомцев")
            print(f"Всего питомцев: *** {table_amount} ***")
            print(f"Питомцев с фото: *** {pets_photos} ***\n")
        assert table_amount/2 <= pets_photos

    # 3. Проверяем, что у всех питомцев есть имя, возраст и порода
    def test_pets_descriptions(self, my_pets, table_amount, names):
        """
        # Здесь тест по образцу модуля. Names - в фикстурах, чтобы не делать два раза.
        species = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td:nth-child(3)')))
        ages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td:nth-child(4)')))

        for i in range(table_amount):
            assert names[i].text != ''
            assert species[i].text != ''
            assert ages[i].text != ''
        """

        # Изначально пример из модуля не совсем поняла, поэтому сделала по-своему. Так тоже работает + есть
        # "статистика" по колонкам таблицы. В общем, здесь мне опять красивее, но если важна скорость,
        # лучше остановиться на предыдущем варианте.
        species = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td:nth-child(3)')))
        ages = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, 'td:nth-child(4)')))
        
        pets_names, pets_species, pets_ages = 0, 0, 0
        for i in range(table_amount):
            if names[i].text != '':
                pets_names += 1
            if species[i].text != '':
                pets_species += 1
            if ages[i].text != '':
                pets_ages += 1
        
        # Проводим проверку:
        if (pets_names and pets_species and pets_ages) == table_amount:
            print("\n✓ — 3. У каждого питомца есть имя, порода и возраст\n")
        else:
            print("\n✖ — 3. Не у каждого питомца есть имя, порода и возраст")
            print(f"Всего питомцев: *** {table_amount} ***")
            print(f"С именем: *** {pets_names} ***")
            print(f"С породой: *** {pets_species} ***")
            print(f"С возрастом: *** {pets_ages} ***\n")
        assert (pets_names and pets_species and pets_ages) == table_amount

    # 4. Проверяем уникальность имён
    def test_pets_names(self, my_pets, table_amount, names):
        # Циклом сохраняем в список имена для каждого питомца:
        all_names = []
        for i in range(table_amount):
            all_names.append(names[i].text)
        # Собираем уникальные имена, преобразовав общий список имён в множество:
        uniq_names = set(all_names)

        if len(all_names) == len(uniq_names):
            print("\n✓ — 4. У всех питомцев разные имена\n")
        else:
            print("\n✖ — 4. Есть повторяющиеся имена питомцев")
            print(f"Всего имён: *** {len(all_names)} ***")
            print(f"Уникальных: *** {len(uniq_names)} ***")
            print(f"Имена: {all_names}")
            print(f"Уникальные имена: {uniq_names}\n")
        assert len(all_names) == len(uniq_names)

    # 5. Проверяем уникальность питомцев
    def test_pets_uniqueness(self, my_pets, table_amount):
        # Циклом сохраняем в список данные каждого питомца:
        all_pets = []
        for i in range(table_amount):
            pet = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f'tbody > tr:nth-child({i+1})'))).text  # "имя порода возраст"
            all_pets.append(pet)
        # Собираем уникальных питомцев, преобразовав общий список в множество:
        uniq_pets = set(all_pets)

        if table_amount == len(uniq_pets):
            print("\n✓ — 5. В списке нет повторяющихся питомцев\n")
        else:
            print("\n✖ — 5. В списке есть повторяющиеся питомцы")
            print(f"Всего питомцев: *** {table_amount} ***")
            print(f"Уникальных: *** {len(uniq_pets)} ***")
            print(f"Все питомцы: {all_pets}")
            print(f"Уникальные: {uniq_pets}\n")
        assert table_amount == len(uniq_pets)
