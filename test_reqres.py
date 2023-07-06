from jsonschema.validators import validate
from helper import load_json_schema, CustomSession, reqres_session


def test_create_user():
    name = "Ilon Mask"
    job = "Space"
    schema = load_json_schema('post_create_user.json')

    response = reqres_session.post('/api/users', json={"name": name, "job": job})

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 201
    assert response.json()['name'] == name
    assert response.json()['job'] == job


def test_login_successful():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    schema = load_json_schema('post_login_successful.json')

    response = reqres_session.post('/api/login', json={
            "email": email,
            "password": password}
    )

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['token'] != ''


def test_login_unsuccessful():
    email = "a1@a1"
    schema = load_json_schema('post_login_unsuccessful.json')

    response = reqres_session.post('/api/login', json={
            "email": email}
    )

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 400
    assert response.json()['error'] == 'Missing password'


def test_single_user_not_found():
    schema = load_json_schema('get_single_user_not_found.json')

    response = reqres_session.get('/api/users/33')

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 404
    assert response.text == '{}'


def test_page_number():
    page = 2
    schema = load_json_schema('get_page_number.json')

    response = reqres_session.get('/api/users', params={'page': page})

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200


def test_register_successful():
    email = "eve.holt@reqres.in"
    password = "pistole"
    schema = load_json_schema('post_register_successful.json')

    response = reqres_session.post('/api/register', json={
                                 "email": email,
                                 "password": password}
                             )

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()['id'] != ''


def test_register_unsuccessful():
    email = "sydney@fife"
    schema = load_json_schema('post_register_unsuccessful.json')

    response = reqres_session.post('/api/register', json={"email": email})

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 400
    assert response.json()["error"] == "Missing password"


def test_update_user_info():
    name = "morpheus"
    job = "zion resident"
    schema = load_json_schema('put_update_user_info.json')

    response = reqres_session.put('/api/users/2', json={"name": name,
                                  "job": job})

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200
    assert response.json()["name"] == name
    assert response.json()["job"] == job


def test_users_list_length():
    default_users_count = 6
    schema = load_json_schema('get_user_list.json')

    response = reqres_session.get('/api/users')

    validate(instance=response.json(), schema=schema)
    assert len(response.json()['data']) == default_users_count


def test_delayed_response():
    schema = load_json_schema('get_delayed_response.json')

    response = reqres_session.get('/api/users?delay=3')

    validate(instance=response.json(), schema=schema)
    assert response.status_code == 200