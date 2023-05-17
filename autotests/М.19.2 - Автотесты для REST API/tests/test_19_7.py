from api import PetFriends
from settings import valid_email, valid_password, long_name
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

pf = PetFriends()

# По заданию вроде бы нужны негативные тесты, но вначале сделаем Happy Path для каждого запроса - заодно убедимся,
# что сами методы описаны верно


# ↓ 0.1. POST /api/create_pet_simple - создаём питомца без фото с полностью валидными данными

def test_post_new_pet_simple_valid(name='Колян', animal_type='ёж', age='2'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name


# ↓ 0.2. POST /api/pets/set_photo/{pet_id} - загружаем фото питомца по его id с полностью валидными данными

def test_post_photo_by_pet_id(pet_photo='images/dog.jpg'):
    """Проверяем, что существующему питомцу можно загрузить фото: сервер возвращает код 200,"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев, чтобы получить id последнего (или создать питомца, если список пуст):
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев:
    if len(my_pets['pets']) == 0:
        pf.add_pet_simple(auth_key, 'Вальдемар', 'пёс', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем в переменную id первого питомца и добавляем фото для него:
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_by_pet_id(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200  # Запрос выполнен успешно
    assert 'pet_photo' in result.keys()  # В ответе есть ключ pet_photo - наверное, можно и без этой проверки
    assert result['pet_photo'] is not ''  # Значение pet_photo - не пустое. Можно ещё вместо is not использовать !=,
    # вроде оба варианта делают то, что нужно, и тест проходит. Или оба ошибочны, но я хотя бы попыталась :)


# Оба теста проходят, методы рабочие - переходим к негативным тестам


# ↓ 1. POST /api/create_pet_simple - неверный ключ авторизации (строка латиница + цифры) - ожидаем код 403

def test_post_new_pet_simple_invalid_key(name='Алексей', animal_type='страус', age='4'):
    """Проверяем, что нельзя добавить питомца при передаче некорректного auth_key"""

    # Задаём некорректный auth_key:
    auth_key = {'key': 'iMHJ59FAPyLBN1sRaY7f3fLIePaf5TmEgeb'}

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 403


# ↓ 2. POST /api/create_pet_simple - string в возрасте вместо int - ожидаем код 400

def test_post_new_pet_simple_invalid_age(name='Алексей', animal_type='страус', age='конь'):
    """Проверяем, что нельзя добавить питомца с текстовыми данными вместо возраста"""
    # На самом деле, конечно, мы изначально задавали для возраста тип srting, но что поделать, если API такое :)
    # Будем всё-таки считать, что возраст "конь" не должен проходить.

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400


# ↓ 3. POST /api/create_pet_simple - передаём пустые строки - ожидаем код 400

def test_post_new_pet_simple_invalid_name(name='', animal_type='', age=''):
    """Проверяем, что нельзя добавить питомца, не заполнив поля"""
    # На самом деле опять можно

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400


# ↓ 4. POST /api/create_pet_simple - имя длиной 1000 символов - ожидаем код 400 или код 200 (а вдруг)

def test_post_new_pet_simple_long_name(name=long_name, animal_type='ёж', age='2'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200 or status == 400
    if status == 200:
        assert result['name'] == name
    # Сейчас получаем код 200, и я не увидела ограничений на длину, хотя кажется, что они всё-таки должны быть, поэтому
    # вроде как и проверка на 400 не будет лишней. Но в реальной работе, вероятно, будет проверяться только один


# ↓ 5. POST /api/create_pet_simple - передаём вместе с нужными данными фото - ожидаем код 400 или 500 (но лучше 400)
""" Показалось, что я придумала классный тест и вроде как правильно всё составила. Но он выполняется уже второй час.
Прерывать не хочу, удалять не хочу, задание отправлять пора. Поэтому пусть будет - может, прокомментируете, где именно 
я ошиблась. Сама понимаю, что отправляю в age строку на много тысяч символов, и всё может висеть из-за этого. Но также
очень вероятно, что просто напортачила в коде)
При оценке можно не учитывать этот тест.
"""

def test_post_new_pet_simple_with_photo(name='Алексей', animal_type='страус', age='images/ostrich.jpg'):
    """Проверяем, что через данный эндпоинт нельзя добавить питомца с фото
    Изображение добавляем в age, т. к. лишний ключ передать не получится"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    photo = os.path.join(os.path.dirname(__file__), age)

    age = MultipartEncoder(
            fields={
                'age': (photo, open(photo, 'rb'), 'image/jpeg')
            })

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400 or status == 500


# ↓ 6. POST /api/pets/set_photo/{pet_id} - неверный ключ авторизации (строка латиница + цифры) - ожидаем код 403

