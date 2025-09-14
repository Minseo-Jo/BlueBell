import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class SetupAnalyzer:
    """
    README 파일을 분석하여 환경 설정 가이드를 생성하는 클래스
    """
    # 객체 생성자 
    def __init__(self, azure_client):
        """
        초기화
        
        Args:
            azure_client: AzureOpenAIClient 인스턴스
        """
        # 객체 생성시 azure_client 주입 -> SetupAnalyzer 안의 다른 메서드들이 언제든 self.azure_client 사용가능
        self.azure_client = azure_client
        
    def generate_guide(self, readme_content: str, os_type: str = "all") -> str:
        """
        README 파일 내용을 분석하여 개발 환경 세팅 가이드 생성
        Args :
            readme_content : README 파일 내용
            os_type : 타겟 OS (all, windows, mac, linux)
        
        Returns:
            생성된 개발 환경 세팅 가이드
        """
        try :
            #Azure OpenAI를 사용하여 가이드 생성
            guide = self.azure_client.analyze_readme(readme_content, os_type)

            # 포맷팅 개선
            guide = self._format_guide(guide, os_type)

            return guide
        
        except Exception as e:
            logger.error(f"가이드 생성 오류 :{str(e)}")
            return self._generate_fallback_guide(readme_content, os_type)
        
    def _format_guide(self, guide: str, os_type : str) -> str :
        """
        생성된 가이드 포맷 개선 
        
        Args :
            guide : 원본 가이드
            os_type : OS 타입

        Returns :
            포맷팅된 가이드
        """
        os_icons = {
            "all" : "🌎",
            "windows" : "🪟",
            "linux" : "🐧",
            "macos" : "🍎"
        }
        # 키가 없으면 기본값 "🖥️"
        icon = os_icons.get(os_type, "🖥️")

        # 헤더 추가
        formatted_guide = f"# {icon} 개발 환경 설정 가이드\n\n"
        formatted_guide += guide

        # 코드 블록 포맷팅
        formatted_guide = re.sub(r'```(\w+)', r'```\1', formatted_guide)
        
        return formatted_guide

    def _generate_fallback_guide(self, readme_content : str, os_type : str) -> str :
        """
        API 오류 시 기본 가이드 생성

        Args :
            readme_content : README 내용
            os_type : OS 타입

        Returns :
            기본 가이드
        """

    # 기본 프로그래밍 언어 감지
        language = self._detect_language(readme_content)

        guide = f""" 개발 환경 설정 가이드
## ℹ️ 감지된 정보 
- **주요 언어 :** {language}
- **대상 OS :** {os_type}

## ⚙️ 기본 설정 단계

### 1. 저장소 클론
```bash
git clone [repository_url]
cd [project-directory] 
```

### 2. 의존성 설치
"""
        if language == "Python" :
            guide += """

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
venv\\Scripts\\activate  # Windows

# 패키지 설치
pip install -r requirements.txt
```
"""
        elif language == "JavaScript" :
            guide += """
```bash
# npm 사용
npm install

# 또는 yarn 사용
yarn install
```
"""
        elif language == "Java" :
            guide += """
```bash
# Maven
mvn install

# 또는 Gradle
gradle build
```
"""

        guide += """
### 3. 환경변수 설정
`.env.example` 파일을 `.env`로 복사하고 필요한 값을 설정하세요.

### 4. 실행
프로젝트 README를 참고하여 실행하세요.

## ⚠️ 주의사항
이것은 기본 가이드입니다. 자세한 내용은 프로젝트 README를 참고하세요.
"""
        return guide


    def _detect_language(self, readme_content : str) -> str :
        """
        README 에서 주요 프로그래밍 언어 감지
        
        Args :
            readme_content : README 내용
            
        Returns :
            감지된 언어
        """

        content_lower = readme_content.lower()
    
        # 언어별 키워드
        language_keywords = {
            "Python" : ["python", "pip", "requirements.txt", "venv", "django", "flask", "fastapi"],
            "JavaScript" : ["javascript", "node", "npm", "yarn", "package.json", "react", "vue", "angular"],
            "Java" : ["java", "maven", "gradle", "spring", "jdk"],
            "C#" : ["c#", "csharp", ".net", "nuget"],
            "Go" : ["go", "golang", "gopath", "go.mod", "go mod"],
            "TypeScript" : ["typescript", "tsconfig.json", "ts", "tsx"]
        }

        for language, keywords in language_keywords.items() :
            if any(keyword in content_lower for keyword in keywords):
                return language
        return "Unknown"
        
