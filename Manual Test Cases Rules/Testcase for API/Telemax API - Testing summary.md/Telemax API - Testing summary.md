# Telemax API — Testing Summary

Based on the full API documentation at docs.telemax.com.au, here is a structured breakdown of everything you need to test.

---

## 1. Authentication & Token Management

Two login paths — both must be tested:

- `POST /api/Authentication/token/user` — username + password (form-encoded)
- `POST /api/Authentication/token/api-key` — API key (GUID or legacy, form-encoded)
- V2 equivalents: `/api/v2/authentication/token/user` and `/api/v2/authentication/token/api-key`

**What to test:**

- Valid credentials return a JWT with correct fields: `access_token`, `token_type` ("bearer"), `expires_in` (~86399 seconds)
- Invalid credentials return `401`
- Missing credentials return appropriate error
- `Content-Type` must be `application/x-www-form-urlencoded` — wrong content-type should fail
- Token contains correct JWT claims: `UserId`, `CompanyId`, `TimeZone`; API key tokens may also include `Vehicles`, `Actions`, `DateFormat`
- Token lifetime is ~24 hours; expired token returns `401 TOKEN_EXPIRED`
- No refresh endpoint exists — clients must re-authenticate
- API key vehicle/action allowlist scoping (note: action restrictions are not currently enforced, only vehicle allowlists are)
- Legacy (non-GUID) API key format still resolves correctly

---

## 2. Authorization & Token Scoping

- Token is company-scoped; accessing another company's resources returns `403 COMPANY_ACCESS_DENIED`
- Accessing a vehicle not in the company tree returns `403 VEHICLE_ACCESS_DENIED`
- API key tokens with a vehicle allowlist (`Vehicles` claim) — cannot access vehicles outside the list
- Super-admin company ID `55` bypass exists — test that it works as expected
- Every data route requires `Authorization: Bearer <token>` — missing header returns `401 TOKEN_MISSING`, malformed token returns `401 TOKEN_MALFORMED`

---

## 3. V1 vs V2 API Differences

> **Critical** — both versions must be tested since V1 remains in production alongside V2.

| Area              | V1                        | V2                              |
|-------------------|---------------------------|----------------------------------|
| Base path         | `/api/...`                | `/api/v2/...`                   |
| HTTP methods      | Mostly POST               | Proper REST (GET, PUT, DELETE)  |
| Parameters        | Query string              | Path + query string             |
| Pagination        | Battery health only       | All list endpoints              |
| Rate limiting     | None                      | 60 req / 60s per token          |
| Error shape       | Inconsistent              | Standardised `ApiError` JSON    |
| X-API-Version header | Absent               | Always `2`                      |
| Webhooks          | Not available             | Full CRUD                       |

---

## 4. Endpoint Groups — What to Test Per Group

### 4.1 Fleet & Position Endpoints

**V1:**

- `POST /api/GetAllLastPositionData/{companyId}` — fleet-wide last positions (unbounded, no pagination)
- `POST /api/GetLastPositionData` — single vehicle last position
- `POST /api/GetPositionData` — historical positions (UTC time range)
- `POST /api/GetNearestVehicles` — nearest vehicles to a coordinate (radius in metres)
- `POST /api/devices` — vehicle list with optional `vehicleIds` filter (JSON body — unique among V1 endpoints)

**V2:**

- `GET /api/v2/companies/{id}/vehicles/last-position` — paginated fleet last positions
- `GET /api/v2/vehicles/{id}/last-position` — single vehicle last position
- `GET /api/v2/vehicles/{id}/positions` — paginated position history
- `GET /api/v2/companies/{id}/vehicles/nearest` — nearest vehicles (paginated)
- `PUT /api/v2/vehicles/{id}/position/refresh` — trigger a location update

**Test cases:**

- Valid vehicle ID → correct position data returned
- Invalid/nonexistent vehicle ID → `404 VEHICLE_NOT_FOUND`
- `radius` parameter in metres (e.g., `5000` = 5 km) for nearest vehicles
- Response field spelling quirks: `ConnectionStrengh`, `UserTimeFormated`, `LastMovementTimeUserFormated` — must appear exactly as misspelled in response
- Mixed casing fields: `timeElapsed`, `startedTime`, `endTime`, `isOnline`, `secondsAgo` are camelCase (not PascalCase)
- Units: Speed in km/h, Odometer in km, Voltage in V, FuelLevel in %,  distance (trips) in metres
- Timestamps: serialised without `Z` and without fractional seconds — `2025-05-01T14:32:00`; UTC fields are UTC despite no suffix
- `PositionDto.Id` is synthetic — do not rely on it across sessions
- `isOnline` may be absent in record-based paths — handle null

---

### 4.2 Trip Replay

**V1:**

- `POST /api/GetReplay` — UTC time context
- `POST /api/GetReplayUserTime` — user timezone context

**V2:**

- `GET /api/v2/replay/{id}` — paginated trip replay

