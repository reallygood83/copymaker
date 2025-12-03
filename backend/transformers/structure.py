"""
Structure transformation module.
Handles sentence splitting, merging, and reordering.
"""
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..utils.openai_client import OpenAIClient
    from ..nlp.korean import KoreanNLP


class StructureTransformer:
    """
    Transform text structure to bypass n-gram based detection.
    
    Operations:
    - Split long sentences into shorter ones
    - Merge short sentences into longer ones  
    - Reorder sentences within paragraphs
    - Convert between active/passive voice
    """
    
    def __init__(self, openai_client: "OpenAIClient", korean_nlp: "KoreanNLP"):
        self.openai = openai_client
        self.nlp = korean_nlp
    
    def transform(self, text: str, intensity: float = 0.5) -> str:
        """
        Apply structure transformations to text.
        
        Args:
            text: Input text to transform
            intensity: Transformation intensity (0.0-1.0)
                      Higher = more aggressive changes
        
        Returns:
            Structurally transformed text
        """
        # Split into sentences
        sentences = self.nlp.split_sentences(text)
        
        if len(sentences) <= 1:
            # Single sentence: try to split if long enough
            if len(text.split()) > 15:
                return self._split_long_text(text)
            return text
        
        # Apply transformations based on intensity
        transformed_sentences = []
        i = 0
        
        while i < len(sentences):
            sentence = sentences[i]
            word_count = len(sentence.split())
            
            # Randomly decide transformation based on intensity
            action = self._decide_action(word_count, intensity)
            
            if action == "split" and word_count > 12:
                # Split long sentence
                split_result = self.openai.split_sentence(sentence)
                transformed_sentences.extend(split_result)
                i += 1
                
            elif action == "merge" and i + 1 < len(sentences):
                # Merge with next sentence
                next_sentence = sentences[i + 1]
                merged = self.openai.merge_sentences(sentence, next_sentence)
                transformed_sentences.append(merged)
                i += 2
                
            elif action == "paraphrase":
                # Paraphrase while changing structure
                paraphrased = self._paraphrase_structure(sentence)
                transformed_sentences.append(paraphrased)
                i += 1
                
            else:
                # Keep as-is
                transformed_sentences.append(sentence)
                i += 1
        
        # Optionally reorder some sentences (if intensity is high)
        if intensity > 0.6 and len(transformed_sentences) > 3:
            transformed_sentences = self._partial_reorder(
                transformed_sentences, 
                intensity
            )
        
        return " ".join(transformed_sentences)
    
    def _decide_action(self, word_count: int, intensity: float) -> str:
        """
        Decide which transformation action to take.
        
        Args:
            word_count: Number of words in sentence
            intensity: Transformation intensity
            
        Returns:
            Action string: "split", "merge", "paraphrase", or "keep"
        """
        rand = random.random()
        
        # Adjust thresholds based on intensity
        split_threshold = 0.3 * intensity
        merge_threshold = split_threshold + 0.2 * intensity
        paraphrase_threshold = merge_threshold + 0.3 * intensity
        
        if word_count > 20 and rand < split_threshold:
            return "split"
        elif word_count < 10 and rand < merge_threshold:
            return "merge"
        elif rand < paraphrase_threshold:
            return "paraphrase"
        else:
            return "keep"
    
    def _split_long_text(self, text: str) -> str:
        """Split a long single text block into multiple sentences."""
        split_sentences = self.openai.split_sentence(text)
        return " ".join(split_sentences)
    
    def _paraphrase_structure(self, sentence: str) -> str:
        """Paraphrase sentence with structural changes."""
        prompt = """다음 문장의 구조를 바꿔서 다시 작성해주세요.
가능한 변환:
- 능동태 ↔ 수동태
- 주어/목적어 순서 변경
- 문장 성분 재배치
의미는 동일하게 유지하되, 구조만 변경해주세요.
결과만 출력하세요."""
        
        return self.openai.transform_text(sentence, prompt, temperature=0.7)
    
    def _partial_reorder(
        self, 
        sentences: list[str], 
        intensity: float
    ) -> list[str]:
        """
        Partially reorder sentences while maintaining coherence.
        
        Only reorders middle sentences to preserve intro/conclusion structure.
        """
        if len(sentences) <= 3:
            return sentences
        
        # Keep first and last sentences in place
        first = sentences[0]
        last = sentences[-1]
        middle = sentences[1:-1]
        
        # Number of swaps based on intensity
        num_swaps = int(len(middle) * intensity * 0.5)
        
        for _ in range(num_swaps):
            if len(middle) >= 2:
                idx1 = random.randint(0, len(middle) - 1)
                idx2 = random.randint(0, len(middle) - 1)
                if idx1 != idx2:
                    middle[idx1], middle[idx2] = middle[idx2], middle[idx1]
        
        return [first] + middle + [last]
    
    def split_by_clauses(self, text: str) -> str:
        """
        Split text by clauses rather than sentences.
        
        Useful for breaking up complex sentences with multiple clauses.
        """
        prompt = """다음 텍스트를 절(clause) 단위로 분리해서 
각각 독립적인 짧은 문장으로 만들어주세요.
- 원래 의미 보존
- 자연스러운 한국어 문장으로
- 결과만 출력"""
        
        return self.openai.transform_text(text, prompt, temperature=0.6)
    
    def combine_short_sentences(self, sentences: list[str]) -> list[str]:
        """
        Combine consecutive short sentences.
        
        Args:
            sentences: List of sentences
            
        Returns:
            List with short sentences combined
        """
        result = []
        i = 0
        
        while i < len(sentences):
            current = sentences[i]
            current_len = len(current.split())
            
            # If current sentence is short and next exists
            if current_len < 8 and i + 1 < len(sentences):
                next_sentence = sentences[i + 1]
                next_len = len(next_sentence.split())
                
                # Combine if both are short
                if next_len < 8:
                    combined = self.openai.merge_sentences(current, next_sentence)
                    result.append(combined)
                    i += 2
                    continue
            
            result.append(current)
            i += 1
        
        return result


