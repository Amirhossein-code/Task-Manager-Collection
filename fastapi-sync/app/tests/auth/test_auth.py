def test_create_access_token(client, create_user, create_access_token):
    res = create_user(
        email="user94@gmail.com",
        password="ILoveFastAPI990@90",
    )
    assert res.status_code == 201, res.text

    res_2 = create_access_token(
        email="user94@gmail.com",
        password="ILoveFastAPI990@90",
    )

    assert res_2.status_code == 200

    response_json = res_2.json()
    assert "access_token" in response_json
    assert "token_type" in response_json
