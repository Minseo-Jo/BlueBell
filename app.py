"""
🧚‍♂️ BlueBell - 개발 환경 셋업 & 코드 스타일 자동화 도우미
"""

import streamlit as st
import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
BASE_DIR = Path(__file__).resolve().parent.parent  # .../dev-pilot
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from modules.azure_client import AzureOpenAIClient
from modules.setup_analyzer import SetupAnalyzer
from modules.code_reviewer import CodeReviewer

from modules.azure_search_client import AzureSearchClient  
from modules.rag_service import RAGService

st.set_page_config(
    page_title="BlueBell", 
    page_icon="🧚‍♂️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    /* 전역 스타일 */
    .main {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%);
    }
    
    /* 메인 헤더 */
    .brand-title {
        font-size: 3.5rem;
        font-weight: bold;
        color: #1e88e5;
        text-align: center !important;
        padding: 1.5rem 0;
        margin: 0 auto;
        text-shadow: 2px 2px 4px rgba(30, 136, 229, 0.3);
        width: 100%;
        display: block;
    }
    
    .brand-container {
        text-align: center !important;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* 서브 헤더 */
    .sub-header {
        text-align: center;
        color: #546e7a;
        margin-bottom: 2rem;
        font-size: 1.2rem;
        font-weight: 300;
    }
    
    /* 기능 카드 - 블루 테마 */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 5px solid #4285f4;
        box-shadow: 0 4px 12px rgba(66, 133, 244, 0.15);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(66, 133, 244, 0.25);
    }
    
    .feature-card h5 {
        color: #1e88e5;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: #546e7a;
        line-height: 1.6;
    }
    
    .feature-card ul {
        color: #37474f;
    }
    
    .feature-card li {
        margin: 0.5rem 0;
    }
    
    /* 성공 메시지 - 블루 톤 */
    .success-message {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 1px solid #90caf9;
        border-radius: 10px;
        padding: 1rem;
        color: #0d47a1;
        border-left: 4px solid #2196f3;
    }
    
    /* 에러 메시지 */
    .error-message {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border: 1px solid #ef9a9a;
        border-radius: 10px;
        padding: 1rem;
        color: #c62828;
        border-left: 4px solid #f44336;
    }
    
    /* 연결 상태 표시 */
    .connection-status {
        position: fixed;
        top: 10px;
        right: 20px;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.8rem;
        box-shadow: 0 2px 10px rgba(66, 133, 244, 0.2);
        z-index: 1000;
        border: 1px solid rgba(66, 133, 244, 0.3);
    }
    
    .connection-status.connected {
        color: #2e7d32;
        border-color: rgba(46, 125, 50, 0.3);
    }
    
    .connection-status.error {
        color: #d32f2f;
        border-color: rgba(211, 47, 47, 0.3);
    }
    
    /* 사이드바 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #4285f4 0%, #1e88e5 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(66, 133, 244, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(66, 133, 244, 0.4);
    }
    
    /* 파일 업로더 스타일 */
    .stFileUploader > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 2px dashed #90caf9;
        border-radius: 15px;
    }
    
    /* 텍스트 영역 스타일 */
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #90caf9;
        border-radius: 10px;
    }
    
    /* 선택 박스 스타일 */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #90caf9;
        border-radius: 10px;
    }
    
    /* 라디오 버튼 스타일 */
    .stRadio > div {
        background: rgba(66, 133, 244, 0.05);
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* 체크박스 스타일 */
    .stCheckbox > label {
        color: #37474f;
        font-weight: 500;
    }
    
    /* 푸터 스타일 */
    .footer {
        background: linear-gradient(135deg, #e3f2fd 0%, #ffffff 100%);
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(66, 133, 244, 0.2);
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%);
        border-radius: 10px;
        padding: 1rem;
        border-left: 3px solid #4285f4;
        box-shadow: 0 2px 8px rgba(66, 133, 244, 0.1);
    }
    
    /* 스피너 색상 변경 */
    .stSpinner > div {
        border-top-color: #4285f4 !important;
    }
    
    /* 경고 메시지 스타일 */
    .stWarning {
        background: linear-gradient(135deg, #fff8e1 0%, #ffecb3 100%);
        border-left: 4px solid #ffa726;
    }
    
    /* 정보 메시지 스타일 */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #42a5f5;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """세션 상태 초기화 함수"""
    if 'azure_client' not in st.session_state:
        try:
            st.session_state.azure_client = AzureOpenAIClient()
            st.session_state.client_status = "connected"
        except Exception as e:
            st.session_state.client_status = f"error: {str(e)}"
            st.session_state.azure_client = None  # 실패 시 None 설정

    # Azure Search 클라이언트 초기화
    if 'search_client' not in st.session_state:
        try:
            if st.session_state.azure_client is not None:
                st.session_state.search_client = AzureSearchClient()
                st.session_state.search_status = "connected"
            else:
                st.session_state.search_status = "azure_client_failed"
        except Exception as e:
            st.session_state.search_status = f"error: {str(e)}"
            st.session_state.search_client = None

    # RAG 서비스 초기화
    if 'rag_service' not in st.session_state:
        try:
            if (st.session_state.azure_client is not None and 
                st.session_state.search_client is not None):
                st.session_state.rag_service = RAGService(
                    st.session_state.azure_client,
                    st.session_state.search_client
                )
                st.session_state.rag_status = "connected"
            else:
                st.session_state.rag_status = "dependencies_failed"
                st.session_state.rag_service = None
        except Exception as e:
            st.session_state.rag_status = f"error: {str(e)}"
            st.session_state.rag_service = None

    # 기존 분석기들 초기화 (RAG 서비스 포함)
    if ('setup_analyzer' not in st.session_state and 
        'azure_client' in st.session_state and 
        st.session_state.azure_client is not None):
        st.session_state.setup_analyzer = SetupAnalyzer(
            st.session_state.azure_client,
            st.session_state.rag_service  # RAG 서비스 추가
        )

    if ('code_reviewer' not in st.session_state and 
        'azure_client' in st.session_state and 
        st.session_state.azure_client is not None):
        st.session_state.code_reviewer = CodeReviewer(
            st.session_state.azure_client,
            st.session_state.rag_service  # RAG 서비스 추가
        )

def show_connection_status():
    """연결 상태를 우아하게 표시하는 함수 - 오류가 있을 때만 표시"""
    if st.session_state.client_status != "connected":
        # 오류가 있을 때만 상단에 경고 표시
        st.markdown("""
        <div class="connection-status error">
            ⚠️ Azure 서비스 연결 오류
        </div>
        """, unsafe_allow_html=True)
        
        # 확장 가능한 상세 오류 정보
        with st.expander("🔧 연결 상태 확인", expanded=False):
            st.error(f"❌ Azure OpenAI 연결 실패: {st.session_state.client_status}")
            st.info("""
            **해결 방법:**
            1. `.env` 파일의 Azure 설정을 확인해주세요
            2. API 키와 엔드포인트가 올바른지 확인해주세요
            3. 네트워크 연결을 확인해주세요
            """)
        
def main():
    # 세션 상태 초기화
    initialize_session_state()
    
    # 헤더 - 새로운 브랜딩
    st.markdown('<h1 class="brand-title">🧚‍♂️ BlueBell</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">개발 환경 셋업 & 코드 스타일 자동화 도우미</p>', unsafe_allow_html=True)

    # 연결 상태 표시 (오류가 있을 때만)
    show_connection_status()

    # 사이드바
    with st.sidebar:
        st.markdown("#### 기능 선택")
        feature = st.radio(
            "",
            ["🏠 홈", "⚙️ 개발 환경 설정", "🔍 코드 리뷰", "ℹ️ 정보"],
            index=0,
            label_visibility="collapsed" 
        )
        
    # 메인 컨텐츠
    if feature == "🏠 홈":
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card">
            <h5>⚙️ 개발 환경 설정</h5>
            <p>README 파일을 분석하여 맞춤 개발 환경 설정 가이드를 생성합니다.</p>
            <ul>
                <li>필수 소프트웨어 설치 명령어</li>
                <li>의존성 패키지 설치</li>
                <li>환경변수 설정</li>
                <li>실행 방법</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card">
            <h5>🔍 코드 리뷰</h5>
            <p>코드를 분석하여 사내/고객사에 맞춤화된 코드 개선 사항을 제안합니다.</p>
            <ul>
                <li>네이밍 컨벤션 검사</li>
                <li>코드 구조 분석</li>
                <li>잠재적 버그 탐지</li>
                <li>성능 개선 제안</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 빠른 시작
        st.markdown("### 🚀 빠른 시작")
        quick_action = st.selectbox(
            "무엇을 도와드릴까요?",
            ["선택하세요", "개발 환경 설정", "코드 리뷰"]
        )
        
        if quick_action == "개발 환경 설정":
            st.info("⚙️ 개발 환경 설정 탭으로 이동하여 README 파일을 업로드해주세요.")
        elif quick_action == "코드 리뷰":
            st.info("🔍 코드 리뷰 탭으로 이동하여 코드 및 파일을 업로드해주세요.")

    elif feature == "⚙️ 개발 환경 설정":
        st.markdown("## ⚙️ 개발 환경 설정")
        st.markdown("프로젝트의 README 파일을 분석하여 OS별 환경 설정 가이드를 생성합니다.")
        
        # 입력 방법 선택
        input_method = st.radio(
            "입력 방법 선택",
            ["📁 파일 업로드", "✏️ 텍스트 직접 입력"]
        )
        
        readme_content = None
        
        if input_method == "📁 파일 업로드":
            uploaded_file = st.file_uploader(
                "README 파일을 업로드하세요",
                type=['md', 'txt', 'rst'],
                help="README.md, README.txt, README.rst 파일을 지원합니다."
            )
            
            if uploaded_file:
                readme_content = uploaded_file.read().decode('utf-8')
                with st.expander("📄 업로드된 내용 미리보기"):
                    st.text(readme_content[:1000] + "..." if len(readme_content) > 1000 else readme_content)
        
        elif input_method == "✏️ 텍스트 직접 입력":
            readme_content = st.text_area(
                "README 내용을 입력하세요",
                height=300,
                placeholder="프로젝트의 README 내용을 여기에 붙여넣으세요..."
            )
        
        # OS 선택
        target_os = st.selectbox(
            "타겟 운영체제",
            ["전체", "Windows", "macOS", "Linux"],
            help="특정 OS를 선택하면 해당 OS에 맞춤화된 가이드를 생성합니다."
        )
        
        # 가이드 생성 버튼
        if st.button("가이드 생성", type="primary"):
            if readme_content:
                with st.spinner("🧚‍♂️ BlueBell이 README를 분석하고 있습니다... (약 10-15초)"):
                    try:
                        # OS 타입 매핑
                        os_map = {
                            "전체": "all",
                            "Windows": "windows",
                            "macOS": "macos",
                            "Linux": "linux"
                        }
                        
                        # 가이드 생성
                        guide = st.session_state.setup_analyzer.generate_guide(
                            readme_content,
                            os_type=os_map[target_os]
                        )
                        
                        st.success("✨ 환경 설정 가이드가 생성되었습니다!")
                        
                        # 결과 표시
                        st.markdown("### 📋 생성된 가이드")
                        st.markdown(guide)
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="📥 가이드 다운로드 (Markdown)",
                            data=guide,
                            file_name=f"setup_guide_{os_map[target_os]}.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ 가이드 생성 중 오류가 발생했습니다: {str(e)}")
            else:
                st.warning("⚠️ README 내용을 입력해주세요.")

    elif feature == "🔍 코드 리뷰":
        st.markdown("## 🔍 코드 리뷰")
        st.markdown("코드를 분석하여 개선 사항을 제안합니다.")
        
        # 입력 방법 선택
        input_method = st.radio(
            "코드 입력 방법",
            ["✏️ 직접 입력", "📁 파일 업로드"]
        )
        
        code_content = None
        language = "자동 감지"
        
        if input_method == "✏️ 직접 입력":
            language = st.selectbox(
                "프로그래밍 언어",
                ["자동 감지", "Python", "JavaScript", "Java", "C#", "Go", "TypeScript"]
            )
            
            code_content = st.text_area(
                "코드를 입력하세요",
                height=400,
                placeholder="리뷰 받을 코드를 여기에 붙여넣으세요..."
            )
        
        elif input_method == "📁 파일 업로드":
            uploaded_file = st.file_uploader(
                "코드 파일을 업로드하세요",
                type=['py', 'js', 'java', 'cs', 'go', 'ts', 'jsx', 'tsx'],
                help="Python, JavaScript, Java, C#, Go, TypeScript 파일을 지원합니다."
            )
            
            if uploaded_file:
                code_content = uploaded_file.read().decode('utf-8')
                # 파일 확장자로 언어 감지
                ext = uploaded_file.name.split('.')[-1]
                language_map = {
                    'py': 'Python',
                    'js': 'JavaScript',
                    'jsx': 'JavaScript',
                    'ts': 'TypeScript',
                    'tsx': 'TypeScript',
                    'java': 'Java',
                    'cs': 'C#',
                    'go': 'Go'
                }
                language = language_map.get(ext, "자동 감지")
                
                with st.expander("👀 업로드된 코드 미리보기"):
                    st.code(code_content[:1000] + "..." if len(code_content) > 1000 else code_content, language=language.lower())
        
        # 리뷰 옵션
        st.markdown("#### 📝 리뷰 옵션")
        col1, col2 = st.columns(2)
        
        with col1:
            check_naming = st.checkbox("네이밍 컨벤션 검사", value=True)
            check_structure = st.checkbox("코드 구조 분석", value=True)
            check_bugs = st.checkbox("잠재적 버그 탐지", value=True)
        
        with col2:
            check_performance = st.checkbox("성능 개선", value=True)
            check_security = st.checkbox("보안 취약점 검사", value=True)
            suggest_refactoring = st.checkbox("리팩토링", value=True)
        
        # 코드 리뷰 버튼
        if st.button("코드 리뷰 시작", type="primary"):
            if code_content:
                with st.spinner("🧚‍♂️ BlueBell이 코드를 분석하고 있습니다... (약 10-15초)"):
                    try:
                        # 언어 매핑
                        lang_map = {
                            "자동 감지": "auto",
                            "Python": "python",
                            "JavaScript": "javascript",
                            "Java": "java",
                            "C#": "csharp",
                            "Go": "go",
                            "TypeScript": "typescript"
                        }
                        
                        # 리뷰 옵션 설정
                        options = {
                            'check_naming': check_naming,
                            'check_structure': check_structure,
                            'check_bugs': check_bugs,
                            'check_performance': check_performance,
                            'check_security': check_security,
                            'suggest_refactoring': suggest_refactoring
                        }
                        
                        # 코드 리뷰 실행
                        review_result = st.session_state.code_reviewer.review(
                            code_content,
                            language=lang_map[language],
                            options=options
                        )
                        
                        st.success("✨ 코드 리뷰가 완료되었습니다!")
                        
                        # 결과 표시
                        st.markdown("### 📋 리뷰 결과")
                        st.markdown(review_result)
                        
                        # 다운로드 버튼
                        st.download_button(
                            label="📥 리뷰 결과 다운로드",
                            data=review_result,
                            file_name="code_review_result.md",
                            mime="text/markdown"
                        )
                        
                    except Exception as e:
                        st.error(f"❌ 코드 리뷰 중 오류가 발생했습니다: {str(e)}")
            else:
                st.warning("⚠️ 코드를 입력해주세요.")

    elif feature == "ℹ️ 정보":
        
        st.markdown("""
        ### 🧚‍♂️ BlueBell
        
        BlueBell은 개발팀의 생산성을 높이기 위해 설계된 AI 기반 개발 지원 도구입니다.
        
        ##### 주요 기능
        
        1. **⚙️ 개발 환경 설정 가이드 생성**
        - README 파일 분석을 통한 프로젝트 이해
        - OS별 맞춤 설치 가이드 제공
        - 의존성 패키지 및 환경변수 설정 안내
        
        2. **🔍 코드 리뷰 및 개선**
        - 네이밍 컨벤션 검사
        - 코드 구조 및 가독성 분석
        - 잠재적 버그 및 보안 취약점 탐지
        - 성능 개선 제안
        
        ##### 타겟 사용자
        
        - **신규 프로젝트 투입 개발자**: 빠른 환경 적응이 필요한 개발자
        - **SI/외주 개발자**: 다양한 클라이언트 프로젝트를 다루는 개발자
        - **신입 개발자**: 프로젝트 파악과 코딩 스타일 학습이 필요한 개발자
        
        ##### 기술 스택
                     
        - **AI Models**
            - **Generation (LLM)**: Azure OpenAI `gpt-4.1-mini`
            - **Embeddings**: Azure OpenAI `text-embedding-3-large`  
        - **Frontend**: Streamlit
        - **Backend**: Python
        - **Search**: Azure AI Search
        - **Deployment**: Azure Web App
        
        ##### 문의 및 피드백
        - 📧 Email: minseo.jo@kt.com
        
        ---
        
        **Version**: 1.0.0 (MVP)  
        **Last Updated**: 2025.09.16
        **Developed by**: KTds AI플랫폼개발팀 조민서
        """)

    # 푸터 
    st.markdown("---")
    st.markdown(
        """
        <div class="footer">
            <div style='text-align: center; color: #546e7a;'>
                <p style="margin: 0; font-size: 1.1rem;">🧚‍♂️ <strong>BlueBell</strong> v1.0.0</p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Powered by Azure OpenAI | © 2025 KTds</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()