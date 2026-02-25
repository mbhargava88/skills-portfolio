from app.infra.github_client import GitHubClientImpl
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_github_parsing():
    client = GitHubClientImpl()
    
    # Test case from user
    url = "https://github.com/mbhargava88/skills-portfolio"
    print(f"Testing URL: {url}")
    
    # This should internally handle the parsing if my fix works
    try:
        analysis = client.fetch_repo(url)
        print(f"Success! Repo: {analysis.repo_name}")
        print(f"File tree size: {len(analysis.file_tree)}")
        print(f"Snippet count: {len(analysis.relevant_code_snippets)}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_github_parsing()
