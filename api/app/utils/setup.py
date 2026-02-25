import openai
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import base64


def get_clients(config):
    openai_client = openai.OpenAI(api_key=config["OPENAI_API_KEY"])

    # Load Firebase credentials from configuration.
    # Prefer an explicit credentials file (safer for multiline JSON keys). If provided,
    # read JSON directly from that file path.
    creds_file = config.get("FIREBASE_CREDENTIALS_FILE") or os.environ.get("FIREBASE_CREDENTIALS_FILE")
    if creds_file:
        try:
            with open(creds_file, "r", encoding="utf-8") as fh:
                firebase_creds = json.load(fh)
        except Exception as e:
            raise RuntimeError(f"Failed to read FIREBASE_CREDENTIALS_FILE={creds_file}: {e}")
        # proceed to initialize

    else:
        # The config value may be either a base64-encoded JSON string or a raw JSON string.
        raw_value = config.get("FIREBASE_CREDENTIALS")
    if not raw_value:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS not set in configuration. Please set the environment variable FIREBASE_CREDENTIALS."
        )

    firebase_creds = None
    decode_attempts = []

    # First, try base64 decode -> JSON
    try:
        decoded = base64.b64decode(raw_value).decode("utf-8")
        decode_attempts.append(("base64_decoded", decoded))
        try:
            firebase_creds = json.loads(decoded)
        except json.JSONDecodeError:
            # Try fixing common issue: unescaped newlines in private key
            try_fixed = decoded.replace("\n", "\\n")
            try:
                firebase_creds = json.loads(try_fixed)
            except json.JSONDecodeError:
                firebase_creds = None
    except Exception:
        decoded = None

    # If base64 path didn't yield valid JSON, try treating the raw value as JSON
    if firebase_creds is None:
        decode_attempts.append(("raw", raw_value))
        try:
            firebase_creds = json.loads(raw_value)
        except json.JSONDecodeError:
            # Try replacing escaped newlines with real newlines (common when pasting keys)
            try_alt = raw_value.replace("\\n", "\n")
            try:
                firebase_creds = json.loads(try_alt)
            except json.JSONDecodeError:
                firebase_creds = None

    if firebase_creds is None:
        # Build a short diagnostic message showing the start of the attempted payloads
        previews = []
        for name, payload in decode_attempts:
            previews.append(f"{name}: {repr(payload)[:200]}")
        preview_text = " | ".join(previews) if previews else "(no payloads)"
        raise RuntimeError(
            "FIREBASE_CREDENTIALS is not valid JSON. Tried base64 decode and raw JSON parsing. "
            f"Preview of attempts: {preview_text}"
        )

    cred = credentials.Certificate(firebase_creds)

    firebase_admin.initialize_app(cred)

    db = firestore.client()

    return {"openai_client": openai_client, "firestore_client": db}