def test_post_photo_invalid_auth_key(pet_photo='images/ostrich.jpg'):
    """Проверяем, что существующему питомцу нельзя загрузить фото, используя некорректный auth_key"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Задаём невалидный auth_key:
    auth_key_invalid = {'key': 'DafnEoc5iV0btZ9QQRcpdK2SiDDMWpO1OH7xNfJVKWuZkN3r9r'}

    # Задаём подставной валидный ключ, чтобы получить список питомцев, что невозможно с невалидным ключом:
    _, auth_key_false = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев, используя подставной auth_key, чтобы получить id последнего:
    _, all_pets = pf.get_list_of_pets(auth_key_false, '')

    # Берём id первого питомца из списка и отправляем запрос на добавление фото с невалидным auth_key:
    pet_id = all_pets['pets'][-1]['id']
    status, result = pf.add_photo_by_pet_id(auth_key_invalid, pet_id, pet_photo)

    # Проверяем статус:
    assert status == 403


# ↓ 7. POST /api/pets/set_photo/{pet_id} - неверный pet_id (строка латиница + цифры) - ожидаем код 400

def test_post_photo_by_invalid_pet_id(pet_photo='images/ostrich.jpg'):
    """Проверяем, что при использовании несуществующего pet_id сервер возвращает код 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Задаём pet_id:
    pet_id = 'x6VkNYfawERMqBF'

    status, result = pf.add_photo_by_pet_id(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400
    # Тест упал, т. к. вернулся код 500. Вроде как по сваггеру всё-таки должен быть 400.


# ↓ 8. POST /api/pets/set_photo/{pet_id} - невалидное вложение (архив вместо изображения) - ожидаем код 400

def test_post_photo_rar(pet_photo='images/cat.rar'):
    """Проверяем, что существующему питомцу нельзя загрузить вместо фото другой файл - в данном случае архив"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев, чтобы получить id последнего (или создать питомца, если список пуст):
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев:
    if len(my_pets['pets']) == 0:
        pf.add_pet_simple(auth_key, 'Вальдемар', 'пёс', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем в переменную id первого питомца и добавляем фото для него:
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_by_pet_id(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400
    # Как и тест 7, возвращает 500, хотя кажется, что должен 400 - The error code means that provided data is incorrect


# ↓ 9. POST /api/pets/set_photo/{pet_id} - невалидное вложение (формат gif) - ожидаем код 400

def test_post_photo_gif(pet_photo='images/0cat.gif'):
    """Проверяем, что существующему питомцу нельзя загрузить фото недопустимого формата (допустимы JPG, JPEG и PNG)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев, чтобы получить id последнего (или создать питомца, если список пуст):
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев:
    if len(my_pets['pets']) == 0:
        pf.add_pet_simple(auth_key, 'Вальдемар', 'пёс', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем в переменную id первого питомца и добавляем фото для него:
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_by_pet_id(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400
    # Как и тест 7, возвращает 500, хотя кажется, что должен 400 - The error code means that provided data is incorrect

# Далее негативные тесты если и придумывались (нп, попробовать не передавать файл вообще или отправить битый), то они
# падали раньше, чем дело доходило до assert. А как это красиво оформить, я пока не знаю. Поэтому пусть дальше будет
# парочка не очень интересных: попробуем ещё один некорректный формат фото (и это будет 10-й негативный тест, что нам
# и нужно) и позитивный с иероглифами, потому что а почему бы и нет? Всё равно я уже второй час жду, что произойдёт
# в 5-ом тесте и не уверена, что он вообще рабочий, а удалять его не хочется, потому что вдруг он всё же норм.

# ↓ 10. POST /api/pets/set_photo/{pet_id} - невалидное вложение (формат arw) - ожидаем код 400

def test_post_photo_arw(pet_photo='images/0dog.arw'):
    """Проверяем, что существующему питомцу нельзя загрузить фото недопустимого формата (допустимы JPG, JPEG и PNG)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Запрашиваем список питомцев, чтобы получить id последнего (или создать питомца, если список пуст):
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем: если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев:
    if len(my_pets['pets']) == 0:
        pf.add_pet_simple(auth_key, 'Вальдемар', 'пёс', '9')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Сохраняем в переменную id первого питомца и добавляем фото для него:
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_by_pet_id(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 400
    # Как и тест 7, возвращает 500, хотя кажется, что должен 400 - The error code means that provided data is incorrect


# ↓ 11. POST /api/create_pet_simple - создаём питомца без фото с предположительно валидными данными

def test_post_new_pet_simple_japan(name='良いサービスが欲しい', animal_type='скунс', age='5'):
    """Проверяем, что можно добавить питомца с иероглифами в имени"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key:
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца:
    status, result = pf.add_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом:
    assert status == 200
    assert result['name'] == name
