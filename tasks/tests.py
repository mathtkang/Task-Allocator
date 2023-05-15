from rest_framework.test import APITestCase
from tasks.models import Task, SubTask
from users.models import User


class TestTasks(APITestCase):
    DEFAULT_TITLE = "test title"
    DEFAULT_CONTENT = "test content"
    URL = "/v1/tasks/"

    def setUp(self):
        # User 생성
        user = User.objects.create(
            username="test user",
        )
        user.set_password("test password")
        user.save()
        self.user = user

        # Task 생성
        Task.objects.create(
            title=self.DEFAULT_TITLE,
            content=self.DEFAULT_CONTENT,
            create_user=user
        )

    def test_get(self):
        response = self.client.get(self.URL)
        # 누구나 read 가능
        self.assertEqual(
            response.status_code,
            200,
            "Status code isn't 200.",
        )
        # print(response)  # <Response status_code=200, "application/json">
        data = response.json()
        # print(data)
        '''
        [{
            'id': 1, 
            'create_user': 
            {
                'username': 'test user', 
                'team_name': ''
            }, 
            'title': 'test title', 
            'content': 'test content', 
            'is_complete': False, 
            'subtasks': [], 
            'created_at': '2023-05-15T21:58:52.610088', 
            'updated_at': '2023-05-15T21:58:52.610102'
        }]
        '''
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
            self.DEFAULT_TITLE,
        )
        self.assertEqual(
            data[0]["content"],
            self.DEFAULT_CONTENT,
        )

    def test_post(self):
        NEW_TITLE = "new test title"
        NEW_CONTENT = "new test content"

        # [Not Authentication CASE]
        response = self.client.post(
            self.URL,
        )
        self.assertEqual(
            response.status_code, 
            403
        )
        # print(response)  # 403
        # print(response.json())  #{'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'}

        # [GOOD CASE]
        self.client.force_login(
            self.user
        )
        response = self.client.post(
            self.URL,
            data={
                "title": NEW_TITLE,
                "content": NEW_CONTENT,
            },
        )
        print(response) # 200
        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )
        data = response.json()
        # print(data)
        # '''
        # {
        #     'id': 2, 
        #     'create_user': 
        #         {'username': 'test user'},
        #     'title': 'new test title', 
        #     'content': 'new test content', 
        #     'is_complete': False,
        #     'created_at': '2023-05-15T21:42:55.065198', 
        #     'updated_at': '2023-05-15T21:42:55.065203'
        # }
        # '''
        self.assertEqual(
            data["title"],
            NEW_TITLE,
        )
        self.assertEqual(
            data["content"],
            NEW_CONTENT,
        )

        # [BAD CASE]
        BAD_CASE_TITLE = "Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다. Models의 조건을 어기는 경우를 의도적으로 넣은 bad case의 title입니다."
        
        fail_response = self.client.post(
            self.URL,
            data={
                "title": BAD_CASE_TITLE,
                "content": NEW_CONTENT,
            },
        )
        # print(fail_response)  # <HttpResponseNotFound status_code=404, "text/html; charset=utf-8">
        self.assertEqual(
            fail_response.status_code,
            400
        )
        # print(fail_response.json())  # {'title': ['이 필드의 글자 수가 256 이하인지 확인하십시오.']}
        error_message = fail_response.json()
        self.assertIn(
            "title",
            error_message
        )
        

class TestTaskDetail(APITestCase):
    pass