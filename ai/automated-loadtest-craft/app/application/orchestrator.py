from typing import TypedDict, Annotated, Union
from langgraph.graph import StateGraph, END

from app.domain.entities import TrafficPattern, RepoAnalysis, LoadTestScript, Dataset, Bundle
from app.domain.usecases import (
    FetchTrafficUseCase, AnalyzeRepoUseCase, GenerateLoadTestUseCase, 
    BundleArtifactsUseCase, UploadToS3UseCase
)
from app.infra.grafana_client import GrafanaClientImpl
from app.infra.github_client import GitHubClientImpl
from app.infra.groq_client import GroqLLMClientImpl
from app.infra.s3_client import S3ClientImpl

# Define the state dict
class AgentState(TypedDict):
    service_name: str
    endpoint: str
    repo_name: str
    traffic_pattern: Annotated[Union[TrafficPattern, None], "Traffic data"]
    repo_analysis: Annotated[Union[RepoAnalysis, None], "Repo analysis data"]
    load_test_script: Annotated[Union[LoadTestScript, None], "Generated script"]
    dataset: Annotated[Union[Dataset, None], "Generated dataset"]
    bundle_path: Annotated[Union[str, None], "Path to zip bundle"]
    s3_url: Annotated[Union[str, None], "Final download URL"]
    error: Annotated[Union[str, None], "Error message"]

class Orchestrator:
    def __init__(self):
        # Initialize Use Cases with Infra Implementations
        self.fetch_traffic_uc = FetchTrafficUseCase(GrafanaClientImpl())
        self.analyze_repo_uc = AnalyzeRepoUseCase(GitHubClientImpl())
        self.generate_loadtest_uc = GenerateLoadTestUseCase(GroqLLMClientImpl())
        self.bundle_artifacts_uc = BundleArtifactsUseCase()
        self.upload_s3_uc = UploadToS3UseCase(S3ClientImpl())

        self.workflow = self._build_graph()

    def _build_graph(self):
        workflow = StateGraph(AgentState)

        # 1. Fetch Traffic
        def fetch_traffic_node(state: AgentState):
            try:
                print(f"Fetching traffic for {state['service_name']}...")
                traffic = self.fetch_traffic_uc.execute(state['service_name'], state['endpoint'])
                return {"traffic_pattern": traffic}
            except Exception as e:
                return {"error": f"Traffic fetch failed: {str(e)}"}

        # 2. Fetch Repo
        def fetch_repo_node(state: AgentState):
            if state.get("error"): return {}
            try:
                print(f"Fetching repo {state['repo_name']}...")
                analysis = self.analyze_repo_uc.execute(state['repo_name'])
                return {"repo_analysis": analysis}
            except Exception as e:
                return {"error": f"Repo fetch failed: {str(e)}"}

        # 3. Analyze & Generate
        def generate_node(state: AgentState):
            if state.get("error"): return {}
            try:
                print("Generating load test script...")
                script, dataset = self.generate_loadtest_uc.execute(state['traffic_pattern'], state['repo_analysis'])
                return {"load_test_script": script, "dataset": dataset}
            except Exception as e:
                return {"error": f"Generation failed: {str(e)}"}

        # 4. Bundle
        def bundle_node(state: AgentState):
            if state.get("error"): return {}
            try:
                print("Bundling artifacts...")
                path = self.bundle_artifacts_uc.execute(state['load_test_script'], state['dataset'])
                return {"bundle_path": path}
            except Exception as e:
                return {"error": f"Bundling failed: {str(e)}"}
        
        # 5. Upload
        def upload_node(state: AgentState):
            if state.get("error"): return {}
            try:
                print("Uploading to S3...")
                url = self.upload_s3_uc.execute(state['bundle_path'], "my-loadtest-bucket", f"bundles/{state['service_name']}_test.zip")
                return {"s3_url": url}
            except Exception as e:
                 # If S3 fails (e.g. no creds), we can just return the local path as a fallback or error
                 if "No S3" in str(e) or "credentials" in str(e):
                      return {"s3_url": f"Local file: {state['bundle_path']}"}
                 return {"error": f"Upload failed: {str(e)}"}

        # Add nodes
        workflow.add_node("FetchTraffic", fetch_traffic_node)
        workflow.add_node("FetchRepo", fetch_repo_node)
        workflow.add_node("Generate", generate_node)
        workflow.add_node("Bundle", bundle_node)
        workflow.add_node("Upload", upload_node)

        # Define edges
        workflow.set_entry_point("FetchTraffic")
        workflow.add_edge("FetchTraffic", "FetchRepo")
        workflow.add_edge("FetchRepo", "Generate")
        workflow.add_edge("Generate", "Bundle")
        workflow.add_edge("Bundle", "Upload")
        workflow.add_edge("Upload", END)

        return workflow.compile()

    def run(self, service: str, endpoint: str, repo: str):
        initial_state = AgentState(
            service_name=service, 
            endpoint=endpoint, 
            repo_name=repo,
            traffic_pattern=None,
            repo_analysis=None,
            load_test_script=None,
            dataset=None,
            bundle_path=None,
            s3_url=None,
            error=None
        )
        return self.workflow.invoke(initial_state)
