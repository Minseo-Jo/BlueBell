"""
Azure AI Search 클라이언트 모듈
RAG 파이프라인을 위한 벡터 검색 및 문서 인덱싱 담당
"""

import os
import json
from typing import Dict, List, Optional
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    VectorSearchAlgorithmKind,
    VectorSearchAlgorithmMetric,
    HnswAlgorithmConfiguration
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class AzureSearchClient:
    """
    Azure AI Search와 통신하는 클라이언트
    벡터 검색 및 하이브리드 검색 지원
    """
    
    def __init__(self):
        """클라이언트 초기화"""
        self.search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        self.search_key = os.getenv("AZURE_SEARCH_KEY")
        self.search_api_version = os.getenv("AZURE_SEARCH_API_VERSION", "2023-11-01")
        
        # 인덱스 이름 설정
        self.conventions_index = "coding-conventions"
        self.templates_index = "setup-templates"
        
        self._validate_config()
        
        # 클라이언트 초기화
        self.credential = AzureKeyCredential(self.search_key)
        self.index_client = SearchIndexClient(
            endpoint=self.search_endpoint,
            credential=self.credential
        )
        
        logger.info("Azure AI Search 클라이언트 초기화 완료")
    
    def _validate_config(self):
        """환경변수 검증"""
        required_vars = {
            "AZURE_SEARCH_ENDPOINT": self.search_endpoint,
            "AZURE_SEARCH_KEY": self.search_key
        }
        
        missing_vars = [var for var, value in required_vars.items() if not value]
        if missing_vars:
            raise ValueError(f"필수 환경 변수가 없습니다: {', '.join(missing_vars)}")
    
    def create_conventions_index(self) -> bool:
        """코딩 컨벤션 인덱스 생성"""
        try:
            # 벡터 검색 설정
            vector_search = VectorSearch(
                profiles=[
                    VectorSearchProfile(
                        name="conventions-profile",
                        algorithm_configuration_name="conventions-hnsw"
                    )
                ],
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="conventions-hnsw",
                        kind=VectorSearchAlgorithmKind.HNSW,
                        parameters={
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                            "metric": VectorSearchAlgorithmMetric.COSINE
                        }
                    )
                ]
            )
            
            # 필드 정의
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="title", type=SearchFieldDataType.String),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="language", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="company", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="project_type", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="tags", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
                SimpleField(name="priority", type=SearchFieldDataType.Int32, filterable=True, sortable=True),
                SearchField(
                    name="content_vector",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True,
                    vector_search_dimensions=1536,
                    vector_search_profile_name="conventions-profile"
                )
            ]
            
            # 인덱스 생성
            index = SearchIndex(
                name=self.conventions_index,
                fields=fields,
                vector_search=vector_search
            )
            
            result = self.index_client.create_or_update_index(index)
            logger.info(f"코딩 컨벤션 인덱스 생성 완료: {result.name}")
            return True
            
        except Exception as e:
            logger.error(f"인덱스 생성 실패: {str(e)}")
            return False
    
    def create_templates_index(self) -> bool:
        """환경 설정 템플릿 인덱스 생성"""
        try:
            # 벡터 검색 설정
            vector_search = VectorSearch(
                profiles=[
                    VectorSearchProfile(
                        name="templates-profile",
                        algorithm_configuration_name="templates-hnsw"
                    )
                ],
                algorithms=[
                    HnswAlgorithmConfiguration(
                        name="templates-hnsw",
                        kind=VectorSearchAlgorithmKind.HNSW,
                        parameters={
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                            "metric": VectorSearchAlgorithmMetric.COSINE
                        }
                    )
                ]
            )
            
            # 필드 정의
            fields = [
                SimpleField(name="id", type=SearchFieldDataType.String, key=True),
                SearchableField(name="title", type=SearchFieldDataType.String),
                SearchableField(name="content", type=SearchFieldDataType.String),
                SimpleField(name="category", type=SearchFieldDataType.String, filterable=True),
                SimpleField(name="tech_stack", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
                SimpleField(name="os_support", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
                SimpleField(name="prerequisites", type=SearchFieldDataType.Collection(SearchFieldDataType.String), filterable=True),
                SimpleField(name="difficulty", type=SearchFieldDataType.String, filterable=True),
                SearchField(
                    name="content_vector",
                    type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True,
                    vector_search_dimensions=1536,
                    vector_search_profile_name="templates-profile"
                )
            ]
            
            # 인덱스 생성
            index = SearchIndex(
                name=self.templates_index,
                fields=fields,
                vector_search=vector_search
            )
            
            result = self.index_client.create_or_update_index(index)
            logger.info(f"환경 설정 템플릿 인덱스 생성 완료: {result.name}")
            return True
            
        except Exception as e:
            logger.error(f"인덱스 생성 실패: {str(e)}")
            return False
    
    def get_search_client(self, index_name: str) -> SearchClient:
        """특정 인덱스용 검색 클라이언트 반환"""
        return SearchClient(
            endpoint=self.search_endpoint,
            index_name=index_name,
            credential=self.credential
        )
    
    def search_conventions(
        self,
        query: str,
        language: str = None,
        category: str = None,
        top: int = 5
    ) -> List[Dict]:
        """
        코딩 컨벤션 검색
        
        Args:
            query: 검색 쿼리
            language: 프로그래밍 언어 필터
            category: 카테고리 필터
            top: 반환할 결과 수
            
        Returns:
            검색 결과 리스트
        """
        try:
            search_client = self.get_search_client(self.conventions_index)
            
            # 필터 생성
            filters = []
            if language:
                filters.append(f"language eq '{language}'")
            if category:
                filters.append(f"category eq '{category}'")
            
            filter_expression = " and ".join(filters) if filters else None
            
            # 검색 실행
            results = search_client.search(
                search_text=query,
                filter=filter_expression,
                top=top,
                include_total_count=True
            )
            
            # 결과 변환
            documents = []
            for result in results:
                documents.append({
                    "id": result["id"],
                    "title": result["title"],
                    "content": result["content"],
                    "language": result["language"],
                    "category": result["category"],
                    "tags": result.get("tags", []),
                    "score": result["@search.score"]
                })
            
            logger.info(f"컨벤션 검색 완료: {len(documents)}개 결과")
            return documents
            
        except Exception as e:
            logger.error(f"컨벤션 검색 실패: {str(e)}")
            return []
    
    def search_templates(
        self,
        query: str,
        tech_stack: List[str] = None,
        os_type: str = None,
        top: int = 5
    ) -> List[Dict]:
        """
        환경 설정 템플릿 검색
        
        Args:
            query: 검색 쿼리
            tech_stack: 기술 스택 필터
            os_type: OS 타입 필터
            top: 반환할 결과 수
            
        Returns:
            검색 결과 리스트
        """
        try:
            search_client = self.get_search_client(self.templates_index)
            
            # 필터 생성
            filters = []
            if tech_stack:
                tech_filters = [f"tech_stack/any(t: t eq '{tech}')" for tech in tech_stack]
                filters.append(f"({' or '.join(tech_filters)})")
            if os_type:
                filters.append(f"os_support/any(os: os eq '{os_type}')")
            
            filter_expression = " and ".join(filters) if filters else None
            
            # 검색 실행
            results = search_client.search(
                search_text=query,
                filter=filter_expression,
                top=top,
                include_total_count=True
            )
            
            # 결과 변환
            documents = []
            for result in results:
                documents.append({
                    "id": result["id"],
                    "title": result["title"],
                    "content": result["content"],
                    "tech_stack": result["tech_stack"],
                    "os_support": result["os_support"],
                    "difficulty": result["difficulty"],
                    "score": result["@search.score"]
                })
            
            logger.info(f"템플릿 검색 완료: {len(documents)}개 결과")
            return documents
            
        except Exception as e:
            logger.error(f"템플릿 검색 실패: {str(e)}")
            return []
    
    def upload_document(self, index_name: str, document: Dict) -> bool:
        """문서 업로드"""
        try:
            search_client = self.get_search_client(index_name)
            
            result = search_client.upload_documents([document])
            
            if result[0].succeeded:
                logger.info(f"문서 업로드 성공: {document['id']}")
                return True
            else:
                logger.error(f"문서 업로드 실패: {result[0].error_message}")
                return False
                
        except Exception as e:
            logger.error(f"문서 업로드 오류: {str(e)}")
            return False
    
    def delete_index(self, index_name: str) -> bool:
        """인덱스 삭제"""
        try:
            self.index_client.delete_index(index_name)
            logger.info(f"인덱스 삭제 완료: {index_name}")
            return True
        except Exception as e:
            logger.error(f"인덱스 삭제 실패: {str(e)}")
            return False

def test_search_client():
    """Azure AI Search 연결 테스트"""
    try:
        client = AzureSearchClient()
        
        # 인덱스 생성 테스트
        print("🔄 코딩 컨벤션 인덱스 생성 중...")
        if client.create_conventions_index():
            print("✅ 코딩 컨벤션 인덱스 생성 성공")
        
        print("🔄 환경 설정 템플릿 인덱스 생성 중...")
        if client.create_templates_index():
            print("✅ 환경 설정 템플릿 인덱스 생성 성공")
        
        print("✅ Azure AI Search 클라이언트 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        return False

if __name__ == "__main__":
    test_search_client()