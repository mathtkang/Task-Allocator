from rest_framework.test import APITestCase
from tasks.models import Task, SubTask
from users.models import User


DEFAULT_TITLE="test title"
DEFAULT_CONTENT="test content"
DEFAULT_USERNAME="test username"
DEFAULT_PASSWORD="test password"
DEFAULT_COMPLETED_DATE="2023-12-25"
DEFAULT_TEAM_NAME="sophia"
BASE_URL="/v1/tasks"

class TestTasks(APITestCase):
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
        response = self.client.get(f"{BASE_URL}/")
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
            f"{BASE_URL}/",
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

        # [2. BAD CASE 1] 로그인 완료, BUT team_name이 없는 경우
        response = self.client.post(
            f"{BASE_URL}/",
            data={
                "title": NEW_TITLE,
                "content": NEW_CONTENT,
            },
        )
        self.assertEqual(
            response.status_code,
            403,
            "Status code isn't 200.",
        )

        # [3. GOOD CASE] 로그인 완료, team_name도 지정해준 경우
        self.user.team_name = DEFAULT_TEAM_NAME
        self.user.save()

        response = self.client.post(
            f"{BASE_URL}/",
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
            f"{BASE_URL}/",
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
        fail_response = self.client.post(f"{BASE_URL}/")
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
            password=DEFAULT_PASSWORD
        )

        # Create Task
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )
    
    # [tid로 찾는 Task가 없는 경우]
    def test_get_task_object(self):
        response = self.client.get(f"{BASE_URL}/2")
        self.assertEqual(
            response.status_code,
            404
        )

    # [tid로 찾는 Task가 있는 경우]
    def test_get(self):
        response = self.client.get(f"{BASE_URL}/1")
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
            f"{BASE_URL}/1",
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
            f"{BASE_URL}/1",
            data={
                "title": BAD_CASE_TITLE,
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

    def test_delete(self):
        # [GOOD CASE]
        response = self.client.delete(
            f"{BASE_URL}/1",
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
            f"{BASE_URL}/2",
        )
        self.assertEqual(
            response.status_code, 
            403
        )


class TestSubTasksAll(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.team_name = DEFAULT_TEAM_NAME
        user.save()
        self.user = user

        self.client.login(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )

        # Create Task => task_id : 1
        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )

        # Create SubTask => subtask_id : 1
        SubTask.objects.create(
            task_id=1,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME
        )

    def test_get(self):
        response = self.client.get(f"{BASE_URL}/subtasks/all")
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
            data[0]["team_name"],
            DEFAULT_TEAM_NAME,
        )


