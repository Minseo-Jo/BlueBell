"""
RAG (Retrieval-Augmented Generation) 서비스
코딩 컨벤션과 환경 설정 템플릿을 검색하여 AI 응답에 통합
"""

import re
from typing import Dict, List, Optional, Tuple
from modules.azure_search_client import AzureSearchClient
from modules.azure_client import AzureOpenAIClient
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """
    검색 증강 생성 서비스
    Azure AI Search + Azure OpenAI 통합
    """
    
    def __init__(self, azure_client: AzureOpenAIClient, search_client: AzureSearchClient):
        """
        초기화
        
        Args:
            azure_client: Azure OpenAI 클라이언트
            search_client: Azure AI Search 클라이언트
        """
        self.azure_client = azure_client
        self.search_client = search_client
        
    def enhance_code_review(
        self,
        code: str,
        language: str,
        company: str = "ktds"
    ) -> Dict[str, any]:
        """
        RAG를 사용한 코드 리뷰 개선
        
        Args:
            code: 리뷰할 코드
            language: 프로그래밍 언어
            company: 회사명 (컨벤션 필터용)
            
        Returns:
            향상된 코드 리뷰 결과 딕셔너리
        """
        try:
            # 1. 코드에서 패턴 및 키워드 추출
            patterns = self._extract_code_patterns(code, language)
            logger.info(f"추출된 패턴: {patterns}")
            
            # 2. 관련 코딩 컨벤션 검색
            conventions = self._search_relevant_conventions(
                patterns, language, company
            )
            logger.info(f"검색된 컨벤션: {len(conventions)}개")
            
            # 3. 컨벤션 정보를 포함한 향상된 프롬프트 생성
            enhanced_prompt = self._create_enhanced_review_prompt(
                code, language, conventions
            )
            
            # 4. AI 리뷰 생성
            review_result = self.azure_client.get_completion(
                enhanced_prompt, temperature=0.3
            )
            
            # 5. 결과 포맷팅
            return {
                "review": review_result,
                "referenced_conventions": conventions,
                "patterns_found": patterns,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"RAG 코드 리뷰 실패: {str(e)}")
            # 폴백: 기본 코드 리뷰
            fallback_review = self.azure_client.review_code(code, language)
            return {
                "review": fallback_review,
                "referenced_conventions": [],
                "patterns_found": [],
                "success": False,
                "error": str(e)
            }
    
    def enhance_setup_guide(
        self,
        readme_content: str,
        os_type: str = "all"
    ) -> Dict[str, any]:
        """
        RAG를 사용한 환경 설정 가이드 개선
        
        Args:
            readme_content: README 파일 내용
            os_type: 타겟 OS
            
        Returns:
            향상된 환경 설정 가이드 딕셔너리
        """
        try:
            # 1. README에서 기술 스택 추출
            tech_stack = self._extract_tech_stack(readme_content)
            logger.info(f"추출된 기술 스택: {tech_stack}")
            
            # 2. 관련 환경 설정 템플릿 검색
            templates = self._search_relevant_templates(
                tech_stack, os_type
            )
            logger.info(f"검색된 템플릿: {len(templates)}개")
            
            # 3. 템플릿 정보를 포함한 향상된 프롬프트 생성
            enhanced_prompt = self._create_enhanced_setup_prompt(
                readme_content, os_type, templates
            )
            
            # 4. AI 가이드 생성
            guide_result = self.azure_client.get_completion(
                enhanced_prompt, temperature=0.3
            )
            
            # 5. 결과 포맷팅
            return {
                "guide": guide_result,
                "referenced_templates": templates,
                "tech_stack_found": tech_stack,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"RAG 환경 설정 가이드 실패: {str(e)}")
            # 폴백: 기본 가이드 생성
            fallback_guide = self.azure_client.analyze_readme(readme_content, os_type)
            return {
                "guide": fallback_guide,
                "referenced_templates": [],
                "tech_stack_found": [],
                "success": False,
                "error": str(e)
            }
    
    def _extract_code_patterns(self, code: str, language: str) -> List[str]:
        """코드에서 리뷰 관련 패턴 추출"""
        patterns = []
        
        # 언어별 패턴 추출 규칙
        if language.lower() == "python":
            # 함수 정의
            if re.search(r'def\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(', code):
                patterns.append("function_naming")
            
            # 클래스 정의
            if re.search(r'class\s+[a-zA-Z_][a-zA-Z0-9_]*\s*[\(:]', code):
                patterns.append("class_naming")
            
            # Import 문
            if re.search(r'import\s+|from\s+.*\s+import', code):
                patterns.append("import_style")
            
            # 상수 (대문자)
            if re.search(r'[A-Z_]{2,}\s*=', code):
                patterns.append("constant_naming")
                
        elif language.lower() in ["javascript", "typescript"]:
            # 함수 선언
            if re.search(r'function\s+\w+|const\s+\w+\s*=.*=>', code):
                patterns.append("function_naming")
            
            # 클래스 정의
            if re.search(r'class\s+\w+', code):
                patterns.append("class_naming")
            
            # 변수 선언
            if re.search(r'(let|const|var)\s+\w+', code):
                patterns.append("variable_naming")
        
        # 공통 패턴
        if re.search(r'//.*|#.*|/\*.*\*/', code):
            patterns.append("comments")
        
        if re.search(r'console\.log|print\(|logger\.|logging\.', code):
            patterns.append("logging")
        
        if re.search(r'try\s*{|except\s|catch\s*\(', code):
            patterns.append("error_handling")
        
        return patterns
    
    def _search_relevant_conventions(
        self,
        patterns: List[str],
        language: str,
        company: str
    ) -> List[Dict]:
        """관련 코딩 컨벤션 검색"""
        try:
            # 패턴을 검색 쿼리로 변환
            query_terms = []
            pattern_queries = {
                "function_naming": "함수 네이밍 function naming",
                "class_naming": "클래스 네이밍 class naming",
                "variable_naming": "변수 네이밍 variable naming",
                "constant_naming": "상수 네이밍 constant naming",
                "import_style": "import 스타일 import style",
                "comments": "주석 스타일 comment style",
                "logging": "로깅 logging",
                "error_handling": "에러 처리 error handling"
            }
            
            for pattern in patterns:
                if pattern in pattern_queries:
                    query_terms.append(pattern_queries[pattern])
            
            query = " ".join(query_terms) if query_terms else f"{language} 코딩 컨벤션"
            
            # Azure AI Search에서 검색
            results = self.search_client.search_conventions(
                query=query,
                language=language if language != "auto" else None,
                top=3
            )
            
            return results
            
        except Exception as e:
            logger.error(f"컨벤션 검색 실패: {str(e)}")
            return []
    
    def _extract_tech_stack(self, readme_content: str) -> List[str]:
        """README에서 기술 스택 추출"""
        tech_stack = []
        content_lower = readme_content.lower()
        
        # 기술 스택 키워드 매칭
        tech_keywords = {
            "react": ["react", "jsx", "tsx"],
            "vue": ["vue", "vuejs"],
            "angular": ["angular"],
            "node": ["node", "nodejs", "npm", "yarn"],
            "python": ["python", "pip", "requirements.txt", "django", "flask", "fastapi"],
            "java": ["java", "maven", "gradle", "spring"],
            "docker": ["docker", "dockerfile", "docker-compose"],
            "typescript": ["typescript", "ts", "tsx"],
            "javascript": ["javascript", "js", "jsx"],
            "express": ["express", "expressjs"],
            "mongodb": ["mongodb", "mongo"],
            "postgresql": ["postgresql", "postgres"],
            "mysql": ["mysql"],
            "redis": ["redis"]
        }
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                tech_stack.append(tech)
        
        return tech_stack
    
    def _search_relevant_templates(
        self,
        tech_stack: List[str],
        os_type: str
    ) -> List[Dict]:
        """관련 환경 설정 템플릿 검색"""
        try:
            # 기술 스택을 검색 쿼리로 변환
            if tech_stack:
                query = " ".join(tech_stack) + " 환경 설정 setup"
            else:
                query = "프로젝트 환경 설정 project setup"
            
            # OS 타입 매핑
            os_map = {
                "전체": None,
                "Windows": "windows",
                "macOS": "macos",
                "Linux": "linux",
                "all": None
            }
            
            os_filter = os_map.get(os_type, None)
            
            # Azure AI Search에서 검색
            results = self.search_client.search_templates(
                query=query,
                tech_stack=tech_stack if tech_stack else None,
                os_type=os_filter,
                top=3
            )
            
            return results
            
        except Exception as e:
            logger.error(f"템플릿 검색 실패: {str(e)}")
            return []
    
    def _create_enhanced_review_prompt(
        self,
        code: str,
        language: str,
        conventions: List[Dict]
    ) -> List[Dict[str, str]]:
        """향상된 코드 리뷰 프롬프트 생성"""
        
        # 컨벤션 정보 요약
        conventions_text = ""
        if conventions:
            conventions_text = "\n\n참조할 코딩 컨벤션:\n"
            for i, conv in enumerate(conventions, 1):
                conventions_text += f"{i}. {conv['title']}\n"
                conventions_text += f"   {conv['content'][:200]}...\n"
        
        system_prompt = f"""당신은 {language} 전문 코드 리뷰어입니다.
주어진 코드를 분석하고 다음 컨벤션을 참조하여 개선 사항을 제안해주세요.
{conventions_text}

리뷰 항목:
- 네이밍 컨벤션 검사
- 코드 구조와 가독성
- 잠재적 버그 및 에러 처리
- 성능 최적화 가능 부분
- 보안 취약점

각 항목에 대해 구체적인 예시와 개선 코드를 제시해주세요.
심각도를 🔴 (심각), 🟡 (주의), 🟢 (권장) 로 표시해주세요."""

        user_prompt = f"다음 {language} 코드를 리뷰해주세요:\n\n```{language}\n{code[:2000]}\n```"

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def _create_enhanced_setup_prompt(
        self,
        readme_content: str,
        os_type: str,
        templates: List[Dict]
    ) -> List[Dict[str, str]]:
        """향상된 환경 설정 가이드 프롬프트 생성"""
        
        # 템플릿 정보 요약
        templates_text = ""
        if templates:
            templates_text = "\n\n참조할 환경 설정 템플릿:\n"
            for i, template in enumerate(templates, 1):
                templates_text += f"{i}. {template['title']}\n"
                templates_text += f"   {template['content'][:300]}...\n"
        
        system_prompt = f"""당신은 숙련된 DevOps 엔지니어입니다.
주어진 README 파일을 분석하여 {os_type} 운영체제용 개발 환경 설정 가이드를 작성해주세요.
{templates_text}

포함해야 할 내용:
1. 필수 소프트웨어 설치
2. 프로젝트 클론 및 설정
3. 의존성 패키지 설치
4. 환경변수 설정
5. 실행 방법
6. 자주 발생하는 문제와 해결법

위의 참조 템플릿을 활용하여 더 구체적이고 실용적인 가이드를 만들어주세요."""

        user_prompt = f"다음 README를 분석하여 환경설정 가이드를 작성해주세요:\n\n{readme_content[:3000]}"

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

def test_rag_service():
    """RAG 서비스 테스트"""
    try:
        from modules.azure_client import AzureOpenAIClient
        from modules.azure_search_client import AzureSearchClient
        
        azure_client = AzureOpenAIClient()
        search_client = AzureSearchClient()
        rag_service = RAGService(azure_client, search_client)
        
        # 테스트 코드
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
        
        print("🧪 RAG 코드 리뷰 테스트...")
        result = rag_service.enhance_code_review(test_code, "python")
        
        if result["success"]:
            print("✅ RAG 코드 리뷰 성공!")
            print(f"참조된 컨벤션: {len(result['referenced_conventions'])}개")
        else:
            print("❌ RAG 코드 리뷰 실패, 폴백 사용")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG 서비스 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    test_rag_service()