# Task-Allocator
하나의 Task를 여러 SubTask로 나누고 다른 팀에게 할당하는 서비스입니다. 업무목록을 통해 진행과정 및 Task의 완료/미완료 되었는지 알 수 있습니다.

<br>

## ⚙️ `.env` 파일을 다운 받을 수 있는 [Google Drive](https://drive.google.com/drive/folders/1GVXT_dHQl9hsvyQCuRdLdtUSqheZPd0S) 입니다.

<br>

## 📑 요구사항 정리 및 API spec | [Notion]()
요구사항 정리 및 ERD, API spec 등이 적혀있습니다.

<br>

## 🚀 서비스 배포 | [link](http://15.164.245.240:8000)
기본 페이지는 not found 404 입니다. 이후 url을 입력해주세요!

<br>

###  🔫 Test-Code 완료
<img width="800" alt="Test-Code" src="https://user-images.githubusercontent.com/51039577/244661736-61bc1881-990b-4ee8-99f1-e47b9fc206dc.png">

<br>
<br>
<br>

### request data 예시
1. 회원가입 & 로그인시 필요한 데이터 예시 (`/v1/users/signup`, `/v1/users/login`)
```
{
    "username":"Sophia",
    "password": "1234"
}
```
2. 마이페이지 팀 이름 업데이트 데이터 예시 (`/v1/users/me`)
```
{
    "team_name": "Sophia"
}
```
3. Task 생성 시 필요한 데이터 예시 (`/v1/tasks`)
```
{
    "title": "title",
    "content": "test content"
}
```
4. SubTask 생성 시 필요한 데이터 예시 (`/v1/tasks/1/subtasks`)
```
{
    "completed_date": "2026-10-24",
    "team_name": "Sophia"
}
```

<br>

## Setting step

[환경설정 시 참고하면 좋은 블로그 (본인 블로그 입니다)](https://kkangsg.tistory.com/108)

간단하게 아래와 같습니다.
1. install poetry
```
$ curl -sSL https://install.python-poetry.org | python3 -
$ export PATH="/home/ubuntu/.local/bin:$PATH"
```
2. 가상환경 활성화 : `$ poetry shell`
3. 마이그레이션 : `$ python3 manage.py migrate`
