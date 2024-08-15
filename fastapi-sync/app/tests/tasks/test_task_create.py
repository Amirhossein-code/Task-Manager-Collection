from datetime import datetime, timedelta, timezone

import pytest

from ...models import Task


class TestTaskCreate:
    @pytest.mark.parametrize(
        "priority",
        [
            "low",
            "medium",
            "high",
            "urgent",
            "immediate",
        ],
    )
    @pytest.mark.parametrize(
        "status",
        [
            "pending",
            "ongoing",
        ],
    )
    def test_logged_in_user_creates_task_returns_201(
        self, client, create_user_with_token, status, priority, db_session
    ):
        status = str(status)
        priority = str(priority)

        title = "Task New 1"
        description = "This is the new task created to test task create endpoint"

        access_token = create_user_with_token(email="user98@gmail.com")

        now = datetime.now(timezone.utc)
        start_time = now + timedelta(minutes=10)
        finish_time = now + timedelta(minutes=20)

        start_time_iso = start_time.isoformat().replace("+00:00", "Z")
        finish_time_iso = finish_time.isoformat().replace("+00:00", "Z")

        response = client.post(
            "/tasks",
            json={
                "title": title,
                "description": description,
                "status": status,
                "priority": priority,
                "start_time": start_time_iso,
                "finish_time": finish_time_iso,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201

        response_json = response.json()

        assert response_json["title"] == title
        assert response_json["description"] == description
        assert response_json["status"] == status
        assert response_json["priority"] == priority
        assert response_json["start_time"] == start_time_iso[:-1]
        assert response_json["finish_time"] == finish_time_iso[:-1]

        task = db_session.query(Task).filter(Task.id == response_json["id"]).first()

        assert task is not None
        assert task.id == response_json["id"]
        assert task.title == title
        assert task.description == description
        assert task.status == status
        assert task.priority == priority

        start_time_db = task.start_time
        finish_time_db = task.finish_time

        assert start_time_db.isoformat() == start_time_iso[:-1]
        assert finish_time_db.isoformat() == finish_time_iso[:-1]

        with open("task_time_stamps.txt", "a") as file:
            lines_to_write = [
                f"now: {now}\n",
                f"start_time at submit is: {start_time}\n",
                f"finish_time is: {finish_time}\n",
                f"iso format of start_time: {start_time_iso}\n",
                f"iso format of finish time: {finish_time_iso}\n",
                f"start_time_db = {start_time_db}\n",
                f"finish_time_db = {finish_time_db}\n",
                f"start_time_db = {start_time_db.isoformat()}\n",
                f"finish_time_db = {finish_time_db.isoformat()}\n\n\n\n\n",
            ]

            file.writelines(lines_to_write)

    def test_create_task_with_status_done_returns_422(
        self, client, create_user_with_token
    ):
        access_token = create_user_with_token(email="user98@gmail.com")
        now = datetime.now(timezone.utc)
        start_time = now + timedelta(minutes=10)
        finish_time = now + timedelta(minutes=20)

        start_time_iso = start_time.isoformat().replace("+00:00", "Z")
        finish_time_iso = finish_time.isoformat().replace("+00:00", "Z")
        response = client.post(
            "/tasks",
            json={
                "title": "Task New 1",
                "description": "This is the new task created to test task create endpoint",
                "status": "done",
                "priority": "low",
                "start_time": start_time_iso,
                "finish_time": finish_time_iso,
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 422
