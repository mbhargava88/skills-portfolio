from app.domain.interfaces import GroqLLMClient
from app.domain.entities import TrafficPattern, RepoAnalysis, LoadTestScript, Dataset
from groq import Groq
import os
import json

class GroqLLMClientImpl(GroqLLMClient):
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def analyze_and_generate(self, traffic: TrafficPattern, repo_analysis: RepoAnalysis) -> tuple[LoadTestScript, Dataset]:
        if not self.client.api_key:
             return LoadTestScript(script_content="// No Groq API Key provided\n import http from 'k6/http';\n export default function() { http.get('http://test.k6.io'); }"), Dataset(csv_content="col1,col2\nval1,val2")
        
        prompt = f"""
        Analyze the following traffic pattern and repository analysis to generate a k6 load testing script in JavaScript and a corresponding CSV dataset.
        
        Traffic Pattern:
        RPS: {traffic.rps}
        Avg Latency: {traffic.avg_latency_ms}
        P95 Latency: {traffic.p95_latency_ms}
        Payload Size: {traffic.payload_size_bytes}
        Error Rate: {traffic.error_rate}
        
        Repo Analysis:
        File Tree: {repo_analysis.file_tree}
        Summary: {repo_analysis.endpoint_logic_summary}
        
        Output valid JSON with keys: "k6_script" and "csv_data".
        """
        
        try:
            completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert performance engineer. valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"},
            )
            
            response_content = completion.choices[0].message.content
            data = json.loads(response_content)
            
            k6_script = data.get("k6_script", "// Error generating script")
            csv_data = data.get("csv_data", "col1,col2\nval1,val2")

            return LoadTestScript(script_content=k6_script), Dataset(csv_content=csv_data)

        except Exception as e:
            return LoadTestScript(script_content=f"// Error communicating with Groq: {str(e)}"), Dataset(csv_content="error\ntrue")
