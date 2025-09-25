# 📈 주식 투자 Strands Agent

초보 투자자를 위한 AI 기반 투자 도우미 웹 애플리케이션입니다. [Kiro AI tool](https://kiro.dev/)을 통해 개발된 어플리케이션으로, Streamlit을 기반으로 구축되어 직관적이고 사용하기 쉬운 인터페이스를 제공합니다. 

## 🌟 주요 기능

### 💬 AI 투자 상담
- 규칙 기반 투자 상담 시스템
- 초보자도 이해하기 쉬운 친근한 언어로 설명
- 투자 기초 개념부터 고급 전략까지 질의응답
- 실시간 채팅 인터페이스

### 📊 주식 정보 조회
- 실시간 주식 데이터 조회 (yfinance API 활용)
- 주가 차트 및 기술적 지표 표시
- 기업 기본 정보 및 재무 지표
- 초보자를 위한 간단한 분석 코멘트

### 📈 포트폴리오 분석
- 개인화된 투자 성향 분석
- 연령별, 위험도별 맞춤 포트폴리오 추천
- 분산투자 전략 가이드
- 리밸런싱 및 리스크 관리 조언

### 📚 투자 교육
- 3단계 체계적 학습 시스템 (기초/중급/고급)
- 실제 사례와 예시를 통한 설명
- 학습 진도 추적 및 완료 시스템
- 투자 지식 퀴즈 및 추가 학습 자료 추천

### 🌍 시장 동향
- 주요 시장 지수 및 동향 분석 (개발 예정)
- 경제 뉴스 및 이슈 정리 (개발 예정)

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Stock Data**: yfinance
- **Data Processing**: Pandas, NumPy
- **Language**: Python 3.8+

## 📋 요구사항

- Python 3.8 이상
- 인터넷 연결 (주식 데이터 조회용)

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. 가상환경 생성 및 활성화
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source .venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
streamlit run app.py
```

### 5. 브라우저에서 접속
애플리케이션이 실행되면 자동으로 브라우저가 열리거나, 다음 주소로 접속하세요:
```
http://localhost:8501
```

## 📦 의존성 패키지

```
streamlit==1.28.1
yfinance==0.2.18
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
requests==2.31.0
```

## 🎯 사용법

### 기본 사용법
1. 사이드바에서 원하는 기능을 선택합니다
2. 각 메뉴별로 제공되는 기능을 활용합니다

### 채팅 기능
- 투자 관련 질문을 자유롭게 입력하세요
- 자주 묻는 질문 버튼을 클릭하여 빠른 답변을 받을 수 있습니다
- 예시 질문:
  - "주식이 뭐예요?"
  - "투자를 어떻게 시작하나요?"
  - "P/E 비율이 뭔가요?"

### 주식 조회
- 주식 티커를 입력하여 실시간 정보를 확인하세요
- 한국 주식: `005930.KS` (삼성전자)
- 미국 주식: `AAPL` (애플)

### 포트폴리오 분석
- 개인 정보를 입력하여 맞춤형 포트폴리오 추천을 받으세요
- 투자 목표, 기간, 위험 성향 등을 고려한 분석 제공

### 투자 교육
- 기초부터 고급까지 단계별 학습
- 각 주제별 학습 완료 체크
- 퀴즈를 통한 학습 효과 확인

## 🏗️ 프로젝트 구조

```
stock-investment-strands-agent/
├── app.py                 # 메인 애플리케이션 파일
├── requirements.txt       # 의존성 패키지 목록
├── README.md             # 프로젝트 설명서
├── .venv/                # 가상환경 (생성 후)
└── .kiro/                # Kiro IDE 설정 파일들
    └── specs/            # 프로젝트 스펙 문서들
```

## 🔧 주요 함수 설명

### `get_investment_advice(user_input)`
- 사용자 입력에 대한 투자 상담 응답 생성
- 규칙 기반 패턴 매칭으로 적절한 답변 제공
- 초보자 친화적인 언어와 예시 포함

### `calculate_risk_score(risk_tolerance, investment_period, investment_experience)`
- 사용자의 위험 성향 점수 계산
- 투자 기간, 경험, 성향을 종합적으로 고려
- 1-5점 척도로 위험도 평가

### `generate_portfolio_advice(...)`
- 개인화된 포트폴리오 조언 생성
- 위험도별 자산 배분 추천
- 구체적인 투자 방법 및 주의사항 제공

## 🎨 UI/UX 특징

- **직관적인 네비게이션**: 사이드바 메뉴로 쉬운 기능 전환
- **반응형 디자인**: 다양한 화면 크기에 최적화
- **시각적 데이터**: Plotly를 활용한 인터랙티브 차트
- **진행률 표시**: 학습 진도 및 완료 상태 시각화
- **색상 코딩**: 상승/하락, 위험도별 색상 구분

## ⚠️ 주의사항

- 본 애플리케이션에서 제공하는 정보는 **교육 및 참고용**입니다
- 실제 투자 결정은 충분한 검토 후 본인 책임하에 이루어져야 합니다
- 과거 수익률이 미래 수익률을 보장하지 않습니다
- 투자에는 원금 손실의 위험이 있습니다

## 🔮 향후 개발 계획

- [ ] 실시간 시장 동향 분석 기능
- [ ] 더 많은 기술적 지표 추가
- [ ] 백테스팅 기능
- [ ] 사용자 포트폴리오 저장 기능
- [ ] 알림 및 리포트 기능
- [ ] 다국어 지원

## 🤝 기여하기

프로젝트 개선에 기여하고 싶으시다면:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 문의

프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해 주세요.

---

**Made with ❤️ for beginner investors**