from app.domain.entities import TrafficPattern, RepoAnalysis, LoadTestScript, Dataset, Bundle
from app.domain.interfaces import GrafanaClient, GitHubClient, GroqLLMClient, S3Client
import zipfile
import os

class FetchTrafficUseCase:
    def __init__(self, grafana_client: GrafanaClient):
        self.grafana_client = grafana_client

    def execute(self, service: str, endpoint: str) -> TrafficPattern:
        return self.grafana_client.fetch_traffic(service, endpoint)

class AnalyzeRepoUseCase:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    def execute(self, repo_name: str) -> RepoAnalysis:
        return self.github_client.fetch_repo(repo_name)

class GenerateLoadTestUseCase:
    def __init__(self, groq_client: GroqLLMClient):
        self.groq_client = groq_client

    def execute(self, traffic: TrafficPattern, repo_analysis: RepoAnalysis) -> tuple[LoadTestScript, Dataset]:
        return self.groq_client.analyze_and_generate(traffic, repo_analysis)

class BundleArtifactsUseCase:
    def execute(self, script: LoadTestScript, dataset: Dataset, output_dir: str = "/tmp") -> str:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        bundle_path = os.path.join(output_dir, "loadtest_bundle.zip")
        with zipfile.ZipFile(bundle_path, 'w') as zipf:
            zipf.writestr("test_script.js", script.script_content)
            zipf.writestr(dataset.filename, dataset.csv_content)
        
        return bundle_path

class UploadToS3UseCase:
    def __init__(self, s3_client: S3Client):
        self.s3_client = s3_client

    def execute(self, bundle_path: str, bucket: str, key: str) -> str:
        return self.s3_client.upload(bundle_path, bucket, key)
