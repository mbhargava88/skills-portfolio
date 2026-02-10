import argparse
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from application.usecases.run_review import RunReview
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AI Architecture Review Board")
    parser.add_argument("--problem", type=str, required=True, help="The problem statement to design an architecture for")
    
    args = parser.parse_args()
    
    print(f"Starting review for problem: {args.problem}\n")
    
    runner = RunReview()
    try:
        final_state = runner.execute(args.problem)
        
        print("="*50)
        print("FINAL ARCHITECTURE")
        print("="*50)
        print(final_state["proposal"])
        print("\n")
        print("="*50)
        print("FINAL CRITIQUE")
        print("="*50)
        print(final_state["critique"])
        print(f"\nFinal Score: {final_state['score']}")
        print(f"Iterations: {final_state['iteration']}")
        
    except Exception as e:
        print(f"Error during execution: {e}")
        # Identify if it's missing API key
        if "GROQ_API_KEY" in str(e):
             print("\nPlease set the GROQ_API_KEY environment variable.")

if __name__ == "__main__":
    main()
