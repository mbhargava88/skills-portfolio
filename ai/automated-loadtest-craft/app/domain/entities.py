from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class TrafficPattern(BaseModel):
    rps: float
    avg_latency_ms: float
    p95_latency_ms: float
    payload_size_bytes: int
    error_rate: float
    raw_data: Optional[Dict[str, Any]] = None

class EndpointDetails(BaseModel):
    service_name: str
    endpoint_path: str
    http_method: str
    headers: Optional[Dict[str, str]] = None
    body_schema: Optional[Dict[str, Any]] = None

class RepoAnalysis(BaseModel):
    repo_name: str
    file_tree: List[str]
    relevant_code_snippets: List[str]
    endpoint_logic_summary: str

class LoadTestScript(BaseModel):
    script_content: str
    language: str = "javascript" # k6 uses JS

class Dataset(BaseModel):
    csv_content: str
    filename: str = "data.csv"

class Bundle(BaseModel):
    s3_key: str
    presigned_url: str
    local_path: str
