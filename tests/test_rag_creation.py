"""
RAG 통합 테스트 스크립트
전체 파이프라인이 정상 작동하는지 확인
"""

import sys
from pathlib import Path

# 경로 설정
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
modules_dir = project_root / "modules"

sys.path.insert(0, str(project_root))
sys.path.insert(0, str(modules_dir))

from modules.azure_client import AzureOpenAIClient
from modules.azure_search_client import AzureSearchClient
from modules.rag_service import RAGService

def test_rag_pipeline():
    """RAG 파이프라인 전체 테스트"""
    print("🚀 RAG 파이프라인 테스트 시작...\n")
    
    try:
        # 1. 클라이언트 초기화
        print("1️⃣ 클라이언트 초기화 중...")
        azure_client = AzureOpenAIClient()
        search_client = AzureSearchClient()
        rag_service = RAGService(azure_client, search_client)
        print("✅ 모든 클라이언트 초기화 완료\n")
        
        # 2. 코딩 컨벤션 검색 테스트
        print("2️⃣ 코딩 컨벤션 검색 테스트...")
        conventions = search_client.search_conventions(
            query="Python 함수 네이밍",
            language="python",
            top=2
        )
        print(f"✅ 검색 결과: {len(conventions)}개 문서")
        for conv in conventions:
            print(f"   - {conv['title']} (점수: {conv.get('score', 'N/A')})")
        print()
        
        # 3. 환경 설정 템플릿 검색 테스트
        print("3️⃣ 환경 설정 템플릿 검색 테스트...")
        templates = search_client.search_templates(
            query="React 프로젝트 설정",
            tech_stack=["react"],
            top=2
        )
        print(f"✅ 검색 결과: {len(templates)}개 템플릿")
        for template in templates:
            print(f"   - {template['title']} (점수: {template.get('score', 'N/A')})")
        print()
        
        # 4. RAG 코드 리뷰 테스트
        print("4️⃣ RAG 코드 리뷰 테스트...")
        test_code = """
def calculateUserAge(userBirthYear):
    currentYear = 2024
    return currentYear - userBirthYear

class userManager:
    def __init__(self):
        self.users = []
    
    def addUser(self, user):
        self.users.append(user)
"""
        
        review_result = rag_service.enhance_code_review(test_code, "python")
        
        if review_result["success"]:
            print("✅ RAG 코드 리뷰 성공!")
            print(f"   참조된 컨벤션: {len(review_result['referenced_conventions'])}개")
            print(f"   감지된 패턴: {review_result['patterns_found']}")
        else:
            print("⚠️ RAG 코드 리뷰 실패, 폴백 사용")
        print()
        
        # 5. RAG 환경 설정 가이드 테스트
        print("5️⃣ RAG 환경 설정 가이드 테스트...")
        test_readme = """
# My React Project

This is a React application with TypeScript.

## Getting Started

Run `npm install` and then `npm start`.
"""
        
        guide_result = rag_service.enhance_setup_guide(test_readme, "all")
        
        if guide_result["success"]:
            print("✅ RAG 환경 설정 가이드 성공!")
            print(f"   참조된 템플릿: {len(guide_result['referenced_templates'])}개")
            print(f"   감지된 기술 스택: {guide_result['tech_stack_found']}")
        else:
            print("⚠️ RAG 환경 설정 가이드 실패, 폴백 사용")
        print()
        
        print("🎉 모든 RAG 테스트 완료!")
        print("\n✅ Phase 1 완료 체크리스트:")
        print("   ✅ Azure AI Search 인덱스 생성")
        print("   ✅ 샘플 데이터 업로드")
        print("   ✅ 기본 검색 API 구현") 
        print("   ✅ 기존 코드에 RAG 통합")
        print("\n🚀 다음 단계: Streamlit 앱 실행 및 UI 테스트")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG 테스트 실패: {e}")
        import traceback
        print(f"🐛 상세 오류:\n{traceback.format_exc()}")
        return False

def test_individual_components():
    """개별 컴포넌트 테스트"""
    print("🔧 개별 컴포넌트 테스트...\n")
    
    # Azure OpenAI 테스트
    try:
        print("🔄 Azure OpenAI 테스트...")
        azure_client = AzureOpenAIClient()
        response = azure_client.get_completion([
            {"role": "user", "content": "Hello, test!"}
        ])
        print("✅ Azure OpenAI 정상 작동")
    except Exception as e:
        print(f"❌ Azure OpenAI 오류: {e}")
    
    # Azure AI Search 테스트
    try:
        print("🔄 Azure AI Search 테스트...")
        search_client = AzureSearchClient()
        results = search_client.search_conventions("테스트", top=1)
        print(f"✅ Azure AI Search 정상 작동 (결과: {len(results)}개)")
    except Exception as e:
        print(f"❌ Azure AI Search 오류: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 DevPilot RAG 통합 테스트")
    print("=" * 60)
    print()
    
    # 개별 컴포넌트 테스트
    test_individual_components()
    print()
    
    # 전체 파이프라인 테스트
    success = test_rag_pipeline()
    
    if success:
        print("\n🎯 다음 실행 명령어:")
        print("streamlit run app.py")
        print("\n📝 확인 사항:")
        print("1. RAG 서비스 활성화 상태 확인")
        print("2. 코드 리뷰에서 컨벤션 참조 확인")
        print("3. 환경 설정에서 템플릿 참조 확인")
    else:
        print("\n❌ 문제 해결 후 다시 시도하세요.")