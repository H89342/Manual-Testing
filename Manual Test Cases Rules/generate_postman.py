"""
Generates a Postman Collection v2.1 JSON for the Device & Vehicle Setup API.
Import the output file directly into Postman via:
  File → Import → Upload Files → select postman_device_vehicle_setup_v1.json
"""

import json
import uuid

# ── Open CQ map for API TCs ──────────────────────────────────────────────────
# Any API TC listed here gets a PENDING warning block injected into its pre-script.
# Format: "TC_ID": ("CQ-REF", "Question summary")
OPEN_API_CQ = {
    "API-002": ("CQ-007", "What are the exact field names in the 404 error response body for unregistered IMEI?"),
    "API-003": ("CQ-008", "Does this endpoint require a Bearer token? What is the exact 401 response body?"),
    "API-006": ("CQ-009", "What is the max file size and accepted MIME types for photo uploads?"),
    "API-007": ("CQ-009", "What is the max file size and accepted MIME types for photo uploads?"),
    "API-008": ("CQ-009", "What is the max file size and accepted MIME types for photo uploads?"),
    "API-009": ("CQ-010", "Is POST /vehicle/sync idempotent? Does a second call create a new job or return the existing one?"),
    "API-010": ("CQ-011", "What is the exact status code and body returned when the 60-second sync timeout is reached?"),
    "API-011": ("CQ-011", "What is the exact status code and body returned when the 60-second sync timeout is reached?"),
    "API-013": ("CQ-012", "Does confirming vehicle details trigger any side effects (email, webhook, background job)?"),
    "API-014": ("CQ-013", "Does PUT /vehicle/{id} require the full object or accept partial field updates only?"),
}


def make_prerequest(auth=True, dynamic_vars=None, clear_vars=None, tc_id=None):
    lines = []

    # Inject open CQ warning block at the very top if this TC has an open question
    if tc_id and tc_id in OPEN_API_CQ:
        cq_ref, cq_question = OPEN_API_CQ[tc_id]
        lines += [
            f"// ⚠️  OPEN CLARIFICATION — {cq_ref}",
            f"// Question: {cq_question}",
            "// Status:   Open — do NOT run this request until resolved.",
            f"// Ref:      Clarify Requirements sheet → {cq_ref}",
            "// ─────────────────────────────────────────────────────────",
            "",
        ]

    if auth:
        lines += [
            "// Set auth token from environment",
            "const token = pm.environment.get('access_token');",
            "pm.request.headers.add({ key: 'Authorization', value: 'Bearer ' + token });",
            "",
        ]
    if dynamic_vars:
        lines.append("// Generate dynamic values")
        for var, expr in dynamic_vars.items():
            lines.append(f"pm.environment.set('{var}', {expr});")
        lines.append("")
    if clear_vars:
        lines.append("// Clear stale chained variables")
        for var in clear_vars:
            lines.append(f"pm.environment.unset('{var}');")
    return lines if lines else ["// No pre-request actions required"]


def make_tests(status_code, status_label, body_assertions, absent_fields=None,
               chain_saves=None, response_time=2000):
    lines = [
        f"// 1. Status code",
        f"pm.test('Status is {status_code} {status_label}', function () {{",
        f"    pm.response.to.have.status({status_code});",
        f"}});",
        "",
    ]

    if body_assertions:
        lines += [
            "// 2. Response body fields",
            "pm.test('Response body contains expected fields', function () {",
            "    const json = pm.response.json();",
        ]
        for field, value in body_assertions.items():
            if value is None:
                lines.append(f"    pm.expect(json).to.have.property('{field}');")
            else:
                lines.append(f"    pm.expect(json.{field}).to.eql({json.dumps(value)});")
        lines += ["});", ""]

    if absent_fields:
        lines += [
            "// 3. Sensitive fields must be absent",
            "pm.test('No sensitive fields exposed', function () {",
            "    const json = pm.response.json();",
        ]
        for f in absent_fields:
            lines.append(f"    pm.expect(json).to.not.have.property('{f}');")
        lines += ["});", ""]

    lines += [
        "// 4. Response time",
        f"pm.test('Response time is under {response_time}ms', function () {{",
        f"    pm.expect(pm.response.responseTime).to.be.below({response_time});",
        "});",
    ]

    if chain_saves:
        lines += ["", "// 5. Save values for chaining"]
        lines.append("pm.test('Save chained values to environment', function () {")
        lines.append("    const json = pm.response.json();")
        for env_var, field_path in chain_saves.items():
            lines.append(f"    pm.environment.set('{env_var}', json.{field_path});")
        lines.append("});")

    return lines


