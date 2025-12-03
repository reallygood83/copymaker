#!/usr/bin/env python3
import os
import sys
import argparse
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import settings
from backend.utils.openai_client import OpenAIClient
from backend.transformers import StructureTransformer, VocabularyTransformer, NoiseInjector
from backend.nlp import KoreanNLP

def main():
    load_dotenv()
    
    if not settings.openai_api_key:
        print("Error: OPENAI_API_KEY not found. Please set it in .env or environment variables.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Not_GPT CLI - Transform text to bypass AI detection")
    parser.add_argument("input_file", help="Path to input text file")
    parser.add_argument("-o", "--output", help="Path to output text file", default="output.txt")
    parser.add_argument("--intensity", type=float, default=0.5, help="Transformation intensity (0.0-1.0)")
    parser.add_argument("--no-structure", action="store_true", help="Disable structure transformation")
    parser.add_argument("--no-vocab", action="store_true", help="Disable vocabulary transformation")
    parser.add_argument("--no-noise", action="store_true", help="Disable noise injection")
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    print(f"Processing text ({len(text)} chars)...")
    
    # Initialize components
    openai_client = OpenAIClient(api_key=settings.openai_api_key, model=settings.openai_model)
    korean_nlp = KoreanNLP()
    
    transformed_text = text
    
    # 1. Structure
    if not args.no_structure:
        print("Applying structure transformation...")
        transformer = StructureTransformer(openai_client, korean_nlp)
        transformed_text = transformer.transform(transformed_text, intensity=args.intensity)
        
    # 2. Vocabulary
    if not args.no_vocab:
        print("Applying vocabulary transformation...")
        transformer = VocabularyTransformer(openai_client, korean_nlp)
        transformed_text = transformer.transform(transformed_text, intensity=args.intensity)
        
    # 3. Noise
    if not args.no_noise:
        print("Applying noise injection...")
        injector = NoiseInjector(openai_client, korean_nlp)
        transformed_text = injector.transform(transformed_text, intensity=args.intensity)
        
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(transformed_text)
        print(f"\nSuccess! Transformed text saved to: {args.output}")
    except Exception as e:
        print(f"Error writing output: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
