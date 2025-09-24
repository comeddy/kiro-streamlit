# 기술 스택 및 빌드 시스템

## 핵심 기술

### 프론트엔드 및 프레임워크
- **Streamlit 1.28.1**: 인터랙티브 UI를 위한 메인 웹 프레임워크
- **Plotly 5.17.0**: 인터랙티브 차트 및 데이터 시각화

### 데이터 및 API
- **yfinance 0.2.18**: Yahoo Finance에서 실시간 주식 데이터 조회
- **pandas 2.0.3**: 데이터 조작 및 분석
- **numpy 1.24.3**: 수치 계산
- **requests 2.31.0**: 외부 API HTTP 요청

### 언어 및 런타임
- **Python 3.8+**: 주요 프로그래밍 언어
- **가상환경**: 의존성 격리를 위한 `.venv`

## 프로젝트 구조

```
stock-investment-strands-agent/
├── app.py                 # 메인 Streamlit 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── .venv/                # 가상환경
└── .kiro/                # Kiro IDE 설정
    └── specs/            # 프로젝트 명세서
```

## 주요 명령어

### 개발 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 애플리케이션 실행
```bash
# 개발 서버 시작
streamlit run app.py

# http://localhost:8501 에서 접속
```

### 개발 워크플로우
```bash
# 새 패키지 설치
pip install package_name
pip freeze > requirements.txt

# 자동 리로드로 실행 (Streamlit 기본값)
streamlit run app.py --server.runOnSave true
```

## 아키텍처 패턴

### 단일 파일 애플리케이션
- 단순함을 위해 모든 기능을 `app.py`에 구현
- 단일 파일 내에서 함수 기반 구조화
- 채팅 기록을 위한 세션 상태 관리

### 규칙 기반 AI 시스템
- 사용자 입력 분류를 위한 패턴 매칭
- 한국어로 미리 정의된 응답 템플릿
- 외부 AI API 없이 자체 포함된 로직

### 데이터 플로우
1. 사용자 입력 → 의도 분류 → 응답 생성
2. 주식 조회 → yfinance API → 데이터 처리 → 시각화
3. 포트폴리오 분석 → 위험도 계산 → 개인화된 추천

## 코드 스타일 가이드라인

### 한국어 지원
- 모든 사용자 대면 텍스트는 한국어
- 함수명과 주석은 영어
- 변수명은 영어로 명확하게 작성

### Streamlit 규칙
- 지속적인 데이터를 위해 `st.session_state` 사용
- 컬럼과 컨테이너로 UI 구성
- API 호출에 대한 적절한 오류 처리 구현

### 오류 처리
- API 실패 시 우아한 성능 저하
- 한국어로 사용자 친화적인 오류 메시지
- 주식 티커 및 사용자 데이터에 대한 입력 검증