#!/usr/bin/env python3
"""
Not_GPT - AI Detection Bypass System
Run script for development server.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n" + "=" * 60)
        print("⚠️  WARNING: OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("=" * 60)
        print("\n다음 방법 중 하나로 API 키를 설정하세요:\n")
        print("1. .env 파일 생성:")
        print("   echo 'OPENAI_API_KEY=sk-your-key-here' > .env\n")
        print("2. 환경 변수로 직접 설정:")
        print("   export OPENAI_API_KEY=sk-your-key-here\n")
        print("=" * 60 + "\n")
    
    print("\n🚀 Not_GPT 서버 시작...")
    print("   URL: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["backend", "frontend"]
    )


