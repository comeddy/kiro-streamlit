import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="주식 투자 Strands Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 메인 타이틀
st.title("📈 주식 투자 Strands Agent")
st.markdown("초보 투자자를 위한 AI 기반 투자 도우미")

# 사이드바 - 네비게이션
st.sidebar.title("메뉴")
menu_option = st.sidebar.selectbox(
    "원하는 기능을 선택하세요:",
    ["채팅", "주식 조회", "포트폴리오 분석", "투자 교육", "시장 동향"]
)

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 투자 상담 AI 응답 시스템
def get_investment_advice(user_input):
    """
    규칙 기반 투자 상담 응답 시스템
    초보자가 이해하기 쉬운 언어로 답변 제공
    """
    user_input_lower = user_input.lower()
    
    # 인사말 및 기본 응답
    if any(keyword in user_input_lower for keyword in ['안녕', '안녕하세요', '처음', '시작']):
        return """안녕하세요! 👋 주식 투자 Strands Agent입니다.
        
저는 초보 투자자분들이 주식 투자를 쉽게 이해할 수 있도록 도와드리는 AI 도우미예요.
        
다음과 같은 질문들을 해보세요:
• "주식이 뭐예요?"
• "투자를 어떻게 시작하나요?"
• "P/E 비율이 뭔가요?"
• "분산투자가 뭐예요?"
• "리스크가 뭔가요?"

궁금한 것이 있으시면 언제든 물어보세요! 😊"""

    # 주식 기본 개념
    elif any(keyword in user_input_lower for keyword in ['주식이 뭐', '주식이란', '주식 개념', '주식 정의']):
        return """📈 **주식이란?**

주식은 쉽게 말해 **회사의 일부분을 소유하는 증명서**예요!

🏢 **예를 들어:**
- 삼성전자 주식 1주를 사면 → 삼성전자 회사의 아주 작은 부분을 소유하게 됩니다
- 회사가 잘되면 → 주식 가격이 올라가요 📈
- 회사가 안 좋으면→ 주식 가격이 내려가요 📉

💰 **수익을 얻는 방법:**
1. **시세차익**: 싸게 사서 비싸게 팔기
2. **배당금**: 회사가 주는 보너스 (모든 회사가 주는 건 아니에요)

⚠️ **주의사항**: 주식은 원금 손실 위험이 있어요. 투자할 돈은 당장 쓸 일이 없는 여유자금으로 하세요!"""

    # 투자 시작 방법
    elif any(keyword in user_input_lower for keyword in ['투자 시작', '어떻게 시작', '처음 투자', '투자 방법']):
        return """🚀 **투자 시작하는 방법**

**1단계: 기본 지식 쌓기** 📚
- 주식, 채권, 펀드 등 기본 개념 이해하기
- 투자 관련 용어 익히기

**2단계: 투자 목표 정하기** 🎯
- 언제까지 투자할 건지 (1년? 10년?)
- 얼마나 수익을 원하는지
- 얼마나 위험을 감수할 수 있는지

**3단계: 증권계좌 개설** 🏦
- 증권회사에서 계좌 만들기
- 신분증과 은행계좌 필요해요

**4단계: 소액으로 시작** 💰
- 처음엔 잃어도 괜찮은 작은 금액으로
- 경험을 쌓으면서 점차 늘려가기

**5단계: 꾸준히 공부하기** 📖
- 투자는 평생 공부예요!

💡 **초보자 팁**: 한 번에 큰 돈을 투자하지 말고, 매달 일정 금액씩 나누어 투자하는 '적립식 투자'를 추천해요!"""

    # P/E 비율 설명
    elif any(keyword in user_input_lower for keyword in ['pe', 'p/e', '피이', '주가수익비율']):
        return """📊 **P/E 비율이란?**

P/E 비율은 **Price Earnings Ratio**의 줄임말로, **주가수익비율**이라고 해요.

🧮 **계산법:**
P/E 비율 = 주가 ÷ 주당순이익(EPS)

🍎 **쉬운 예시:**
- 사과 가게 주식이 10,000원
- 1년 동안 주식 1주당 1,000원의 이익을 냄
- P/E 비율 = 10,000 ÷ 1,000 = 10배

💡 **의미:**
- **P/E 10배** = 현재 주가로 10년 동안 벌어야 투자금을 회수
- **낮을수록** = 상대적으로 저평가 (싸다는 뜻)
- **높을수록** = 상대적으로 고평가 (비싸다는 뜻)

📏 **일반적인 기준:**
- 10배 이하: 저평가 가능성
- 15-20배: 적정 수준
- 25배 이상: 고평가 가능성

⚠️ **주의**: P/E만으로 판단하면 안 돼요! 다른 지표들도 함께 봐야 해요."""

    # 분산투자 설명
    elif any(keyword in user_input_lower for keyword in ['분산투자', '분산', '포트폴리오', '리스크 분산']):
        return """🥚 **분산투자란?**

"계란을 한 바구니에 담지 마라"는 말 들어보셨죠? 바로 분산투자의 핵심이에요!

🎯 **분산투자의 원리:**
- 여러 종목에 나누어 투자하기
- 한 종목이 떨어져도 다른 종목이 올라서 손실을 줄임

📊 **분산 방법들:**

**1. 종목 분산** 🏢
- 삼성전자, LG화학, 카카오 등 여러 회사에 투자

**2. 섹터 분산** 🏭
- IT, 바이오, 금융, 소비재 등 다양한 업종에 투자

**3. 지역 분산** 🌍
- 한국, 미국, 유럽 등 여러 나라에 투자

**4. 시간 분산** ⏰
- 한 번에 사지 말고 여러 번에 나누어 매수

💰 **초보자 추천:**
- 처음엔 3-5개 종목으로 시작
- ETF(상장지수펀드) 활용하면 자동으로 분산투자 효과!

✅ **장점**: 위험 감소, 안정적 수익
❌ **단점**: 큰 수익 기회 놓칠 수 있음"""

    # 리스크 설명
    elif any(keyword in user_input_lower for keyword in ['리스크', '위험', '손실', '위험도']):
        return """⚠️ **투자 리스크란?**

리스크는 **투자한 돈을 잃을 가능성**을 말해요.

📉 **주요 리스크 종류:**

**1. 시장 리스크** 📊
- 전체 시장이 떨어질 때 함께 떨어지는 위험
- 예: 경제 위기, 금리 인상 등

**2. 개별 기업 리스크** 🏢
- 특정 회사에만 생기는 문제
- 예: 경영진 문제, 제품 결함 등

**3. 유동성 리스크** 💧
- 팔고 싶을 때 못 파는 위험
- 거래량이 적은 종목에서 주로 발생

**4. 환율 리스크** 💱
- 해외 투자 시 환율 변동으로 인한 손실

🛡️ **리스크 관리 방법:**

**1. 분산투자** - 여러 종목에 나누어 투자
**2. 손절매** - 일정 손실 시 매도
**3. 여유자금 투자** - 당장 쓸 돈 말고 여유 돈으로
**4. 꾸준한 공부** - 지식이 최고의 방어책!

💡 **기억하세요**: 높은 수익 = 높은 위험! 자신의 위험 감수 능력을 정확히 파악하는 게 중요해요."""

    # 금융 용어 설명
    elif any(keyword in user_input_lower for keyword in ['시가총액', '시총']):
        return """💰 **시가총액이란?**

시가총액은 **회사의 전체 가치**를 나타내는 지표예요!

🧮 **계산법:**
시가총액 = 주가 × 발행주식수

🏢 **쉬운 예시:**
- 삼성전자 주가: 70,000원
- 발행주식수: 59억 주
- 시가총액: 70,000 × 59억 = 약 413조원

📏 **규모별 분류:**
- **대형주**: 2조원 이상
- **중형주**: 3,000억~2조원
- **소형주**: 3,000억원 미만

💡 **투자 의미:**
- 시총이 클수록 → 안정적이지만 성장성 제한적
- 시총이 작을수록 → 변동성 크지만 성장 가능성 높음

🌍 **글로벌 비교:**
- 애플: 약 3,000조원 (세계 1위)
- 삼성전자: 약 400조원 (한국 1위)"""

    elif any(keyword in user_input_lower for keyword in ['배당', '배당금']):
        return """💵 **배당금이란?**

배당금은 **회사가 주주들에게 나누어주는 이익**이에요!

🎁 **배당의 개념:**
- 회사가 돈을 벌면 → 그 이익의 일부를 주주들과 나눔
- 주식을 가지고 있으면 → 정기적으로 돈을 받을 수 있어요

📅 **배당 일정:**
- **배당 기준일**: 이 날 주식을 가지고 있어야 배당 받음
- **배당락일**: 배당 권리가 없어지는 날
- **배당 지급일**: 실제로 돈을 받는 날

💰 **배당수익률 계산:**
배당수익률 = (연간 배당금 ÷ 주가) × 100

📊 **예시:**
- 주가: 100,000원
- 연간 배당금: 3,000원
- 배당수익률: 3%

🏦 **배당주 투자 장점:**
- 정기적인 현금 수입
- 상대적으로 안정적
- 장기 투자에 적합

⚠️ **주의사항:**
- 배당금이 높다고 무조건 좋은 건 아니에요
- 회사 상황에 따라 배당이 줄거나 없어질 수 있어요"""

    # 일반적인 투자 조언
    elif any(keyword in user_input_lower for keyword in ['조언', '추천', '어떤 주식', '뭘 사야']):
        return """💡 **투자 조언**

죄송하지만 구체적인 종목 추천은 드릴 수 없어요. 대신 투자 원칙을 알려드릴게요!

🎯 **투자 기본 원칙:**

**1. 자신만의 투자 철학 만들기**
- 왜 이 주식을 사는지 명확한 이유 있기
- 감정이 아닌 논리로 판단하기

**2. 기업 분석하기**
- 회사가 뭘 하는지 이해하기
- 재무제표 기본은 알아두기
- 경쟁사와 비교해보기

**3. 장기 관점 갖기**
- 단기 등락에 일희일비하지 않기
- 최소 1년 이상 보유할 각오로 투자

**4. 꾸준히 공부하기**
- 투자는 평생 공부예요
- 경제 뉴스, 기업 실적 관심 갖기

**5. 위험 관리하기**
- 잃어도 괜찮은 돈으로만 투자
- 분산투자로 리스크 줄이기

⚠️ **투자 결정은 본인의 책임**이에요. 충분히 공부하고 신중하게 결정하세요!"""

    # 기타 질문들
    elif any(keyword in user_input_lower for keyword in ['etf', '펀드']):
        return """📦 **ETF란?**

ETF는 **Exchange Traded Fund**의 줄임말로, **상장지수펀드**라고 해요!

🎯 **ETF의 특징:**
- 여러 주식을 한 번에 살 수 있는 상품
- 주식처럼 실시간으로 거래 가능
- 자동으로 분산투자 효과

📊 **ETF 종류:**
- **KODEX 200**: 코스피 200 종목에 투자
- **TIGER 미국S&P500**: 미국 대형주 500개에 투자
- **섹터별 ETF**: IT, 바이오, 금융 등 특정 업종

💰 **장점:**
- 소액으로도 분산투자 가능
- 관리비용이 저렴
- 투명한 운용

❌ **단점:**
- 개별 종목 대비 큰 수익 어려움
- 추적 오차 발생 가능

💡 **초보자에게 추천하는 이유:**
개별 종목 선택이 어려운 초보자도 쉽게 분산투자할 수 있어요!"""

    # 모르는 질문에 대한 기본 응답
    else:
        return f"""죄송해요, '{user_input}'에 대한 구체적인 답변을 준비하지 못했어요. 😅

하지만 다음과 같은 주제들에 대해서는 도움을 드릴 수 있어요:

📚 **투자 기초:**
• "주식이 뭐예요?"
• "투자를 어떻게 시작하나요?"
• "분산투자가 뭐예요?"

📊 **투자 지표:**
• "P/E 비율이 뭔가요?"
• "시가총액이 뭐예요?"
• "배당금이 뭐예요?"

⚠️ **리스크 관리:**
• "리스크가 뭐예요?"
• "손실을 줄이는 방법은?"

💡 **투자 상품:**
• "ETF가 뭐예요?"
• "펀드와 주식의 차이는?"

궁금한 것이 있으시면 위의 주제들로 다시 질문해 주세요! 😊"""

