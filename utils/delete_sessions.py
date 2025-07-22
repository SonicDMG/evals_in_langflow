"""
This script deletes all sessions for a given flow endpoint name.
"""
import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# This allows the script to be run from any directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# ─── Configure ────────────────────────────────────────────────────────────────
LANGFLOW_URL = os.getenv("LANGFLOW_URL")

# Your Langflow API key (set in LANGFLOW_API_KEY env var)
# You can generate this from the Settings -> Langflow API Keys menu in the UI.
API_KEY = os.getenv("LANGFLOW_API_KEY")

# The endpoint name of the flow whose sessions you want to clear
FLOW_ENDPOINT_NAME = os.getenv("FLOW_ENDPOINT_NAME", "evals_in_langflow")
# ────────────────────────────────────────────────────────────────────────────────

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY,
}

def get_flow_id_by_name(endpoint_name: str) -> str | None:
    """Fetch the ID of a flow by its endpoint name."""
    print(f"Searching for flow with endpoint name: {endpoint_name}")
    resp = requests.get(f"{LANGFLOW_URL}/api/v1/flows/", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    flows = resp.json()  # The endpoint returns a list directly
    for flow in flows:
        if flow.get("endpoint_name") == endpoint_name:
            print(f"Found flow '{flow.get('name')}' with ID: {flow['id']}")
            return flow["id"]
    print("Flow not found.")
    return None

def delete_session_messages(session_id: str):
    """Delete all stored messages for one session."""
    resp = requests.delete(
        f"{LANGFLOW_URL}/api/v1/monitor/messages/session/{session_id}",
        headers={"x-api-key": API_KEY},
        timeout=30
    )
    # A 204 No Content status is a success for DELETE operations.
    if resp.status_code == 200 or resp.status_code == 204:
        print(f"✔ Cleared messages for session {session_id}")
        return True
    else:
        print(f"✖ Failed to clear {session_id}: {resp.status_code} {resp.text}")
        return False

def main():
    if not API_KEY or not LANGFLOW_URL:
        print("❌ Error: LANGFLOW_URL or LANGFLOW_API_KEY is not configured.", file=sys.stderr)
        print("Please set the following environment variables:", file=sys.stderr)
        print("  - LANGFLOW_URL: Your Langflow instance URL (e.g., from Phoenix Cloud).", file=sys.stderr)
        print("  - LANGFLOW_API_KEY: Your Langflow API key.", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching ID for flow with endpoint name '{FLOW_ENDPOINT_NAME}'…")
    flow_id = get_flow_id_by_name(FLOW_ENDPOINT_NAME)

    if not flow_id:
        print(f"No flow found with endpoint name '{FLOW_ENDPOINT_NAME}'.")
        return

    print(f"Starting to fetch and delete sessions for flow {flow_id} in batches...")

    processed_session_ids = set()
    total_deleted = 0
    page = 1
    per_page = 50 # Process 50 messages at a time

    while True:
        print(f"Fetching page {page} of messages...")
        resp = requests.get(
            f"{LANGFLOW_URL}/api/v1/monitor/messages",
            headers=HEADERS,
            params={"flow_id": flow_id, "page": page, "per_page": per_page},
            timeout=60, # Increased timeout for potentially slower API calls
        )
        resp.raise_for_status()
        messages = resp.json()

        if not messages:
            print("No more messages found.")
            break

        session_ids_on_page = {msg["session_id"] for msg in messages if isinstance(msg, dict) and "session_id" in msg}

        new_sessions_to_delete = session_ids_on_page - processed_session_ids

        if new_sessions_to_delete:
            print(f"Found {len(new_sessions_to_delete)} new session(s) to delete on this page.")
            for session_id in new_sessions_to_delete:
                if delete_session_messages(session_id):
                    total_deleted += 1
                processed_session_ids.add(session_id)
        else:
            print("No new sessions found on this page.")

        # If we received fewer messages than we asked for, we're on the last page
        if len(messages) < per_page:
            print("Finished fetching all pages.")
            break

        page += 1

    print(f"\n✨ Process complete. Total unique sessions cleared: {total_deleted}")

if __name__ == "__main__":
    main()
