# Not_GPT - AI Detection Bypass System 🎯

> AI가 생성한 텍스트를 인간이 작성한 것처럼 자연스럽게 변환하는 웹 애플리케이션

AI 탐지 시스템이 감지하기 어려운 형태로 텍스트를 변환하는 웹 기반 시스템입니다. **Neo-Brutalism Design System**을 적용하여 강렬하고 직관적인 사용자 경험을 제공합니다.

---

## 📋 목차

- [개요](#개요)
- [🎨 Neo-Brutalism 디자인](#-neo-brutalism-디자인)
- [시스템 아키텍처](#시스템-아키텍처)
- [기술 스택](#기술-스택)
- [🔐 보안 및 인증](#-보안-및-인증)
- [프로젝트 구조](#프로젝트-구조)
- [탐지 우회 원리](#탐지-우회-원리)
- [🛠️ 로컬 개발 환경 설정](#️-로컬-개발-환경-설정)
- [🌐 Vercel 배포 가이드](#-vercel-배포-가이드)
- [API 문서](#api-문서)
- [변환 모듈 상세](#변환-모듈-상세)
- [문제 해결](#-문제-해결)

---

## 개요

### 배경

현대의 AI 탐지 시스템은 다음과 같은 지표를 분석합니다:

| 탐지 지표 | 설명 |
|----------|------|
| **N-gram 유사도** | 문장/구 단위 패턴 매칭 |
| **퍼플렉시티 (Perplexity)** | 텍스트의 예측 가능성 측정 |
| **Burstiness** | 단어 사용 분포의 균일성 |
| **문장 길이 분포** | AI는 균일한 길이, 인간은 불균일 |
| **어휘 다양성** | Type-Token Ratio |

### 목표

Not_GPT는 이러한 탐지 지표를 역으로 공략하여:
- N-gram 패턴을 파괴
- 퍼플렉시티를 증가
- 문장 길이를 불균일화
- 어휘 다양성을 확대

---

## 🎨 Neo-Brutalism 디자인

이 프로젝트는 **Neo-Brutalism (네오 부루탈리즘)** 디자인 철학을 채택했습니다.

### 디자인 특징

#### 시각적 요소
- **굵은 검정 테두리** (4-8px): 모든 요소를 명확하게 구분
- **단단한 그림자** (블러 없음): 입체감과 시각적 깊이
- **밝은 대비 색상**: 높은 가독성과 주목도
- **기하학적 형태**: 직선적이고 구조적인 레이아웃

#### 타이포그래피
- **Space Grotesk**: 기하학적이고 대담한 메인 폰트
- **Pretendard**: 한국어 최적화 폰트
- **대담한 굵기**: 700-800 font-weight로 강한 인상

### 컬러 팔레트

```css
/* Neo-Brutalism Colors */
:root {
  --primary-bg: #FFFFFF;        /* 배경 - 순백 */
  --primary-text: #000000;      /* 텍스트 - 순흑 */
  --secondary-text: #4A4A4A;    /* 보조 텍스트 */

  --accent-1: #FF6B6B;          /* Bright Red - 주요 액션 */
  --accent-2: #4ECDC4;          /* Cyan - 시스템 상태 */
  --accent-3: #FFE66D;          /* Yellow - 하이라이트 */
  --accent-4: #A8DADC;          /* Light Blue - 배경 */

  --border-thick: 4px solid #000000;
  --shadow-small: 4px 4px 0px #000000;
  --shadow-medium: 6px 6px 0px #000000;
  --shadow-large: 8px 8px 0px #000000;
}
```

### 컴포넌트 스타일

```css
/* Button Example */
.btn-neo {
  background: var(--accent-1);
  color: var(--primary-text);
  border: var(--border-thick);
  box-shadow: var(--shadow-medium);
  padding: 16px 32px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.1s ease;
}

.btn-neo:hover {
  transform: translate(2px, 2px);
  box-shadow: 4px 4px 0px #000000;
}

.btn-neo:active {
  transform: translate(6px, 6px);
  box-shadow: 0px 0px 0px #000000;
}
```

---

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT (Browser)                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Frontend (HTML/CSS/JS + Neo-Brutalism)                             │    │
│  │  - 텍스트 입력/출력 UI                                                │    │
│  │  - 변환 옵션 선택                                                     │    │
│  │  - Firebase 인증                                                      │    │
│  │  - 메트릭 시각화                                                      │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP POST /api/transform
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SERVER (Vercel Serverless Functions)                      │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  api/index.py - API 엔드포인트                                        │   │
│  │  ├── POST /api/transform                                              │   │
│  │  ├── GET /api/health                                                  │   │
│  │  └── GET / (Static Frontend)                                          │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                      │                                       │
│         ┌────────────────────────────┼────────────────────────────┐         │
│         ▼                            ▼                            ▼         │
│  ┌─────────────┐            ┌─────────────┐            ┌─────────────┐      │
│  │  Structure  │            │ Vocabulary  │            │    Noise    │      │
│  │ Transformer │            │ Transformer │            │  Injector   │      │
│  └─────────────┘            └─────────────┘            └─────────────┘      │
│         │                            │                            │         │
│         └────────────────────────────┼────────────────────────────┘         │
│                                      ▼                                       │
│                        ┌──────────────────────┐                             │
│                        │   OpenAI Client      │                             │
│                        │   (GPT-4o API)       │                             │
│                        └──────────────────────┘                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
                        ┌──────────────────────┐
                        │   OpenAI API         │
                        │   (External)         │
                        └──────────────────────┘
```

---

## 기술 스택

### Backend

| 기술 | 버전 | 용도 |
|-----|------|------|
| **Python** | 3.11+ | 메인 언어 |
| **FastAPI** | 0.109+ | REST API 프레임워크 |
| **Uvicorn** | 0.27+ | ASGI 서버 |
| **OpenAI** | 2.8+ | GPT-4o API 클라이언트 |
| **KoNLPy** | 0.6+ | 한국어 형태소 분석 |
| **Pydantic** | 2.5+ | 데이터 검증 |

### Frontend

| 기술 | 용도 |
|-----|------|
| **HTML5** | 구조 |
| **Neo-Brutalism CSS** | 스타일링 (736줄 커스텀 시스템) |
| **Vanilla JS** | 클라이언트 로직 (ES6+ Modules) |
| **Firebase SDK v9+** | 인증 및 실시간 데이터 |
| **Space Grotesk** | 영문 폰트 |
| **Pretendard** | 한국어 폰트 |

### Deployment & Infrastructure

| 서비스 | 용도 |
|--------|------|
| **Vercel** | 프론트엔드 호스팅 + Serverless Functions |
| **Firebase Authentication** | 사용자 인증 (이메일/비밀번호) |
| **Firebase Realtime Database** | 실시간 데이터 동기화 |
| **OpenAI API** | 텍스트 변환 엔진 |

---

## 🔐 보안 및 인증

### Firebase Authentication

- **이메일/비밀번호 인증**: Firebase SDK v9+ 사용
- **특별 코드 시스템**: 추가 접근 제어 레이어
- **사용자 세션 관리**: 자동 로그인 유지

### 환경 변수 보안

⚠️ **절대로 GitHub에 올리면 안 되는 파일:**

```
.env
.env.local
firebase-config.js
*.key
*.pem
firebase-adminsdk*.json
```

이미 `.gitignore`에 등록되어 있으니, **절대 수정하지 마세요!**

### Firebase Security Rules

Firebase Console > Firestore Database (또는 Realtime Database) > Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // 인증된 사용자만 읽기/쓰기 가능
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

---

## 프로젝트 구조

```
copymaker/
├── api/                          # Vercel Serverless Functions
│   └── index.py                  # FastAPI 엔트리포인트
│
├── backend/                      # Backend 소스코드
│   ├── __init__.py
│   ├── main.py                   # FastAPI 앱
│   ├── config.py                 # 환경 설정 (Pydantic Settings)
│   │
│   ├── transformers/             # 변환 모듈
│   │   ├── __init__.py
│   │   ├── structure.py          # 구조 재배열
│   │   ├── vocabulary.py         # 어휘 다양화
│   │   └── noise.py              # 노이즈 주입
│   │
│   ├── nlp/                      # NLP 유틸리티
│   │   ├── __init__.py
│   │   ├── korean.py             # 한국어 처리
│   │   └── metrics.py            # 텍스트 메트릭 계산
│   │
│   └── utils/
│       ├── __init__.py
│       └── openai_client.py      # OpenAI API 래퍼
│
├── frontend/                     # Frontend 소스코드
│   ├── index.html                # 메인 HTML (Neo-Brutalism)
│   ├── style.css                 # Neo-Brutalism CSS (736줄)
│   ├── app.js                    # JavaScript 로직
│   ├── firebase-config.example.js # Firebase 설정 템플릿
│   └── firebase-config.js        # Firebase 실제 설정 (Git 제외)
│
├── .env.example                  # 환경 변수 템플릿
├── .env                          # 환경 변수 실제 값 (Git 제외)
├── .gitignore                    # Git 제외 파일 목록
├── vercel.json                   # Vercel 배포 설정
├── requirements.txt              # Python 의존성
├── SPEC.md                       # 프로젝트 명세서
└── README.md                     # 이 파일
```

---

## 탐지 우회 원리

### 1. 구조 재배열 (Structure Transformer)

**목표:** N-gram 기반 탐지 우회

```
[탐지 원리]
- 5-gram 이상의 연속된 토큰 패턴 매칭
- Jaccard 유사도로 직접 복사 탐지

[우회 전략]
┌─────────────────────────────────────────────────────────────┐
│ 원문: "인공지능 기술의 발전은 현대 사회에 큰 영향을 미친다."  │
│                           ↓                                  │
│ 변환: "현대 사회에 지대한 영향을 미치는 것이 인공지능 기술의   │
│       진보이다."                                             │
└─────────────────────────────────────────────────────────────┘

- 문장 분리/합치기: 긴 문장 → 2-3개 짧은 문장
- 순서 재배열: 문장 성분 위치 변경
- 능동/수동태 전환
```

### 2. 어휘 다양화 (Vocabulary Transformer)

**목표:** 어휘 유사도 기반 탐지 우회

```
[탐지 원리]
- TF-IDF 벡터 코사인 유사도
- 임베딩 기반 의미 유사도

[우회 전략]
┌────────────────────────────────────────┐
│ "그러나" → "하지만", "그렇지만", "근데"  │
│ "따라서" → "그래서", "결국", "그러므로"  │
│ "중요하다" → "핵심이다", "긴요하다"      │
│ "발전" → "진보", "진전", "향상"          │
└────────────────────────────────────────┘

- 접속사 변경
- 동의어 치환
- 구어체/문어체 혼합
- 담화 표지 삽입 ("사실", "솔직히", "물론")
```

### 3. 노이즈 주입 (Noise Injector)

**목표:** 퍼플렉시티/Burstiness 기반 탐지 우회

```
[탐지 원리]
- AI 글: 낮은 퍼플렉시티 (예측 가능)
- AI 글: 균일한 문장 길이 분포
- AI 글: 일정한 단어 사용 패턴

[우회 전략]
┌─────────────────────────────────────────────────────────────┐
│ 문장 길이 불균일화:                                          │
│   원문: [12, 14, 13, 15, 12] 단어 (균일)                     │
│   변환: [5, 22, 8, 18, 6, 15] 단어 (불균일)                  │
│                                                              │
│ 예측 불가능한 요소 삽입:                                      │
│   "흥미롭게도", "생각해보면", "한 가지 덧붙이자면"             │
│                                                              │
│ 괄호 삽입:                                                   │
│   "(물론 이건 한 가지 관점일 뿐이지만)"                       │
└─────────────────────────────────────────────────────────────┘
```

### 탐지 회피 효과

| 탐지 지표 | 원본 AI 글 | 변환 후 |
|----------|-----------|--------|
| N-gram 매칭 | 높음 | **낮음** |
| 퍼플렉시티 | 낮음 (예측 가능) | **높음** (인간적) |
| 문장 길이 편차 | 낮음 (균일) | **높음** (불균일) |
| 어휘 다양성 | 중간 | **높음** |
| Burstiness | 낮음 | **중간~높음** |

---

## 🛠️ 로컬 개발 환경 설정

### 요구 사항
- Python 3.11+
- Node.js 18+ (Vercel CLI)
- OpenAI API 키
- Firebase 프로젝트

### 1. 저장소 클론
```bash
git clone <repository-url>
cd copymaker
```

### 2. Python 의존성 설치
```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 3. Firebase 설정

#### (a) Firebase Console에서 프로젝트 생성
1. [Firebase Console](https://console.firebase.google.com/) 접속
2. "프로젝트 추가" 클릭
3. 프로젝트 이름 입력 (예: `not-gpt-production`)
4. Google Analytics 설정 (선택사항)

#### (b) Firebase Authentication 활성화
1. Firebase Console > Authentication > Sign-in method
2. "이메일/비밀번호" 활성화
3. 저장

#### (c) Firebase 설정 파일 생성
```bash
# 템플릿 복사
cp frontend/firebase-config.example.js frontend/firebase-config.js

# firebase-config.js 파일 편집
# Firebase Console > 프로젝트 설정 > 일반 > 내 앱 > 웹 앱 추가
# 제공된 설정 값을 firebase-config.js에 입력
```

**firebase-config.js 예시:**
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "not-gpt-production.firebaseapp.com",
  projectId: "not-gpt-production",
  storageBucket: "not-gpt-production.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890",
  measurementId: "G-XXXXXXXXXX"
};
```

### 4. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집
nano .env  # 또는 vscode, vim 등
```

**필수 환경 변수:**
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4o

# Special Access Code
SPECIAL_CODE=verygood2025
```

### 5. 로컬 서버 실행
```bash
# Backend (FastAPI)
cd backend
uvicorn main:app --reload --port 8000

# Frontend (Live Server 또는 Python HTTP Server)
cd frontend
python -m http.server 3000
```

브라우저에서 `http://localhost:3000` 접속

---

## 🌐 Vercel 배포 가이드

### 1. Vercel CLI 설치
```bash
npm install -g vercel
```

### 2. Vercel 로그인
```bash
vercel login
```

### 3. 프로젝트 연결
```bash
# 프로젝트 루트에서 실행
vercel

# 질문에 답변:
# - Set up and deploy? Yes
# - Which scope? (계정 선택)
# - Link to existing project? No
# - Project name? not-gpt (또는 원하는 이름)
# - Directory? ./ (현재 디렉토리)
```

### 4. 환경 변수 설정

Vercel Dashboard에서 환경 변수 추가:

1. Vercel Dashboard > 프로젝트 선택 > Settings > Environment Variables
2. 다음 변수들을 추가 (Production, Preview, Development 모두 체크):

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `OPENAI_API_KEY` | `sk-proj-your-key-here` | All |
| `OPENAI_MODEL` | `gpt-4o` | All |
| `SPECIAL_CODE` | `verygood2025` | All |

3. 저장 후 프로젝트 재배포:
```bash
vercel --prod
```

### 5. 배포 확인
```bash
vercel --prod
```

배포 완료 후 제공되는 URL에서 서비스 확인:
```
✅ Production: https://not-gpt.vercel.app
```

---

## API 문서

### POST /api/transform

텍스트 변환 엔드포인트

**Request:**
```json
{
  "text": "변환할 텍스트",
  "options": {
    "structure": true,
    "vocabulary": true,
    "noise": true
  },
  "intensity": 0.5
}
```

**Parameters:**

| 필드 | 타입 | 설명 |
|-----|------|------|
| `text` | string | 변환할 텍스트 (1-10,000자) |
| `options.structure` | boolean | 구조 재배열 적용 |
| `options.vocabulary` | boolean | 어휘 다양화 적용 |
| `options.noise` | boolean | 노이즈 주입 적용 |
| `intensity` | float | 변환 강도 (0.0-1.0) |

**Response:**
```json
{
  "original": "원본 텍스트",
  "transformed": "변환된 텍스트",
  "metrics": {
    "original_sentence_count": 5,
    "transformed_sentence_count": 6,
    "original_avg_length": 12.4,
    "transformed_avg_length": 10.7,
    "original_length_std": 2.7,
    "transformed_length_std": 3.4,
    "vocabulary_diversity_change": 0.059
  },
  "applied_transforms": ["structure", "vocabulary", "noise"]
}
```

### GET /api/health

헬스 체크 엔드포인트

**Response:**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "firebase_configured": true
}
```

---

## 변환 모듈 상세

### StructureTransformer

```python
class StructureTransformer:
    """문장 구조 변환"""

    def transform(self, text: str, intensity: float) -> str:
        # 1. 문장 분리
        # 2. 각 문장에 대해:
        #    - 긴 문장 → 분리
        #    - 짧은 문장 → 병합
        #    - 구조 재구성
        # 3. 부분 순서 재배열
```

### VocabularyTransformer

```python
class VocabularyTransformer:
    """어휘 다양화"""

    CONNECTOR_VARIATIONS = {
        "그러나": ["하지만", "그렇지만", "근데"],
        "따라서": ["그래서", "그러므로", "결국"],
        # ...
    }

    def transform(self, text: str, intensity: float) -> str:
        # 1. 접속사 변경
        # 2. 동의어 치환 (OpenAI)
        # 3. 문체 혼합
        # 4. 담화 표지 삽입
```

### NoiseInjector

```python
class NoiseInjector:
    """통계적 노이즈 주입"""

    UNEXPECTED_TRANSITIONS = [
        "흥미롭게도", "생각해보면", "한 가지 덧붙이자면",
        # ...
    ]

    def transform(self, text: str, intensity: float) -> str:
        # 1. 문장 길이 불균일화
        # 2. 예측 불가능한 전환어 삽입
        # 3. 퍼플렉시티 증가 처리
        # 4. 비선형 흐름 요소 추가
```

---

## 🆘 문제 해결

### Q1: Firebase 연결이 안 돼요
**A:** `firebase-config.js` 파일이 제대로 생성되었는지 확인하세요. Firebase Console의 설정 값이 정확한지 다시 확인하세요.

### Q2: Vercel 배포 시 에러가 발생해요
**A:** 환경 변수가 모두 설정되었는지 확인하세요. 특히 `OPENAI_API_KEY`가 올바른지 체크하세요.

### Q3: 텍스트 변환이 너무 느려요
**A:** OpenAI API 응답 시간에 따라 10-30초 소요될 수 있습니다. 입력 텍스트 길이를 줄이거나 변환 강도를 낮춰보세요.

### Q4: Neo-Brutalism 디자인이 제대로 안 보여요
**A:** 브라우저 캐시를 클리어하고 페이지를 새로고침하세요 (Ctrl+Shift+R). `style.css` 파일이 제대로 로드되는지 확인하세요.

### Q5: 특별 코드가 작동하지 않아요
**A:** `.env` 파일의 `SPECIAL_CODE` 값이 정확한지 확인하세요. 기본값은 `verygood2025`입니다.

---

## 📊 성능 목표 (Lighthouse)

- **Performance**: 90+ / 100
- **Accessibility**: 95+ / 100
- **Best Practices**: 95+ / 100
- **SEO**: 90+ / 100

**UX 메트릭:**
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Time to Interactive (TTI): < 3.0s

---

## 🤝 기여 가이드

### Git Workflow
```bash
# Feature 브랜치 생성
git checkout -b feature/새기능-이름

# 변경사항 커밋
git add .
git commit -m "feat: 새로운 기능 추가"

# Push
git push origin feature/새기능-이름

# Pull Request 생성 (GitHub)
```

### Commit Convention
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 스타일 변경 (포맷팅)
- `design`: 디자인 시스템 변경 (Neo-Brutalism)
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가
- `chore`: 빌드/설정 변경

---

## 📝 라이센스

Educational Purpose Only

---

## ⚠️ 주의사항

이 도구는 교육 및 연구 목적으로 제작되었습니다.
학술적 무결성을 위반하는 용도로 사용하지 마세요.

---

**Made with ❤️ using Neo-Brutalism Design System**

*Bold borders, hard shadows, bright colors - because subtlety is overrated.*