def make_request(method, path, headers=None, body=None):
    default_headers = [
        {"key": "Content-Type", "value": "application/json"},
        {"key": "Authorization",  "value": "Bearer {{access_token}}"},
    ]
    all_headers = default_headers + (headers or [])

    url_parts = [p for p in path.split("/") if p and not p.startswith("{")]
    raw_url   = "{{base_url}}" + path

    req = {
        "method": method,
        "header": all_headers,
        "url": {
            "raw":  raw_url,
            "host": ["{{base_url}}"],
            "path": url_parts,
        },
    }
    if body:
        req["body"] = {
            "mode": "raw",
            "raw": json.dumps(body, indent=2),
            "options": {"raw": {"language": "json"}},
        }
    return req


def make_item(tc_id, title, prerequest_lines, test_lines, request_obj):
    is_pending = tc_id in OPEN_API_CQ
    prefix     = "[PENDING] " if is_pending else ""
    return {
        "name": f"{prefix}{tc_id}: {title}",
        "event": [
            {
                "listen": "prerequest",
                "script": {"exec": prerequest_lines, "type": "text/javascript"},
            },
            {
                "listen": "test",
                "script": {"exec": test_lines, "type": "text/javascript"},
            },
        ],
        "request":  request_obj,
        "response": [],
    }


# ══════════════════════════════════════════════════════════════
#  TEST CASES
# ══════════════════════════════════════════════════════════════

items_phase1 = [

    # ── API-001 Happy path: valid IMEI ──
    make_item(
        "API-001",
        "Verify validating registered IMEI returns 200 with connected status",
        make_prerequest(auth=True, clear_vars=["response_device_id"], tc_id="API-001"),
        make_tests(
            200, "OK",
            {"device_id": None, "status": "connected", "imei": "860211234567890"},
            absent_fields=["secret_key", "internal_token"],
            chain_saves={"response_device_id": "device_id"},
        ),
        make_request("POST", "/api/v1/device/validate-imei",
                     body={"imei": "860211234567890"}),
    ),

    # ── API-002 Negative: unregistered IMEI ──
    make_item(
        "API-002",
        "Verify validating unregistered IMEI returns 404 Device Not Found",
        make_prerequest(auth=True, tc_id="API-002"),
        make_tests(
            404, "Not Found",
            {"error": "device_not_found",
             "message": "The IMEI provided is not registered to your account."},
        ),
        make_request("POST", "/api/v1/device/validate-imei",
                     body={"imei": "860299999999999"}),
    ),

    # ── API-003 Negative: missing auth token ──
    make_item(
        "API-003",
        "Verify validating IMEI without auth token returns 401 Unauthorized",
        [
            "// ⚠️  OPEN CLARIFICATION — CQ-008",
            "// Question: Does this endpoint require a Bearer token? What is the exact 401 response body?",
            "// Status:   Open — do NOT run this request until resolved.",
            "// Ref:      Clarify Requirements sheet → CQ-008",
            "// ─────────────────────────────────────────────────────────",
            "",
            "// No auth token set — testing unauthenticated request",
            "pm.request.headers.remove('Authorization');",
        ],
        make_tests(
            401, "Unauthorized",
            {"error": "unauthorized", "message": None},
        ),
        make_request("POST", "/api/v1/device/validate-imei",
                     body={"imei": "860211234567890"}),
    ),

    # ── API-004 Negative: malformed IMEI (not 15 digits) ──
    make_item(
        "API-004",
        "Verify validating malformed IMEI returns 422 Unprocessable Entity",
        make_prerequest(auth=True, tc_id="API-004"),
        make_tests(
            422, "Unprocessable Entity",
            {"error": "validation_error", "field": "imei"},
        ),
        make_request("POST", "/api/v1/device/validate-imei",
                     body={"imei": "12345"}),
    ),

    # ── API-005 Negative: missing IMEI field ──
    make_item(
        "API-005",
        "Verify validating request with missing IMEI field returns 422",
        make_prerequest(auth=True, tc_id="API-005"),
        make_tests(
            422, "Unprocessable Entity",
            {"error": "validation_error", "field": "imei"},
        ),
        make_request("POST", "/api/v1/device/validate-imei", body={}),
    ),
]

