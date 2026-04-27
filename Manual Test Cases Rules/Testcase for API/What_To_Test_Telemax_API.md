# What to Test — Telemax API Documentation Review

> Source: Telemax API Documentation Review.docx (14 April 2026)
> Scope: 10 existing API issues (Part A) + 5 new features (Part B) + 3 API bugs
> Status: Pre-TC planning — use this as input before writing formal test cases

---

## Table of Contents

- [Part A — Existing API Issues](#part-a--existing-api-issues)
  - [1. Error Response Standardisation](#1-error-response-standardisation-high-priority)
  - [2. Rate Limiting & Pagination](#2-rate-limiting--pagination-high-priority)
  - [3. Token Lifecycle](#3-token-lifecycle-medium-priority)
  - [4. Internal Endpoint Protection](#4-internal-endpoint-protection-medium-priority)
  - [5. X-API-Version Header](#5-x-api-version-header-low-priority)
- [Part B — New Features](#part-b--new-features)
  - [Feature 1 — DTC / Engine Code Enrichment](#feature-1--dtc--engine-code-enrichment-high-priority)
  - [Feature 2 — Webhooks](#feature-2--webhooks-high-priority--largest-feature)
  - [Feature 3 — VIN Lookup / Vehicle Details](#feature-3--vin-lookup--vehicle-details-high-priority)
  - [Feature 4 — Fuel Level Volume](#feature-4--fuel-level-volume-medium-priority)
  - [Feature 5 — Vehicle Details Fields](#feature-5--vehicle-details-rego-make-model-year-medium-priority)
- [API Bugs](#api-bugs)
  - [Bug 1 — SetAlertAsRead isRead Fix](#bug-1--setalertasread-isread-no-op-fix)
  - [Bug 2 — Engine Disable Safety Check](#bug-2--engine-disable-safety-check)
- [Priority Summary](#priority-summary)
- [Open Clarification Questions](#open-clarification-questions)

---

## Part A — Existing API Issues

### 1. Error Response Standardisation (High priority)

Every endpoint must now return a consistent error JSON structure:

```json
{
  "type": "AUTHENTICATION",
  "code": "TOKEN_EXPIRED",
  "description": "The access token has expired. Request a new token.",
  "requestId": "req_7f3a2b1c",
  "docUrl": "https://docs.telemax.com.au/errors/token-expired"
}
```

| What to Test | TC Type |
|---|---|
| Each endpoint returns `401` with correct JSON structure on expired token | Negative |
| Each endpoint returns `401` with correct JSON structure on missing token | Negative |
| Each endpoint returns `403` on valid token with wrong company scope | Negative |
| Each endpoint returns `404` with correct JSON on unknown vehicle ID | Negative |
| Each endpoint returns `404` with correct JSON on unknown IMEI | Negative |
| Each endpoint returns `404` with correct JSON on unknown company ID | Negative |
| Each endpoint returns `422` on invalid parameter format (bad ISO 8601 date string) | Negative |
| Each endpoint returns `422` on invalid parameter format (negative vehicle ID) | Negative |
| Each endpoint returns `429` with `Retry-After` header when rate limit exceeded | Edge Case |
| Each endpoint returns `500` with `requestId` field present for support correlation | Negative |

---

### 2. Rate Limiting & Pagination (High priority)

| What to Test | TC Type |
|---|---|
| Response headers include `X-RateLimit-Limit` on every API call | Functional |
| Response headers include `X-RateLimit-Remaining` on every API call | Functional |
| Response headers include `X-RateLimit-Reset` on every API call | Functional |
| `429` is returned when rate limit is exceeded | Negative |
| `429` response includes `Retry-After` header | Negative |
| `GetAlerts` with `page=1&pageSize=50` returns correct data slice | Functional |
| `GetAlerts` response includes `pagination` metadata (`page`, `pageSize`, `totalCount`, `totalPages`) | Functional |
| `GetAllLastPositionData` with pagination returns `totalCount` and `totalPages` | Functional |
| `pageSize` above max (101 for `GetAlerts`) is rejected with `422` | Edge Case |
| `pageSize` above max (501 for `GetAllLastPositionData`) is rejected with `422` | Edge Case |
| `page=0` is rejected with `422` | Edge Case |
| `page=-1` is rejected with `422` | Edge Case |

---

### 3. Token Lifecycle (Medium priority)

| What to Test | TC Type |
|---|---|
| Token actual expiry is ~24 hours (86,399 seconds), not 3,600 seconds | Functional |
| Expired token returns `401` with error code `TOKEN_EXPIRED` | Negative |
| Malformed/invalid token returns `401` | Negative |
| Re-authenticating with a valid API key returns a new valid token | Functional |
| Token from Company A cannot access Company B's vehicles — returns `404` | Security |

---

### 4. Internal Endpoint Protection (Medium priority)

| What to Test | TC Type |
|---|---|
| `POST /api/rebuild-vehicle-movement-cache` returns `403` or `404` for partner-level tokens | Security |
| Endpoint is no longer listed in the public OpenAPI spec | Functional |

---

### 5. X-API-Version Header (Low priority)

| What to Test | TC Type |
|---|---|
| Every API response includes `X-API-Version` header | Functional |
| `X-API-Version` header value matches the documented version string | Functional |

---

## Part B — New Features

### Feature 1 — DTC / Engine Code Enrichment (High priority)

**Background:** Current response returns `description` and `severity` as empty strings in an array-of-arrays structure. The fix exposes the same enrichment data the front-end already displays, in a flattened array.

**Expected response structure after fix:**
```json
{
  "vehicleId": 85,
  "deviceId": "ABC123",
  "codes": [
    {
      "code": "P1094",
      "description": "...",
      "whyItMatters": "...",
      "possibleCauses": ["..."],
      "recommendedAction": ["..."],
      "severity": "Critical",
      "persistenceNote": "...",
      "detectedAt": "2026-02-18T12:15:46Z",
      "location": { "address": "...", "latitude": -27.448, "longitude": 153.023 },
      "isActive": true
    }
  ]
}
```

| What to Test | TC Type |
|---|---|
| `GET /api/devices/{deviceId}/dtc-codes` returns a flat array (not array-of-arrays) | Functional |
| Response includes `description` field with human-readable text (not empty string) | Functional |
| Response includes `whyItMatters` field | Functional |
| Response includes `possibleCauses` as a string array | Functional |
| Response includes `recommendedAction` as an ordered string array | Functional |
| Response includes `severity` field | Functional |
| Response includes `persistenceNote` field | Functional |
| Response includes `detectedAt` as ISO 8601 UTC timestamp | Functional |
| Response includes `location` object with `address`, `latitude`, `longitude` | Functional |
| Response includes `isActive` boolean field | Functional |
| `severity` value is one of: `Critical`, `Warning`, `Informational` | Functional |
| Vehicle with no active DTC codes returns empty `codes` array (not `null`, not error) | Edge Case |
| Unknown `deviceId` returns `404` with standard error JSON | Negative |
| Cross-company `deviceId` returns `404` (not `403`) — must not leak vehicle existence | Security |
| Manufacturer-specific code not in lookup table returns raw `code` with `null` enrichment fields | Edge Case |

---

### Feature 2 — Webhooks (High priority — largest feature)

#### Subscription CRUD

| What to Test | TC Type |
|---|---|
| `POST /api/webhooks` creates a new subscription and returns the subscription object | Functional |
| `GET /api/webhooks` returns all subscriptions belonging to the authenticated company | Functional |
| `GET /api/webhooks/{id}` returns a specific subscription by ID | Functional |
| `PUT /api/webhooks/{id}` updates the subscription URL and event list | Functional |
| `DELETE /api/webhooks/{id}` removes the subscription | Functional |
| `POST /api/webhooks/{id}/test` sends a test ping to the registered URL | Functional |
| Creating a subscription with an invalid URL format returns `422` | Negative |
| Accessing another company's subscription ID returns `404` | Security |
| Deleting another company's subscription returns `404` | Security |

#### Event Delivery

| What to Test | TC Type |
|---|---|
| `vehicle.engine.enabled` event fires when engine is turned on | Functional |
| `vehicle.engine.disabled` event fires when engine is turned off | Functional |
| `vehicle.geofence.enter` event fires on geofence boundary crossing (entry) | Functional |
| `vehicle.geofence.exit` event fires on geofence boundary crossing (exit) | Functional |
| `vehicle.overspeed` event fires when speed threshold is exceeded | Functional |
| `vehicle.battery.low` event fires on low battery alert | Functional |
| `vehicle.disconnect` event fires when device goes offline | Functional |
| `vehicle.reconnect` event fires when device comes back online | Functional |
| Delivery payload contains `id`, `event`, `timestamp`, `companyId`, `vehicle`, `data` fields | Functional |
| `X-Telemax-Signature` header is present on every delivery | Security |
| `X-Telemax-Signature` HMAC-SHA256 value can be verified using the subscription secret | Security |
| `X-Telemax-Event` header is present and matches the event type | Functional |
| `X-Telemax-Delivery-Id` header is present and is unique per delivery | Functional |
| Non-2xx response from partner endpoint triggers retry | Functional |
| Timeout (no response within 10 seconds) triggers retry | Functional |
| Retry follows exponential backoff: 30s → 2m → 15m → 1h → 6h | Functional |
| Maximum 5 retry attempts — no further delivery after 5th failure | Edge Case |
| Same `event.id` delivered twice is not processed twice (idempotency) | Edge Case |

---

### Feature 3 — VIN Lookup / Vehicle Details (High priority)

| What to Test | TC Type |
|---|---|
| `POST /api/GetVehicleDetails?id=85` returns vehicle metadata for valid ID | Functional |
| `POST /api/GetVehicleDetails?vin=...` returns correct vehicle for valid VIN | Functional |
| `POST /api/GetVehicleDetails?imei=...` returns correct vehicle for valid IMEI | Functional |
| No query parameter provided returns `400` | Negative |
| VIN belonging to a different company returns `404` (not `403`) | Security |
| IMEI belonging to a different company returns `404` (not `403`) | Security |
| `POST /api/GetAllVehicleDetails?compId=12&page=1&pageSize=50` returns paginated list | Functional |
| Paginated response includes `data` array and `pagination` metadata object | Functional |
| `pageSize` above max (200) is rejected with `422` | Edge Case |
| Rate limit on VIN lookup (30 req/min) returns `429` when exceeded | Edge Case |
| All VIN lookup attempts are recorded in the audit log | Functional |

---

### Feature 4 — Fuel Level Volume (Medium priority)

| What to Test | TC Type |
|---|---|
| `GetLastPositionData` response includes `fuelLevelVolume` field in litres | Functional |
| `GetAllLastPositionData` response includes `fuelLevelVolume` field | Functional |
| `GetReplay` response includes `fuelLevelVolume` field | Functional |
| `GetReplayUserTime` response includes `fuelLevelVolume` field | Functional |
| `GetPositionData` response includes `fuelLevelVolume` field | Functional |
| Vehicle without volumetric fuel sensor returns `null` for `fuelLevelVolume` (not `0`) | Edge Case |
| Existing `fuelLevel` (percentage, 0–100) field is unchanged in all position endpoints | Regression |

---

### Feature 5 — Vehicle Details: Rego, Make, Model, Year (Medium priority)

| What to Test | TC Type |
|---|---|
| `GetVehicleDetails` response includes `rego` field | Functional |
| `GetVehicleDetails` response includes `make` field | Functional |
| `GetVehicleDetails` response includes `model` field | Functional |
| `GetVehicleDetails` response includes `year` field | Functional |
| `GetVehicleDetails` response includes `fuelTankCapacity` field | Functional |
| `GetAllVehicleDetails` paginated response includes `page`, `pageSize`, `totalCount`, `totalPages` | Functional |
| `GetLastPositionData` and position endpoints do NOT include `rego`, `make`, `model`, `year` — payload stays lean | Regression |

---

## API Bugs

### Bug 1 — SetAlertAsRead isRead No-Op Fix

**Background:** The `isRead` parameter on `POST /api/SetAlertAsRead` is currently ignored — alerts are always marked as read regardless of the value passed.

| What to Test | TC Type |
|---|---|
| `isRead=true` marks the alert as read | Functional |
| `isRead=false` marks the alert as unread | Functional |
| After fix: passing `isRead=false` no longer silently marks the alert as read | Regression |

---

### Bug 2 — Engine Disable Safety Check

**Background:** No safety check exists to prevent engine disable while vehicle is moving. The fix adds a speed check with a `force` override.

| What to Test | TC Type |
|---|---|
| Sending engine disable command (`isOn=false`) to a stationary vehicle (speed = 0) succeeds | Functional |
| Sending engine disable command to a moving vehicle (speed > 5 km/h) returns `422` | Negative |
| `422` response body contains `type: "SAFETY"`, `code: "VEHICLE_IN_MOTION"`, and current speed in description | Negative |
| `force=true` parameter bypasses speed check and executes engine disable on moving vehicle | Edge Case |
| Audit log entry is created for every engine disable command — includes user, vehicle ID, speed, timestamp | Functional |
| Audit log entry is created for every engine enable command | Functional |

---

## Priority Summary

| Priority | Areas |
|---|---|
| **High** | Error response standardisation, DTC enrichment, Webhooks (CRUD + delivery + retry), VIN lookup / vehicle details |
| **Medium** | Rate limiting & pagination, Token lifecycle, Fuel volume, Engine safety check, isRead fix |
| **Low / Regression** | X-API-Version header, Internal endpoint removal, Backward compatibility on all existing endpoints |

---

## Open Clarification Questions

Log these as CQ entries before writing formal test cases. Each blocks or partially blocks the TCs noted.

| Ref | Blocks | Question |
|---|---|---|
| CQ-001 | Error response TCs (Part A §1) | What are the exact `type` and `code` values for each error scenario? (e.g. is 403 type `AUTHORIZATION` or `FORBIDDEN`?) |
| CQ-002 | DTC enrichment TCs (Feature 1) | Is the front-end DTC data source confirmed and accessible? Feature 1 TCs cannot be written until the data source is known. |
| CQ-003 | Rate limiting TCs (Part A §2) | What is the exact rate limit per endpoint? (e.g. is `GetAlerts` 60/min or different from `GetVehicleDetails`?) |
| CQ-004 | SetAlertAsRead TCs (Bug 1) | Is `isRead=false` (mark unread) the chosen fix, or is the parameter being removed entirely? The TC scope differs for each option. |
| CQ-005 | Webhook retry TCs (Feature 2) | Is the max retry count exactly 5, and does the final failure state create a dead-letter record? |
