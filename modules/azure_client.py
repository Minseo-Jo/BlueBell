"""
Azure OpenAI 클라이언트 모듈
개발 환경 분석 및 코드 리뷰를 위한 AI 통신 담당
"""

import os
from typing import Dict, List, Optional
from openai import AzureOpenAI
from dotenv import load_dotenv
import logging

# 환경 변수 로드
load_dotenv()

# 로깅 설정 (모듈 단위로 로그 관리 기능)
logging.basicConfig(level=logging.INFO) # 로그 레벨을 INFO(일반적인 정보 메시지)로 설정
logger = logging.getLogger(__name__) # 특정 이름을 가진 로거 객체 생성 (__name_은 현재 모듈(파일 기반)의 이름으로 생성)

class AzureOpenAIClient:
    """
    Azure OpenAI와 통신하는 클라이언트
    """

    def __init__(self):
        """
        클라이언트 초기화
        """
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.api_type = os.getenv("AZURE_OPENAI_API_TYPE")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")


        # 필수 환경변수 확인
        self._validate_config()

        # Azure OpenAI 클라이언트 생성
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version=self.api_version
        )
        logger.info("Azure OpenAI 클라이언트 초기화 완료")

    def _validate_config(self):
        """
        환경변수 검증
        """

        required_vars = {
            "AZURE_OPENAI_API_KEY": self.api_key,
            "AZURE_OPENAI_ENDPOINT": self.endpoint,
            "AZURE_OPENAI_API_VERSION": self.api_version,
            "AZURE_OPENAI_API_TYPE": self.api_type,
            "AZURE_OPENAI_DEPLOYMENT_NAME": self.deployment_name
        }

        missing_vars = [var for var, value in required_vars.items() if not value]
        # 잘못 지정된 변수값도 함께 체크
        if missing_vars:
            raise ValueError(f"필수 환경 변수가 없습니다 : {', ' .join(missing_vars)}")
        

    # chatgpt api 래퍼
    def get_completion(
       self,
       messages : List[Dict[str, str]],
       temperature : float = 0.7,
       max_tokens : int = 2000,
       top_p: float = 0.95     
    ) -> str :
        """
        ChatGPT 응답 생성
        
        Args(대화메시지 + 파라미터) :
            messages : 대화 메시지 리스트
            temperatture : 창의성 정도 (0.0~1.0)
            max_tokens : 최대 토큰 수
            top_p : 토큰 선택 확률
        Returns :
            생성된 응답 텍스트
            
        """

        try : 
            response = self.client.chat.completions.create(
                model = self.deployment_name,
                messages = messages,
                temperature =  temperature,
                max_tokens = max_tokens,
                top_p = top_p
            )
            return response.choices[0].message.content
        except Exception as e :
            logger.error(f"API 호출 오류 : {str(e)}")
            return f"오류가 발생했습니다. {str(e)}"
        
    def analyze_readme(self, readme_content : str, os_type : str = "all") -> str :
        """
        README 파일을 분석하여 환경 설정 가이드 생성

        Args :
            readme_content : README 파일 내용
            os_type : 대상 운영체제 (all, windows, linux, macos)

        Returns :
            생성된 환경설정 가이드
        
        """

        system_prompt = """당신은 숙련된 DevOps 엔지니어입니다.
        주어진 README 파일을 분석하여 개발자가 빠르게 프로젝트를 시작할 수 있는
        상세한 환경 설정 가이드를 작성해주세요.

        포함해야 할 내용 :
        1. 필수 소프트웨어 설치
        2. 프로젝트 클론 및 설정
        3. 의존성 패키지 설치
        4. 환경변수 설정
        5. 실행 방법
        6. 자주 발생하는 문제와 해결법                 
        """
                        
        user_prompt = f"""
        다음의 README를 분석하여 {os_type} 운영체제용 환경설정 가이드를 작성해주세요 :

        {readme_content[:3000]} #토큰 제한
        """

        messages = [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]

        return self.get_completion(messages, temperature=0.3)
    

    def review_code(self, code: str, language : str = "auto") -> str :
        """
        코드 스타일 검사 및 개선 제안

        Args :
            code : 검사할 코드
            language : 프로그래밍 언어
        Returns :
            코드 리뷰 결과
        """
        system_prompt = """당신은 경험 많은 코드 리뷰어입니다.
        주어진 코드를 분석하여 다음 항목들을 검사하고 개선사항을 제안해주세요:
        
        1. 네이밍 컨벤션
        2. 코드 구조와 가독성
        3. 잠재적 버그
        4. 성능 개선 가능 부분
        5. 보안 취약점

        건설적이고 교육적인 톤으로 피드백을 제공해주세요.
        """

        user_prompt = f"""
        다음 {language} 코드를 검토해주세요 :

        '''{language}
        {code[:2000]} #토큰 제한
        '''
        """

        messages = [
            {"role" : "system", "content" : system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]

        return self.get_completion(messages, temperature=0.3)
    

def test_connection():
    """연결 테스트"""
    try:
        client = AzureOpenAIClient()
        response = client.get_completion([
            {"role": "user", "content": "Hello, Azure OpenAI!"}
        ])
        print(f"✅ 연결 성공!\n응답: {response}")
        return True
    except Exception as e:
        print(f"❌ 연결 실패: {e}")
        return False

if __name__ == "__main__":
    # azure_client 모듈 직접 실행 시 테스트
    test_connection()

