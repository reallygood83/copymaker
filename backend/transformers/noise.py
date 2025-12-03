"""
Statistical noise injection module.
Handles perplexity manipulation and burstiness adjustment.
"""
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..utils.openai_client import OpenAIClient
    from ..nlp.korean import KoreanNLP


class NoiseInjector:
    """
    Inject statistical noise to bypass AI detection metrics.
    
    Targets:
    - Perplexity: Make text less predictable
    - Burstiness: Create uneven word/sentence distribution
    - Sentence length: Vary lengths to appear more human-like
    """
    
    # Unexpected transition phrases
    UNEXPECTED_TRANSITIONS = [
        "흥미롭게도",
        "생각해보면",
        "한 가지 덧붙이자면",
        "여기서 잠깐",
        "다른 관점에서 보면",
        "사족을 붙이자면",
        "덧붙여 말하자면",
        "개인적으로는",
        "솔직히 말해서",
        "어쩌면",
    ]
    
    # Rare/unusual expressions to increase perplexity
    RARE_EXPRESSIONS = {
        "중요하다": ["긴요하다", "핵심적이다", "지대하다"],
        "생각하다": ["사료하다", "헤아리다", "가늠하다"],
        "많다": ["다수이다", "비일비재하다", "허다하다"],
        "좋다": ["양호하다", "긍정적이다", "바람직하다"],
        "나쁘다": ["부정적이다", "미흡하다", "난점이 있다"],
        "어렵다": ["난해하다", "용이하지 않다", "만만치 않다"],
        "쉽다": ["수월하다", "용이하다", "간편하다"],
    }
    
    # Parenthetical insertions
    PARENTHETICAL_INSERTS = [
        "(물론 이건 한 가지 관점일 뿐이지만)",
        "(정확히 말하자면)",
        "(다소 과장된 표현이긴 하지만)",
        "(이 부분은 논쟁의 여지가 있으나)",
        "(일반화하기는 어렵지만)",
    ]
    
    def __init__(self, openai_client: "OpenAIClient", korean_nlp: "KoreanNLP"):
        self.openai = openai_client
        self.nlp = korean_nlp
    
    def transform(self, text: str, intensity: float = 0.5) -> str:
        """
        Apply statistical noise to text.
        
        Args:
            text: Input text to transform
            intensity: Noise intensity (0.0-1.0)
        
        Returns:
            Noise-injected text
        """
        # Step 1: Vary sentence lengths
        text = self._vary_sentence_lengths(text, intensity)
        
        # Step 2: Add unexpected elements
        if intensity > 0.4:
            text = self._add_unexpected_elements(text, intensity)
        
        # Step 3: Increase lexical unpredictability
        if intensity > 0.5:
            text = self._increase_unpredictability(text)
        
        # Step 4: Add non-linear flow elements
        if intensity > 0.6:
            text = self._add_nonlinear_flow(text)
        
        return text
    
    def _vary_sentence_lengths(self, text: str, intensity: float) -> str:
        """
        Adjust sentence lengths to create uneven distribution.
        
        AI text tends to have uniform sentence lengths.
        Human text has more variation.
        """
        sentences = self.nlp.split_sentences(text)
        
        if len(sentences) < 3:
            return text
        
        # Calculate target variation level
        lengths = [len(s.split()) for s in sentences]
        current_std = self._std(lengths)
        target_std = current_std * (1 + intensity)  # Increase std
        
        modified = []
        for i, sentence in enumerate(sentences):
            word_count = len(sentence.split())
            
            # Randomly modify some sentences
            if random.random() < intensity:
                if random.random() < 0.5 and word_count > 8:
                    # Make some sentences shorter
                    shortened = self._shorten_sentence(sentence)
                    modified.append(shortened)
                elif word_count < 15:
                    # Make some sentences longer
                    lengthened = self._lengthen_sentence(sentence)
                    modified.append(lengthened)
                else:
                    modified.append(sentence)
            else:
                modified.append(sentence)
        
        return " ".join(modified)
    
    def _shorten_sentence(self, sentence: str) -> str:
        """Shorten a sentence while preserving meaning."""
        prompt = """다음 문장을 더 간결하게 줄여주세요.
- 핵심 의미 보존
- 불필요한 수식어 제거
- 자연스러운 문장 유지
결과만 출력하세요."""
        
        return self.openai.transform_text(sentence, prompt, temperature=0.6)
    
    def _lengthen_sentence(self, sentence: str) -> str:
        """Lengthen a sentence with details or qualifiers."""
        prompt = """다음 문장에 적절한 수식어나 부연 설명을 추가해주세요.
- 자연스럽게 문장을 늘리기
- 과하지 않게, 3-5단어 정도만 추가
- 의미는 유지
결과만 출력하세요."""
        
        return self.openai.transform_text(sentence, prompt, temperature=0.7)
    
    def _add_unexpected_elements(self, text: str, intensity: float) -> str:
        """Add unexpected transitions and expressions."""
        sentences = self.nlp.split_sentences(text)
        
        if len(sentences) < 2:
            return text
        
        # Number of insertions based on intensity
        num_insertions = max(1, int(len(sentences) * intensity * 0.2))
        
        # Choose positions (avoid first and last)
        if len(sentences) > 2:
            available_positions = list(range(1, len(sentences) - 1))
            positions = random.sample(
                available_positions,
                min(num_insertions, len(available_positions))
            )
            
            for pos in sorted(positions, reverse=True):
                transition = random.choice(self.UNEXPECTED_TRANSITIONS)
                sentences[pos] = f"{transition}, {sentences[pos][0].lower()}{sentences[pos][1:]}"
        
        return " ".join(sentences)
    
    def _increase_unpredictability(self, text: str) -> str:
        """Increase lexical unpredictability using LLM."""
        prompt = """다음 텍스트를 더 예측하기 어렵게 만들어주세요.
방법:
1. 흔한 표현 대신 덜 일반적인 동의어 사용
2. 문장 구조를 다양하게
3. 예상치 못한 비유나 표현 1-2개 추가
4. 전체적인 의미는 유지
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.9)
    
    def _add_nonlinear_flow(self, text: str) -> str:
        """Add elements that break linear predictability."""
        sentences = self.nlp.split_sentences(text)
        
        if len(sentences) < 4:
            return text
        
        # Randomly add a parenthetical remark
        if random.random() < 0.5:
            insert_pos = random.randint(1, len(sentences) - 2)
            parenthetical = random.choice(self.PARENTHETICAL_INSERTS)
            sentences[insert_pos] = f"{sentences[insert_pos]} {parenthetical}"
        
        return " ".join(sentences)
    
    def add_rhetorical_elements(self, text: str) -> str:
        """Add rhetorical questions or self-dialogue."""
        prompt = """다음 텍스트에 수사적 질문이나 자문자답을 1-2개 추가해주세요.
