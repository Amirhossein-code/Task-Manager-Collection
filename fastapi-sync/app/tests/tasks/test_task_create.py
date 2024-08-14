import pytest
from datetime import datetime, timedelta, timezone
import pytz


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
        self, client, create_user_with_token, status, priority
    ):
        access_token = create_user_with_token(email="user98@gmail.com")

        now = datetime.now(timezone.utc).replace(tzinfo=pytz.utc)
        start_time = now + timedelta(minutes=10)
        finish_time = now + timedelta(minutes=20)

        response = client.post(
            "/tasks",
            json={
                "title": "Task New 1",
                "description": "This is the new task created to test task create endpoint",
                "status": str(status),
                "priority": str(priority),
                "start_time": start_time.isoformat(),
                "finish_time": finish_time.isoformat(),
            },
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert response.status_code == 201
