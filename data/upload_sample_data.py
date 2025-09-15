"""
Azure AI Search 샘플 데이터 업로드
RAG 테스트를 위한 코딩 컨벤션 및 환경 설정 템플릿 데이터
"""

import sys
from pathlib import Path
import json

# 경로 설정
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
modules_dir = project_root / "modules"

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(modules_dir))

from modules.azure_search_client import AzureSearchClient
from modules.azure_client import AzureOpenAIClient

class SampleDataUploader:
    """샘플 데이터 업로드 클래스"""
    
    def __init__(self):
        self.search_client = AzureSearchClient()
        self.openai_client = AzureOpenAIClient()
    
    def get_sample_conventions(self):
        """코딩 컨벤션 샘플 데이터"""
        return [
            {
                "id": "conv_python_naming",
                "title": "Python 네이밍 컨벤션 - PEP 8",
                "content": """
함수명과 변수명은 snake_case를 사용합니다.
- 함수: def calculate_total_price()
- 변수: user_name, total_amount
- 상수: MAX_RETRY_COUNT, DEFAULT_TIMEOUT

클래스명은 PascalCase를 사용합니다.
- 클래스: class UserManager, DatabaseConnection

비공개 속성은 언더스코어로 시작합니다.
- _private_method(), __very_private
                """,
                "category": "coding_convention",
                "language": "python",
                "company": "ktds",
                "project_type": "backend",
                "tags": ["naming", "pep8", "snake_case"],
                "priority": 1
            },
            {
                "id": "conv_python_imports",
                "title": "Python Import 스타일 가이드",
                "content": """
Import 순서와 스타일:
1. 표준 라이브러리
2. 서드파티 라이브러리  
3. 로컬 애플리케이션/라이브러리

예시:
import os
import sys
from typing import Dict, List

import requests
import pandas as pd

from myapp.models import User
from myapp.utils import helper
                """,
                "category": "coding_convention",
                "language": "python",
                "company": "ktds",
                "project_type": "backend",
                "tags": ["import", "organization", "pep8"],
                "priority": 2
            },
            {
                "id": "conv_javascript_naming",
                "title": "JavaScript 네이밍 컨벤션",
                "content": """
함수명과 변수명은 camelCase를 사용합니다.
- 함수: calculateTotalPrice()
- 변수: userName, totalAmount

클래스명과 생성자는 PascalCase를 사용합니다.
- 클래스: class UserManager
- 컴포넌트: function UserProfile()

상수는 UPPER_SNAKE_CASE를 사용합니다.
- const MAX_RETRY_COUNT = 3
- const API_BASE_URL = 'https://api.example.com'
                """,
                "category": "coding_convention",
                "language": "javascript",
                "company": "ktds",
                "project_type": "frontend",
                "tags": ["naming", "camelCase", "javascript"],
                "priority": 1
            },
            {
                "id": "conv_logging_style",
                "title": "로깅 스타일 가이드",
                "content": """
로그 레벨 사용 기준:
- ERROR: 시스템 오류, 예외 상황
- WARN: 경고, 잠재적 문제
- INFO: 일반적인 정보, 주요 이벤트
- DEBUG: 개발 시 디버깅 정보

로그 메시지 형식:
- 명확하고 구체적으로 작성
- 사용자 정보는 마스킹 처리
- 예: logger.info("사용자 로그인 성공: user_id=***")
                """,
                "category": "coding_convention",
                "language": "general",
                "company": "ktds",
                "project_type": "all",
                "tags": ["logging", "error_handling", "debugging"],
                "priority": 1
            },
            {
                "id": "conv_error_handling",
                "title": "에러 처리 베스트 프랙티스",
                "content": """
에러 처리 원칙:
1. 구체적인 예외 타입 사용
2. 의미 있는 에러 메시지 제공
3. 로깅과 사용자 알림 분리

Python 예시:
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"데이터 처리 오류: {e}")
    return {"error": "유효하지 않은 데이터입니다"}
except Exception as e:
    logger.error(f"예상치 못한 오류: {e}")
    return {"error": "서버 오류가 발생했습니다"}
                """,
                "category": "coding_convention",
                "language": "general",
                "company": "ktds",
                "project_type": "all",
                "tags": ["error_handling", "exception", "robustness"],
                "priority": 1
            }
        ]
    
    def get_sample_templates(self):
        """환경 설정 템플릿 샘플 데이터"""
        return [
            {
                "id": "template_python_fastapi",
                "title": "FastAPI 프로젝트 환경 설정",
                "content": """
# FastAPI 프로젝트 설정 가이드

## 1. 가상환경 생성
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate   # Windows
```

## 2. 의존성 설치
```bash
pip install fastapi uvicorn python-dotenv pydantic sqlalchemy
pip freeze > requirements.txt
```

## 3. 프로젝트 구조
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── database.py
├── requirements.txt
└── .env
```

## 4. 실행
```bash
uvicorn app.main:app --reload
```
                """,
                "category": "environment_setup",
                "tech_stack": ["fastapi", "python", "uvicorn"],
                "os_support": ["windows", "macos", "linux"],
                "prerequisites": ["python", "pip"],
                "difficulty": "intermediate"
            },
            {
                "id": "template_react_typescript",
                "title": "React + TypeScript 프로젝트 설정",
                "content": """
# React + TypeScript 환경 설정

## 1. Node.js 설치 확인
```bash
node --version  # v18+ 권장
npm --version
```

## 2. 프로젝트 생성
```bash
npx create-react-app my-app --template typescript
cd my-app
```

## 3. 추가 패키지 설치
```bash
npm install @types/react @types/react-dom
npm install -D eslint prettier @typescript-eslint/parser
```

## 4. VSCode 설정 (.vscode/settings.json)
```json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

## 5. 실행
```bash
npm start
```
                """,
                "category": "environment_setup",
                "tech_stack": ["react", "typescript", "nodejs"],
                "os_support": ["windows", "macos", "linux"],
                "prerequisites": ["nodejs", "npm"],
                "difficulty": "beginner"
            },
            {
                "id": "template_docker_python",
                "title": "Docker를 사용한 Python 환경 설정",
                "content": """
# Docker Python 환경 설정

## 1. Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
```

## 2. docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=development
    volumes:
      - .:/app
```

## 3. 실행
```bash
docker-compose up --build
```
                """,
                "category": "environment_setup",
                "tech_stack": ["docker", "python"],
                "os_support": ["windows", "macos", "linux"],
                "prerequisites": ["docker", "docker-compose"],
                "difficulty": "intermediate"
            }
        ]
    
    def create_embedding(self, text: str):
        """텍스트를 벡터로 변환"""
        try:
            response = self.openai_client.client.embeddings.create(
                model='minseo-embedding915',
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ 임베딩 생성 실패: {e}")
            # 더미 벡터 반환 (1536차원)
            return [0.0] * 1536
    
    def upload_conventions(self):
        """코딩 컨벤션 데이터 업로드"""
        print("🔄 코딩 컨벤션 데이터 업로드 중...")
        
        conventions = self.get_sample_conventions()
        success_count = 0
        
        for conv in conventions:
            # 벡터 생성
            embedding_text = f"{conv['title']} {conv['content']}"
            conv['content_vector'] = self.create_embedding(embedding_text)
            
            # 업로드
            if self.search_client.upload_document("coding-conventions", conv):
                print(f"✅ 업로드 성공: {conv['title']}")
                success_count += 1
            else:
                print(f"❌ 업로드 실패: {conv['title']}")
        
        print(f"📊 코딩 컨벤션 업로드 완료: {success_count}/{len(conventions)}")
        return success_count == len(conventions)
    
    def upload_templates(self):
        """환경 설정 템플릿 데이터 업로드"""
        print("🔄 환경 설정 템플릿 데이터 업로드 중...")
        
        templates = self.get_sample_templates()
        success_count = 0
        
        for template in templates:
            # 벡터 생성
            embedding_text = f"{template['title']} {template['content']}"
            template['content_vector'] = self.create_embedding(embedding_text)
            
            # 업로드
            if self.search_client.upload_document("setup-templates", template):
                print(f"✅ 업로드 성공: {template['title']}")
                success_count += 1
            else:
                print(f"❌ 업로드 실패: {template['title']}")
        
        print(f"📊 환경 설정 템플릿 업로드 완료: {success_count}/{len(templates)}")
        return success_count == len(templates)

def main():
    print("🚀 샘플 데이터 업로드 시작...\n")
    
    try:
        uploader = SampleDataUploader()
        
        # 코딩 컨벤션 업로드
        conv_success = uploader.upload_conventions()
        print()
        
        # 환경 설정 템플릿 업로드
        template_success = uploader.upload_templates()
        print()
        
        if conv_success and template_success:
            print("🎉 모든 샘플 데이터 업로드 완료!")
            print("📍 Azure Portal > AI Search > 인덱스에서 문서 확인 가능")
            print("✅ 다음 단계: RAG 서비스 구현을 진행하세요!")
            return True
        else:
            print("❌ 일부 데이터 업로드에 실패했습니다.")
            return False
            
    except Exception as e:
        print(f"❌ 업로드 중 오류 발생: {e}")
        import traceback
        print(f"🐛 상세 오류:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    main()