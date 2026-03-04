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

    def fetch_repo(self, repo_name: str, branch: str = None) -> RepoAnalysis:
        import re
        
        # Defaults
        parsed_branch = "main"
        folder_path = ""
        
        # Handle full URLs with branch and path like https://github.com/owner/repo/tree/branch/path
        tree_match = re.search(r'github\.com[:/]([^/]+/[^/]+?)/tree/([^/]+)/(.*)$', repo_name)
        if tree_match:
            repo_name = tree_match.group(1)
            parsed_branch = tree_match.group(2)
            folder_path = tree_match.group(3)
            if folder_path.endswith('/'):
                folder_path = folder_path[:-1]
        else:
            # Handle standard full URLs like https://github.com/owner/repo
            match = re.search(r'github\.com[:/]([^/]+/[^/]+?)(?:\.git|/)?$', repo_name)
            if match:
                repo_name = match.group(1)
            
        # Resolve Branch priority (Explicit parameter > Parsed URL Branch > 'main')
        resolved_branch = branch if branch else parsed_branch
            
        try:
            repo = self.client.get_repo(repo_name)
            logging.info(f"Fetching repo: {repo_name}, branch: {resolved_branch}, path: {folder_path}")
            contents = repo.get_contents(folder_path, ref=resolved_branch)
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
                           queue.extend(repo.get_contents(file_content.path, ref=resolved_branch))
                       except Exception as e:
                           logging.warning(f"Failed to fetch content for {file_content.path}: {e}")
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
