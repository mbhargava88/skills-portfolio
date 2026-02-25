from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import TrafficPattern, RepoAnalysis, LoadTestScript, Dataset, Bundle

class GrafanaClient(ABC):
    @abstractmethod
    def fetch_traffic(self, service: str, endpoint: str) -> TrafficPattern:
        pass

class GitHubClient(ABC):
    @abstractmethod
    def fetch_repo(self, repo_name: str) -> RepoAnalysis:
        pass

class GroqLLMClient(ABC):
    @abstractmethod
    def analyze_and_generate(self, traffic: TrafficPattern, repo_analysis: RepoAnalysis) -> tuple[LoadTestScript, Dataset]:
        pass

class S3Client(ABC):
    @abstractmethod
    def upload(self, bundle_path: str, bucket: str, key: str) -> str:
        """Uploads file and returns presigned URL"""
        pass
