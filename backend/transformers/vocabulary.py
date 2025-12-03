"""
Vocabulary transformation module.
Handles synonym substitution, style mixing, and lexical diversification.
"""
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..utils.openai_client import OpenAIClient
    from ..nlp.korean import KoreanNLP


class VocabularyTransformer:
    """
    Transform vocabulary to bypass lexical similarity detection.
    
    Operations:
    - Synonym substitution
    - Formal/informal style mixing
    - Connector word variation
    - Expression diversification
    """
    
    # Korean synonym/variation mappings
    CONNECTOR_VARIATIONS = {
        "그러나": ["하지만", "그렇지만", "그런데", "반면에", "한편"],
        "하지만": ["그러나", "그렇지만", "근데", "다만"],
        "그리고": ["또한", "게다가", "더불어", "아울러", "그뿐만 아니라"],
        "또한": ["그리고", "게다가", "뿐만 아니라", "더불어"],
        "따라서": ["그래서", "그러므로", "결국", "이로 인해", "이에 따라"],
        "그래서": ["따라서", "그러므로", "결과적으로", "그 결과"],
        "왜냐하면": ["그 이유는", "이유는", "~때문에"],
        "예를 들어": ["예컨대", "가령", "이를테면", "구체적으로"],
        "즉": ["다시 말해", "바꿔 말하면", "달리 말하면", "요컨대"],
        "물론": ["당연히", "분명히", "확실히", "사실"],
    }
    
    FORMALITY_PAIRS = {
        # Formal -> Informal
        "~이다": ["~이에요", "~입니다", "~인 거예요"],
        "~였다": ["~였어요", "~이었습니다"],
        "~한다": ["~해요", "~합니다", "~하는 거예요"],
        "~이다": ["~야", "~이야"],  # Very informal
        # Common expressions
        "매우": ["정말", "아주", "굉장히", "엄청"],
        "중요하다": ["핵심이다", "필수적이다", "빼놓을 수 없다"],
        "필요하다": ["요구된다", "있어야 한다", "갖춰야 한다"],
        "생각하다": ["여기다", "판단하다", "보다", "느끼다"],
        "알다": ["파악하다", "인지하다", "이해하다", "깨닫다"],
    }
    
    COLLOQUIAL_INSERTIONS = [
        "사실",
        "물론",
        "솔직히",
        "확실히",
        "분명히",
        "아무래도",
        "어쨌든",
        "결국",
        "실제로",
        "정말로",
    ]
    
    def __init__(self, openai_client: "OpenAIClient", korean_nlp: "KoreanNLP"):
        self.openai = openai_client
        self.nlp = korean_nlp
    
    def transform(self, text: str, intensity: float = 0.5) -> str:
        """
        Apply vocabulary transformations to text.
        
        Args:
            text: Input text to transform
            intensity: Transformation intensity (0.0-1.0)
        
        Returns:
            Vocabulary-transformed text
        """
        # Step 1: Vary connectors
        text = self._vary_connectors(text, intensity)
        
        # Step 2: Apply synonym substitution via LLM
        if intensity > 0.3:
            text = self._apply_synonyms(text, intensity)
        
        # Step 3: Mix formality levels
        if intensity > 0.5:
            text = self._mix_formality(text)
        
        # Step 4: Add colloquial insertions (for higher intensity)
        if intensity > 0.6:
            text = self._add_colloquial_touches(text, intensity)
        
        return text
    
    def _vary_connectors(self, text: str, intensity: float) -> str:
        """Replace connector words with variations."""
        result = text
        
        for connector, variations in self.CONNECTOR_VARIATIONS.items():
            if connector in result:
                # Decide whether to replace based on intensity
                if random.random() < intensity:
                    replacement = random.choice(variations)
                    # Replace only first occurrence to maintain some consistency
                    result = result.replace(connector, replacement, 1)
        
        return result
    
    def _apply_synonyms(self, text: str, intensity: float) -> str:
        """Use LLM to apply sophisticated synonym substitution."""
        
        # Determine how aggressive to be
        if intensity < 0.5:
            level = "약간의"
            pct = "20-30%"
        elif intensity < 0.7:
            level = "적절한"
            pct = "40-50%"
        else:
            level = "적극적인"
            pct = "60-70%"
        
        prompt = f"""다음 텍스트의 어휘를 {level} 수준으로 다양화해주세요.
규칙:
1. 핵심 의미는 반드시 보존
2. 단어의 약 {pct}를 동의어/유사어로 교체
3. 전문 용어는 유지하되, 일반 어휘는 다양하게
4. 자연스러운 문장 유지
5. 결과만 출력 (설명 없이)"""
        
        return self.openai.transform_text(text, prompt, temperature=0.8)
    
    def _mix_formality(self, text: str) -> str:
        """Mix formal and informal expressions."""
        
        prompt = """다음 텍스트의 문체를 자연스럽게 섞어주세요.
- 기본적으로 격식체를 유지하되
- 일부 문장에서 "~요", "~거든요" 같은 구어체 사용
- 딱딱하지 않고 자연스러운 느낌으로
- 의미 변경 없이 문체만 조금씩 변화
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.7)
    
    def _add_colloquial_touches(self, text: str, intensity: float) -> str:
        """Add natural filler expressions."""
        sentences = self.nlp.split_sentences(text)
        
        if len(sentences) < 2:
            return text
        
        # Determine how many insertions based on intensity
        num_insertions = max(1, int(len(sentences) * intensity * 0.3))
        
        # Choose random positions (not first sentence)
        positions = random.sample(
            range(1, len(sentences)), 
            min(num_insertions, len(sentences) - 1)
        )
        
        for pos in positions:
            insertion = random.choice(self.COLLOQUIAL_INSERTIONS)
            sentence = sentences[pos]
            
            # Insert at the beginning of the sentence
            if not any(sentence.startswith(c) for c in self.COLLOQUIAL_INSERTIONS):
                sentences[pos] = f"{insertion}, {sentence[0].lower()}{sentence[1:]}" if sentence else sentence
        
        return " ".join(sentences)
    
    def diversify_expressions(self, text: str) -> str:
        """
        Diversify repeated expressions and patterns.
        
        Identifies repetitive patterns and varies them.
        """
        prompt = """다음 텍스트에서 반복되는 표현을 찾아 다양화해주세요.
