from rest_framework.test import APITestCase
from tasks.models import Task, SubTask
from users.models import User


DEFAULT_TITLE = "test title"
DEFAULT_CONTENT = "test content"
DEFAULT_USERNAME = "test username"
DEFAULT_PASSWORD = "test password"


class TestTasks(APITestCase):
    
    URL = "/v1/tasks/"

    def setUp(self):
        # Create User
        user = User.objects.create(
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.save()
        self.user = user

        # print(type(self.user))  # <class 'users.models.User'>

        # Create Task
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )

    def test_get(self):
        response = self.client.get(self.URL)
        # [Anyone Readable]
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        data = response.json()
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["title"],
            DEFAULT_TITLE,
        )
        self.assertEqual(
            data[0]["content"],
            DEFAULT_CONTENT,
        )

    def test_post(self):
        NEW_TITLE = "test new title"
        NEW_CONTENT = "test new content"

        # [1. Not Authentication CASE]
        response = self.client.post(
            self.URL,
        )
        self.assertEqual(
            response.status_code, 
            403
        )

        # [Authentication]
        self.client.login(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
        )

        # [2. BAD CASE 1] 로그인 완료 BUT team_name이 없는 경우
        response = self.client.post(
            self.URL,
            data={
                "title": NEW_TITLE,
                "content": NEW_CONTENT,
            },
        )
        
        # print(response)  # <Response status_code=403, "application/json">
        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 200.",
        )

        # [3. GOOD CASE]
        self.client.put(
            "/v1/users/me",
            data={
                "team_name": "danbi",
            },
        )

        response = self.client.post(
            self.URL,
            data={
                "title": NEW_TITLE,
                "content": NEW_CONTENT,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        data = response.json()
        self.assertEqual(
            data["title"],
            NEW_TITLE,
        )
        self.assertEqual(
            data["content"],
            NEW_CONTENT,
        )

        # [4. BAD CASE 2]
        BAD_CASE_TITLE = "Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다."
        
        fail_response = self.client.post(
            self.URL,
            data={
                "title": BAD_CASE_TITLE,
                "content": NEW_CONTENT,
            },
        )
        self.assertEqual(
            fail_response.status_code,
            400
        )
        error_message = fail_response.json()
        self.assertIn(
            "title",
            error_message
        )

        # [5. BAD CASE 3]
        fail_response = self.client.post(self.URL)
        self.assertEqual(
            fail_response.status_code,
            400
        )
        error_message = fail_response.json()
        self.assertIn(
            "title",
            error_message
        )


class TestTaskDetail(APITestCase):
    URL = "/v1/tasks"

    def setUp(self):
        # Create User and Update team_name
        user = User.objects.create(
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.save()
        self.user = user

        self.client.login(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD,
        )

        self.client.put(
            "/v1/users/me",
            data={
                "team_name": "danbi",
            },
        )

        # Create Task
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )
    
    # [tid로 찾는 Task가 없는 경우]
    def test_get_task_object(self):
        response = self.client.get(f"{self.URL}/2")
        self.assertEqual(
            response.status_code,
            404
        )

    # [tid로 찾는 Task가 있는 경우]
    def test_get(self):
        response = self.client.get(f"{self.URL}/1")
        self.assertEqual(
            response.status_code, 
            200
        )
        data = response.json()
        self.assertEqual(
            data["title"],
            DEFAULT_TITLE,
        )
        self.assertEqual(
            data["content"],
            DEFAULT_CONTENT,
        )

    def test_put(self):
        UPDATED_TITLE = "test updated title"
        UPDATED_CONTENT = "test updated content"

        # [GOOD CASE]
        response = self.client.put(
            f"{self.URL}/1",
            data={
                "title": UPDATED_TITLE, 
                "content": UPDATED_CONTENT,
            },
        )
        self.assertEqual(
            response.status_code, 
            200,
        )
        data = response.json()
        self.assertEqual(
            data["title"],
            UPDATED_TITLE,
        )
        self.assertEqual(
            data["content"],
            UPDATED_CONTENT,
        )

        # [BAD CASE 1] 
        BAD_CASE_TITLE = "Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다. Task Models의 title 조건을 어기는 경우를 의도적으로 작성합니다. title의 글자 수를 256 초과하도록 작성합니다."

        fail_response = self.client.put(
            f"{self.URL}/1",
            data={
                "title": BAD_CASE_TITLE,
            },
        )
        self.assertEqual(
            fail_response.status_code, 
            400
        )
        error_message = fail_response.json()
        # print(error_message)
        self.assertIn(
            "title",
            error_message
        )

    def test_delete(self):
        # [GOOD CASE]
        response = self.client.delete(
            f"{self.URL}/1",
        )
        self.assertEqual(
            response.status_code, 
            204
        )

        # [이미 완료된 Task의 경우]
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=self.user,
            is_complete=True,
        )
        response = self.client.delete(
            f"{self.URL}/2",
        )
        self.assertEqual(
            response.status_code, 
            403
        )


