from datetime import datetime, timedelta, timezone

import pytest


class TestUserUpdate:
    @pytest.mark.parametrize(
        "method, email",
        [
            ("PUT", "user27@gmail.com"),
            ("PATCH", "user26@gmail.com"),
        ],
    )
    def test_logged_in_user_updates_task_owned_by_them_returns_201(
        self, client, create_task, create_access_token, method, email
    ):
        password = "albo2322@MnopW"

        title = "title"
        updated_title = "Updated Title"

        description = "description"
        updated_description = "Updated des"

        status = "ongoing"
        updated_status = "pending"

        priority = "high"
        updated_priority = "low"

        res, _ = create_task(
            email=email,
            password=password,
            title=title,
            description=description,
            status=status,
            priority=priority,
        )

        response_json = res.json()
        task_id = response_json["id"]

        access_token_res = create_access_token(email=email, password=password)
        access_token_response = access_token_res.json()
        access_token = access_token_response["access_token"]

        update_data = {
            "title": updated_title,
            "description": updated_description,
            "status": updated_status,
            "priority": updated_priority,
        }

        response = client.request(
            method,
            f"/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 200
        update_res = response.json()
        assert update_res["title"] == updated_title
        assert update_res["description"] == updated_description
        assert update_res["status"] == updated_status
        assert update_res["priority"] == updated_priority

    @pytest.mark.parametrize(
        "method",
        [
            "PUT",
            "PATCH",
        ],
    )
    def test_logged_in_user_tries_updating_task_of_other_user_returns_401(
        self, create_task, create_user_with_token, client, method
    ):
        user_1_email = "user28@gmail.com"
        user_1_password = "Halo9980@@#don"

        user_2_email = "user29@gmail.com"
        user_2_password = "Halo99736580@@#don2323"

        # Create task with the specified email and password
        response_create_task, _ = create_task(
            email=user_1_email, password=user_1_password
        )
        response_create_task_json = response_create_task.json()
        task_id = response_create_task_json["id"]

        #  Get the access token for the second user that is not task owner
        access_token = create_user_with_token(
            email=user_2_email, password=user_2_password
        )

        update_data = {
            "title": "updated_title",
            "description": "updated_description",
        }

        get_response = client.request(
            method,
            f"/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_response.status_code == 403

    @pytest.mark.parametrize(
        "start_time, finish_time, updated_start_time_mins, updated_finish_time_mins, expected_response",
        [
            (10, 15, 25, 20, 422),  # Updated finish time is before updated start time
            (10, 15, -5, 20, 422),  # updated_start_time is before current time
            (10, None, 10, 10, 422),
            (None, None, 10, 10, 422),
            (None, None, 10, 5, 422),
            (None, None, -5, 5, 422),
            (None, None, 15, 25, 200),
            (None, None, None, 10, 200),
            (None, None, 10, None, 200),
            (None, None, None, None, 200),
            (10, 15, 25, 30, 200),  # Normal case
        ],
    )
    @pytest.mark.parametrize(
        "method, email",
        [
            ("PUT", "user273@gmail.com"),
            ("PATCH", "user263@gmail.com"),
        ],
    )
    def test_logged_in_user_updates_task_with_invalid_start_finish_time_returns_422(
        self,
        client,
        create_task,
        create_access_token,
        method,
        email,
        start_time,
        finish_time,
        updated_start_time_mins,
        updated_finish_time_mins,
        expected_response,
    ):
        password = "albo2322@MnopW"

        res, _ = create_task(
            email=email,
            password=password,
            start_time=start_time,
            finish_time=finish_time,
        )

        response_json = res.json()
        task_id = response_json["id"]

        access_token_res = create_access_token(email=email, password=password)
        access_token_response = access_token_res.json()
        access_token = access_token_response["access_token"]
        # Prep updated start/finish times
        now = datetime.now(timezone.utc)

        if updated_start_time_mins is None:
            updated_start_time = None
        else:
            start_time_dt = now + timedelta(minutes=updated_start_time_mins)
            updated_start_time = start_time_dt.isoformat().replace("+00:00", "Z")

        if updated_finish_time_mins is None:
            updated_finish_time = None
        else:
            finish_time_dt = now + timedelta(minutes=updated_finish_time_mins)
            updated_finish_time = finish_time_dt.isoformat().replace("+00:00", "Z")

        update_data = {
            "start_time": updated_start_time,
            "finish_time": updated_finish_time,
        }

        response = client.request(
            method,
            f"/tasks/{task_id}",
            json=update_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == expected_response
