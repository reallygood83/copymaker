/**
 * Not_GPT - Frontend Application
 * AI Detection Bypass System Client
 */

import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { 
    getAuth, 
    createUserWithEmailAndPassword, 
    signInWithEmailAndPassword, 
    signOut, 
    onAuthStateChanged 
} from "firebase/auth";

// API Configuration
const API_BASE = '';  // Same origin

// DOM Elements
const elements = {
    inputText: document.getElementById('input-text'),
    outputText: document.getElementById('output-text'),
    transformBtn: document.getElementById('btn-transform'), // Updated ID
    copyBtn: document.getElementById('btn-copy'), // Updated ID
    inputStats: document.getElementById('input-stats'),
    intensitySlider: document.getElementById('intensity-slider'),
    intensityValue: document.getElementById('intensity-value'),
    loadingOverlay: document.getElementById('loading-overlay'),
    metricsPanel: document.getElementById('metrics-panel'),
    statusIndicator: document.getElementById('status-indicator'),
    // Options
    optStructure: document.getElementById('opt-structure'),
    optVocabulary: document.getElementById('opt-vocabulary'),
    optNoise: document.getElementById('opt-noise'),
    // Metrics
    metricSentencesOld: document.getElementById('metric-sentences-old'),
    metricSentencesNew: document.getElementById('metric-sentences-new'),
    metricLengthOld: document.getElementById('metric-length-old'),
    metricLengthNew: document.getElementById('metric-length-new'),
    metricDiversity: document.getElementById('metric-diversity'),
    
    // Auth Elements
    authOverlay: document.getElementById('auth-overlay'),
    loginFormContainer: document.getElementById('login-form-container'),
    signupFormContainer: document.getElementById('signup-form-container'),
    codeFormContainer: document.getElementById('code-form-container'),
    loginForm: document.getElementById('login-form'),
    signupForm: document.getElementById('signup-form'),
    codeForm: document.getElementById('code-form'),
    
    btnShowSignup: document.getElementById('btn-show-signup'),
    btnShowLogin: document.getElementById('btn-show-login'),
    btnLogout: document.getElementById('btn-logout'),
    btnLogoutCode: document.getElementById('btn-logout-code'),
    
    loginError: document.getElementById('login-error'),
    signupError: document.getElementById('signup-error'),
    codeError: document.getElementById('code-error'),
    userInfo: document.getElementById('user-info')
};

// State
let currentUser = null;
let isCodeVerified = false;
const SPECIAL_CODE = 'verygood2025';

// Initialize Firebase
function initFirebase() {
    if (!window.FIREBASE_CONFIG) {
        console.error("Firebase config not found!");
        return null;
    }
    const app = initializeApp(window.FIREBASE_CONFIG);
    const auth = getAuth(app);
    try {
        const analytics = getAnalytics(app);
    } catch (e) {
        console.warn("Analytics failed to load", e);
    }
    return auth;
}

// Application Entry Point
document.addEventListener('DOMContentLoaded', () => {
    const auth = initFirebase();
    if (auth) {
        setupAuthListeners(auth);
    }
    
    initializeEventListeners();
    checkHealth();
    updateCharCount();
});

// Auth Logic
function setupAuthListeners(auth) {
    // Auth State Observer
    onAuthStateChanged(auth, (user) => {
        currentUser = user;
        if (user) {
            // Logged in
            elements.userInfo.textContent = user.email;
            elements.userInfo.classList.remove('hidden');
            elements.btnLogout.classList.remove('hidden');
            
            // Check if code is verified (In a real app, check DB. Here, simple session state)
            if (isCodeVerified) {
                showApp();
            } else {
                showCodeInput();
            }
        } else {
            // Logged out
            elements.userInfo.classList.add('hidden');
            elements.btnLogout.classList.add('hidden');
            isCodeVerified = false;
            showLogin();
        }
    });

    // Login
    elements.loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        elements.loginError.classList.add('hidden');
        
        try {
            await signInWithEmailAndPassword(auth, email, password);
        } catch (error) {
            elements.loginError.textContent = getErrorMessage(error.code);
            elements.loginError.classList.remove('hidden');
        }
    });

    // Signup
    elements.signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('signup-email').value;
        const password = document.getElementById('signup-password').value;
        elements.signupError.classList.add('hidden');
        
        try {
            await createUserWithEmailAndPassword(auth, email, password);
        } catch (error) {
            elements.signupError.textContent = getErrorMessage(error.code);
            elements.signupError.classList.remove('hidden');
        }
    });

    // Logout
    const handleLogout = async () => {
        try {
            await signOut(auth);
        } catch (error) {
            console.error("Logout failed", error);
        }
    };
    elements.btnLogout.addEventListener('click', handleLogout);
    elements.btnLogoutCode.addEventListener('click', handleLogout);
}

// Special Code Logic
function setupCodeVerification() {
    elements.codeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const code = document.getElementById('special-code').value;
        
        if (code === SPECIAL_CODE) {
            isCodeVerified = true;
            showApp();
        } else {
            elements.codeError.classList.remove('hidden');
            elements.codeForm.classList.add('animate-shake');
            setTimeout(() => elements.codeForm.classList.remove('animate-shake'), 500);
        }
    });
}

