# Not_GPT Web App Specification

## 1. 프로젝트 개요
**Not_GPT**는 AI 탐지 우회 텍스트 변환 시스템입니다. 이 프로젝트를 웹 애플리케이션으로 전환하여 Vercel에 배포하고, Firebase Authentication을 통한 사용자 인증 및 특별 코드 기반의 접근 제어를 구현합니다.

- **GitHub Repository**: [https://github.com/reallygood83/copymaker](https://github.com/reallygood83/copymaker)
- **배포 플랫폼**: Vercel
- **인증 공급자**: Firebase Auth (Email/Password)

## 2. 시스템 아키텍처

### 2.1 기술 스택
- **Frontend**:
  - HTML5, CSS3, JavaScript (Vanilla)
  - Firebase SDK v9+
  - **Design System**: Neo-Brutalism (네오 부루탈리즘)
    - Bold borders (4-8px thick)
    - Hard shadows (no blur)
    - Bright, contrasting colors
    - Geometric shapes
    - High visual impact UI components
- **Backend**: Python FastAPI (Vercel Serverless Functions)
- **Deployment**: Vercel
- **Database/Auth**: Firebase Authentication

### 2.2 디렉토리 구조 (Vercel 배포용 재구성)
```
/
├── api/                 # Vercel Serverless Functions (Backend)
│   └── index.py         # FastAPI entry point
├── backend/             # Existing Backend Logic (Imports)
├── frontend/            # Static Files (Served by Vercel)
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── firebase-config.js (Environment Variables)
├── vercel.json          # Vercel Configuration
├── requirements.txt     # Python Dependencies
└── README.md
```

## 3. 기능 요구사항

### 3.1 인증 (Authentication)
- **회원가입/로그인**: Firebase Email/Password 인증 사용.
- **UI**:
  - 로그인 페이지 (기본 진입 화면)
  - 회원가입 모달 또는 별도 뷰
  - 로그인 성공 시 메인 앱 화면으로 전환

### 3.2 접근 제어 (Access Control)
- **특별 코드 (Special Code)**: `verygood2025`
- **로직**:
  1. 사용자가 로그인 성공.
  2. "특별 코드 입력" 모달 또는 입력창 표시.
  3. 코드가 일치해야만 텍스트 변환 기능 사용 가능.
  4. 코드가 일치하지 않으면 기능 잠금 유지.
  - *보안 참고*: 클라이언트 측 검증은 우회 가능성이 있으므로, 추후 백엔드 API 호출 시 헤더에 코드를 포함하여 서버 검증을 추가하는 것이 권장됨. (현재 단계에서는 UX 흐름 구현에 집중)

### 3.3 사용 신청
- **UI**: 로그인/회원가입 화면 하단에 "사용 신청" 버튼 배치.
- **기능**: 클릭 시 지정된 링크(추후 설정)로 이동.

### 3.4 텍스트 변환
- 기존 기능 유지 (구조 변환, 어휘 변환, 노이즈 주입).
- Backend API는 Vercel Serverless Function으로 동작.

## 4. 환경 변수 및 보안 (Security)

GitHub에 민감한 정보를 노출하지 않기 위해 환경 변수를 사용합니다.

### 4.1 Vercel Environment Variables
Vercel 대시보드에서 다음 변수들을 설정해야 합니다.

**Backend (Python)**:
- `OPENAI_API_KEY`: OpenAI API 키

**Frontend (Build Time / Runtime)**:
- `VITE_FIREBASE_API_KEY`: Firebase API Key
- `VITE_FIREBASE_AUTH_DOMAIN`: Firebase Auth Domain
- `VITE_FIREBASE_PROJECT_ID`: Firebase Project ID
- `VITE_FIREBASE_STORAGE_BUCKET`: Firebase Storage Bucket
- `VITE_FIREBASE_MESSAGING_SENDER_ID`: Firebase Messaging Sender ID
- `VITE_FIREBASE_APP_ID`: Firebase App ID
- `VITE_FIREBASE_MEASUREMENT_ID`: Firebase Measurement ID

*(참고: 바닐라 JS 프로젝트이므로 `config.js` 등을 통해 런타임에 주입하거나, Vercel의 환경 변수 치환 기능을 활용해야 합니다. 또는 보안상 덜 민감한 Firebase Config는 코드에 포함하되, API Key 등은 제한 설정을 걸어두는 것이 일반적입니다. 사용자 요청에 따라 최대한 분리합니다.)*

## 5. 네오 부루탈리즘 디자인 시스템

### 5.1 디자인 철학
Not_GPT는 **대담하고 직관적인 사용자 경험**을 제공하기 위해 네오 부루탈리즘 디자인 시스템을 채택합니다.

### 5.2 핵심 디자인 원칙

#### 5.2.1 Color Palette
```css
:root {
  /* Primary Colors - High Contrast */
  --primary-bg: #FFFFFF;
  --primary-text: #000000;
  --accent-1: #FF6B6B;      /* Bright Red */
  --accent-2: #4ECDC4;      /* Cyan */
  --accent-3: #FFE66D;      /* Yellow */
  --accent-4: #A8DADC;      /* Light Blue */

  /* Shadows - Hard & Bold */
  --shadow-small: 4px 4px 0px #000000;
  --shadow-medium: 6px 6px 0px #000000;
  --shadow-large: 8px 8px 0px #000000;

  /* Borders */
  --border-thick: 4px solid #000000;
  --border-extra-thick: 6px solid #000000;
}
```

#### 5.2.2 Typography
- **Font Family**: 'Space Grotesk', 'Pretendard', sans-serif (bold, geometric)
- **Font Weights**: 700 (Bold), 800 (Extra Bold)
- **Heading Sizes**:
  - H1: 48px (Extra Bold)
  - H2: 36px (Bold)
  - H3: 24px (Bold)
- **Body Text**: 16px (Regular weight for readability)

#### 5.2.3 UI Components

**Buttons**:
```css
.btn-neo {
  background: var(--accent-1);
  border: var(--border-thick);
  box-shadow: var(--shadow-medium);
  padding: 16px 32px;
  font-weight: 800;
  text-transform: uppercase;
  cursor: pointer;
  transition: transform 0.1s ease;
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

**Input Fields**:
```css
.input-neo {
  background: #FFFFFF;
  border: var(--border-thick);
  box-shadow: var(--shadow-small);
  padding: 12px 16px;
  font-size: 16px;
  outline: none;
}

.input-neo:focus {
  border-color: var(--accent-2);
  box-shadow: var(--shadow-medium);
}
```

**Cards/Containers**:
```css
.card-neo {
  background: #FFFFFF;
  border: var(--border-extra-thick);
  box-shadow: var(--shadow-large);
  padding: 24px;
  margin: 16px 0;
}
```

#### 5.2.4 Layout Principles
- **Grid-based Layout**: 명확한 구조와 정렬
- **Bold Dividers**: 섹션 간 두꺼운 경계선 (4px+)
- **Asymmetric Balance**: 대칭보다는 시각적 무게감의 균형
- **Generous Spacing**: 충분한 여백으로 콘텐츠 강조

### 5.3 페이지별 UI 컴포넌트

#### 5.3.1 로그인/회원가입 페이지
- **Hero Section**: 대담한 타이포그래피 + 기하학적 배경 패턴
- **Form Container**: 두꺼운 테두리 + 강한 그림자
- **CTA Buttons**: 밝은 색상 + 호버 효과
- **"사용 신청" 버튼**: 눈에 띄는 대비 색상

#### 5.3.2 메인 앱 화면
- **Header**: 고정 상단 바 (두꺼운 하단 테두리)
- **Text Input Area**: 큰 텍스트박스 + 네오 브루탈리즘 스타일
- **Convert Button**: 중앙 배치, 큰 크기, 강렬한 색상
- **Output Display**: 카드 형태 + 복사 버튼

#### 5.3.3 특별 코드 입력 모달
- **Overlay**: 반투명 검정 배경
- **Modal Box**: 중앙 배치, 흰 배경, 두꺼운 테두리
- **Input + Button**: 인라인 배치, 시각적 피드백

## 6. 개발 로드맵

### Phase 1: 프로젝트 셋업 및 구조 리팩토링 (1-2일)
- [ ] Vercel 배포를 위한 디렉토리 구조 재구성
- [ ] `api/index.py` FastAPI 엔트리포인트 생성
- [ ] `vercel.json` 설정 파일 작성
- [ ] `requirements.txt` 업데이트
- [ ] 기존 백엔드 로직을 `backend/` 폴더로 정리

### Phase 2: 네오 부루탈리즘 UI 기반 구축 (2-3일)
- [ ] `frontend/style.css` - 네오 부루탈리즘 CSS 변수 정의
- [ ] 공통 컴포넌트 스타일 작성 (버튼, 입력창, 카드)
- [ ] 타이포그래피 시스템 구축
- [ ] 레이아웃 그리드 시스템 구현
- [ ] 반응형 디자인 미디어 쿼리

### Phase 3: Firebase Authentication 연동 (2일)
- [ ] Firebase 프로젝트 생성 및 설정
- [ ] `frontend/firebase-config.js` 작성
- [ ] Email/Password 인증 로직 구현
- [ ] 회원가입 UI + 로직 (`app.js`)
- [ ] 로그인 UI + 로직
- [ ] 로그아웃 기능
- [ ] 인증 상태 관리 (session persistence)

### Phase 4: 접근 제어 및 특별 코드 (1일)
- [ ] 특별 코드 입력 모달 UI 구현
- [ ] 클라이언트 측 코드 검증 로직
- [ ] 인증 + 코드 검증 통과 시 메인 앱 화면 전환
- [ ] 실패 시 에러 메시지 표시

### Phase 5: 메인 앱 UI 구현 (2-3일)
- [ ] 텍스트 입력 영역 (네오 스타일 적용)
- [ ] 변환 옵션 선택 UI (구조/어휘/노이즈)
- [ ] "변환하기" 버튼 (강렬한 CTA)
- [ ] 로딩 상태 표시 (진행률 바 또는 애니메이션)
- [ ] 결과 출력 영역 + 복사 버튼
- [ ] 에러 핸들링 UI (실패 메시지)

### Phase 6: Backend API 연동 (1-2일)
- [ ] FastAPI 엔드포인트 테스트 (`/api/transform`)
- [ ] Frontend에서 Fetch API로 백엔드 호출
- [ ] 요청/응답 데이터 포맷 검증
- [ ] 환경 변수 처리 (OpenAI API Key)
- [ ] CORS 설정 확인

### Phase 7: 테스트 및 디버깅 (2일)
- [ ] 로컬 환경 테스트 (Vercel CLI)
- [ ] 인증 플로우 E2E 테스트
- [ ] 텍스트 변환 기능 테스트
- [ ] 에러 시나리오 테스트
- [ ] 모바일 반응형 테스트
- [ ] 브라우저 호환성 체크 (Chrome, Firefox, Safari)

### Phase 8: 배포 및 최적화 (1일)
- [ ] GitHub Repository 정리
- [ ] Vercel 프로젝트 연동
- [ ] 환경 변수 설정 (Vercel Dashboard)
- [ ] 첫 배포 및 검증
- [ ] 성능 최적화 (Lighthouse 점수 80+ 목표)
- [ ] SEO 메타태그 추가

### Phase 9: 문서화 및 마무리 (1일)
- [ ] README.md 업데이트 (설치, 실행, 배포 가이드)
- [ ] 사용자 매뉴얼 작성
- [ ] 코드 주석 정리
- [ ] 라이선스 명시
- [ ] 최종 검토 및 버그 픽스

## 7. 개발 우선순위 및 핵심 체크리스트

### 🔴 Critical (반드시 구현)
- Firebase Authentication (Email/Password)
- 특별 코드 입력 및 검증 (`verygood2025`)
- 텍스트 변환 기능 (기존 로직 유지)
- 네오 부루탈리즘 디자인 시스템 적용
- Vercel 배포 성공

### 🟡 Important (중요하지만 우선순위 낮음)
- 사용 신청 버튼 링크 설정
- 에러 메시지 한국어/영어 지원
- 로딩 애니메이션 고도화
- 반응형 디자인 최적화

### 🟢 Nice to Have (추후 개선)
- 소셜 로그인 (Google, GitHub)
- 사용자 히스토리 저장 (Firebase Firestore)
- 변환 결과 다운로드 기능 (.txt, .docx)
- 다크 모드 지원

## 8. 개발 가이드라인

### 8.1 코드 품질 기준
- **Always Works™ 원칙 준수**: 모든 기능은 반드시 테스트 후 커밋
- **30초 리얼리티 체크**: 실제 실행, 기능 트리거, 결과 확인, 에러 체크, $100 베팅 가능?
- **타입 안정성**: JSDoc 활용하여 주요 함수 타입 명시
- **에러 핸들링**: 모든 API 호출에 try-catch 및 사용자 친화적 에러 메시지

### 8.2 Git 워크플로우
- **브랜치 전략**:
  - `main`: 배포 가능한 안정 버전
  - `develop`: 개발 진행 중인 브랜치
  - `feature/*`: 기능별 브랜치
- **커밋 메시지**:
  - `feat:` 새 기능
  - `fix:` 버그 수정
  - `style:` UI/CSS 변경
  - `refactor:` 코드 리팩토링
  - `docs:` 문서 업데이트

### 8.3 보안 고려사항
- 환경 변수로 모든 API 키 관리
- Firebase Security Rules 설정
- 클라이언트 측 입력 검증 + 서버 측 재검증
- HTTPS 강제 (Vercel 자동 지원)
- XSS 방지를 위한 입력 sanitization

## 9. 성능 목표

### 9.1 Lighthouse 점수 목표
- **Performance**: 85+ (모바일), 95+ (데스크톱)
- **Accessibility**: 90+
- **Best Practices**: 95+
- **SEO**: 90+

### 9.2 사용자 경험 지표
- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.0s
- **텍스트 변환 응답 시간**: < 5s (네트워크 정상 시)

## 10. 개발 및 배포 계획 (요약)

1. **프로젝트 구조 리팩토링**: Vercel 배포를 위한 `api/index.py` 생성 및 `vercel.json` 설정
2. **네오 부루탈리즘 UI 구축**: 디자인 시스템 CSS 작성 및 공통 컴포넌트 개발
3. **Firebase 연동**: Frontend에 Firebase SDK 설치 및 인증 로직 구현
4. **UI 업데이트**: 로그인/회원가입 폼 및 특별 코드 입력창 추가
5. **메인 앱 개발**: 텍스트 변환 UI 및 Backend API 연동
6. **테스트 및 최적화**: E2E 테스트, 성능 최적화, 버그 수정
7. **배포**: GitHub Push 및 Vercel 자동 배포

---
**작성일**: 2025-12-02
**최종 업데이트**: 2025-12-02
**버전**: 2.0 (Neo-Brutalism Design System 추가)