def calculate_risk_score(risk_tolerance, investment_period, investment_experience):
    """
    사용자의 위험 성향, 투자 기간, 경험을 바탕으로 위험도 점수 계산
    """
    score = 0
    
    # 위험 성향 점수 (1-5)
    risk_scores = {
        "매우 보수적": 1,
        "보수적": 2, 
        "중립적": 3,
        "적극적": 4,
        "매우 적극적": 5
    }
    score += risk_scores.get(risk_tolerance, 3)
    
    # 투자 기간 점수 (장기일수록 위험 감수 가능)
    period_scores = {
        "1년 미만": 1,
        "1-3년": 2,
        "3-5년": 3, 
        "5-10년": 4,
        "10년 이상": 5
    }
    period_score = period_scores.get(investment_period, 3)
    
    # 투자 경험 점수
    experience_scores = {
        "완전 초보": 1,
        "기초 지식 보유": 2,
        "어느 정도 경험": 3,
        "상당한 경험": 4
    }
    experience_score = experience_scores.get(investment_experience, 2)
    
    # 가중 평균으로 최종 점수 계산 (위험성향 50%, 기간 30%, 경험 20%)
    final_score = round((score * 0.5 + period_score * 0.3 + experience_score * 0.2))
    final_score = max(1, min(5, final_score))  # 1-5 범위로 제한
    
    # 위험도 설명
    descriptions = {
        1: "매우 보수적 - 안전성을 최우선으로 하는 투자자",
        2: "보수적 - 안정적인 수익을 선호하는 투자자", 
        3: "중립적 - 적당한 위험과 수익을 추구하는 투자자",
        4: "적극적 - 높은 수익을 위해 위험을 감수하는 투자자",
        5: "매우 적극적 - 고위험 고수익을 추구하는 투자자"
    }
    
    return final_score, descriptions[final_score]

