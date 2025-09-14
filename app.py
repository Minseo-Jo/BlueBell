"""
DevPilot - 개발 환경 셋업 & 코드 스타일 자동화 도우미
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

# 페이지 설정
st.set_page_config(
    page_title="DevPilot",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #155724;
    }
    .error-message {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 1rem;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'azure_client' not in st.session_state:
    try:
        st.session_state.azure_client = AzureOpenAIClient()
        st.session_state.client_status = "connected"
    except Exception as e:
        st.session_state.client_status = f"error: {str(e)}"

if 'setup_analyzer' not in st.session_state:
    st.session_state.setup_analyzer = SetupAnalyzer(st.session_state.azure_client)

if 'code_reviewer' not in st.session_state:
    st.session_state.code_reviewer = CodeReviewer(st.session_state.azure_client)

# 헤더
st.markdown('<h1 class="main-header">🚁 DevPilot</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">개발 환경 셋업 & 코드 스타일 자동화 도우미</p>', unsafe_allow_html=True)

# 연결 상태 표시
if st.session_state.client_status == "connected":
    st.success("✅ Azure OpenAI 연결 성공")
else:
    st.error(f"❌ Azure OpenAI 연결 실패: {st.session_state.client_status}")

# 사이드바
with st.sidebar:
    st.markdown("### 🎯 기능 선택")
    feature = st.radio(
        "원하는 기능을 선택하세요",
        ["🏠 홈", "📋 환경 설정 가이드", "🔍 코드 리뷰", "ℹ️ 정보"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 사용 통계")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("분석한 프로젝트", "12")
    with col2:
        st.metric("리뷰한 코드", "47")
    
    st.markdown("---")
    st.markdown("### ⚙️ 설정")
    os_type = st.selectbox(
        "타겟 OS",
        ["전체", "Windows", "macOS", "Linux"]
    )
    code_language = st.selectbox(
        "주 사용 언어",
        ["자동 감지", "Python", "JavaScript", "Java", "C#", "Go"]
    )

# 메인 컨텐츠
if feature == "🏠 홈":
    st.markdown("## 🎯 DevPilot으로 개발 생산성을 높이세요!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
        <h3>📋 환경 설정 가이드</h3>
        <p>README 파일이나 프로젝트 URL을 분석하여 OS별 맞춤 환경 설정 가이드를 자동 생성합니다.</p>
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
        <h3>🔍 코드 리뷰</h3>
        <p>코드를 분석하여 사내/고객사 코딩 규칙에 맞는 개선 사항을 제안합니다.</p>
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
        ["선택하세요", "새 프로젝트 환경 설정", "코드 리뷰 받기", "README 분석하기"]
    )
    
    if quick_action == "새 프로젝트 환경 설정":
        st.info("📋 환경 설정 가이드 탭으로 이동하여 README 파일을 업로드해주세요.")
    elif quick_action == "코드 리뷰 받기":
        st.info("🔍 코드 리뷰 탭으로 이동하여 코드를 입력하거나 파일을 업로드해주세요.")

elif feature == "📋 환경 설정 가이드":
    st.markdown("## 📋 환경 설정 가이드 생성")
    st.markdown("프로젝트의 README 파일을 분석하여 OS별 환경 설정 가이드를 생성합니다.")
    
    # 입력 방법 선택
    input_method = st.radio(
        "입력 방법 선택",
        ["파일 업로드", "텍스트 직접 입력", "GitHub URL (미구현)"]
    )
    
    readme_content = None
    
    if input_method == "파일 업로드":
        uploaded_file = st.file_uploader(
            "README 파일을 업로드하세요",
            type=['md', 'txt', 'rst'],
            help="README.md, README.txt, README.rst 파일을 지원합니다."
        )
        
        if uploaded_file:
            readme_content = uploaded_file.read().decode('utf-8')
            with st.expander("업로드된 내용 미리보기"):
                st.text(readme_content[:1000] + "..." if len(readme_content) > 1000 else readme_content)
    
    elif input_method == "텍스트 직접 입력":
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
    if st.button("🚀 환경 설정 가이드 생성", type="primary"):
        if readme_content:
            with st.spinner("AI가 README를 분석하고 있습니다... (약 10-15초)"):
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
                    
                    st.success("✅ 환경 설정 가이드가 생성되었습니다!")
                    
                    # 결과 표시
                    st.markdown("### 📝 생성된 가이드")
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
        ["직접 입력", "파일 업로드"]
    )
    
    code_content = None
    language = "자동 감지"
    
    if input_method == "직접 입력":
        language = st.selectbox(
            "프로그래밍 언어",
            ["자동 감지", "Python", "JavaScript", "Java", "C#", "Go", "TypeScript"]
        )
        
        code_content = st.text_area(
            "코드를 입력하세요",
            height=400,
            placeholder="리뷰 받을 코드를 여기에 붙여넣으세요..."
        )
    
    elif input_method == "파일 업로드":
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
            
            with st.expander("업로드된 코드 미리보기"):
                st.code(code_content[:1000] + "..." if len(code_content) > 1000 else code_content, language=language.lower())
    
    # 리뷰 옵션
    st.markdown("### ⚙️ 리뷰 옵션")
    col1, col2 = st.columns(2)
    
    with col1:
        check_naming = st.checkbox("네이밍 컨벤션 검사", value=True)
        check_structure = st.checkbox("코드 구조 분석", value=True)
        check_bugs = st.checkbox("잠재적 버그 탐지", value=True)
    
    with col2:
        check_performance = st.checkbox("성능 개선 제안", value=True)
        check_security = st.checkbox("보안 취약점 검사", value=True)
        suggest_refactoring = st.checkbox("리팩토링 제안", value=True)
    
    # 코드 리뷰 버튼
    if st.button("🔍 코드 리뷰 시작", type="primary"):
        if code_content:
            with st.spinner("AI가 코드를 분석하고 있습니다... (약 10-15초)"):
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
                    
                    st.success("✅ 코드 리뷰가 완료되었습니다!")
                    
                    # 결과 표시
                    st.markdown("### 📝 리뷰 결과")
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
    st.markdown("## ℹ️ DevPilot 정보")
    
    st.markdown("""
    ### 🚁 DevPilot
    
    DevPilot은 개발팀의 생산성을 높이기 위해 설계된 AI 기반 개발 지원 도구입니다.
    
    ### 주요 기능
    
    1. **📋 환경 설정 가이드 자동 생성**
       - README 파일 분석을 통한 프로젝트 이해
       - OS별 맞춤 설치 가이드 제공
       - 의존성 패키지 및 환경변수 설정 안내
    
    2. **🔍 코드 스타일 리뷰 및 개선**
       - 네이밍 컨벤션 검사
       - 코드 구조 및 가독성 분석
       - 잠재적 버그 및 보안 취약점 탐지
       - 성능 개선 제안
    
    ### 타겟 사용자
    
    - **신규 프로젝트 투입 개발자**: 빠른 환경 적응이 필요한 개발자
    - **SI/외주 개발자**: 다양한 클라이언트 프로젝트를 다루는 개발자
    - **신입 개발자**: 프로젝트 파악과 코딩 스타일 학습이 필요한 개발자
    
    ### 기술 스택
    
    - **AI Engine**: Azure OpenAI Service (GPT-4.1-mini)
    - **Frontend**: Streamlit
    - **Backend**: Python
    - **Deployment**: Azure Web App
    
    ### 문의 및 피드백
    
    개선 사항이나 버그 리포트는 아래로 연락주세요:
    - 📧 Email: minseo.jo@kt.com
    ---
    
    **Version**: 1.0.0 (MVP)  
    **Last Updated**: 2025.09.14
    **Developed by**: KTds AI플랫폼개발팀 조민서 전임
    """)

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
        <p>🚁 DevPilot v1.0.0 | Powered by Azure OpenAI | © 2025 KTds</p>
    </div>
    """,
    unsafe_allow_html=True
)