**Test cases:**

- Valid date range returns ordered waypoints
- Empty range (no trips) returns empty array, not error
- User-time vs UTC endpoints handle timezone correctly
- `TripDto.distance` is in metres; `Odometer` is in km — both correct and distinct
- `TripDto.Id` is synthetic — do not persist
- `Fatigue` field uses ISO 8601 duration (e.g. `"PT2H30M"`)

---

### 4.3 Alerts

**V1:**

- `POST /api/GetAlerts` — list alerts with reverse geocoding
- `POST /api/SetAlertAsRead` — mark single alert read
- `POST /api/SetAllAlertAsRead` — mark all alerts read

**V2:**

- `GET /api/v2/companies/{id}/alert-records` — paginated alert records
- `GET /api/v2/companies/{id}/alerts` — alert configurations (new in V2)
- `PUT /api/v2/alerts/{id}/{date}/update-read-status` — mark single alert read/unread (bidirectional, new in V2)
- `PUT /api/v2/companies/{id}/set-all-alerts-read` — mark all as read

**Test cases:**

- Alert list scoped to company — cannot read another company's alerts
- Mark one alert read → verify status changes
- Mark all alerts read → verify all statuses change
- V2: mark alert as unread (new capability)
- Alert configurations include type IDs `1, 2, 5, 8, 9, 10` for webhook linking

---

### 4.4 Vehicle Commands (Write Operations)

**V1:**

- `POST /api/ChangeOdometer` — update odometer
- `POST /api/SetVehicleName` — rename vehicle
- `POST /api/UpdateLocation` — trigger location update (requires IMEI)
- `POST /api/SendIgnition` — ignition on/off via SMS+GPRS
- `POST /api/SendDoorLock` — door lock/unlock (ATrack SMS path only)

**V2:**

- `PUT /api/v2/vehicles/{id}/odometer`
- `PUT /api/v2/vehicles/{id}/name`
- `PUT /api/v2/vehicles/{id}/position/refresh`
- `POST /api/v2/vehicles/{id}/ignition`
- `PUT /api/v2/vehicles/{id}/door-lock`

**Test cases:**

- Rename: valid name updates successfully; empty/null name should be validated
- Odometer: valid positive value updates; negative or non-numeric should return `422`
- Ignition: on command and off command both tested; confirm protocol-specific behaviour (SMS/GPRS)
- Door lock: lock and unlock — ATrack protocol only; non-ATrack vehicles may fail
- Location update: requires a valid IMEI; missing IMEI should fail validation
- All commands: unauthorised vehicle ID returns `403`

---

### 4.5 IMEI & Vehicle Info Lookups

**V1:**

- `GET /api/GetDeviceId/{imei}` — IMEI → legacy vehicle ID (one of only two GET endpoints in V1)

**V2:**

- `GET /api/v2/vehicles/{imei}/device-ids` — IMEI to vehicle ID and name
- `GET /api/v2/vehicles/info?imei=` / `?id=` / `?vin=` — flexible vehicle metadata lookup (new in V2)

**Test cases:**

- Valid IMEI resolves to correct vehicle
- Invalid IMEI → `404 IMEI_NOT_FOUND`
- `GET /api/v2/vehicles/info` with all three lookup types: by IMEI, by vehicle ID, by VIN

---

### 4.6 Battery Health

**V1:**

- `POST /api/GetCompanyVehiclesBatteryHealth` — paginated; uses `pageNumber` / `resultsPerPage` (max 500)
- Returns legacy prediction model: `batteryPredictionValue` = `Healthy`, `Check`, or `Failing`

**V2:**

- `GET /api/v2/battery-health` — paginated; uses `page` / `pageSize`
- Returns AI-based predictions with richer data

**Test cases:**

- Pagination: page 1, last page, beyond last page
- Voltage unit is Volts (float)
- Compare V1 vs V2 prediction models on same vehicle

---

### 4.7 Safety Score

**V1:**

- `POST /api/GetSafetyScore` — note: parameter renamed from `id` to `vehicleId` (breaking change)
- New optional parameters: `start`, `finish`, `intervalType` (1=instant, 2=relative to end of local day, 3=three-day, 4=week)

**Test cases:**

- Explicit date range (`start` + `finish`)
- Preset intervals via `intervalType` (1–4) without `start`/`finish`
- Missing `vehicleId` or using old `id` parameter name → validate correct error
- Known quirk: `intervalType` 2/3/4 have a date-arithmetic issue — test and document actual behaviour vs expected

---

### 4.8 DTC Codes (Diagnostic Trouble Codes)

**V1:**

- `GET /api/devices/{id}/dtc-codes` — basic DTC codes from latest record

**V2:**

- `GET /api/v2/vehicles/{id}/dtc` — enriched: code + AI description + severity + detection location

**Test cases:**

- Vehicle with active DTC codes returns correct data
- Vehicle with no DTC history returns empty array
- V2 AI fields: `description`, `severity`, and `location` are populated

