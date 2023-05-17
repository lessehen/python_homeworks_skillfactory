from api import PetFriends
from settings import valid_email, valid_password, invalid_password
import os

pf = PetFriends()


# ↓ 1. Готовый GET api key valid

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result:
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 200
    assert 'key' in result


# ↓ 2. Свой GET api key invalid

def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api-ключа с некорректным паролем возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result:
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями:
    assert status == 403


# ↓ 3. Готовый GET all pets valid

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает непустой список.
    Для этого сначала получаем api-ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список непустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


# ↓ 4. Готовый POST new pet valid

def test_add_new_pet_with_valid_data(name='Арчизавр', animal_type='пёс', age='12', pet_photo='images/dog.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


# ↓ 5. Свой GET my pets valid

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем, что запрос my_pets возвращает непустой список.
    Для этого сначала получаем api-ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список своих питомцев и проверяем, что список непустой. Если список пустой - создаём питомца и повторяем
    проверку."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем статус-код и список питомцев и создаём нового питомца при необходимости:
    if len(result['pets']) > 0:
        assert status == 200
        assert len(result['pets']) > 0
    else:
        pf.add_new_pet(auth_key, 'Пиксель', 'комар', '12', 'images/mosquito.jpeg')
        status, result = pf.get_list_of_pets(auth_key, filter)  # Повторяем запрос списка после добавления питомца
        assert status == 200
        assert len(result['pets']) > 0


# ↓ 6. Свой POST new pet invalid

def test_add_new_pet_with_invalid_data(name='Арбуз', animal_type='кот', age='3', pet_photo='images/cat.rar'):
    # Сейчас падает, потому что питомец создаётся, несмотря на некорректные данные
    """Проверяем, что нельзя добавить питомца с некорректными данными (здесь - с архивом вместо фото)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400


# ↓ 7. Готовый DELETE valid

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев:
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/hedgehod.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление:
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев:
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца:
    assert status == 200
    assert pet_id not in my_pets.values()


# ↓ 8. Свой DELETE invalid - нужны пояснения ментора (вопрос под тестом)

def test_unsuccessful_delete_pet():
    """Проверяем невозможность удаления питомца при невалидном ключе авторизации"""

    # Задаём невалидный auth_key для отправки DELETE-запроса (просто постучала по клавиатуре):
    auth_key = {'key': 'blieg98783t088863080'}

    # Задаём подставной валидный ключ, чтобы получить список питомцев, что невозможно с невалидным ключом:
    _, auth_key_false = pf.get_api_key(valid_email, valid_password)

    # Получаем список всех питомцев:
    _, all_pets = pf.get_list_of_pets(auth_key_false, '')

    # Берём id первого питомца из списка и отправляем запрос на удаление с невалидным auth_key:
    pet_id = all_pets['pets'][-1]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Запрашиваем список питомцев для проверки:
    _, all_pets = pf.get_list_of_pets(auth_key_false, "")

    # Проверяем, что статус ответа равен 403:
    assert status == 403

    # Проверяем, что в списке питомцев есть id питомца, которого мы пытались удалить:
    # assert pet_id in all_pets.values() - так нужно делать, если идти по образцу готового теста
    assert pet_id == all_pets['pets'][-1]['id']

    '''Вопрос по этому тесту.
    За основу я брала готовый на успешное удаление и работала с ним. Но проверку на то, что питомец не удалился,
    пришлось написать иначе - не через поиск id во всем теле ответа, а через сверку с последним id в списке. Потому 
    что assert pet_id in all_pets.values() не видел, что внутри есть нужное значение, а будто сравнивал id со всем телом
    ответа. Поэтому в итоге я сделала проверку с обращением по индексу к последнему питомцу в общем списке, но есть 
    риск, что в момент прогона теста именно этого питомца успеет удалить кто-то другой. Поэтому по-хорошему нужно 
    обращение ко всему списку, но кажется, что там какая-то загвоздка в json, и значения в нём нужно проверять как-то
    иначе. Но тогда тест из готового репозитория неправильный :) 
    В общем, если всё это сократить, вопрос в том, почему не проходит проверка из строки 144? Я ошиблась в логике /
    синтаксисе ещё чём-то или она изначально не совсем правильная?
    '''


# ↓ 9. Готовый PUT - update pet valid

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст последнего созданного питомца:
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному:
        assert status == 200
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев:
        raise Exception("There is no My_pets")
    '''По этому тесту тоже вопрос. Зачем нам выкидывать исключение, если всё-таки можно создать питомца в рамках этого
    теста, и обновить его? Я понимаю, что может быть баг и при создании питомца, но в готовом тесте на удаление
    питомец создавался внутри теста, если список был пустым. Какой подход будет правильнее: вызывать исключение или
    пробовать создать питомца и работать с ним?'''


# ↓ 10. Свой PUT invalid animal_type

def test_unsuccessful_update_self_pet(name='Джоуль', animal_type=35, age=7):
    # Падает, потому что сервер принимает число там, где по документации должен принимать строку, и возвращает код 200
    """Проверяем, что запрос с числом вместо строки в animal_type вернёт код 400"""

    # Получаем ключ auth_key и список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст последнего созданного питомца:
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 400 и имя питомца соответствует заданному:
        assert status == 400
        assert result['name'] == name
    else:
        # Если список питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев:
        raise Exception("There is no My_pets")


# ↓ 11. Свой PUT invalid ID

def test_unsuccessful_update_false_pet(name='Барсик', animal_type='котёнок', age=0):
    """Проверяем, что запрос с некорректным pet_id вернёт код 400"""

    # Получаем ключ auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Отправляем запрос, где в id передаём случайную строку, и сохраняем ответ:
    status, _ = pf.update_pet_info(auth_key, 'barmoglotbrandoshmygov', name, animal_type, age)

    # Проверяем, что статус ответа = 400 и имя питомца соответствует заданному:
    assert status == 400
