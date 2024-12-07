import requests

API_URL = 'http://127.0.0.1:5000/api/'

def create_user_request(name, login, email, password, description, country, phone, isPublic, image):
    return requests.post(
        API_URL + 'registration',
        json={'name': name,
              'login': login,
              'email': email,
              'password':password,
              'description': description,
              'country': country,
              'phone':phone,
              'isPublic': isPublic,
              'image': image
    }
    )
def delete_user(name):
    return requests.delete(API_URL + 'delete/' + str(name))

def get_country_request(alpha2):
    return requests.get(API_URL + 'country/' + str(alpha2))

def registration():
    return requests.get(API_URL + 'registration')
def all_countries():
    return requests.get(API_URL + 'countries')

def run_artists_api_tests():
    # проверяем создание артистов
    user = create_user_request('name', 'login', 'email', 'password', 'description', 'RU', 'phone', True, 'image')
    print(user.json())
    assert user.status_code == 200

    print("Artist creation tests passed!")

    # сохраняем id новых артистов
    user_country = user.json().get('country')
    user_name = user.json().get('name')

    # проверяем, что нельзя создать артиста с уже использованным именем
    artist_response = create_user_request('name1', 'login', 'email', 'password', 'description', 'RU', 'phone', True, 'image')
    assert artist_response.status_code == 400
    print("Artist login uniqueness tests passed!")

    # проверяем, что можно получить артиста по alpha2
    artist_response = get_country_request(user_country)
    assert artist_response.status_code == 200
    print("Get country by alpha2 tests passed!")




    # проверяем, что можно получить список артистов
    artist_response = all_countries()
    assert artist_response.status_code == 200
    print("Get all artists tests passed!")

    userer = delete_user('name')
    assert userer.status_code == 200

    print("Delete artist tests passed!")

    print("All tests passed!")

if __name__ == '__main__':
    run_artists_api_tests()
