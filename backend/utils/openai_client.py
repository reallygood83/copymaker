"""
OpenAI API client wrapper for text transformation.
"""
from openai import OpenAI
from typing import Optional
import json


class OpenAIClient:
    """Wrapper for OpenAI API calls used in text transformation."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def transform_text(
        self, 
        text: str, 
        system_prompt: str,
        temperature: float = 0.8
    ) -> str:
        """
        Transform text using OpenAI API.
        
        Args:
            text: Input text to transform
            system_prompt: System prompt defining transformation behavior
            temperature: Creativity level (0.0-2.0)
        
        Returns:
            Transformed text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=temperature,
            max_tokens=4096
        )
        
        return response.choices[0].message.content.strip()
    
    def merge_sentences(self, sentence1: str, sentence2: str) -> str:
        """Merge two sentences into one natural sentence."""
        prompt = """당신은 한국어 문장 병합 전문가입니다.
두 개의 문장을 자연스럽게 하나의 문장으로 합쳐주세요.
- 의미는 보존하되, 문장 구조는 자연스럽게 변경
- 접속사나 연결어미를 적절히 사용
- 결과만 출력 (설명 없이)"""
        
        return self.transform_text(
            f"문장1: {sentence1}\n문장2: {sentence2}",
            prompt,
            temperature=0.7
        )
    
    def split_sentence(self, sentence: str) -> list[str]:
        """Split a long sentence into multiple shorter sentences."""
        prompt = """당신은 한국어 문장 분리 전문가입니다.
긴 문장을 자연스러운 2-3개의 짧은 문장으로 분리해주세요.
- 의미는 보존
- 각 문장이 독립적으로 의미가 통하도록
- JSON 배열 형식으로 출력: ["문장1", "문장2", ...]"""
        
        result = self.transform_text(sentence, prompt, temperature=0.5)
        
        try:
            # Try to parse as JSON array
            if result.startswith("["):
                return json.loads(result)
            else:
                # Fallback: split by newlines
                return [s.strip() for s in result.split("\n") if s.strip()]
        except json.JSONDecodeError:
            return [sentence]  # Return original if parsing fails
    
    def paraphrase(self, text: str, style: str = "neutral") -> str:
        """Paraphrase text while preserving meaning."""
        style_instructions = {
            "neutral": "자연스럽고 중립적인 문체로",
            "colloquial": "구어체로 자연스럽게",
            "formal": "격식체로 정중하게",
            "academic": "학술적이고 객관적인 문체로"
        }
        
        style_desc = style_instructions.get(style, style_instructions["neutral"])
        
        prompt = f"""당신은 한국어 패러프레이징 전문가입니다.
주어진 텍스트를 {style_desc} 다시 작성해주세요.
- 핵심 의미는 반드시 보존
- 문장 구조와 어휘는 다양하게 변경
- 원문과 최대한 다른 표현 사용
- 결과만 출력 (설명 없이)"""
        
        return self.transform_text(text, prompt, temperature=0.9)
    
    def reorder_paragraph(self, sentences: list[str]) -> list[str]:
        """Reorder sentences while maintaining logical flow."""
        prompt = """당신은 한국어 문단 재구성 전문가입니다.
주어진 문장들의 순서를 자연스럽게 재배열해주세요.
- 논리적 흐름 유지
- 전체 의미 보존
- JSON 배열 형식으로 출력: ["문장1", "문장2", ...]"""
        
        text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(sentences)])
        result = self.transform_text(text, prompt, temperature=0.6)
        
        try:
            if result.startswith("["):
                return json.loads(result)
            return sentences
        except json.JSONDecodeError:
            return sentences
    
    def add_filler_expressions(self, text: str) -> str:
        """Add natural filler expressions to make text more human-like."""
        prompt = """당신은 한국어 글쓰기 전문가입니다.
주어진 텍스트에 자연스러운 담화 표지(filler)를 추가해주세요.
- 예: "사실", "물론", "아무래도", "어쨌든", "솔직히" 등
- 과하지 않게, 2-3개 정도만 자연스러운 위치에 추가
- 의미 변경 없이 자연스러움만 추가
- 결과만 출력"""
        
        return self.transform_text(text, prompt, temperature=0.8)
    
    def vary_connectors(self, text: str) -> str:
        """Replace common connectors with varied alternatives."""
        prompt = """당신은 한국어 문장 연결 전문가입니다.
텍스트 내의 접속사와 연결어를 다양하게 바꿔주세요.
- "그러나" → "하지만", "그렇지만", "근데" 등
- "그리고" → "또한", "게다가", "더불어" 등  
- "따라서" → "그래서", "결국", "그러므로" 등
- 문맥에 맞게 자연스럽게 변경
- 결과만 출력"""
        
        return self.transform_text(text, prompt, temperature=0.7)


