import streamlit as st
import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Add project root to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.application.orchestrator import Orchestrator

st.set_page_config(page_title="Antigravity Load Test Automator", page_icon="🚀", layout="wide")

st.title("🚀 Antigravity Load-Testing Automator")
st.markdown("Automate the generation of k6 load-testing bundles using Grafana traffic data and GitHub repo analysis.")

with st.sidebar:
    st.header("Configuration")
    st.info("Ensure environment variables for GRAFANA, GITHUB, GROQ, and AWS are set.")

col1, col2 = st.columns(2)

with col1:
    service_name = st.text_input("Service Name", value="payment-service")
    endpoint = st.text_input("Endpoint Path", value="/api/v1/process")

with col2:
    repo_name = st.text_input("GitHub Repo Name", value="org/payment-service")

if st.button("Generate Load Test Bundle", type="primary"):
    with st.spinner("Orchestrating agents..."):
        try:
            orchestrator = Orchestrator()
            result = orchestrator.run(service_name, endpoint, repo_name)
            
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
