from app.infra.github_client import GitHubClientImpl
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_github_parsing():
    client = GitHubClientImpl()
    
    # Test cases to verify parsing works (URL, Branch Override)
    urls_to_test = [
        ("https://github.com/mbhargava88/skills-portfolio", None),
        ("https://github.com/mbhargava88/skills-portfolio/tree/main/golang/catalog-service-grpc-http", None),
        ("mbhargava88/skills-portfolio", None),
        ("https://github.com/mbhargava88/skills-portfolio", "main") # Test override
    ]
    
    for url, branch_override in urls_to_test:
        print(f"\\nTesting URL: {url} | Branch Override: {branch_override}")
        
        try:
            analysis = client.fetch_repo(url, branch=branch_override)
            print(f"Success! Repo: {analysis.repo_name}")
            print(f"File tree size: {len(analysis.file_tree)}")
            print(f"First few files: {analysis.file_tree[:5]}")
            print(f"Snippet count: {len(analysis.relevant_code_snippets)}")
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    test_github_parsing()
