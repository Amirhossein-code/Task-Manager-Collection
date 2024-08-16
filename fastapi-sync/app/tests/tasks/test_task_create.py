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
        self, create_task, status, priority, db_session
    ):
        title = "Task Create fixture"
        description = "This is the new task created to test task create endpoint"
        start_time_mins_from_now = 10
        finish_time_mins_from_now = 20

        response, posted_task_data = create_task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            start_time=start_time_mins_from_now,
            finish_time=finish_time_mins_from_now,
        )

        start_time_iso = posted_task_data["start_time"]
        finish_time_iso = posted_task_data["finish_time"]

        # Ensure the API response body data is valid
        response_json = response.json()

        assert response_json["title"] == title
        assert response_json["description"] == description
        assert response_json["status"] == status
        assert response_json["priority"] == priority
        assert response_json["start_time"] == start_time_iso[:-1]
        assert response_json["finish_time"] == finish_time_iso[:-1]

        # Ensure the changes are correct in the database
        task = db_session.query(Task).filter(Task.id == response_json["id"]).first()

        assert repr(task) == f"<Task(title='{title}'>"

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

        # Printing the time stamps a good way to understand what is going on
        with open("task_time_stamps.txt", "a") as file:
            lines_to_write = [
                f"start_time at submit is: {start_time_mins_from_now}\n",
                f"finish_time is: {finish_time_mins_from_now}\n",
                f"iso format of start_time: {start_time_iso}\n",
                f"iso format of finish time: {finish_time_iso}\n",
                f"start_time_db = {start_time_db}\n",
                f"finish_time_db = {finish_time_db}\n",
                f"start_time_db = {start_time_db.isoformat()}\n",
                f"finish_time_db = {finish_time_db.isoformat()}\n\n\n\n\n",
            ]

            file.writelines(lines_to_write)

    def test_create_task_with_status_done_returns_422(self, create_task):
        res, _ = create_task(status="done", start_time=10, finish_time=30)

        assert res.status_code == 422

    @pytest.mark.parametrize(
        "start_time, finish_time",
        [
            (10, 10),  # Test same start and finish time
            (15, 10),  # Test start time after finish time
            (-5, 10),  # Test start time 5 minutes before current time
        ],
    )
    def test_create_task_with_invalid_times_returns_422(
        self, create_task, start_time, finish_time
    ):
        res, _ = create_task(
            start_time=start_time,
            finish_time=finish_time,
        )
        assert res.status_code == 422

    @pytest.mark.parametrize(
        "start_time, finish_time",
        [
            (None, 5),
            (None, None),
            (5, None),
        ],
    )
    def test_create_task_with_none_times_returns_201(
        self, create_task, start_time, finish_time
    ):
        res, _ = create_task(
            start_time=start_time,
            finish_time=finish_time,
        )
        assert res.status_code == 201
