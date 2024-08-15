class TestTaskRead:
    def test_logged_in_user_retrieve_task_owned_by_them_by_id_returns_200(
        self, create_task, create_access_token, client
    ):
        email = "user20@gmail.com"
        password = "Halo9980@@#don"

        res, _ = create_task(email=email, password=password)
        response_json = res.json()
        task_id = response_json["id"]

        response_access_token = create_access_token(email=email, password=password)
        response_access_token_json = response_access_token.json()
        access_token = response_access_token_json["access_token"]

        get_response = client.get(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_response.status_code == 200

        get_res_json = get_response.json()
        assert get_res_json["id"] == task_id

    def test_logged_out_user_tries_retrieve_task_by_id_returns_401(
        self, create_task, client
    ):
        res, _ = create_task(
            email="user20@gmail.com",
            password="Halo9980@@#don",
        )
        response_json = res.json()
        task_id = response_json["id"]

        get_response = client.get(
            f"/tasks/{task_id}",
        )

        assert get_response.status_code == 401

    def test_logged_in_user_retrieves_all_tasks_owned_returns_200(
        self, create_task, client, create_access_token
    ):
        email = "user23@gmail.com"
        password = "Halo9980@@#don"

        res, _ = create_task(email=email, password=password)
        res_json = res.json()
        task_1_id = res_json["id"]

        res_2, _ = create_task(email=email, password=password)
        res_2_json = res_2.json()
        task_2_id = res_2_json["id"]

        response_access_token = create_access_token(email=email, password=password)
        response_access_token_json = response_access_token.json()
        access_token = response_access_token_json["access_token"]

        get_response = client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_response.status_code == 200

        get_res_json = get_response.json()

        task_ids = [task["id"] for task in get_res_json]
        assert task_1_id in task_ids
        assert task_2_id in task_ids

    def test_logged_out_user_tries_to_retrieves_all_tasks_returns_401(
        self, create_task, client
    ):
        email = "user23@gmail.com"
        password = "Halo9980@@#don"

        _, _ = create_task(email=email, password=password)

        get_response = client.get(
            "/tasks",
        )

        assert get_response.status_code == 401
