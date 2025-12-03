"""
Text metrics calculation module.
"""
import math
from typing import Optional
from collections import Counter


class TextMetrics:
    """
    Calculate various text metrics for analysis and comparison.
    
    Metrics include:
    - Sentence length statistics (avg, std)
    - Vocabulary diversity (type-token ratio)
    - Burstiness indicators
    """
    
    def calculate(self, text: str, sentences: list[str]) -> dict:
        """
        Calculate all metrics for given text.
        
        Args:
            text: Full text content
            sentences: Pre-split sentences
            
        Returns:
            Dictionary of metrics
        """
        # Basic counts
        word_count = len(text.split())
        sentence_count = len(sentences)
        
        # Sentence length statistics
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_length = self._mean(sentence_lengths) if sentence_lengths else 0
        length_std = self._std(sentence_lengths) if sentence_lengths else 0
        
        # Vocabulary diversity
        words = text.lower().split()
        unique_words = set(words)
        vocabulary_diversity = len(unique_words) / len(words) if words else 0
        
        # Burstiness (variation in word usage)
        burstiness = self._calculate_burstiness(words)
        
        # Length distribution metrics
        length_variance = self._variance(sentence_lengths) if sentence_lengths else 0
        length_range = (max(sentence_lengths) - min(sentence_lengths)) if sentence_lengths else 0
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": round(avg_length, 2),
            "sentence_length_std": round(length_std, 2),
            "sentence_length_variance": round(length_variance, 2),
            "sentence_length_range": length_range,
            "vocabulary_diversity": round(vocabulary_diversity, 4),
            "burstiness": round(burstiness, 4),
            "sentence_lengths": sentence_lengths
        }
    
    def compare(self, original_metrics: dict, transformed_metrics: dict) -> dict:
        """
        Compare two sets of metrics and return differences.
        
        Args:
            original_metrics: Metrics from original text
            transformed_metrics: Metrics from transformed text
            
        Returns:
            Dictionary of metric differences
        """
        return {
            "sentence_count_change": (
                transformed_metrics["sentence_count"] - 
                original_metrics["sentence_count"]
            ),
            "avg_length_change": (
                transformed_metrics["avg_sentence_length"] - 
                original_metrics["avg_sentence_length"]
            ),
            "length_std_change": (
                transformed_metrics["sentence_length_std"] - 
                original_metrics["sentence_length_std"]
            ),
            "vocabulary_diversity_change": (
                transformed_metrics["vocabulary_diversity"] - 
                original_metrics["vocabulary_diversity"]
            ),
            "burstiness_change": (
                transformed_metrics["burstiness"] - 
                original_metrics["burstiness"]
            )
        }
    
    def _mean(self, values: list) -> float:
        """Calculate mean of values."""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    def _variance(self, values: list) -> float:
        """Calculate variance of values."""
        if len(values) < 2:
            return 0.0
        mean = self._mean(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _std(self, values: list) -> float:
        """Calculate standard deviation of values."""
        return math.sqrt(self._variance(values))
    
    def _calculate_burstiness(self, words: list[str]) -> float:
        """
        Calculate burstiness metric.
        
        Burstiness measures how "bursty" word usage is.
        Higher values indicate more uneven word distribution.
        
        Uses the formula: B = (σ - μ) / (σ + μ)
        where σ is standard deviation and μ is mean of word frequencies.
        
        Returns value between -1 and 1:
        - Closer to 1: Very bursty (words appear in clusters)
        - Closer to 0: Random (Poisson-like)
        - Closer to -1: Very regular (evenly distributed)
        """
        if not words:
            return 0.0
        
        # Count word frequencies
        word_counts = Counter(words)
        frequencies = list(word_counts.values())
        
        if len(frequencies) < 2:
            return 0.0
        
        mean = self._mean(frequencies)
        std = self._std(frequencies)
        
        if mean + std == 0:
            return 0.0
        
        burstiness = (std - mean) / (std + mean)
        return burstiness
    
    def get_percentile_lengths(self, sentence_lengths: list[int]) -> dict:
        """
        Get percentile values for sentence lengths.
        
        Returns:
            Dictionary with p25, p50 (median), p75 values
        """
        if not sentence_lengths:
            return {"p25": 0, "p50": 0, "p75": 0}
        
        sorted_lengths = sorted(sentence_lengths)
        n = len(sorted_lengths)
        
        return {
            "p25": sorted_lengths[int(n * 0.25)],
            "p50": sorted_lengths[int(n * 0.50)],
            "p75": sorted_lengths[int(n * 0.75)] if n > 1 else sorted_lengths[0]
        }
    
    def analyze_uniformity(self, sentence_lengths: list[int]) -> dict:
        """
        Analyze how uniform sentence lengths are.
        
        AI-generated text tends to have more uniform lengths.
        Human text tends to have more variation.
        
        Returns:
            Dictionary with uniformity analysis
        """
        if not sentence_lengths or len(sentence_lengths) < 2:
            return {
                "coefficient_of_variation": 0,
                "uniformity_score": 1.0,
                "is_suspicious": False
            }
        
        mean = self._mean(sentence_lengths)
        std = self._std(sentence_lengths)
        
        # Coefficient of variation (CV)
        cv = std / mean if mean > 0 else 0
        
        # Uniformity score (0 = very varied, 1 = very uniform)
        # Lower CV means more uniform
        uniformity_score = max(0, 1 - cv)
        
        # AI-generated text suspicion threshold
        # Very uniform text (uniformity > 0.7) might be AI-generated
        is_suspicious = uniformity_score > 0.7
        
        return {
            "coefficient_of_variation": round(cv, 4),
            "uniformity_score": round(uniformity_score, 4),
            "is_suspicious": is_suspicious
        }