---

## 5. Webhooks (V2 Only)

Full CRUD lifecycle must be tested:

- **Create** `POST /api/v2/webhooks` — HMAC secret returned only once; must be saved
- **Get** `GET /api/v2/webhooks/{id}`
- **List** `GET /api/v2/webhooks` — paginated
- **Update** `PUT /api/v2/webhooks/{id}` — replaces full configuration
- **Delete** `DELETE /api/v2/webhooks/{id}` — soft delete, stops future deliveries
- **Link alert** `POST /api/v2/webhooks/{id}/link-alert`

**Test cases:**

- Create webhook, receive HMAC secret — second call does not return secret
- Link alert types `1, 2, 5, 8, 9, 10`; linking unsupported type IDs should fail/be rejected
- Maximum 50 alert configurations per webhook — test boundary at 50 and 51
- `isGlobal: true` fires for all company alerts without requiring `alertIds`
- Delivery payload: verify shape for each alert type (Geofence, Ignition, Low battery, Speeding; `data` is null for others)
- Signature verification: `X-Telemax-Signature: sha256=<hex>` using HMAC-SHA256 of raw body
- `X-Telemax-Delivery` UUID is unique per attempt
- Soft-delete stops future deliveries but does not purge history
- Update webhook URL, active state, and linked alerts separately

---

## 6. Pagination (V2)

All V2 list endpoints support pagination and must be tested:

- Default: `page=1`, `pageSize=50`
- Max `pageSize=500`; above 500 should be rejected or capped
- Page beyond total pages returns empty `items` array
- `page=0` or negative → `422 INVALID_PARAMETER`
- Response envelope fields: `items`, `currentPage`, `numberOfPages`, `totalResults`, `lastResultIndex`
- Optional `searchString` filter (where supported) — by name or IMEI

---

## 7. Error Handling

The V2 standardised error shape must always be returned:

```json
{
  "type": "AUTHENTICATION",
  "code": "TOKEN_EXPIRED",
  "description": "...",
  "requestId": "req_...",
  "docUrl": "..."
}
```

**HTTP status codes and error codes to test:**

| Status | Codes                                               | Trigger scenario            |
|--------|-----------------------------------------------------|-----------------------------|
| 401    | `TOKEN_EXPIRED`, `TOKEN_MALFORMED`, `TOKEN_MISSING` | Expired/bad/absent JWT      |
| 403    | `COMPANY_ACCESS_DENIED`, `VEHICLE_ACCESS_DENIED`    | Wrong scope                 |
| 404    | `VEHICLE_NOT_FOUND`, `COMPANY_NOT_FOUND`, `IMEI_NOT_FOUND` | Bad IDs            |
| 422    | `INVALID_DATE_FORMAT`, `INVALID_ID`, `INVALID_PARAMETER` | Malformed input        |
| 429    | `TOO_MANY_REQUESTS`                                 | Rate limit exceeded         |
| 500    | `INTERNAL_ERROR`                                    | Server fault                |

- V1 error responses may omit `requestId` — verify
- `Retry-After` header is present on `429`
- Retryable: `429`, `500`, `503` — Non-retryable: `401`, `403`, `404`, `422`

---

## 8. Rate Limiting (V2 Only)

- 60 requests per 60-second sliding window per token
- Every V2 response includes: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- At request 61: `429` returned with `Retry-After` header
- V1 endpoints have no rate limit

---

## 9. Response Headers & API Version

- V2 responses always include `X-API-Version: 2`
- V1 responses do not include this header
- Verify presence/absence on every endpoint

---

## 10. Health Check

- `POST /api/Test` (V1) — anonymous, no JWT required, returns plain text
- Verifies basic connectivity without authentication

---

## 11. Deprecation & Sunset Monitoring

- `POST /api/rebuild-vehicle-movement-cache` — removed; should return `404` or `410`
- `POST /api/GetSafetyScore` — old `id` parameter name is a breaking change; test both old and new parameter names
- Watch for `Sunset` HTTP response headers on any V1 routes — plan migration 6 months before Sunset date
- V1 continues working alongside V2 — ensure no regression on V1 endpoints

---

## Key Testing Priorities (Ranked)

1. **Authentication** — both login methods, token expiry, scoping
2. **V2 error shape consistency** — all error cases return standardised JSON
3. **V2 rate limiting** — headers present, `429` triggered correctly
4. **Vehicle commands** — ignition, door lock, odometer, rename (write operations, hardware-dependent)
5. **Webhooks CRUD + HMAC signature** — full lifecycle
6. **Pagination** — boundary conditions on all V2 list endpoints
7. **Known quirks** — misspelled field names, unit conventions, timestamp format without `Z`
8. **Safety score `intervalType`** — new presets and the known date-arithmetic quirk
9. **DTC V2 enriched data** — AI descriptions and severity
10. **V1 vs V2 parity** — same data returned by equivalent endpoints