예시:
- "왜 그럴까? 이유는 간단하다."
- "과연 그럴까? 꼭 그렇다고만은 할 수 없다."
- "여기서 의문이 생긴다."
자연스럽게 녹여서 추가하세요.
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.8)
    
    def inject_personal_touches(self, text: str) -> str:
        """Add personal/subjective elements to increase human-likeness."""
        prompt = """다음 텍스트에 약간의 주관적/개인적 터치를 추가해주세요.
- "개인적으로는", "내 생각에는" 같은 표현 1-2개
- 완전한 객관성보다는 저자의 목소리가 느껴지게
- 과하지 않게, 자연스럽게
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.7)
    
    def _std(self, values: list) -> float:
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def create_burstiness(self, text: str, target_level: float = 0.3) -> str:
        """
        Adjust text to have specific burstiness level.
        
        Args:
            text: Input text
            target_level: Target burstiness (-1 to 1)
                         Higher = more bursty word usage
        
        Returns:
            Text with adjusted burstiness
        """
        prompt = f"""다음 텍스트의 단어 사용 패턴을 조정해주세요.
목표: 일부 핵심 단어는 반복하고, 다른 부분은 다양한 어휘 사용
- 중요한 개념은 의도적으로 2-3번 반복
- 나머지 부분은 동의어를 활용해 다양하게
- 전체적으로 불균일한 단어 분포 만들기
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.8)


