"""
Azure AI Search 인덱스 생성 테스트
$ python tests/test_index_creation.py
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트 찾기 (tests 폴더의 부모 디렉토리)
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent  # tests 폴더의 부모 = 프로젝트 루트
modules_dir = project_root / "modules"

# 프로젝트 루트와 modules 디렉토리를 Python 경로에 추가
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(modules_dir))

print(f"📁 프로젝트 루트: {project_root}")
print(f"📁 모듈 디렉토리: {modules_dir}")

try:
    from azure_search_client import AzureSearchClient
    print("✅ azure_search_client 모듈 import 성공")
    
except ImportError as e:
    print(f"❌ azure_search_client import 실패: {e}")
    print(f"\n🔍 확인 사항:")
    print(f"1. 파일 존재 확인: {modules_dir / 'azure_search_client.py'}")
    print("2. 필요한 패키지가 설치되었는지 확인:")
    print("   pip install azure-search-documents azure-identity")
    sys.exit(1)

def test_environment():
    """환경변수 테스트"""
    print("\n🔍 환경변수 확인:")
    
    # .env 파일 경로 확인
    env_file = project_root / ".env"
    print(f"📄 .env 파일 위치: {env_file}")
    print(f"📄 .env 파일 존재: {'✅' if env_file.exists() else '❌'}")
    
    # 환경변수 로드를 위해 python-dotenv 사용
    try:
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("✅ .env 파일 로드 성공")
    except ImportError:
        print("⚠️ python-dotenv가 설치되지 않음")
    except Exception as e:
        print(f"⚠️ .env 파일 로드 실패: {e}")
    
    endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
    key = os.getenv('AZURE_SEARCH_KEY')
    
    print(f"AZURE_SEARCH_ENDPOINT: {endpoint if endpoint else '❌ 설정되지 않음'}")
    print(f"AZURE_SEARCH_KEY: {'✅ 설정됨' if key else '❌ 설정되지 않음'}")
    
    if not endpoint or not key:
        print("\n❌ 필수 환경변수가 설정되지 않았습니다.")
        print(f".env 파일({env_file})에 다음 항목들을 추가해주세요:")
        print("AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net")
        print("AZURE_SEARCH_KEY=your_search_admin_key")
        return False
    return True

def main():
    print("🔄 Azure AI Search 인덱스 생성 테스트 시작...\n")
    
    # 환경변수 테스트
    if not test_environment():
        return False
    
    try:
        # 클라이언트 초기화
        print("🔄 Azure AI Search 클라이언트 초기화 중...")
        search_client = AzureSearchClient()
        print("✅ Azure AI Search 클라이언트 초기화 성공\n")
        
        # 코딩 컨벤션 인덱스 생성
        print("🔄 코딩 컨벤션 인덱스 생성 중...")
        if search_client.create_conventions_index():
            print("✅ 코딩 컨벤션 인덱스 생성 성공")
        else:
            print("❌ 코딩 컨벤션 인덱스 생성 실패")
            return False
        
        # 환경 설정 템플릿 인덱스 생성
        print("🔄 환경 설정 템플릿 인덱스 생성 중...")
        if search_client.create_templates_index():
            print("✅ 환경 설정 템플릿 인덱스 생성 성공")
        else:
            print("❌ 환경 설정 템플릿 인덱스 생성 실패")
            return False
        
        print("\n🎉 모든 인덱스 생성 완료!")
        print("📍 Azure Portal > AI Search 서비스 > 인덱스에서 확인 가능합니다.")
        print("\n✅ 다음 단계: 샘플 데이터 업로드를 진행하세요!")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("\n🔍 가능한 원인:")
        print("1. Azure Search 서비스가 생성되지 않음")
        print("2. API 키가 잘못됨")
        print("3. 네트워크 연결 문제")
        print("4. Azure 구독 권한 문제")
        import traceback
        print(f"\n🐛 상세 오류:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ 문제가 발생했습니다. 위의 확인 사항을 점검해주세요.")
        sys.exit(1)