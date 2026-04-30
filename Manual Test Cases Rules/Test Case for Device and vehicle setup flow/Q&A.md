# Q&A — Telemax Device & Vehicle Setup Flow

---

## Q1. Lights-Not-Blinking Guidance — Is it in Figma?

**What the brief says:**
The Developer Brief (Step 10) states that if the device lights are not yet blinking every second by the time the user reaches the Start Engine step, the user should:

1. Wait up to 60 seconds.
2. Check the device is firmly seated in the OBD2 port.
3. If still no fix — try a short 2–3 minute drive.

**What Figma shows:**

> ⚠️ This guidance screen does not currently exist as a visible screen in Figma.

After reviewing Phase 3: Start Engine in the Figma file, there is only:

- One main Start Engine screen (Handbrake ON / Park Mode checklist with *"I've Turned On The Engine"* button)
- Active Synchronization screens

There is **no dedicated screen or state** showing the "lights not blinking" warning or troubleshooting guidance. This is a gap between the spec and the design — a confirmation question for Steph/developer is recommended below.

---

## Q2. Low-Confidence Flagging — How Does the App Know an OCR Result is Low Confidence?

**What low confidence means:**
When the app sends a photo to OpenAI or Vincario for OCR, the API doesn't just return the text — it also returns a **confidence score** (usually 0–100% or 0.0–1.0) that tells the app how certain it is that it read the text correctly.

**What causes a low confidence score:**
The API gives a lower score when the photo has issues such as:

- Glare or reflection on the screen or plate
- Blurry or out-of-focus image
- Poor lighting or deep shadow
- Partial obstruction (finger in frame, dirt on lens)
- Image too far away or at a bad angle
- Text that is worn or faded

**What the app does with it:**
Each OCR result arrives tagged with its confidence level (High / Medium / Low). The app checks this score against a threshold and then at the Review screen (Step 12):

| Confidence Level | What the User Sees |
|------------------|--------------------|
| **High** | Field displays normally with a green tick |
| **Low** | Field flagged with a warning icon and a **"Retake Photo"** button |

The user can retake only the specific photo that needs attention — all other captured data is preserved.

> **Note:** The user never sees the raw confidence score number — they only see the warning icon. The threshold that defines "low" vs "high" confidence is a developer/API decision that is **not specified in the brief**, so this is worth confirming.

---

## Q3. Vincario API Priority — Step 8 (Photo VIN) or Step 10 (OBD VIN)?

The key point is that this is **not a choice between two calls** — both can fire, but at different times and for different purposes.

**Step 8 — Photo VIN (fires first, if successful):**
When the user takes the VIN plate photo, Vincario OCR VIN Scanner fires immediately and tries to read the VIN from the image. If it succeeds, Vincario's decode also completes in the same call, giving Make, Model, Year, Fuel Type. This is the earliest possible trigger.

**Step 10 — OBD VIN (fires later, if available):**
When the user starts the engine and OBD data is read from the car's computer, if the OBD also returns a VIN, the Vincario Decode API fires again using that OBD VIN to cross-reference with the photo VIN. This is a second, separate call — not the same one as Step 8.

**Comparison table:**

|  | **Step 8 — Photo VIN** | **Step 10 — OBD VIN** |
|---|---|---|
| **Source** | Camera photo of VIN plate | OBD2 port reading from car ECU |
| **API called** | Vincario OCR VIN Scanner (OCR + decode) | Vincario Decode API (decode only) |
| **Fires when** | Immediately after VIN photo taken | When engine starts and OBD returns data |
| **Purpose** | Get vehicle data as early as possible | Cross-reference and verify photo VIN |
| **Result if both match** | "VIN Verified" badge shown on Review screen | — |
| **Priority for vehicle data** | Used first (earliest available) | Used to verify, not replace |

**In plain terms:** Step 8 fires first and gives you the vehicle data. Step 10 fires later and confirms it. If both agree, the user sees a **"VIN Verified"** badge. If they disagree, there is a VIN resolution step (Step 11) to decide which one to trust — but the brief does not specify the logic for that conflict, which is another item worth confirming.

---

## Confirmation Questions to Ask

### Question 1 — Lights-not-blinking guidance (Figma gap)