// UI Navigation
function showLogin() {
    elements.authOverlay.classList.remove('hidden');
    elements.loginFormContainer.classList.remove('hidden');
    elements.signupFormContainer.classList.add('hidden');
    elements.codeFormContainer.classList.add('hidden');
}

function showSignup() {
    elements.loginFormContainer.classList.add('hidden');
    elements.signupFormContainer.classList.remove('hidden');
}

function showCodeInput() {
    elements.authOverlay.classList.remove('hidden');
    elements.loginFormContainer.classList.add('hidden');
    elements.signupFormContainer.classList.add('hidden');
    elements.codeFormContainer.classList.remove('hidden');
}

function showApp() {
    elements.authOverlay.classList.add('hidden');
}

function getErrorMessage(code) {
    switch (code) {
        case 'auth/invalid-email': return '유효하지 않은 이메일 형식입니다.';
        case 'auth/user-disabled': return '비활성화된 계정입니다.';
        case 'auth/user-not-found': return '존재하지 않는 계정입니다.';
        case 'auth/wrong-password': return '비밀번호가 올바르지 않습니다.';
        case 'auth/email-already-in-use': return '이미 사용 중인 이메일입니다.';
        case 'auth/weak-password': return '비밀번호는 6자 이상이어야 합니다.';
        default: return '로그인/회원가입 중 오류가 발생했습니다.';
    }
}

// Core Functionality
function initializeEventListeners() {
    setupCodeVerification();
    
    // Toggle Login/Signup
    elements.btnShowSignup.addEventListener('click', showSignup);
    elements.btnShowLogin.addEventListener('click', () => {
        elements.loginFormContainer.classList.remove('hidden');
        elements.signupFormContainer.classList.add('hidden');
    });

    // Core App Logic
    elements.inputText.addEventListener('input', updateCharCount);
    elements.transformBtn.addEventListener('click', handleTransform);
    elements.copyBtn.addEventListener('click', handleCopy);
    elements.intensitySlider.addEventListener('input', updateIntensityDisplay);
    
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (elements.authOverlay.classList.contains('hidden')) {
                e.preventDefault();
                handleTransform();
            }
        }
    });
}

async function handleTransform() {
    const text = elements.inputText.value.trim();
    if (!text) return;
    
    setLoading(true);
    
    try {
        const response = await fetch(`${API_BASE}/api/transform`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                options: {
                    structure: elements.optStructure.checked,
                    vocabulary: elements.optVocabulary.checked,
                    noise: elements.optNoise.checked
                },
                intensity: elements.intensitySlider.value / 100
            })
        });
        
        if (!response.ok) throw new Error('Transform failed');
        
        const data = await response.json();
        
        // Update UI with results
        elements.outputText.value = data.transformed;
        updateMetrics(data.metrics);
        elements.metricsPanel.classList.remove('hidden');
        
    } catch (error) {
        alert('변환 중 오류가 발생했습니다: ' + error.message);
    } finally {
        setLoading(false);
    }
}

function updateMetrics(metrics) {
    // Animate numbers
    animateValue(elements.metricSentencesOld, metrics.original_sentence_count);
    animateValue(elements.metricSentencesNew, metrics.transformed_sentence_count);
    
    animateValue(elements.metricLengthOld, Math.round(metrics.original_avg_length));
    animateValue(elements.metricLengthNew, Math.round(metrics.transformed_avg_length));
    
    const divChange = Math.round(metrics.vocabulary_diversity_change * 100);
    elements.metricDiversity.textContent = (divChange > 0 ? '+' : '') + divChange + '%';
}

function animateValue(obj, end, duration = 1000) {
    let startTimestamp = null;
    const start = parseInt(obj.textContent) || 0;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function handleCopy() {
    const text = elements.outputText.value;
    if (!text) return;
    
    navigator.clipboard.writeText(text).then(() => {
        const originalText = elements.copyBtn.innerHTML;
        elements.copyBtn.innerHTML = `
            <svg class="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            완료!
        `;
        setTimeout(() => {
            elements.copyBtn.innerHTML = originalText;
        }, 2000);
    });
}

function updateCharCount() {
    const count = elements.inputText.value.length;
    elements.inputStats.textContent = `${count.toLocaleString()} chars`;
}

function updateIntensityDisplay() {
    elements.intensityValue.textContent = `${elements.intensitySlider.value}%`;
}

function setLoading(isLoading) {
    if (isLoading) {
        elements.loadingOverlay.classList.remove('hidden');
        elements.transformBtn.disabled = true;
        elements.transformBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
        elements.loadingOverlay.classList.add('hidden');
        elements.transformBtn.disabled = false;
        elements.transformBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        
        if (data.status === 'healthy' && data.openai_configured) {
            updateStatus('ready', '시스템 준비');
        } else if (!data.openai_configured) {
            updateStatus('warning', 'API 키 필요');
        }
    } catch (error) {
        updateStatus('error', '연결 실패');
    }
}

function updateStatus(type, message) {
    const indicator = elements.statusIndicator;
    const dot = indicator.querySelector('div');
    const text = indicator.querySelector('span');
    
    dot.className = 'w-2 h-2 rounded-full ' + 
        (type === 'ready' ? 'bg-neon-green animate-pulse' : 
         type === 'warning' ? 'bg-yellow-500' : 'bg-red-500');
    
    text.textContent = message;
    if (type === 'error') text.classList.add('text-red-500');
}
