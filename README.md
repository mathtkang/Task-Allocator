# danbiedu
단비교육 사전과제 레포지토리입니다.

<br>

## ⚙️ `.env` 파일을 다운 받을 수 있는 [Google Drive](https://drive.google.com/drive/folders/1GVXT_dHQl9hsvyQCuRdLdtUSqheZPd0S) 입니다.

<br>

## 📑 과제 분석 및 진행과정 작성한 개인페이지 | [Notion](https://sprinkle-piccolo-9fc.notion.site/4f84847a4bf84e6283df767183154b5d)
해당 페이지에 과제 분석 및 의사결정, ERD, API spec 등이 적혀있습니다.

<br>

## 🚀 서비스 배포 | [link](http://15.164.245.240:8000)
기본 페이지는 not found 404 입니다. 이후 url을 입력해주세요!

<br>

## 🔫 Test-Code 완료
<img width="956" alt="스크린샷 2023-05-16 오전 5 59 28" src="https://github.com/mathtkang/danbiedu/assets/51039577/2b58d522-de38-4bfc-a11f-c2eaa96419b0">

<br>

## request data 예시
1. 회원가입 & 로그인시 필요한 데이터 예시 (`/v1/users/signup`, `/v1/users/login`)
```
{
    "username":"danbi",
    "password": "1234"
}
```
2. 마이페이지 팀 이름 업데이트 데이터 예시 (`/v1/users/me`)
```
{
    "team_name": "danbi"
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
    "team_name": "danbi"
}
```

<br>

## setting step

[환경설정 시 참고하면 좋은 블로그 (본인 블로그 입니다)](https://kkangsg.tistory.com/108)

간단하게 아래와 같습니다.
1. install poetry
```
$ curl -sSL https://install.python-poetry.org | python3 -
$ export PATH="/home/ubuntu/.local/bin:$PATH"
```
2. 가상환경 활성화 : `$ poetry shell`
3. 마이그레이션 : `$ python3 manage.py migrate`
