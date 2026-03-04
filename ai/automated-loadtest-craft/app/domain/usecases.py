from app.domain.entities import TrafficPattern, RepoAnalysis, LoadTestScript, Dataset, Bundle
from app.domain.interfaces import GrafanaClient, GitHubClient, GroqLLMClient, S3Client
import zipfile
import os

class FetchTrafficUseCase:
    def __init__(self, grafana_client: GrafanaClient):
        self.grafana_client = grafana_client

    def execute(self, service: str, endpoint: str, http_method: str = "POST") -> TrafficPattern:
        return self.grafana_client.fetch_traffic(service, endpoint, http_method)

class AnalyzeRepoUseCase:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    def execute(self, repo_name: str, branch: str = None) -> RepoAnalysis:
        return self.github_client.fetch_repo(repo_name, branch)

class GenerateLoadTestUseCase:
    def __init__(self, groq_client: GroqLLMClient):
        self.groq_client = groq_client

    def execute(self, traffic: TrafficPattern, repo_analysis: RepoAnalysis, target_endpoint: str) -> tuple[LoadTestScript, Dataset]:
        script, dataset = self.groq_client.analyze_and_generate(traffic, repo_analysis, target_endpoint)
        
        try:
            import jsbeautifier
            opts = jsbeautifier.default_options()
            opts.indent_size = 2
            formatted_script = jsbeautifier.beautify(script.script_content, opts)
            script.script_content = formatted_script
        except ImportError:
            pass # Ignore if jsbeautifier is not installed

        return script, dataset

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
