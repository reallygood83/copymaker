"""
Korean NLP module for text processing.
"""
import re
from typing import Optional


class KoreanNLP:
    """
    Korean Natural Language Processing utilities.
    
    Provides sentence splitting, tokenization, and morphological analysis
    for Korean text processing.
    """
    
    def __init__(self, use_konlpy: bool = True):
        """
        Initialize Korean NLP processor.
        
        Args:
            use_konlpy: Whether to use KoNLPy for morphological analysis.
                       Falls back to regex-based processing if unavailable.
        """
        self.tagger = None
        self._konlpy_available = False
        
        if use_konlpy:
            try:
                from konlpy.tag import Komoran
                self.tagger = Komoran()
                self._konlpy_available = True
            except ImportError:
                print("Warning: KoNLPy not available. Using regex-based fallback.")
            except Exception as e:
                print(f"Warning: KoNLPy initialization failed: {e}. Using regex-based fallback.")
    
    def split_sentences(self, text: str) -> list[str]:
        """
        Split text into sentences.
        
        Uses Korean sentence-ending patterns including:
        - Period (.), Question mark (?), Exclamation mark (!)
        - Korean sentence endings (요, 다, 까, 네, 죠, etc.)
        
        Args:
            text: Input text to split
            
        Returns:
            List of sentences
        """
        if not text or not text.strip():
            return []
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Korean sentence ending pattern
        # Matches: .?! followed by space or end, or Korean endings followed by space
        sentence_pattern = r'(?<=[.?!])\s+|(?<=[다요죠네까])\s+(?=[A-Z가-힣"])'
        
        # Split by pattern
        raw_sentences = re.split(sentence_pattern, text)
        
        # Clean and filter
        sentences = []
        for s in raw_sentences:
            s = s.strip()
            if s and len(s) > 1:  # Filter out single characters
                sentences.append(s)
        
        # If no splits were made, try alternative pattern
        if len(sentences) <= 1 and len(text) > 100:
            # Try splitting on period/question/exclamation followed by space
            alt_pattern = r'(?<=[.?!])\s+'
            raw_sentences = re.split(alt_pattern, text)
            sentences = [s.strip() for s in raw_sentences if s.strip()]
        
        return sentences if sentences else [text]
    
    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into words/morphemes.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of tokens
        """
        if self._konlpy_available and self.tagger:
            # Use KoNLPy morpheme analysis
            morphs = self.tagger.morphs(text)
            return morphs
        else:
            # Fallback: simple word tokenization
            return self._simple_tokenize(text)
    
    def _simple_tokenize(self, text: str) -> list[str]:
        """Simple regex-based tokenization fallback."""
        # Remove punctuation and split on whitespace
        text = re.sub(r'[^\w\s가-힣]', ' ', text)
        tokens = text.split()
        return [t for t in tokens if t.strip()]
    
    def pos_tag(self, text: str) -> list[tuple[str, str]]:
        """
        Perform part-of-speech tagging.
        
        Args:
            text: Input text
            
        Returns:
            List of (word, POS tag) tuples
        """
        if self._konlpy_available and self.tagger:
            return self.tagger.pos(text)
        else:
            # Fallback: return tokens with 'UNKNOWN' tag
            tokens = self._simple_tokenize(text)
            return [(t, 'UNKNOWN') for t in tokens]
    
    def extract_nouns(self, text: str) -> list[str]:
        """Extract nouns from text."""
        if self._konlpy_available and self.tagger:
            return self.tagger.nouns(text)
        else:
            # Fallback: return all tokens (not accurate but functional)
            return self._simple_tokenize(text)
    
    def get_word_count(self, text: str) -> int:
        """Get word count for text."""
        tokens = self.tokenize(text)
        return len(tokens)
    
    def get_sentence_lengths(self, sentences: list[str]) -> list[int]:
        """Get word counts for each sentence."""
        return [self.get_word_count(s) for s in sentences]
    
    def extract_connectors(self, text: str) -> list[str]:
        """
        Extract connector words (접속사, 연결어) from text.
        
        Returns list of found connectors.
        """
        connectors = [
            '그러나', '하지만', '그렇지만', '그런데', '근데',
            '그리고', '또한', '게다가', '더불어', '아울러',
            '따라서', '그래서', '그러므로', '결국', '결과적으로',
            '왜냐하면', '때문에', '이유는',
            '예를 들어', '예컨대', '가령',
            '즉', '다시 말해', '바꿔 말하면',
            '반면', '반대로', '오히려',
            '물론', '사실', '실제로', '어쨌든', '아무튼'
        ]
        
        found = []
        for conn in connectors:
            if conn in text:
                found.append(conn)
        
        return found
    
    def extract_function_words(self, text: str) -> dict[str, int]:
        """
        Extract and count function words (기능어) usage.
        
        Returns dictionary of function word frequencies.
        """
        function_words = [
            '은', '는', '이', '가', '을', '를', '에', '에서', '으로', '로',
            '와', '과', '의', '도', '만', '까지', '부터', '처럼', '같이',
            '그', '이', '저', '그것', '이것', '저것',
            '그리고', '그러나', '그래서', '하지만', '그런데'
        ]
        
        if self._konlpy_available and self.tagger:
            pos_tags = self.tagger.pos(text)
            counts = {}
            for word, tag in pos_tags:
                if tag.startswith('J') or tag.startswith('E'):  # 조사, 어미
                    counts[word] = counts.get(word, 0) + 1
            return counts
        else:
            # Fallback: count occurrences of known function words
            counts = {}
            for fw in function_words:
                count = text.count(fw)
                if count > 0:
                    counts[fw] = count
            return counts


