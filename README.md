# MONDE-data-server
MONDEIQUE data management 및 알바 page server repo입니다. 
<br></br>
## Prerequsite
### How to install 
```
$ pip install -r requirements.txt
```

## API
### Login page
1. RegistraionAPI : username과 password를 입력하고 회원가입 버튼을 눌렀을 때 호출되는 API
2. LoginAPI : username과 password를 입력하고 로그인 버튼을 눌렀을 때 호출되는 API
3. UserAPI : User 자체에 대한 접근을 하기 위한 API
### Main Homepage
4. HomeRetrieveAPIView : Home (Main 화면) 으로 넘어갔을 때 호출되는 API
5. BoxingAssignAPIView : Boxing 할당받기 버튼을 눌렀을 때 호출되는 API
6. LabelingAssignAPIView : Labeling 할당받기 버튼을 눌렀을 때 호출되는 API
7. OriginalImageCreateAPIView : Original Image 생성 시 호출되는 API (미리 upload 되어 있어야 하는 API)
### Boxing page
8. BoxingRetrieveAPIView : Boxing 화면 url 입력 시 호출되는 API
9. BoxingCreateUpdateAPI : Box 생성 및 업데이트 시 호출되는 API (enter 쳤을 때 호출)
10. BoxingDestroyAPIView : Box 삭제 시 호출되는 API (delete 버튼 눌렀을 때 호출)
11. BoxingHoldAPIView : Box의 모양이 그대로 남아있는 holding 될 때 호출되는 API (maybe deprecated)
### Labeling page
12. LabelingRetrieveAPIView : Labeling 화면 url 입력 시 호출되는 API
13. LabelingDestroyAPIView : Labeling Image 삭제 시 호출되는 API (delete 버튼 눌렀을 때 호출)
