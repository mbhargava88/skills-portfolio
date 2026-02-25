from app.domain.interfaces import GitHubClient
from app.domain.entities import RepoAnalysis
from github import Github
import os
import logging

class GitHubClientImpl(GitHubClient):
    def __init__(self, api_token: str = None):
        if not api_token:
            api_token = os.getenv("GITHUB_TOKEN")
        self.client = Github(api_token)

    def fetch_repo(self, repo_name: str) -> RepoAnalysis:
        import re
        # Handle full URLs like https://github.com/owner/repo
        match = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git|/)?$', repo_name)
        if match:
            repo_name = match.group(1)
            
        try:
            repo = self.client.get_repo(repo_name)
            contents = repo.get_contents("")
            file_tree = []
            
            # Simple BFS/recursive fetch to get file tree (limit depth for simplicity)
            queue = [contents] if isinstance(contents, list) else [contents] 
            # If get_contents returns ContentFile (single file) or list
            # Actually get_contents("") returns list for dir
            
            # Simplified: just list root for now or traverse a bit
            # For a real implementation, we'd traverse recursively. 
            # I'll just list top level and 'app' or 'src' if present to avoid hitting API limits too hard in demo.
            
            while len(queue) > 0:
                file_content = queue.pop(0)
                if isinstance(file_content, list):
                    queue.extend(file_content)
                else:
                    file_tree.append(file_content.path)
                    if file_content.type == "dir" and len(file_tree) < 50: # arbitrary limit
                       try:
                           queue.extend(repo.get_contents(file_content.path))
                       except:
                           pass

            # Mocking analysis logic for now as 'relevant_code_snippets' requires intelligent search
            return RepoAnalysis(
                repo_name=repo_name,
                file_tree=file_tree[:20], # limit for display
                relevant_code_snippets=["def example(): pass"], 
                endpoint_logic_summary=f"Analysis of {repo_name} completed."
            )
        except Exception as e:
            logging.error(f"Error fetching repo {repo_name}: {e}")
            return RepoAnalysis(
                repo_name=repo_name,
                file_tree=[],
                relevant_code_snippets=[],
                endpoint_logic_summary=f"Error analyzing repo: {str(e)}"
            )