def generate_portfolio_advice(investment_goal, investment_period, investment_experience, 
                            risk_tolerance, investment_amount, monthly_investment):
    """
    사용자 프로필을 바탕으로 개인화된 포트폴리오 조언 생성
    """
    risk_score, _ = calculate_risk_score(risk_tolerance, investment_period, investment_experience)
    
    # 위험도별 기본 포트폴리오 구성
    if risk_score == 1:  # 매우 보수적
        portfolio = {
            "예금/적금": 40,
            "국채/회사채": 30,
            "배당주": 20,
            "안정형 펀드": 10
        }
        explanation = """
        **매우 보수적인 포트폴리오**
        
        안전성을 최우선으로 하는 구성입니다. 원금 보장이 되는 예금과 채권의 비중을 높였고, 
        주식은 배당을 꾸준히 주는 안정적인 기업들로 구성했습니다.
        
        • 예상 연 수익률: 3-5%
        • 변동성: 매우 낮음
        • 원금 손실 위험: 매우 낮음
        """
        
        investment_methods = [
            "CMA나 MMF 같은 단기 금융상품 활용",
            "국고채, 회사채 ETF 투자",
            "통신주, 유틸리티주 등 배당주 투자",
            "목표전환형 펀드나 TDF 활용"
        ]
        
        risk_warning = ""
        alternatives = []
        
    elif risk_score == 2:  # 보수적
        portfolio = {
            "예금/채권": 30,
            "배당주": 25,
            "대형주": 25,
            "안정형 펀드": 15,
            "리츠": 5
        }
        explanation = """
        **보수적인 포트폴리오**
        
        안정성을 중시하면서도 적당한 성장을 추구하는 구성입니다. 
        대형주와 배당주 중심으로 구성하여 변동성을 줄였습니다.
        
        • 예상 연 수익률: 4-7%
        • 변동성: 낮음
        • 원금 손실 위험: 낮음
        """
        
        investment_methods = [
            "KODEX 200, TIGER 200 같은 대형주 ETF",
            "배당주 ETF나 개별 배당주 투자",
            "리츠 ETF로 부동산 간접 투자",
            "혼합형 펀드 활용"
        ]
        
        risk_warning = ""
        alternatives = []
        
    elif risk_score == 3:  # 중립적
        portfolio = {
            "대형주": 30,
            "중소형주": 20,
            "해외주식": 20,
            "채권": 15,
            "섹터 ETF": 10,
            "현금": 5
        }
        explanation = """
        **균형잡힌 포트폴리오**
        
        안정성과 성장성의 균형을 맞춘 구성입니다. 
        국내외 주식에 분산투자하고 채권으로 안정성을 확보했습니다.
        
        • 예상 연 수익률: 6-9%
        • 변동성: 보통
        • 원금 손실 위험: 보통
        """
        
        investment_methods = [
            "코스피 200 ETF + 코스닥 150 ETF 조합",
            "S&P 500 ETF로 미국 시장 투자",
            "섹터별 ETF로 테마 투자",
            "채권 ETF로 안정성 확보"
        ]
        
        risk_warning = ""
        alternatives = []
        
    elif risk_score == 4:  # 적극적
        portfolio = {
            "대형주": 25,
            "중소형주": 25,
            "해외주식": 25,
            "성장주": 15,
            "섹터 ETF": 10
        }
        explanation = """
        **성장 중심 포트폴리오**
        
        높은 성장을 추구하는 구성입니다. 
        중소형주와 성장주의 비중을 높여 수익 기회를 확대했습니다.
        
        • 예상 연 수익률: 8-12%
        • 변동성: 높음
        • 원금 손실 위험: 높음
        """
        
        investment_methods = [
            "코스닥 ETF로 중소형주 투자",
            "나스닥 ETF로 미국 성장주 투자",
            "테마 ETF (AI, 바이오, 2차전지 등)",
            "개별 성장주 직접 투자"
        ]
        
        risk_warning = """
        **⚠️ 고위험 투자 경고**
        
        선택하신 포트폴리오는 높은 변동성을 가지고 있습니다:
        • 단기간에 20-30% 이상 손실 가능
        • 시장 상황에 따라 큰 폭의 등락 반복
        • 투자 원금의 상당 부분을 잃을 수 있음
        • 심리적 스트레스가 클 수 있음
        """
        
        alternatives = [
            "채권 비중을 10-20% 추가하여 안정성 확보",
            "적립식 투자로 시간 분산 효과 활용", 
            "처음엔 보수적으로 시작해서 경험 쌓은 후 확대",
            "투자 금액을 줄이고 여유자금으로만 투자"
        ]
        
    else:  # 매우 적극적 (5점)
        portfolio = {
            "중소형주": 30,
            "해외주식": 25,
            "성장주": 20,
            "테마주": 15,
            "개별주식": 10
        }
        explanation = """
        **고위험 고수익 포트폴리오**
        
        최대 수익을 추구하는 공격적인 구성입니다. 
        변동성이 큰 중소형주와 성장주 중심으로 구성했습니다.
        
        • 예상 연 수익률: 10-15% (또는 큰 손실)
        • 변동성: 매우 높음
        • 원금 손실 위험: 매우 높음
        """
        
        investment_methods = [
            "개별 중소형 성장주 직접 투자",
            "신흥국 ETF, 테마 ETF 투자",
            "IPO, 공모주 투자 참여",
            "옵션, 선물 등 파생상품 활용"
        ]
        
        risk_warning = """
        **🚨 매우 고위험 투자 경고**
        
        선택하신 포트폴리오는 매우 높은 위험을 수반합니다:
        • 단기간에 50% 이상 손실 가능
        • 투자 원금 전액 손실 위험
        • 극심한 변동성으로 인한 스트레스
        • 전문적 지식과 경험 필요
        • 지속적인 모니터링 필수
        """
        
        alternatives = [
            "전체 자산의 10-20%만 고위험 투자에 배분",
            "안정적인 포트폴리오와 병행 운용",
            "충분한 투자 공부 후 단계적 확대",
            "전문가 상담 후 투자 결정",
            "모의투자로 충분한 경험 축적 후 실전 투자"
        ]
    
    # 투자 목표별 추가 조언
    goal_advice = {
        "자산 증식": "장기적 관점에서 꾸준한 적립식 투자를 추천합니다.",
        "노후 준비": "안정성을 중시하되, 인플레이션을 고려한 적절한 성장성도 필요합니다.",
        "단기 수익": "단기 투자는 위험이 높으니 여유자금으로만 하시기 바랍니다.",
        "안정적 수입": "배당주나 리츠 등 정기적 수입이 있는 상품을 고려해보세요.",
        "자녀 교육비": "목표 시점을 고려하여 점진적으로 안전 자산 비중을 늘려가세요."
    }
    
    # 분산투자 설명
    diversification_explanation = """
    **분산투자가 중요한 이유:**
    
    • **섹터 분산**: IT가 어려울 때 금융이나 소비재가 좋을 수 있어요
    • **지역 분산**: 한국 경제가 어려울 때 미국이나 유럽이 좋을 수 있어요  
    • **시간 분산**: 매월 일정 금액씩 투자하면 평균 매입 단가를 낮출 수 있어요
    • **자산 분산**: 주식, 채권, 부동산 등 다양한 자산에 투자하면 위험을 줄일 수 있어요
    
    "계란을 한 바구니에 담지 마라"는 투자의 기본 원칙입니다!
    """
    
    # 포트폴리오 관리 팁
    management_tips = [
        "3-6개월마다 포트폴리오 비중을 점검하고 리밸런싱하세요",
        "시장 상황이 크게 변할 때는 전략을 재검토하세요",
        "감정적 판단보다는 미리 정한 원칙을 따르세요",
        "투자 일기를 써서 자신의 투자 패턴을 파악하세요",
        "정기적으로 투자 목표와 현재 상황을 점검하세요",
        f"투자 목표 '{investment_goal}'에 맞게 전략을 조정하세요"
    ]
    
    return {
        "portfolio": portfolio,
        "explanation": explanation + f"\n\n**투자 목표 고려사항:** {goal_advice.get(investment_goal, '')}",
        "investment_methods": investment_methods,
        "risk_warning": risk_warning,
        "alternatives": alternatives,
        "diversification_explanation": diversification_explanation,
        "management_tips": management_tips
    }

