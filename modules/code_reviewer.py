"""
코드 리뷰 및 스타일 검사 모듈
"""

import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CodeReviewer:
    """
    코드를 분석하고 개선 사항을 제안하는 클래스
    """
    
    def __init__(self, azure_client, rag_service=None):
        """
        초기화
        
        Args:
            azure_client: AzureOpenAIClient 인스턴스
            rag_service: RAGService 인스턴스 (선택사항)
        """
        self.azure_client = azure_client
        self.rag_service = rag_service
        
        # 언어별 네이밍 규칙
        self.naming_conventions = {
            "python": {
                "function": "snake_case",
                "class": "PascalCase",
                "variable": "snake_case",
                "constant": "UPPER_SNAKE_CASE"
            },
            "javascript": {
                "function": "camelCase",
                "class": "PascalCase",
                "variable": "camelCase",
                "constant": "UPPER_SNAKE_CASE"
            },
            "java": {
                "function": "camelCase",
                "class": "PascalCase",
                "variable": "camelCase",
                "constant": "UPPER_SNAKE_CASE"
            }
        }
    
    def review(self, code: str, language: str = "auto", options: Dict = None) -> str:
        """
        코드 리뷰 수행
        
        Args:
            code: 리뷰할 코드
            language: 프로그래밍 언어
            options: 리뷰 옵션
            
        Returns:
            리뷰 결과
        """
        try:
            # 기본 옵션 설정
            if options is None:
                options = {
                    'check_naming': True,
                    'check_structure': True,
                    'check_bugs': True,
                    'check_performance': True,
                    'check_security': True,
                    'suggest_refactoring': True
                }
            
            # 언어 자동 감지
            if language == "auto":
                language = self._detect_language(code)
        
            # RAG 서비스가 있으면 RAG 사용, 없으면 기본 방식
            if self.rag_service:
                logger.info("RAG 서비스를 사용하여 코드 리뷰")
                result = self.rag_service.enhance_code_review(code, language)
                
                if result["success"]:
                    # RAG 결과 포맷팅
                    formatted_result = self._format_rag_review_result(result, language)
                    return formatted_result
                else:
                    logger.warning("RAG 실패, 기본 방식으로 폴백")
                    # 폴백: 기본 방식
                    return self._perform_basic_review(code, language, options)
            else:
                logger.info("기본 방식으로 코드 리뷰")
                # 기본 방식
                return self._perform_basic_review(code, language, options)
            
        except Exception as e:
            logger.error(f"코드 리뷰 실패: {str(e)}")
            return self._generate_basic_review(code, language)
        

    def _perform_basic_review(self, code: str, language: str, options: Dict) -> str:
        """기본 코드 리뷰 수행"""
        # 맞춤형 프롬프트 생성
        prompt = self._create_review_prompt(code, language, options)
        
        # Azure OpenAI를 사용하여 리뷰 수행
        review_result = self._perform_ai_review(prompt, code, language)
        
        # 포맷팅 및 추가 분석
        formatted_result = self._format_review_result(review_result, language)
        
        return formatted_result
    
    def _format_rag_review_result(self, rag_result: Dict, language: str) -> str:
        """RAG 결과를 포맷팅"""
        formatted = f"""#### 📝 코드 리뷰 결과

    **언어**: {language}
    **리뷰 일시**: {self._get_current_time()}

    ---

    {rag_result["review"]}


    📚 참조된 코딩 컨벤션

    """
        
        # 참조된 컨벤션 정보 추가
        if rag_result["referenced_conventions"]:
            for i, conv in enumerate(rag_result["referenced_conventions"], 1):
                formatted += f"**{i}. {conv['title']}**\n"
                formatted += f"- 언어: {conv.get('language', 'N/A')}\n"
                formatted += f"- 태그: {', '.join(conv.get('tags', []))}\n\n"
        else:
            formatted += "참조된 컨벤션이 없습니다.\n\n"
        
        # 감지된 패턴 정보
        if rag_result["patterns_found"]:
            formatted += f"""## 🔍 감지된 코드 패턴

    **발견된 패턴**: {', '.join(rag_result["patterns_found"])}

    """
        
        formatted += """###### 📊 요약

    이 리뷰는 AI 기반 자동 분석 + RAG 검색 결과입니다.
    관련 코딩 컨벤션을 참조하여 더 정확한 피드백을 제공했습니다.

    ### 다음 단계
    1. 🔴 심각한 문제부터 수정
    2. 🟡 주의 사항 검토
    3. 🟢 권장 사항은 시간이 있을 때 적용

    ---

    *Generated by DevPilot with RAG*
    """
        
        return formatted
        
    def _create_review_prompt(self, code: str, language: str, options: Dict) -> str:
        """
        리뷰 프롬프트 생성
        
        Args:
            code: 코드
            language: 언어
            options: 옵션
            
        Returns:
            프롬프트
        """
        prompt = f"""당신은 {language} 전문 코드 리뷰어입니다.
다음 코드를 분석하고 개선 사항을 제안해주세요.

리뷰 항목:
"""
        
        if options.get('check_naming'):
            prompt += "- 네이밍 컨벤션 (변수명, 함수명, 클래스명)\n"
        if options.get('check_structure'):
            prompt += "- 코드 구조와 가독성\n"
        if options.get('check_bugs'):
            prompt += "- 잠재적 버그 및 에러 처리\n"
        if options.get('check_performance'):
            prompt += "- 성능 최적화 가능 부분\n"
        if options.get('check_security'):
            prompt += "- 보안 취약점\n"
        if options.get('suggest_refactoring'):
            prompt += "- 리팩토링 제안\n"
        
        prompt += """
각 항목에 대해 구체적인 예시와 개선 코드를 제시해주세요.
심각도를 🔴 (심각), 🟡 (주의), 🟢 (권장) 로 표시해주세요.
"""
        
        return prompt
    
    def _perform_ai_review(self, prompt: str, code: str, language: str) -> str:
        """
        AI를 사용한 코드 리뷰
        
        Args:
            prompt: 프롬프트
            code: 코드
            language: 언어
            
        Returns:
            리뷰 결과
        """
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"다음 {language} 코드를 리뷰해주세요:\n\n```{language}\n{code[:2000]}\n```"}
        ]
        
        return self.azure_client.get_completion(messages, temperature=0.3)
    
    def _format_review_result(self, review_result: str, language: str) -> str:
        """
        리뷰 결과 포맷팅
        
        Args:
            review_result: 원본 리뷰 결과
            language: 언어
            
        Returns:
            포맷팅된 결과
        """
        formatted = f"""#### 📝 코드 리뷰 결과

**언어**: {language}
**리뷰 일시**: {self._get_current_time()}

---

{review_result}

---

## 📊 요약

이 리뷰는 AI 기반 자동 분석 결과입니다. 
실제 프로젝트 컨텍스트에 따라 일부 제안사항은 적용하지 않아도 됩니다.

### 다음 단계
1. 🔴 심각한 문제부터 수정
2. 🟡 주의 사항 검토
3. 🟢 권장 사항은 시간이 있을 때 적용

---

*Generated by DevPilot*
"""
        
        return formatted
    
    def _generate_basic_review(self, code: str, language: str) -> str:
        """
        기본 리뷰 생성 (API 오류 시)
        
        Args:
            code: 코드
            language: 언어
            
        Returns:
            기본 리뷰
        """
        lines = code.split('\n')
        
        review = f"""#### 📝 기본 코드 리뷰 결과

**언어**: {language}
**코드 라인 수**: {len(lines)}

## 기본 분석

### 📏 코드 메트릭스
- 총 라인 수: {len(lines)}
- 빈 라인 수: {sum(1 for line in lines if not line.strip())}
- 주석 라인 수: {self._count_comments(code, language)}

### 🔍 기본 검사 항목

#### 네이밍 컨벤션
"""
        
        # 언어별 기본 체크
        if language.lower() == "python":
            review += """
- ✅ 함수명은 snake_case 사용 권장
- ✅ 클래스명은 PascalCase 사용 권장
- ✅ 상수는 UPPER_SNAKE_CASE 사용 권장
"""
        elif language.lower() in ["javascript", "java"]:
            review += """
- ✅ 함수명은 camelCase 사용 권장
- ✅ 클래스명은 PascalCase 사용 권장
- ✅ 상수는 UPPER_SNAKE_CASE 사용 권장
"""
        
        review += """
#### 일반 권장사항
- 함수는 한 가지 일만 수행하도록 작성
- 중복 코드 제거
- 매직 넘버 대신 상수 사용
- 적절한 에러 처리 추가
- 주석으로 복잡한 로직 설명

## ⚠️ 참고
API 연결 문제로 간단한 분석만 제공됩니다.
전체 리뷰를 원하시면 다시 시도해주세요.
"""
        
        return review
    
    def _detect_language(self, code: str) -> str:
        """
        코드에서 언어 자동 감지
        
        Args:
            code: 코드
            
        Returns:
            감지된 언어
        """
        # 언어별 특징적인 패턴
        patterns = {
            "python": [r"def\s+\w+\s*\(", r"import\s+\w+", r"if\s+__name__\s*==\s*['\"]__main__['\"]"],
            "javascript": [r"function\s+\w+\s*\(", r"const\s+\w+\s*=", r"console\.log"],
            "java": [r"public\s+class\s+\w+", r"public\s+static\s+void\s+main", r"System\.out\.println"],
            "csharp": [r"using\s+System", r"namespace\s+\w+", r"public\s+class\s+\w+"],
            "go": [r"package\s+\w+", r"func\s+\w+\s*\(", r"import\s+\("],
            "typescript": [r"interface\s+\w+", r"type\s+\w+\s*=", r"const\s+\w+:\s*\w+"]
        }
        
        for language, language_patterns in patterns.items():
            for pattern in language_patterns:
                if re.search(pattern, code):
                    return language
        
        return "unknown"
    
    def _count_comments(self, code: str, language: str) -> int:
        """
        주석 라인 수 계산
        
        Args:
            code: 코드
            language: 언어
            
        Returns:
            주석 라인 수
        """
        comment_patterns = {
            "python": r"^\s*#",
            "javascript": r"^\s*//",
            "java": r"^\s*//",
            "csharp": r"^\s*//",
            "go": r"^\s*//"
        }
        
        pattern = comment_patterns.get(language.lower(), r"^\s*//")
        lines = code.split('\n')
        
        return sum(1 for line in lines if re.match(pattern, line))
    
    def _get_current_time(self) -> str:
        """
        현재 시간 반환
        
        Returns:
            포맷팅된 현재 시간
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")