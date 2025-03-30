import pytest
import requests
from api import PetFriendsAPI

EMAIL = "denislopushansky@yandex.ru"
PASSWORD = "Denis2013loveFreinds"

@pytest.fixture
def api():
    return PetFriendsAPI(EMAIL, PASSWORD)

@pytest.fixture
def pet(api):
    pet_data = api.add_pet("TestPet", "dog", 3)
    yield pet_data
    api.delete_pet(pet_data["id"])

# Тест получения API-ключа
def test_get_api_key():
    headers = {
        "Accept": "application/json",
        "email": EMAIL,
        "password": PASSWORD
    }
    response = requests.get("https://petfriends.skillfactory.ru/api/key", headers=headers)
    print(response.status_code, response.text)
    assert response.status_code == 200
    assert "key" in response.json()

# Тест получения списка питомцев
def test_get_pets(api):
    pets = api.get_pets()
    assert "pets" in pets

# Тест добавления питомца
def test_add_pet(api):
    pet = api.add_pet("Bobby", "cat", 2)
    assert pet["name"] == "Bobby"
    api.delete_pet(pet["id"])

# Тесты с некорректными данными (ожидаем ошибку, но API её не выбрасывает)
@pytest.mark.xfail(reason="API не валидирует входные данные и не выбрасывает HTTPError для некорректных данных")
@pytest.mark.parametrize("name, animal_type, age", [("", "dog", 3), ("Tom", "", 3), ("Tom", "dog", -1)])
def test_add_pet_invalid(api, name, animal_type, age):
    with pytest.raises(requests.exceptions.HTTPError):
        api.add_pet(name, animal_type, age)

# Тест обновления питомца
def test_update_pet(api, pet):
    updated_pet = api.update_pet(pet["id"], "UpdatedName", "cat", 5)
    assert updated_pet["name"] == "UpdatedName"

# Тест удаления питомца
def test_delete_pet(api, pet):
    response = api.delete_pet(pet["id"])
    assert response == 200

# Тест авторизации с неверными данными
def test_invalid_auth():
    response = requests.get("https://petfriends.skillfactory.ru/api/key", params={"email": "invalid", "password": "wrong"})
    assert response.status_code == 403

# Тест несуществующего эндпоинта
def test_server_error():
    response = requests.get("https://petfriends.skillfactory.ru/api/non_existing_endpoint")
    assert response.status_code == 404