> Hi Steph — The Developer Brief mentions that if the device lights are not blinking by the time the user reaches Step 10, the user should receive guidance to wait up to 60 seconds and check the device is seated correctly. However, I cannot find a dedicated screen or state for this in the current Figma Phase 3 screens. Could you confirm:
>
> Is there a "lights not blinking" guidance screen or tooltip state that still needs to be designed? Or is this guidance intended to appear inline on the existing Start Engine screen (e.g., as a conditional warning message)?

---

### Question 2 — Low-confidence threshold

> The brief states that low-confidence OCR results will be flagged on the Review screen. Could you confirm what confidence threshold the app uses to determine "low" vs "high"? For example, is anything below 80% considered low confidence? This is needed to define test pass/fail criteria for OCR confidence flagging.

---

### Question 3 — VIN conflict resolution at Step 11

> The brief says Step 11 resolves which VIN to trust if the photo VIN (Step 8) and OBD VIN (Step 10) do not match. Could you confirm the logic for this — for example, does OBD always take priority over photo? Or does the app present both to the user and ask them to choose? This affects the test cases for the VIN mismatch scenario.


Review: "Success animation — summary card with vehicle name, GPS status, and network status on completion"

What the Developer Brief Specifies
The brief describes the final screen (Step 15 — Ready to Drive & Finish) as:

"Success animation with summary card (e.g. 'Your 344IT2 FORD RANGER is ready to track!'). Two options: Return Home or Set Up Another Vehicle."

And in Section 2 (What Changed in v2) it says:

"Success confirmation: A success animation with a summary card (vehicle name, GPS status, network status) plays on completion."

So the full spec includes: vehicle name + GPS status + network status + success animation + two action buttons (Return Home / Set Up Another Vehicle).

What Figma Shows
From reviewing the Figma screens, the "Onboarding Success" screen (labeled in Phase 5) shows:
ElementFigmaSpecSuccess icon (large checkmark/tick animation)✅ Present — large blue circle checkmark✅ Matches"Ready to Drive" heading✅ Present✅ MatchesVehicle name (e.g. "344ITU Ford Ranger")✅ Present✅ MatchesTracker status✅ Present — "Fully Synced" label shown✅ Matches (maps to network status)Health score / GPS score✅ Present — shows percentage values⚠️ Partial match (see below)"Go to Vehicles" button✅ Present✅ Matches (Return Home equivalent)"Set Up Another Vehicle" link✅ Present✅ Matches

The Gap — GPS Status and Network Status
The brief says: summary card should show GPS status and network status explicitly.
What Figma shows: The screen displays a health score percentage and a "Real-time" or "Fully Synced" tracker status — but these are not labelled clearly as "GPS Status" and "Network Status" as separate named fields the way the brief describes. The Health Check screen (Phase 5) is where GPS % and Mobile Network % are shown with clear labels — but on the final success screen, these values appear as a combined summary widget rather than individually labelled GPS/network fields.
Specifically what's unclear:

The success card shows what appears to be two metric values (health score %, real-time status) — but the label names are not confirmed to explicitly say "GPS Status" and "Network Status"
There is no visible "success animation" in a static Figma frame — this is expected since animations can't be shown in static screens, but it is unconfirmed whether an animation is designed (e.g. as a Lottie/animation file)


Summary: Matches vs Gaps
✅ Present in Figma: Vehicle name, completion icon, tracker status (Fully Synced), Go to Vehicles button, Set Up Another Vehicle option.
⚠️ Unclear/partially present: GPS Status and Network Status are not explicitly labelled as separate named fields on the success card — they appear as metric values but the labelling may not match the spec.
❌ Not verifiable in Figma: The success animation itself (Figma shows a static frame only — no animation file visible).

Suggested Confirmation Question

Hi Steph — On the final "Ready to Drive / Onboarding Success" screen, the Developer Brief specifies a summary card showing vehicle name, GPS status, and network status explicitly. In the current Figma screen, I can see the vehicle name and a tracker status ("Fully Synced"), and what appears to be health percentage values — but the labels for GPS Status and Network Status are not clearly visible as separate named fields. Could you confirm: (1) Are GPS Status and Network Status intended to appear as individually labelled fields on the success card, or are they represented by the combined health score shown? (2) Is there a separate animation file (e.g. Lottie) for the success animation, or is this still to be designed? This will help define the test criteria for the completion screen.
Get notified when tasks complete or need input