# 메인 컨텐츠 영역
if menu_option == "채팅":
    st.header("💬 AI 투자 상담")
    st.markdown("궁금한 것이 있으시면 언제든 물어보세요! 초보자도 쉽게 이해할 수 있도록 설명해드릴게요. 😊")
    
    # 자주 묻는 질문 버튼들
    st.markdown("**💡 자주 묻는 질문들:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("주식이 뭐예요?"):
            st.session_state.chat_history.append({"role": "user", "content": "주식이 뭐예요?"})
            response = get_investment_advice("주식이 뭐예요?")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("투자 어떻게 시작하나요?"):
            st.session_state.chat_history.append({"role": "user", "content": "투자를 어떻게 시작하나요?"})
            response = get_investment_advice("투자를 어떻게 시작하나요?")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("P/E 비율이 뭔가요?"):
            st.session_state.chat_history.append({"role": "user", "content": "P/E 비율이 뭔가요?"})
            response = get_investment_advice("P/E 비율이 뭔가요?")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown("---")
    
    # 채팅 히스토리 표시
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # 사용자 입력
    if prompt := st.chat_input("투자에 대해 궁금한 것을 물어보세요..."):
        # 사용자 메시지 추가
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI 응답 생성
        response = get_investment_advice(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # 페이지 새로고침하여 버튼 상태 초기화
        st.rerun()

elif menu_option == "주식 조회":
    st.header("📊 주식 정보 조회")
    st.markdown("관심 있는 주식의 기본 정보를 확인해보세요.")
    
    # 주식 티커 입력
    ticker = st.text_input("주식 티커를 입력하세요 (예: AAPL, MSFT, 005930.KS):")
    
    if ticker:
        try:
            # yfinance로 주식 데이터 조회
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            hist = stock.history(period="1y")
            
            if not info or 'regularMarketPrice' not in info:
                st.error("유효하지 않은 티커입니다. 다시 확인해주세요.")
            else:
                # 기본 정보 표시
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"{info.get('longName', ticker)} ({ticker.upper()})")
                    
                    # 현재 주가 정보
                    current_price = info.get('regularMarketPrice', info.get('currentPrice', 0))
                    previous_close = info.get('regularMarketPreviousClose', info.get('previousClose', 0))
                    
                    if current_price and previous_close:
                        price_change = current_price - previous_close
                        price_change_percent = (price_change / previous_close) * 100
                        
                        # 가격 변동에 따른 색상 설정
                        color = "green" if price_change >= 0 else "red"
                        arrow = "▲" if price_change >= 0 else "▼"
                        
                        st.metric(
                            label="현재 주가",
                            value=f"${current_price:.2f}",
                            delta=f"{arrow} ${abs(price_change):.2f} ({price_change_percent:+.2f}%)"
                        )
                    
                    # 기본 지표들
                    st.write("**기본 정보**")
                    
                    # 52주 최고/최저가
                    week_52_high = info.get('fiftyTwoWeekHigh', 'N/A')
                    week_52_low = info.get('fiftyTwoWeekLow', 'N/A')
                    if week_52_high != 'N/A' and week_52_low != 'N/A':
                        st.write(f"• 52주 최고가: ${week_52_high:.2f}")
                        st.write(f"• 52주 최저가: ${week_52_low:.2f}")
                    
                    # 시가총액
                    market_cap = info.get('marketCap')
                    if market_cap:
                        if market_cap >= 1e12:
                            market_cap_str = f"${market_cap/1e12:.2f}T"
                        elif market_cap >= 1e9:
                            market_cap_str = f"${market_cap/1e9:.2f}B"
                        elif market_cap >= 1e6:
                            market_cap_str = f"${market_cap/1e6:.2f}M"
                        else:
                            market_cap_str = f"${market_cap:,.0f}"
                        st.write(f"• 시가총액: {market_cap_str}")
                    
                    # P/E 비율
                    pe_ratio = info.get('trailingPE')
                    if pe_ratio:
                        st.write(f"• P/E 비율: {pe_ratio:.2f}")
                    
                    # 거래량
                    volume = info.get('regularMarketVolume', info.get('volume'))
                    if volume:
                        st.write(f"• 거래량: {volume:,}")
                
                with col2:
                    # 주가 차트 (최근 1년)
                    if not hist.empty:
                        st.subheader("주가 차트 (1년)")
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=hist.index,
                            y=hist['Close'],
                            mode='lines',
                            name='종가',
                            line=dict(color='blue', width=2)
                        ))
                        
                        fig.update_layout(
                            title=f"{ticker.upper()} 주가 추이",
                            xaxis_title="날짜",
                            yaxis_title="주가 ($)",
                            height=400,
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                # 추가 정보
                st.subheader("회사 정보")
                
                # 섹터 및 산업
                sector = info.get('sector', 'N/A')
                industry = info.get('industry', 'N/A')
                if sector != 'N/A' or industry != 'N/A':
                    col3, col4 = st.columns(2)
                    with col3:
                        st.write(f"**섹터:** {sector}")
                    with col4:
                        st.write(f"**산업:** {industry}")
                
                # 회사 설명
                business_summary = info.get('longBusinessSummary', '')
                if business_summary:
                    st.write("**회사 개요:**")
                    # 설명이 너무 길면 일부만 표시
                    if len(business_summary) > 500:
                        st.write(business_summary[:500] + "...")
                    else:
                        st.write(business_summary)
                
                # 초보자를 위한 간단한 분석 코멘트
                st.subheader("💡 초보자를 위한 간단 분석")
                
                analysis_comments = []
                
                # P/E 비율 분석
                if pe_ratio:
                    if pe_ratio < 15:
                        analysis_comments.append("• P/E 비율이 낮아 상대적으로 저평가되어 보입니다.")
                    elif pe_ratio > 25:
                        analysis_comments.append("• P/E 비율이 높아 성장 기대가 반영되어 있거나 고평가되어 보입니다.")
                    else:
                        analysis_comments.append("• P/E 비율이 적정 수준입니다.")
                
                # 52주 고점/저점 대비 현재 위치
                if week_52_high != 'N/A' and week_52_low != 'N/A' and current_price:
                    position_in_range = (current_price - week_52_low) / (week_52_high - week_52_low)
                    if position_in_range > 0.8:
                        analysis_comments.append("• 현재 주가가 52주 고점 근처에 있습니다.")
                    elif position_in_range < 0.2:
                        analysis_comments.append("• 현재 주가가 52주 저점 근처에 있습니다.")
                    else:
                        analysis_comments.append("• 현재 주가가 52주 범위의 중간 정도에 위치합니다.")
                
                if analysis_comments:
                    for comment in analysis_comments:
                        st.write(comment)
                else:
                    st.write("분석을 위한 충분한 데이터가 없습니다.")
                
                st.warning("⚠️ 이 분석은 참고용이며, 투자 결정은 신중하게 하시기 바랍니다.")
                
        except Exception as e:
            st.error(f"주식 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
            st.info("티커 형식을 확인해주세요. 미국 주식은 'AAPL', 한국 주식은 '005930.KS' 형태로 입력하세요.")

elif menu_option == "포트폴리오 분석":
    st.header("📈 포트폴리오 분석")
    st.markdown("개인화된 투자 포트폴리오 조언을 받아보세요.")
    
    # 사용자 프로필 입력 섹션
    st.subheader("👤 투자자 프로필")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 투자 목표
        investment_goal = st.selectbox(
            "투자 목표를 선택하세요:",
            ["자산 증식", "노후 준비", "단기 수익", "안정적 수입", "자녀 교육비"]
        )
        
        # 투자 기간
        investment_period = st.selectbox(
            "투자 기간을 선택하세요:",
            ["1년 미만", "1-3년", "3-5년", "5-10년", "10년 이상"]
        )
        
        # 투자 경험
        investment_experience = st.selectbox(
            "투자 경험을 선택하세요:",
            ["완전 초보", "기초 지식 보유", "어느 정도 경험", "상당한 경험"]
        )
    
    with col2:
        # 위험 성향
        risk_tolerance = st.selectbox(
            "위험 성향을 선택하세요:",
            ["매우 보수적", "보수적", "중립적", "적극적", "매우 적극적"]
        )
        
        # 투자 가능 금액
        investment_amount = st.selectbox(
            "투자 가능 금액을 선택하세요:",
            ["100만원 미만", "100-500만원", "500-1000만원", "1000-5000만원", "5000만원 이상"]
        )
        
        # 월 추가 투자 가능 금액
        monthly_investment = st.selectbox(
            "월 추가 투자 가능 금액:",
            ["없음", "10만원 미만", "10-30만원", "30-50만원", "50만원 이상"]
        )
    
    # 포트폴리오 조언 생성 버튼
    if st.button("💡 개인화된 포트폴리오 조언 받기", type="primary"):
        # 포트폴리오 조언 생성
        advice = generate_portfolio_advice(
            investment_goal, investment_period, investment_experience,
            risk_tolerance, investment_amount, monthly_investment
        )
        
        st.markdown("---")
        st.subheader("🎯 맞춤형 포트폴리오 조언")
        
        # 위험도 평가
        st.markdown("### 📊 위험도 평가")
        risk_score, risk_description = calculate_risk_score(risk_tolerance, investment_period, investment_experience)
        
        # 위험도에 따른 색상 설정
        if risk_score <= 2:
            risk_color = "green"
        elif risk_score <= 3:
            risk_color = "orange"
        else:
            risk_color = "red"
        
        st.markdown(f"**위험도 점수:** :{risk_color}[{risk_score}/5] - {risk_description}")
        
        # 추천 포트폴리오
        st.markdown("### 💼 추천 포트폴리오 구성")
        
        portfolio = advice["portfolio"]
        
        # 포트폴리오 비중을 차트로 표시
        import plotly.express as px
        
        labels = list(portfolio.keys())
        values = list(portfolio.values())
        
        fig = px.pie(
            values=values, 
            names=labels, 
            title="추천 포트폴리오 구성",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 포트폴리오 설명
        st.markdown("### 📝 포트폴리오 설명")
        st.write(advice["explanation"])
        
        # 구체적인 투자 방법
        st.markdown("### 🛠️ 구체적인 투자 방법")
        for method in advice["investment_methods"]:
            st.write(f"• {method}")
        
        # 위험 경고 및 주의사항
        if risk_score >= 4:
            st.markdown("### ⚠️ 고위험 투자 경고")
            st.error(advice["risk_warning"])
            
            st.markdown("**대안 제시:**")
            for alternative in advice["alternatives"]:
                st.write(f"• {alternative}")
        
        # 분산투자 중요성 설명
        st.markdown("### 🌐 분산투자의 중요성")
        st.info(advice["diversification_explanation"])
        
        # 정기적인 리밸런싱 안내
        st.markdown("### 🔄 포트폴리오 관리 팁")
        for tip in advice["management_tips"]:
            st.write(f"• {tip}")
    
    # 분산투자 교육 섹션
    st.markdown("---")
    st.subheader("📚 분산투자 가이드")
    
    tab1, tab2, tab3 = st.tabs(["섹터별 분산", "지역별 분산", "시간 분산"])
    
    with tab1:
        st.markdown("""
        ### 🏭 섹터별 분산투자
        
        **왜 섹터를 나누어 투자해야 할까요?**
        
        각 산업은 서로 다른 경제 사이클을 가지고 있어요. 한 섹터가 어려울 때 다른 섹터가 좋을 수 있습니다.
        
        **주요 섹터들:**
        
        🏢 **기술(IT)**: 삼성전자, 네이버, 카카오
        - 성장성 높지만 변동성도 큼
        - 미래 트렌드에 민감
        
        🏦 **금융**: 국민은행, 삼성생명, 메리츠증권  
        - 금리 변동에 민감
        - 경기 사이클과 연관성 높음
        
        🏭 **제조업**: 현대차, LG화학, 포스코
        - 원자재 가격에 영향 받음
        - 글로벌 경기와 연관
        
        🛒 **소비재**: 아모레퍼시픽, 롯데, CJ제일제당
        - 상대적으로 안정적
        - 내수 경기와 연관
        
        ⚡ **에너지/유틸리티**: 한국전력, SK이노베이션
        - 필수재로 안정적
        - 정부 정책에 민감
        """)
    
    with tab2:
        st.markdown("""
        ### 🌍 지역별 분산투자
        
        **왜 여러 나라에 투자해야 할까요?**
        
        각 나라는 서로 다른 경제 상황을 가지고 있어요. 한국이 어려울 때 다른 나라는 좋을 수 있습니다.
        
        **지역별 특징:**
        
        🇰🇷 **한국 (30-50%)**
        - 내가 잘 아는 기업들
        - 정보 접근이 쉬움
        - 환율 리스크 없음
        
        🇺🇸 **미국 (20-40%)**
        - 세계 최대 경제 규모
        - 글로벌 기업들 (애플, 구글, 아마존)
        - 달러 강세 시 유리
        
        🇪🇺 **유럽 (10-20%)**
        - 안정적인 경제
        - 명품, 자동차 등 강한 산업
        - 유로화 분산 효과
        
        🌏 **신흥국 (5-15%)**
        - 높은 성장 가능성
        - 높은 변동성
        - 장기 투자 관점 필요
        
        **💡 초보자 팁:**
        - 처음엔 한국 70%, 미국 30%로 시작
        - 경험이 쌓이면 점차 다양화
        - ETF 활용하면 쉽게 분산 가능
        """)
    
    with tab3:
        st.markdown("""
        ### ⏰ 시간 분산투자 (적립식 투자)
        
        **시간을 나누어 투자하는 이유:**
        
        주식 시장은 언제 오르고 내릴지 예측하기 어려워요. 시간을 나누어 투자하면 평균 매입 단가를 낮출 수 있습니다.
        
        **적립식 투자의 장점:**
        
        📈 **평균 매입 단가 효과**
        - 주가가 높을 때: 적게 매수
        - 주가가 낮을 때: 많이 매수
        - 결과적으로 평균 단가 하락
        
        💰 **부담 없는 투자**
        - 매월 일정 금액만 투자
        - 큰 돈이 없어도 시작 가능
        - 투자 습관 형성
        
        😌 **심리적 안정감**
        - 시장 타이밍 고민 불필요
        - 단기 변동성에 덜 민감
        - 장기 관점 유지 가능
        
        **적립식 투자 예시:**
        
        ```
        매월 50만원씩 1년간 투자하는 경우:
        
        1월: 주가 100원 → 5,000주 매수
        2월: 주가 80원 → 6,250주 매수  
        3월: 주가 120원 → 4,167주 매수
        ...
        
        평균 매입 단가: 약 95원
        (한 번에 투자했다면 100원)
        ```
        
        **💡 실천 방법:**
        - 증권사 자동 적립 서비스 이용
        - 매월 일정일에 자동 매수 설정
        - 최소 1년 이상 꾸준히 지속
        """)
    
    # 면책 조항
    st.markdown("---")
    st.warning("""
    ⚠️ **투자 유의사항**
    
    • 본 조언은 일반적인 가이드라인이며, 개인의 구체적인 상황을 모두 반영하지 못할 수 있습니다.
    • 투자 결정은 충분한 검토 후 본인 책임하에 이루어져야 합니다.
    • 과거 수익률이 미래 수익률을 보장하지 않습니다.
    • 투자에는 원금 손실의 위험이 있습니다.
    """)

elif menu_option == "투자 교육":
    st.header("📚 투자 교육")
    st.markdown("투자 기초부터 차근차근 배워보세요.")
    st.info("투자 교육 콘텐츠는 다음 단계에서 구현됩니다.")

elif menu_option == "시장 동향":
    st.header("🌍 시장 동향")
    st.markdown("현재 시장 상황과 주요 뉴스를 확인해보세요.")
    st.info("시장 동향 기능은 다음 단계에서 구현됩니다.")

# 푸터
st.markdown("---")
st.markdown(
    """
    **⚠️ 투자 유의사항**
    
    본 서비스에서 제공하는 정보는 투자 참고용이며, 투자 결정에 대한 책임은 투자자 본인에게 있습니다.
    투자에는 원금 손실의 위험이 있으니 신중하게 결정하시기 바랍니다.
    """
)