items_phase2 = [

    # ── API-006 Upload odometer photo ──
    make_item(
        "API-006",
        "Verify uploading odometer photo returns 200 with OCR processing status",
        make_prerequest(
            auth=True,
            dynamic_vars={"upload_timestamp": "new Date().toISOString()"},
            clear_vars=["response_ocr_odometer"],
            tc_id="API-006",
        ),
        make_tests(
            200, "OK",
            {"status": "processing", "photo_type": "odometer", "job_id": None},
            chain_saves={"response_ocr_odometer_job": "job_id"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/photos/upload",
            headers=[{"key": "Content-Type", "value": "multipart/form-data"}],
            body={"photo_type": "odometer", "file": "{{odometer_image_base64}}"},
        ),
    ),

    # ── API-007 Upload VIN photo ──
    make_item(
        "API-007",
        "Verify uploading VIN photo returns 200 with OCR processing status",
        make_prerequest(auth=True, clear_vars=["response_ocr_vin_job"], tc_id="API-007"),
        make_tests(
            200, "OK",
            {"status": "processing", "photo_type": "vin", "job_id": None},
            chain_saves={"response_ocr_vin_job": "job_id"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/photos/upload",
            headers=[{"key": "Content-Type", "value": "multipart/form-data"}],
            body={"photo_type": "vin", "file": "{{vin_image_base64}}"},
        ),
    ),

    # ── API-008 Upload registration plate photo ──
    make_item(
        "API-008",
        "Verify uploading registration plate photo returns 200 with OCR processing status",
        make_prerequest(auth=True, clear_vars=["response_ocr_plate_job"], tc_id="API-008"),
        make_tests(
            200, "OK",
            {"status": "processing", "photo_type": "registration_plate", "job_id": None},
            chain_saves={"response_ocr_plate_job": "job_id"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/photos/upload",
            headers=[{"key": "Content-Type", "value": "multipart/form-data"}],
            body={"photo_type": "registration_plate", "file": "{{plate_image_base64}}"},
        ),
    ),
]

items_phase3 = [

    # ── API-009 Start OBD sync ──
    make_item(
        "API-009",
        "Verify starting OBD sync returns 200 with sync job ID",
        make_prerequest(
            auth=True,
            dynamic_vars={"sync_start_time": "new Date().toISOString()"},
            clear_vars=["response_sync_job_id"],
            tc_id="API-009",
        ),
        make_tests(
            200, "OK",
            {"status": "syncing", "timeout_seconds": 60, "job_id": None},
            chain_saves={"response_sync_job_id": "job_id"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/sync",
            body={"device_id": "{{response_device_id}}", "engine_on": True},
        ),
    ),

    # ── API-010 Sync result: success ──
    make_item(
        "API-010",
        "Verify polling sync result returns 200 Sync Successful with verified OBD data",
        make_prerequest(auth=True, tc_id="API-010"),
        make_tests(
            200, "OK",
            {"status": "completed", "vin_verified": True,
             "odometer_km": None, "battery_voltage": None},
            absent_fields=["raw_obd_dump"],
            chain_saves={"response_vin": "vin", "response_odometer": "odometer_km"},
        ),
        make_request(
            "GET", "/api/v1/vehicle/sync/{{response_sync_job_id}}",
        ),
    ),

    # ── API-011 Sync timeout ──
    make_item(
        "API-011",
        "Verify polling sync result after 60 seconds returns 408 Sync Timeout",
        make_prerequest(auth=True, tc_id="API-011"),
        make_tests(
            408, "Request Timeout",
            {"status": "timeout",
             "message": "We haven't received OBD data from your vehicle in over 60 seconds."},
        ),
        make_request("GET", "/api/v1/vehicle/sync/{{response_sync_job_id}}"),
    ),
]

items_phase4 = [

    # ── API-012 Get review details ──
    make_item(
        "API-012",
        "Verify getting vehicle review details returns 200 with all OCR fields",
        make_prerequest(auth=True, tc_id="API-012"),
        make_tests(
            200, "OK",
            {"vehicle_name": None, "make": None, "model": None,
             "vin": None, "vin_confidence": None,
             "registration_number": None, "odometer_km": None},
            absent_fields=["password", "internal_id"],
        ),
        make_request("GET", "/api/v1/vehicle/review"),
    ),

    # ── API-013 Confirm vehicle details ──
    make_item(
        "API-013",
        "Verify confirming vehicle details returns 200 with confirmed status",
        make_prerequest(auth=True, tc_id="API-013"),
        make_tests(
            200, "OK",
            {"status": "confirmed", "vehicle_id": None},
            chain_saves={"response_vehicle_id": "vehicle_id"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/confirm",
            body={
                "vehicle_name":        "344ITU Ford Ranger",
                "make":                "Ford",
                "model":               "Ranger",
                "build_year":          2024,
                "fuel_type":           "Diesel",
                "fuel_capacity_litres": 80,
                "transmission":        "Automatic",
            },
        ),
    ),

    # ── API-014 Update vehicle details ──
    make_item(
        "API-014",
        "Verify updating vehicle fuel type returns 200 with updated values",
        make_prerequest(auth=True, tc_id="API-014"),
        make_tests(
            200, "OK",
            {"fuel_type": "Diesel", "status": "updated"},
        ),
        make_request(
            "PUT", "/api/v1/vehicle/{{response_vehicle_id}}",
            body={"fuel_type": "Diesel"},
        ),
    ),

    # ── API-015 Confirm with missing required field ──
    make_item(
        "API-015",
        "Verify confirming vehicle details with missing make field returns 422",
        make_prerequest(auth=True, tc_id="API-015"),
        make_tests(
            422, "Unprocessable Entity",
            {"error": "validation_error", "field": "make"},
        ),
        make_request(
            "POST", "/api/v1/vehicle/confirm",
            body={
                "vehicle_name": "344ITU Ford Ranger",
                "model":        "Ranger",
                "build_year":   2024,
            },
        ),
    ),
]

# ══════════════════════════════════════════════════════════════
#  ASSEMBLE COLLECTION
# ══════════════════════════════════════════════════════════════

collection = {
    "info": {
        "_postman_id": str(uuid.uuid4()),
        "name":        "Telemax — Device & Vehicle Setup API",
        "description": (
            "API test collection for the Telemax Device & Vehicle Setup flow.\n"
            "Generated from TESTCASE_RULES.md and TC data.\n"
            "Import into Postman: File → Import → Upload Files.\n"
            "Set environment variables before running: base_url, access_token."
        ),
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [
        {"name": "Phase 1 — Device Connection",  "item": items_phase1},
        {"name": "Phase 2 — Photo Upload (OCR)", "item": items_phase2},
        {"name": "Phase 3 — OBD Sync",           "item": items_phase3},
        {"name": "Phase 4 — Vehicle Review",      "item": items_phase4},
    ],
    "variable": [
        {"key": "base_url",              "value": "https://staging.telemax.com", "type": "string"},
        {"key": "access_token",          "value": "",   "type": "string"},
        {"key": "response_device_id",    "value": "",   "type": "string"},
        {"key": "response_sync_job_id",  "value": "",   "type": "string"},
        {"key": "response_vehicle_id",   "value": "",   "type": "string"},
        {"key": "response_vin",          "value": "",   "type": "string"},
        {"key": "response_odometer",     "value": "",   "type": "string"},
    ],
}

out = r"d:\Manual Testing\Manual Test Cases Rules\postman_device_vehicle_setup_v1.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(collection, f, indent=2, ensure_ascii=False)

print(f"Saved: {out}")
print(f"Total requests: {sum(len(g['item']) for g in collection['item'])}")
print(f"Folders: {len(collection['item'])}")
