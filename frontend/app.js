/**
 * Not_GPT - Frontend Application
 * AI Detection Bypass System Client (Simplified - Special Code Only)
 */

// API Configuration
const API_BASE = '';  // Same origin

// DOM Elements
const elements = {
    inputText: document.getElementById('input-text'),
    outputText: document.getElementById('output-text'),
    transformBtn: document.getElementById('btn-transform'),
    copyBtn: document.getElementById('btn-copy'),
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

    // Auth Elements (Special Code Only)
    authOverlay: document.getElementById('auth-overlay'),
    codeFormContainer: document.getElementById('code-form-container'),
    codeForm: document.getElementById('code-form'),
    codeError: document.getElementById('code-error'),
    specialCodeInput: document.getElementById('special-code'),

    // Process Modal Elements
    stepAnalyze: document.getElementById('step-analyze'),
    stepTransform: document.getElementById('step-transform'),
    stepComplete: document.getElementById('step-complete'),
    progressBar: document.getElementById('progress-bar'),
    statusText: document.getElementById('status-text')
};

// State
const SPECIAL_CODE = 'verygood2025';
const STORAGE_KEY = 'not_gpt_verified';

// Application Entry Point
document.addEventListener('DOMContentLoaded', () => {
    // Check if already verified
    const isVerified = localStorage.getItem(STORAGE_KEY) === 'true';

    if (isVerified) {
        showApp();
    } else {
        showCodeInput();
    }

    initializeEventListeners();
    checkHealth();
    updateCharCount();
});

// Special Code Verification
function setupCodeVerification() {
    elements.codeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const code = elements.specialCodeInput.value.trim().toLowerCase();

        if (code === SPECIAL_CODE) {
            // Save verification state
            localStorage.setItem(STORAGE_KEY, 'true');

            // Hide error if visible
            elements.codeError.style.display = 'none';

            // Show app
            showApp();

            // Clear input
            elements.specialCodeInput.value = '';
        } else {
            // Show error
            elements.codeError.style.display = 'block';

            // Shake animation
            elements.codeForm.classList.add('animate-shake');
            setTimeout(() => elements.codeForm.classList.remove('animate-shake'), 500);

            // Clear input
            elements.specialCodeInput.value = '';
            elements.specialCodeInput.focus();
        }
    });
}

// UI Navigation
function showCodeInput() {
    elements.authOverlay.classList.remove('hidden');
    elements.codeFormContainer.style.display = 'block';

    // Focus input
    setTimeout(() => elements.specialCodeInput.focus(), 100);
}

function showApp() {
    elements.authOverlay.classList.add('hidden');
}

// Core Functionality
function initializeEventListeners() {
    // Setup code verification
    setupCodeVerification();

    // Core App Logic
    elements.inputText.addEventListener('input', updateCharCount);
    elements.transformBtn.addEventListener('click', handleTransform);
    elements.copyBtn.addEventListener('click', handleCopy);
    elements.intensitySlider.addEventListener('input', updateIntensityDisplay);

    // Keyboard shortcut: Ctrl/Cmd + Enter to transform
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
        // Step 1: Analyze (0-33%)
        updateProcessStep('analyze');
        updateProgress(10);
        updateStatusText('텍스트를 분석하는 중...');

        await new Promise(resolve => setTimeout(resolve, 300)); // Visual feedback
        updateProgress(33);

        // Step 2: Transform (33-66%)
        updateProcessStep('transform');
        updateProgress(40);
        updateStatusText('AI가 텍스트를 변환하는 중...');

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

        updateProgress(66);
        const data = await response.json();

        // Step 3: Complete (66-100%)
        updateProcessStep('complete');
        updateProgress(80);
        updateStatusText('결과를 준비하는 중...');

        // Update UI with results
        elements.outputText.value = data.transformed;
        updateMetrics(data.metrics);
        elements.metricsPanel.style.display = 'block';

        updateProgress(100);
        updateStatusText('완료! ✨');

        // Auto-close after showing completion
        await new Promise(resolve => setTimeout(resolve, 800));

    } catch (error) {
        updateStatusText('⚠️ 오류 발생');
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
        elements.copyBtn.innerHTML = '✅ 복사 완료!';
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
        elements.loadingOverlay.style.display = 'flex';
        elements.transformBtn.disabled = true;
        elements.transformBtn.classList.add('opacity-50', 'cursor-not-allowed');

        // Reset process modal state
        resetProcessModal();
    } else {
        elements.loadingOverlay.style.display = 'none';
        elements.transformBtn.disabled = false;
        elements.transformBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
}

// Process Modal Control Functions
function resetProcessModal() {
    // Reset all steps to inactive state
    elements.stepAnalyze.classList.remove('active', 'completed');
    elements.stepTransform.classList.remove('active', 'completed');
    elements.stepComplete.classList.remove('active', 'completed');

    // Reset progress bar
    elements.progressBar.style.width = '0%';

    // Reset status text
    elements.statusText.textContent = '텍스트를 분석하고 재구성하는 중...';
}

function updateProcessStep(step) {
    // Remove all active/completed states
    elements.stepAnalyze.classList.remove('active', 'completed');
    elements.stepTransform.classList.remove('active', 'completed');
    elements.stepComplete.classList.remove('active', 'completed');

    // Set states based on current step
    if (step === 'analyze') {
        elements.stepAnalyze.classList.add('active');
    } else if (step === 'transform') {
        elements.stepAnalyze.classList.add('completed');
        elements.stepTransform.classList.add('active');
    } else if (step === 'complete') {
        elements.stepAnalyze.classList.add('completed');
        elements.stepTransform.classList.add('completed');
        elements.stepComplete.classList.add('active');
    }
}

function updateProgress(percentage) {
    elements.progressBar.style.width = `${percentage}%`;
}

function updateStatusText(text) {
    elements.statusText.textContent = text;
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

    // Update badge classes
    indicator.className = 'badge-neo';
    if (type === 'ready') {
        indicator.className += ' badge-neo-success';
    } else if (type === 'warning') {
        indicator.className += ' badge-neo-warning';
    } else {
        indicator.className += ' badge-neo-error';
    }

    indicator.textContent = message;
}
