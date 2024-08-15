from ...models import Task


class TestTaskDelete:
    def test_logged_in_user_deletes_their_task_returns_204(
        self, create_task, create_access_token, client, db_session
    ):
        #  Create a task
        email = "user990@gmail.com"
        password = "Halo9980@@#don"

        # Create task with the specified email and password
        response_create_task, _ = create_task(email=email, password=password)
        response_create_task_json = response_create_task.json()
        task_id = response_create_task_json["id"]

        #  Get the access token for the user
        response_access_token = create_access_token(email=email, password=password)
        response_access_token_json = response_access_token.json()
        access_token = response_access_token_json["access_token"]

        # Delete the task with the access token
        delete_response = client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert delete_response.status_code == 204

        # Make sure it is deleted from the database
        task = db_session.query(Task).filter(Task.id == task_id).first()
        assert task is None

    def test_delete_other_users_task_returns_403(
        self,
        create_task,
        client,
        db_session,
        create_user_with_token,
    ):
        user_1_email = "user20@gmail.com"
        user_1_password = "Halo9980@@#don"

        user_2_email = "user21@gmail.com"
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

        # Delete user 1 task with second users access token
        delete_response = client.delete(
            f"/tasks/{task_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert delete_response.status_code == 403

        # Make sure it is deleted from the database
        task = db_session.query(Task).filter(Task.id == task_id).first()
        assert task is not None

    def test_logged_out_user_deletes_task_returns_401(self, create_task, client):
        
        res, _ = create_task(
            email="user22@gmail.com",
            password="Halo9980@@#don",
        )
        res_json = res.json()
        task_id = res_json["id"]

        # Delete the task without the access token
        delete_response = client.delete(
            f"/tasks/{task_id}",
        )

        assert delete_response.status_code == 401
