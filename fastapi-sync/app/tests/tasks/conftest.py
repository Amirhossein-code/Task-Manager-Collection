import pytest
from datetime import datetime, timedelta, timezone


@pytest.fixture()
def create_task(client, create_user_with_token):
    def do_create_task(
        title: str = "Task Create fixture",
        description: str = "This is the new task created to test task create endpoint",
        status: str = "pending",
        priority: str = "low",
        start_time: int | None = None,
        finish_time: int | None = None,
    ):
        access_token = create_user_with_token(email="user98@gmail.com")

        now = datetime.now(timezone.utc)
        posted_task_data = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
        }

        # Conditionally add start_time and finish_time if they are not None
        if start_time is not None:
            start_time_dt = now + timedelta(minutes=start_time)
            posted_task_data["start_time"] = start_time_dt.isoformat().replace(
                "+00:00", "Z"
            )

        if finish_time is not None:
            finish_time_dt = now + timedelta(minutes=finish_time)
            posted_task_data["finish_time"] = finish_time_dt.isoformat().replace(
                "+00:00", "Z"
            )

        res = client.post(
            "/tasks",
            json=posted_task_data,
            headers={"Authorization": f"Bearer {access_token}"},
        )

        return res, posted_task_data

    return do_create_task
