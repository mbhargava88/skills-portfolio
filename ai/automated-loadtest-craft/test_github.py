import streamlit as st
import sys
import os

print(f"DEBUG: Python executable: {sys.executable}")
print(f"DEBUG: Python version: {sys.version}")
print(f"DEBUG: Sys path: {sys.path}")
print(f"DEBUG: CWD: {os.getcwd()}")

try:
    import github
    print(f"DEBUG: Github imported successfully: {github}")
    print(f"DEBUG: Github file: {github.__file__}")
except Exception as e:
    print(f"DEBUG: Error importing github: {e}")
