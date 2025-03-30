import requests

class PetFriendsAPI:
    BASE_URL = "https://petfriends.skillfactory.ru"

    def __init__(self, email: str, password: str):
        self.auth_key = self.get_api_key(email, password)

    def get_api_key(self, email: str, password: str):
        """Получение API-ключа для работы с API.
        Данные передаются в заголовках, как в Postman."""
        headers = {
            "email": email,
            "password": password
        }
        response = requests.get(f"{self.BASE_URL}/api/key", headers=headers)
        response.raise_for_status()
        return response.json().get("key")

    def get_pets(self, filter: str = ""):
        """Получение списка питомцев (с возможной фильтрацией)"""
        headers = {"auth_key": self.auth_key}
        response = requests.get(f"{self.BASE_URL}/api/pets", headers=headers, params={"filter": filter})
        response.raise_for_status()
        return response.json()

    def add_pet(self, name: str, animal_type: str, age: int):
        """Добавление нового питомца (без фото) через multipart/form-data"""
        headers = {
            "auth_key": self.auth_key,
            "accept": "application/json"
        }
        files = {
            "name": (None, name),
            "animal_type": (None, animal_type),
            "age": (None, str(age))
        }
        response = requests.post(f"{self.BASE_URL}/api/create_pet_simple", headers=headers, files=files)
        response.raise_for_status()
        return response.json()

    def update_pet(self, pet_id: str, name: str, animal_type: str, age: int):
        """Обновление информации о питомце через multipart/form-data"""
        headers = {
            "auth_key": self.auth_key,
            "accept": "application/json"
        }
        files = {
            "name": (None, name),
            "animal_type": (None, animal_type),
            "age": (None, str(age))
        }
        response = requests.put(f"{self.BASE_URL}/api/pets/{pet_id}", headers=headers, files=files)
        response.raise_for_status()
        return response.json()

    def delete_pet(self, pet_id: str):
        """Удаление питомца по ID"""
        headers = {"auth_key": self.auth_key}
        response = requests.delete(f"{self.BASE_URL}/api/pets/{pet_id}", headers=headers)
        response.raise_for_status()
        return response.status_code

    def add_pet_photo(self, pet_id: str, photo_path: str):
        """Добавление фото питомца"""
        headers = {"auth_key": self.auth_key}
        with open(photo_path, "rb") as photo:
            files = {"pet_photo": photo}
            response = requests.post(f"{self.BASE_URL}/api/pets/set_photo/{pet_id}", headers=headers, files=files)
        response.raise_for_status()
        return response.json()