- 같은 단어/표현이 반복되면 다른 표현으로
- 문장 시작 패턴이 비슷하면 변경
- 자연스러운 글의 흐름 유지
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.8)
    
    def apply_style_transfer(self, text: str, target_style: str) -> str:
        """
        Transfer text to a specific writing style.
        
        Args:
            text: Input text
            target_style: Target style (e.g., "academic", "casual", "journalistic")
        
        Returns:
            Style-transferred text
        """
        style_prompts = {
            "academic": "학술적이고 객관적인 문체로, 전문 용어를 적절히 사용하며",
            "casual": "편안하고 친근한 구어체로, 일상 대화처럼",
            "journalistic": "간결하고 명확한 기사체로, 핵심을 먼저 전달하며",
            "narrative": "서술적이고 묘사적인 문체로, 이야기하듯이",
        }
        
        style_desc = style_prompts.get(target_style, style_prompts["casual"])
        
        prompt = f"""다음 텍스트를 {style_desc} 다시 작성해주세요.
- 핵심 내용과 의미는 보존
- 문체와 어조만 변경
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.8)
    
    def add_hedging_language(self, text: str) -> str:
        """
        Add hedging expressions to make text less assertive.
        
        This makes text feel more human-like and uncertain.
        """
        prompt = """다음 텍스트에 완화 표현(hedging)을 적절히 추가해주세요.
예시:
- "~이다" → "~인 것 같다", "~일 수 있다"
- "확실히" → "아마도", "어느 정도"
- 단정적 표현을 부드럽게
- 과하지 않게, 자연스럽게
결과만 출력하세요."""
        
        return self.openai.transform_text(text, prompt, temperature=0.7)


