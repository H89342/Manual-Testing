What to Test — Telemax API Documentation Review
The document covers 10 existing API issues (Part A) and 5 new features (Part B), plus 3 API bugs. Below is what needs test cases, grouped by area.

Part A — Existing API Issues
1. Error Response Standardisation (High priority)
Every endpoint must now return a consistent error JSON { type, code, description, requestId, docUrl }.

What to test	TC type
Each endpoint returns 401 with correct JSON structure on expired/missing token	Negative
Each endpoint returns 403 on valid token with wrong company scope	Negative
Each endpoint returns 404 with correct JSON on unknown vehicle/IMEI/company ID	Negative
Each endpoint returns 422 on invalid parameter format (bad date, negative ID)	Negative
Each endpoint returns 429 with Retry-After header when rate limit exceeded	Edge Case
Each endpoint returns 500 with requestId field for support correlation	Negative
2. Rate Limiting & Pagination (High priority)
What to test	TC type
Response headers include X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset on every call	Functional
429 is returned when limit exceeded; Retry-After header is present	Negative
GetAlerts with page=1&pageSize=50 returns correct data slice and pagination metadata	Functional
GetAllLastPositionData with pagination returns totalCount and totalPages	Functional
pageSize above max (e.g. 101 for GetAlerts) is rejected with 422	Edge Case
page=0 or page=-1 is rejected	Edge Case
3. Token Lifecycle (Medium priority)
What to test	TC type
Token actual expiry is ~24 hours (86,399 seconds), not 3,600 seconds	Functional
Expired token returns 401 with error code TOKEN_EXPIRED	Negative
Re-authenticating with API key returns a new valid token	Functional
Token from Company A cannot access Company B's vehicles (403/404)	Security
4. Internal Endpoint Protection (Medium priority)
What to test	TC type
POST /api/rebuild-vehicle-movement-cache returns 403 or 404 for partner-level tokens	Security
Endpoint is no longer listed in the public OpenAPI spec	Functional
5. X-API-Version Header (Low priority)
What to test	TC type
Every response includes X-API-Version header	Functional
Header value matches documented version string	Functional
Part B — New Features
Feature 1 — DTC / Engine Code Enrichment (High priority)
Current response is empty description and severity fields, array-of-arrays structure.

What to test	TC type
GET /api/devices/{deviceId}/dtc-codes returns flat array (not array-of-arrays)	Functional
Response includes description, whyItMatters, possibleCauses, recommendedAction, severity, persistenceNote, detectedAt, location, isActive	Functional
severity is one of Critical, Warning, Informational	Functional
Vehicle with no active DTC codes returns empty array (not null, not error)	Edge Case
Unknown deviceId returns 404	Negative
Cross-company device ID returns 404 (not 403)	Security
Manufacturer-specific codes not in lookup table return raw code with null enrichment fields	Edge Case
Feature 2 — Webhooks (High priority — largest feature)
Subscription CRUD:

What to test	TC type
POST /api/webhooks creates subscription and returns subscription object	Functional
GET /api/webhooks returns all subscriptions for the company	Functional
PUT /api/webhooks/{id} updates URL and event list	Functional
DELETE /api/webhooks/{id} removes subscription	Functional
POST /api/webhooks/{id}/test sends test ping to registered URL	Functional
Creating subscription with invalid URL returns 422	Negative
Accessing another company's subscription returns 404	Security
Event delivery:

What to test	TC type
Each of the 5 events fires correctly: vehicle.engine.enabled/disabled, vehicle.geofence.enter/exit, vehicle.overspeed, vehicle.battery.low, vehicle.disconnect/reconnect	Functional
Delivery payload contains id, event, timestamp, companyId, vehicle, data	Functional
X-Telemax-Signature header is present and HMAC-SHA256 verified correctly	Security
X-Telemax-Event and X-Telemax-Delivery-Id headers are present	Functional
Non-2xx response from partner triggers retry	Functional
Retry follows exponential backoff: 30s, 2m, 15m, 1h, 6h — max 5 retries	Functional
Same event ID delivered twice is idempotent (not processed twice)	Edge Case
Feature 3 — VIN Lookup / Vehicle Details (High priority)
What to test	TC type
POST /api/GetVehicleDetails?id=85 returns vehicle metadata	Functional
POST /api/GetVehicleDetails?vin=... returns correct vehicle	Functional
POST /api/GetVehicleDetails?imei=... returns correct vehicle	Functional
No query parameter provided returns 400	Negative
VIN belonging to a different company returns 404 (not 403)	Security
POST /api/GetAllVehicleDetails?compId=12&page=1&pageSize=50 returns paginated list	Functional
pageSize above max (200) is rejected with 422	Edge Case
Rate limit on VIN lookup endpoint (30 req/min) is enforced	Edge Case
Feature 4 — Fuel Level Volume (Medium priority)
What to test	TC type
GetLastPositionData response includes fuelLevelVolume (litres) field	Functional
GetAllLastPositionData, GetReplay, GetReplayUserTime, GetPositionData all include the new field	Functional
Vehicle without volumetric sensor returns null for fuelLevelVolume (not 0)	Edge Case
Existing fuelLevel (percentage) field is unchanged	Regression
Feature 5 — Vehicle Details: Rego, Make, Model, Year (Medium priority)
What to test	TC type
GetVehicleDetails response includes rego, make, model, year, fuelTankCapacity	Functional
GetAllVehicleDetails response includes pagination metadata (page, pageSize, totalCount, totalPages)	Functional
Position endpoints (GetLastPositionData etc.) do NOT include static metadata — payload stays lean	Regression
API Bugs to Test
Bug 1 — SetAlertAsRead isRead no-op fix
What to test	TC type
isRead=true marks the alert as read	Functional
isRead=false marks the alert as unread	Functional
Previously broken case (isRead ignored) no longer occurs	Regression
Bug 2 — Engine Disable Safety Check
What to test	TC type
Sending engine disable command to a stationary vehicle (speed = 0) succeeds	Functional
Sending engine disable command to a moving vehicle (speed > 5 km/h) returns 422 with VEHICLE_IN_MOTION code	Negative
force=true parameter bypasses the speed check and executes the command	Edge Case
Audit log entry is created for every engine disable/enable command with speed and timestamp	Functional
Quick Priority Summary
Priority	Areas
High	Error responses, DTC enrichment, Webhooks (CRUD + delivery + retry), VIN/vehicle details
Medium	Rate limiting, Pagination, Token lifecycle, Fuel volume, Engine safety check, isRead fix
Low / Regression	X-API-Version header, Internal endpoint removal, Backward compatibility on all existing endpoints
Clarification questions to log before writing TCs:

What are the exact field names and error codes in the standardised error JSON? (needed for expected results)
Is the DTC data source confirmed? (Feature 1 blocks on this)
What is the exact rate limit per endpoint? (needed for edge case TCs)
Is isRead=false (unread) the chosen fix, or is the parameter being removed entirely? (affects TC scope)