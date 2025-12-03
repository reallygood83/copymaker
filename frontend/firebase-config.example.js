/**
 * Firebase Configuration Template
 *
 * 🔒 보안 중요:
 * 1. 이 파일은 템플릿입니다. GitHub에 커밋됩니다.
 * 2. 실제 사용 시:
 *    - 이 파일을 복사하여 firebase-config.js로 이름을 변경하세요
 *    - Firebase Console에서 실제 값을 입력하세요
 *    - firebase-config.js는 .gitignore에 의해 자동으로 제외됩니다
 *
 * 📝 Firebase 설정 방법:
 * 1. Firebase Console (https://console.firebase.google.com/) 접속
 * 2. 프로젝트 생성 또는 선택
 * 3. 프로젝트 설정 > 일반 > 내 앱 > 웹 앱 추가
 * 4. 앱 등록 후 제공되는 설정 값을 아래에 입력
 * 5. Authentication 활성화 (이메일/비밀번호 로그인 방식 사용)
 */

import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js';
import { getAuth } from 'https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js';

// Firebase 설정 객체 - 실제 값으로 교체하세요
const firebaseConfig = {
  apiKey: "YOUR_FIREBASE_API_KEY",                    // Firebase Console > 프로젝트 설정에서 확인
  authDomain: "your-project.firebaseapp.com",        // 프로젝트ID.firebaseapp.com 형식
  projectId: "your-project-id",                       // Firebase 프로젝트 ID
  storageBucket: "your-project.appspot.com",         // 프로젝트ID.appspot.com 형식
  messagingSenderId: "123456789012",                 // 숫자 형태의 Sender ID
  appId: "1:123456789012:web:abcdef1234567890",     // Firebase 앱 ID
  measurementId: "G-XXXXXXXXXX"                      // Google Analytics ID (선택사항)
};

// Firebase 초기화
const app = initializeApp(firebaseConfig);

// Firebase Authentication 초기화
const auth = getAuth(app);

// Export - 다른 파일에서 사용할 수 있도록
export { auth };

/**
 * 사용 예시 (app.js에서):
 *
 * import { auth } from './firebase-config.js';
 * import {
 *   signInWithEmailAndPassword,
 *   createUserWithEmailAndPassword,
 *   signOut
 * } from 'https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js';
 *
 * // 로그인
 * signInWithEmailAndPassword(auth, email, password)
 *   .then((userCredential) => {
 *     console.log('로그인 성공:', userCredential.user);
 *   })
 *   .catch((error) => {
 *     console.error('로그인 실패:', error.message);
 *   });
 */
