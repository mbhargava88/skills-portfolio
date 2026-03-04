import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add project root to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.application.orchestrator import Orchestrator

st.set_page_config(page_title="Load Test Automator", page_icon="🚀", layout="wide")

st.title("🚀 Load-Testing Automator")
st.markdown("Automate the generation of k6 load-testing bundles using Grafana traffic data and GitHub repo analysis.")

with st.sidebar:
    st.header("Configuration")
    st.info("Ensure environment variables for GRAFANA, GITHUB, GROQ, and AWS are set.")

col1, col2 = st.columns(2)

with col1:
    service_name = st.text_input("Service Name", value="payment-service")
    endpoint = st.text_input("Endpoint Path", value="/api/v1/process")
    http_method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])

with col2:
    repo_name = st.text_input("GitHub Repo URL", value="https://github.com/mbhargava88/skills-portfolio/tree/main/golang/catalog-service-grpc-http")
    branch_override = st.text_input("Branch Override", value="")

if st.button("Generate Load Test Bundle", type="primary"):
    with st.spinner("Orchestrating agents..."):
        try:
            orchestrator = Orchestrator()
            
            # Pass None explicitly if branch_override string is empty
            branch = branch_override.strip() if branch_override.strip() else None
            result = orchestrator.run(service_name, endpoint, repo_name, branch=branch, http_method=http_method)
            
            if result.get("error"):
                st.error(f"Workflow failed: {result['error']}")
            else:
                st.success("Workflow completed successfully!")
                
                st.subheader("Results")
                
                # Display Traffic Pattern
                with st.expander("Traffic Pattern Analysis"):
                    st.json(result.get("traffic_pattern").dict())
                
                # Display Repo Analysis
                with st.expander("Repo Analysis"):
                    st.json(result.get("repo_analysis").dict())
                
                # Display Generated Script
                with st.expander("Generated k6 Script"):
                    st.code(result.get("load_test_script").script_content, language="javascript")
                
                # Download Link
                s3_url = result.get("s3_url")
                if s3_url and s3_url.startswith("http"):
                    st.markdown(f"### [📥 Download Bundle from S3]({s3_url})")
                elif s3_url:
                    st.warning(f"Upload returned: {s3_url}")
                else:
                    st.warning("No download URL generated.")
                    
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