class TestSubTasks(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.team_name = DEFAULT_TEAM_NAME
        user.save()
        self.user = user

        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )

        SubTask.objects.create(
            task_id=1,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME
        )

    def test_get(self):
        response = self.client.get(f"{BASE_URL}/1/subtasks")
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
            data[0]["team_name"],
            DEFAULT_TEAM_NAME,
        )

    def test_post(self):
        NEW_COMPLETED_DATE = "2024-12-25"
        NEW_TEAM_NAME = "darae"

        # [1. Not Authentication CASE]
        response = self.client.post(
            f"{BASE_URL}/1/subtasks",
        )
        self.assertEqual(
            response.status_code, 
            403
        )

        # [Authentication]
        self.client.login(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )

        # [2. BAD CASE 1] 로그인 완료, BUT Task 생성자와 client가 다른 경우 
        #   => 새로운 User를 만들어주고 그 user로 만든 task.id=2를 만든다.
        user2 = User.objects.create(
            username="new user name",
        )
        user2.set_password("password")
        user2.team_name = "cheollo"
        user2.save()

        Task.objects.create(
            create_user=user2
        )

        response = self.client.post(
            f"{BASE_URL}/2/subtasks",
            data={
                "completed_date": NEW_COMPLETED_DATE,
                "team_name": NEW_TEAM_NAME,
            },
        )
        self.assertEqual(
            response.status_code,
            403,
        )

        # [3. GOOD CASE] 로그인 완료, Task 생성자와 client가 같은 경우
        response = self.client.post(
            f"{BASE_URL}/1/subtasks",
            data={
                "completed_date": NEW_COMPLETED_DATE,
                "team_name": NEW_TEAM_NAME,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        data = response.json()
        self.assertEqual(
            data["completed_date"],
            NEW_COMPLETED_DATE,
        )
        self.assertEqual(
            data["team_name"],
            NEW_TEAM_NAME,
        )


class TestSubTaskDetail(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username=DEFAULT_USERNAME,
        )
        user.set_password(DEFAULT_PASSWORD)
        user.team_name = DEFAULT_TEAM_NAME
        user.save()
        self.user = user

        self.client.login(
            username=DEFAULT_USERNAME,
            password=DEFAULT_PASSWORD
        )

        Task.objects.create(
            title=DEFAULT_TITLE,
            content=DEFAULT_CONTENT,
            create_user=user
        )

        SubTask.objects.create(
            task_id=1,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME
        )

    def test_get_task_object(self):
        # [1. stid로 찾는 SubTask가 없는 경우]
        response = self.client.get(f"{BASE_URL}/1/subtasks/2")
        self.assertEqual(
            response.status_code,
            404
        )
        # [2. tid로 찾는 Task가 없는 경우]
        response = self.client.get(f"{BASE_URL}/2/subtasks/1")
        self.assertEqual(
            response.status_code,
            404
        )

    def test_get(self):
        response = self.client.get(f"{BASE_URL}/1/subtasks/1")
        self.assertEqual(
            response.status_code, 
            200
        )

        data = response.json()
        self.assertEqual(
            data["completed_date"],
            DEFAULT_COMPLETED_DATE,
        )
        self.assertEqual(
            data["team_name"],
            DEFAULT_TEAM_NAME,
        )

    def test_put(self):
        UPDATED_COMPLETED_DATE = "2025-12-25"
        UPDATED_TEAM_NAME = "cheollo"
        # UPDATED_IS_COMPLETE_TRUE = True
        # UPDATED_IS_COMPLETE_FALSE = False

        # [1. Task 생성자인 경우]
        response = self.client.put(
            f"{BASE_URL}/1/subtasks/1",
            data={
                "completed_date": UPDATED_COMPLETED_DATE,
                "team_name": UPDATED_TEAM_NAME,
                "is_complete": True,
            },
        )
        self.assertEqual(
            response.status_code, 
            200,
        )
        data = response.json()
        # print(data)
        self.assertEqual(
            data["completed_date"],
            UPDATED_COMPLETED_DATE,
        )
        self.assertEqual(
            data["team_name"],
            UPDATED_TEAM_NAME,
        )
        self.assertEqual(
            data["is_complete"],
            True,
        )
        # [2. Subtask 소속 팀원인 경우] 
        # task의 생성자는 아니지만(새로운 user, task, subtask를 만들어줌), user의 team_name이 subtasks의 team_name일 때
        user2 = User.objects.create(
            username="new user name",
        )
        user2.set_password("password")
        user2.team_name = DEFAULT_TEAM_NAME
        user2.save()

        Task.objects.create(
            create_user=user2
        )
        SubTask.objects.create(
            task_id=2,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME
        )

        # [GOOD CASE]
        response = self.client.put(
            f"{BASE_URL}/2/subtasks/2",
            data={
                "is_complete": True,
            },
        )
        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()
        self.assertEqual(
            data["is_complete"],
            True,
        )
        

        # [BAD CASE]
        response = self.client.put(
            f"{BASE_URL}/2/subtasks/2",
            data={
                "completed_date": UPDATED_COMPLETED_DATE,
                "team_name": UPDATED_TEAM_NAME,
            },
        )
        self.assertEqual(
            response.status_code,
            400,
        )
        # print(response.json())  # {'detail': '해당 subtask의 completed_date 또는 team_name는 수정할 수 없습니다. is_complete 만 수정 가능합니다.'}


    def test_validate_task_complete(self):
        # 1. 새로운 subtask를 생성한다 (subtask가 2개 이상이여야 해당 테스트 실행 가능)
        SubTask.objects.create(
            task_id=1,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME
        )
        # 2. subtask_id=1 의 is_complete을 true로 변환 후
        response_of_first_subtasks = self.client.put(
            f"{BASE_URL}/1/subtasks/1",
            data={
                "is_complete": True,
            },
        )
        self.assertEqual(
            response_of_first_subtasks.status_code,
            200,
        )
        data_subtask = response_of_first_subtasks.json()
        self.assertEqual(
            data_subtask["is_complete"],
            True,
        )
        
        # 3. task=1 의 is_complete이 False로 유지되는지 확인한다. (아직 subtask_id=2의 is_complete이 False이기 때문에!)
        response_task = self.client.get(f"{BASE_URL}/1")
        self.assertEqual(
            response_task.status_code,
            200,
        )
        data_task = response_task.json()
        self.assertEqual(
            data_task["is_complete"],
            False,
        )
        # print(data_task)
        '''
        {
            'id': 1, 
            'create_user': 
            {
                'username': 'test username'
            }, 
            'title': 'test title', 
            'content': 'test content', 
            'is_complete': False,   <- 아직 안 바뀌었다!
            'created_at': '2023-05-16T05:00:08.516159', 
            'updated_at': '2023-05-16T05:00:08.521424'
        }
        '''

        # 4. subtask_id=2 의 is_complete을 true로 변환 후
        response_of_second_subtasks = self.client.put(
            f"{BASE_URL}/1/subtasks/2",
            data={
                "is_complete": True,
            },
        )
        self.assertEqual(
            response_of_second_subtasks.status_code,
            200,
        )
        data_subtask = response_of_second_subtasks.json()
        self.assertEqual(
            data_subtask["is_complete"],
            True,
        )

        # 5. task=1 의 is_complete이 True로 자동 변환 되었는지 확인한다.
        response_task = self.client.get(f"{BASE_URL}/1")
        self.assertEqual(
            response_task.status_code,
            200,
        )
        data_task = response_task.json()
        self.assertEqual(
            data_task["is_complete"],
            True,
        )
        # print(data_task)
        '''
        {
            'id': 1, 
            'create_user': 
            {
                'username': 'test username'
            }, 
            'title': 'test title', 
            'content': 'test content', 
            'is_complete': True,   <- 여기 바뀌었다! 
            'created_at': '2023-05-16T05:01:56.185399', 
            'updated_at': '2023-05-16T05:01:56.198867'
        }
        '''
    
    
    def test_delete(self):
        # [GOOD CASE]
        response = self.client.delete(
            f"{BASE_URL}/1/subtasks/1",
        )
        self.assertEqual(
            response.status_code, 
            204
        )

        # [이미 완료된 SubTask의 경우]
        SubTask.objects.create(
            task_id=1,
            completed_date=DEFAULT_COMPLETED_DATE,
            team_name=DEFAULT_TEAM_NAME,
            is_complete=True,
        )
        response = self.client.delete(
            f"{BASE_URL}/1/subtasks/2",
        )
        self.assertEqual(
            response.status_code, 
            403
        )