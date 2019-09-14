# MONDE-data-server
MONDEIQUE data management 및 알바 page server repo입니다. 
<br></br>
## Prerequsite
### How to install 
```
$ pip install -r requirements.txt
```
- mysqlclient의 경우 따로 install 해야함 (OSX Mojave에서 지속적인 error 발생)
## API
### Login page
- RegistraionAPI : username과 password를 입력하고 회원가입 버튼을 눌렀을 때 호출되는 API
- LoginAPI : username과 password를 입력하고 로그인 버튼을 눌렀을 때 호출되는 API
- UserAPI : User 자체에 대한 접근을 하기 위한 API
### Main Homepage
- HomeRetrieveAPIView : Home (Main 화면) 으로 넘어갔을 때 호출되는 API
- BoxingAssignAPIView : Boxing 할당받기 버튼을 눌렀을 때 호출되는 API
- LabelingAssignAPIView : Labeling 할당받기 버튼을 눌렀을 때 호출되는 API
- OriginalImageCreateAPIView : Original Image 생성 시 호출되는 API (미리 upload 되어 있어야 하는 API)
### Boxing page
- BoxingRetrieveAPIView : Boxing 화면 url 입력 시 호출되는 API
- BoxingCreateUpdateAPI : Box 생성 및 업데이트 시 호출되는 API (enter 쳤을 때 호출)
- BoxingDestroyAPIView : Box 삭제 시 호출되는 API (delete 버튼 눌렀을 때 호출)
- BoxingHoldAPIView : Box의 모양이 그대로 남아있는 holding 될 때 호출되는 API (maybe deprecated)
### Labeling page
- LabelingRetrieveAPIView : Labeling 화면 url 입력 시 호출되는 API
- LabelingDestroyAPIView : Labeling Image 삭제 시 호출되는 API (delete 버튼 눌렀을 때 호출)
- LabelCreateUpdateAPI (6개) : 각 Label 생성 및 업데이트 시 호출되는 API (enter 쳤을 때 호출)
