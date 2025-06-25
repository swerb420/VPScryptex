import os, json, gspread
from datetime import datetime

# You must add 'gspread' to this script's dependencies in the Windmill UI.

def main(log_data: dict, sheet_name: str = "MasterLog"):
    print(f"INFO: [Learning] Logging event to Google Sheet '{sheet_name}'...")
    try:
        gcp_secret_json = os.environ.get("WMILL_SECRET_GCP_SERVICE_ACCOUNT_JSON")
        sheet_id = os.environ.get("WMILL_VARIABLE_GOOGLE_SHEET_ID") # Set Sheet ID as a Variable
        if not all([gcp_secret_json, sheet_id]):
            raise ValueError("GCP Service Account or Google Sheet ID is missing.")

        gc = gspread.service_account_from_dict(json.loads(gcp_secret_json))
        worksheet = gc.open_by_key(sheet_id).worksheet(sheet_name)

        row_to_insert = [
            datetime.utcnow().isoformat(),
            log_data.get("event_type", "UNKNOWN"),
            log_data.get("title", ""),
            log_data.get("status", ""),
            json.dumps(log_data.get("details", {}))
        ]
        worksheet.append_row(row_to_insert)
        print("INFO: [Learning] Successfully logged data to Google Sheets.")
        return {"status": "success"}
    except Exception as e:
        print(f"ERROR: [Learning] Failed to log to Google Sheets. Error: {e}")
        return {"status": "error", "message": str(e)}