# SKN16-1st-5Team
SKN 16기 1차 단위프로젝트

<br>
# 📌 프로젝트 소개

연료비 변화에 따른 자동차 유형 등록 추이

전국 자동차의 등록 현황을 시각적으로 분석하고<br>
대표적인 자동차 기업들의 자주 묻는 질문(FAQ)을 제공하는 시스템

<br>

# 🫂 팀 소개
|구성|이름|담당|
|:---:|:---:|:---:|
|조장|한혜경|기획, 웹 화면 구성/개발(Streamlit), 문서|
|조원|신지윤|웹 화면 구성/개발(Streamlit)|
|조원|신희정|데이터 크롤링(FAQ)|
|조원|김민석|데이터 크롤링(연료별 자동차 등록수)|
|조원|양승호|ERD, 데이터 정제, 발표|

<br>

# 🛠 기술 스택
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white">
<img src="https://img.shields.io/badge/beautifulsoup-80F5D2?style=for-the-badge&logo=beautifulsoup&logoColor=white">
<img src="https://img.shields.io/badge/selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white">
<img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white">
<img src="https://img.shields.io/badge/streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">


<br>


# 📄 화면 설계서
분석 그래프 PAGE (연료별 자동차 등록대수, 연료별 비용 추이, 지역별 히트맵)
![화면설계서1](https://github.com/user-attachments/assets/f3609736-61f4-403c-ae38-0fa59ac854eb)
![화면설계서2](https://github.com/user-attachments/assets/2c6ab44a-f16c-4bcb-8a79-ebdb5a4e8eb3)


FAQ PAGE (브랜드별 FAQ)
![화면설계서3](https://github.com/user-attachments/assets/514ce548-ca51-4476-a1f4-8f9910daf7e0)



<br>


# 🔍 수집 데이터
유형별, 시간별 데이터 범위 설정
- 연료는 TOP3 유형인 휘발유, 경유, LPG 로 선정 (전기는 전기비용 추세를 추가로 찾아야 하는 관계로 제외)
- 시간은 데이터가 잘 쌓여있고 동등한 데이터 조건으로 비교할 수 있는 2020.01 ~ 2025.05 로 선정

[국토교통 통계누리](https://stat.molit.go.kr/portal/cate/statMetaView.do?hRsId=58)<br>
[한국석유공사](https://www.opinet.co.kr/user/main/mainView.do)<br>
[KIA FAQ](https://www.kia.com/kr/customer-service/center/faq)<br>
[GENESIS FAQ](https://www.genesis.com/kr/ko/support/faq.html)<br>
[BENZ FAQ](https://shop.mercedes-benz.com/ko-kr/connect/service/faq)<br>



<br>


# 📁 프로젝트 구조
```
SKN16-1st-5Team/
├── main.py                 # 메인 애플리케이션
├── requirements.txt        # Python 의존성 라이브러리
├── install_dependencies.bat # Windows 설치 스크립트
├── README.md              # 프로젝트 문서
├── .gitignore             # Git 제외 파일 설정
├── contents/              # 애플리케이션 모듈
│   ├── dashboard.py       # 대시보드 기능
│   └── faq.py             # FAQ 기능
└── docs/                  # 데이터 파일
    ├── benz_faq.csv
    ├── genesis_faq.csv
    ├── kia_faq.csv
    ├── 시도별_연료별_등록현황.xlsx
    ├── 유류비.csv
    └── 지역별 좌표.csv
```


<br>

# 💻 실제 화면
<b>실행 방법</b>
```
# 1. git clone
git clone https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN16-1st-5Team.git

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 애플리케이션 실행
streamlit run main.py
```
<br>

# 🖊 회고

>"AI 캠프에서 처음으로 진행한 팀 프로젝트라 기대도 많았지만 걱정도 컸습니다. 그래서 개인적으로도 미리 준비를 해봤는데, 다행히 팀원분들께서 잘 따라와 주셨습니다. 서로 잘 모르는 부분도 많았을 텐데, 팀원들끼리 적극적으로 질문하고 정보를 찾아보며 협력하는 모습이 인상적이었습니다. 또 각자 맡은 일을 빠르게 끝낸 뒤에는 어려움을 겪는 팀원을 도와주시는 등, 모두가 최선을 다해 프로젝트를 마무리해 주셔서 진심으로 감사했습니다." 

>"FAQ 화면  개발을 하는 과정에서 페이지 정보가 원하는 대로 정리가 되지 않아서 한참 헤매다가 해결했습니다. 비전공자여서 팀에 도움이 되지 못할까봐 걱정도 많이 했는데, 맡은 일을 만족스럽게 할 수 있어서 뿌듯했고 어디가 부족하고 얼만큼 아는지 파악할 수 있는 좋은 기회였습니다."

>데이터를 처음 수집할 때 자동차 연료 관련 생소한 단어가 있어서 헤맸습니다. 데이터를 정제하고 잘 수집하는 것의 중요성을 느꼈고 그 과정에서 팀원들과 소통하고 확인하는 게 큰 부분을 차지한다는 것을 배울 수 있었습니다. 수업 떄 배운 내용들을 하나씩 적용해볼 수 있어 유익한 시간이었습니다.

>"FAQ를 뽑는 과정에서 아래로 스크롤을 하지 않는 문제가 발생해서 해결하느라 시간이 꽤 걸렸습니다. OpenAPI key로 못 해본게 아쉽지만 웹사이트에서 정보얻는데는 크롤링으로 충분했고 좋은 경험이었습니다."

>"raw data에서 특정 데이터를 추출하여 dataframe에 정제하려는데 자꾸 NaN값이 들어와서 문제찾느라 힘들었습니다. index값이 잘 못 들어가 있어서 생긴 문제였습니다. 절대적인 시간이 모자라 아쉬웠습니다."
