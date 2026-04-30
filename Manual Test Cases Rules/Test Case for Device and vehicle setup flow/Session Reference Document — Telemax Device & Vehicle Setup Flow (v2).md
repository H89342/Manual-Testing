# Session Reference Document
## Telemax Device & Vehicle Setup Flow (v2)

> Save this document so you can refer back without needing to ask again.

---

## 1. UI / UX Concepts

### What is a Non-blocking Toast?

A **toast** is a small, temporary pop-up notification that briefly appears on screen (usually 2–3 seconds) and then disappears automatically. **Non-blocking** means it does not interrupt or freeze the user — the user can still tap, scroll, or move to the next step while it is showing. It is the opposite of a modal alert, which forces the user to respond before continuing.

**Example in this app:** After the user takes the VIN photo, a toast slides in saying *"VIN captured — processing…"* and the camera immediately advances to the next photo. The user never waits.

---

## 2. Phase 2 — Rapid Photo Capture Processing Steps

When the user takes each photo in Phase 2, this is the exact sequence that happens:

| Step | Action |
|------|--------|
| **Step 1** | User taps shutter. Photo is captured and uploaded to the server instantly. |
| **Step 2** | A non-blocking toast appears: *"Odometer/VIN/Plate captured — processing…"* It disappears on its own. The camera immediately moves to the next photo. |
| **Step 3** | The relevant API fires in the background while the user continues to the next photo. |
| **Step 4** | All OCR results run simultaneously in the background. By the time the user reaches the Review screen (Step 12), all results are already ready. |

---

## 3. Which API Handles Which Photo

| Photo | API Used | What It Does |
|-------|----------|--------------|
| **Odometer** | OpenAI OCR | Reads the number on the odometer dial. Returns raw text only (e.g., `142,305 km`). |
| **VIN Plate** | Vincario OCR VIN Scanner | Reads the VIN text from the photo **and** decodes it into vehicle details — Make, Model, Year, Fuel Type — in a single combined API call. |
| **License Plate** | OpenAI OCR | Reads the registration plate text (e.g., `344 IT2`). Returns raw text only. |

---

## 4. OpenAI OCR vs Vincario OCR — Key Differences

**OpenAI OCR** is a general-purpose AI vision tool. It is used for the odometer and license plate photos because those photos only need the text read — there is nothing to decode or look up. It reads what it sees and returns the text.

**Vincario OCR VIN Scanner** is a specialist tool purpose-built for VINs. It is used for the VIN plate photo because a VIN alone is meaningless — it must be decoded into vehicle data. Vincario does both reading and decoding in a single API call, which means only one network request is needed instead of two. This makes the process faster.

> **Critical distinction:** OpenAI reads text only. Vincario reads the VIN *and* tells you what car it belongs to, all in one step.

---

## 5. How OpenAI OCR and Vincario OCR Work Together

The two APIs are not alternatives to each other — they run on different photos at the same time and their results are combined on the Review screen.

Here is the full picture of how they work together from the moment photos are taken to the moment the user sees the Review screen:

```
User takes Photo 1 — Odometer
  → OpenAI OCR fires in background
  → Reads: "142,305 km"
  → Result stored silently

User takes Photo 2 — VIN Plate
  → Vincario OCR VIN Scanner fires in background
  → Reads VIN: "1HGCM82633A123456"
  → Decodes: Make: Honda / Model: Civic / Year: 2003 / Fuel: Petrol
  → All vehicle details stored silently

User takes Photo 3 — License Plate
  → OpenAI OCR fires in background
  → Reads: "344 IT2"
  → Result stored silently

All three run simultaneously in background ↑

User reaches Review Screen (Step 12)
  → Odometer field: "142,305 km"       ← from OpenAI
  → Make / Model / Year / Fuel Type    ← from Vincario
  → Registration: "344 IT2"            ← from OpenAI
  → VIN shown with confidence level    ← from Vincario
```

The key point is that neither API waits for the other. All three fire at the same time as each photo is taken, they process in parallel in the background, and by the time the user finishes taking all three photos and walks through to the Review screen, all the results are already waiting. **The user experiences no loading or waiting at all.**

> If a result comes back with low confidence (e.g. the odometer photo was blurry), that field is flagged with a **warning icon** and a **"Retake Photo"** button on the Review screen. The other fields that returned fine are unaffected.

---

## 6. Figma vs Developer Brief — Known Gap (Toast Notification)

The Developer Brief (v2) specifies that after each photo a non-blocking toast should appear. After reviewing the Figma screens in Phase 2, the following gaps were found:

- A layer named **"Toaast"** *(typo — double "a")* exists in the Odometer processing screen but is **not visible** on the screen. It is positioned with `position: absolute; top: 316px` and appears to be clipped or hidden.
- The **VIN** and **Registration Plate** screens have **no toast layer at all**.
- A **"SYNCING IN BACKGROUND"** banner exists at the top of some screens but this is a separate element, not the toast.

---

## 7. Photo Capture Order in Phase 2 (and Why)

The order is deliberately optimised to minimise the user's walking and movement:

| Order | Photo | Reason |
|-------|-------|--------|
| **1st** | Odometer | User is already inside the car from plugging in the OBD2 device. |
| **2nd** | VIN Plate | Located on the driver's door jamb, so the user takes this as they step out of the car. |
| **3rd** | License Plate | Located at the rear of the vehicle, so the user walks there last. |

---

## 8. Quick Glossary

| Term | Definition |
|------|------------|
| **OCR** | Optical Character Recognition. Technology that reads text from a photo. |
| **VIN** | Vehicle Identification Number. A unique 17-character code assigned to every vehicle. Used to look up all vehicle details. |
| **VIN Decode** | The process of taking a VIN number and looking it up in a database to get Make, Model, Year, Fuel Type, etc. |
| **Non-blocking** | A UI action or notification that does not stop or freeze the user's workflow. |
| **Toast** | A small temporary notification that appears briefly and disappears without user action. |
| **Vincario** | A third-party vehicle data API service. Their OCR VIN Scanner reads a VIN from a photo and decodes vehicle details in one combined call. |
| **OpenAI OCR** | OpenAI's vision model used to read general text from photos (odometer readings, licence plate numbers). |
| **OBD2** | On-Board Diagnostics port found in most vehicles. The GPS tracker plugs into this port to read vehicle data (VIN, odometer, battery voltage) directly from the car's computer. |
