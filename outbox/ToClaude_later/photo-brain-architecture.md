# Picture Brain: The Local-First Photo Architecture

**Vision:** A massive, intelligent, zero-recurring-cost photo management system. It must deduplicate, tag, recognize faces, and extract metadata from thousands of photos—*without* sending every single image to a paid cloud AI API like Gemini or OpenAI.

**Integration:** It acts as a heavy-lifting processing engine that runs externally, but feeds distilled knowledge (events, people, timelines) back into your `sean-vault` as lightweight Markdown.

---

## 1. Core Principles

1.  **Local First, Free Forever:** Facial recognition and auto-tagging will use open-source, locally run Python models. No per-token API costs.
2.  **No Vault Bloat:** Do *not* create one Markdown file per photo. That would destroy the vault's searchability. Instead, group photos into "Events" or "Albums" and create one Markdown file per event.
3.  **Immutable Storage:** Images are stored on a reliable backend (OneDrive / NAS), renamed deterministically (e.g., by timestamp + hash).
4.  **Non-Destructive Intake:** The system copies images from your untidy source folders, processes them, and outputs them to a pristine destination folder. It never deletes your originals until you verify the intake.

---

## 2. The Architecture & Tech Stack

This requires a multi-stage Python pipeline (`picture-intake.py`) running on your machine.

### Stage 1: Absolute Deduplication (The Filter)
*   **Tool:** Standard Python `hashlib` (SHA-256) and `ImageHash` (Perceptual hashing).
*   **How it works:** 
    *   *Exact duplicates:* Checked via SHA-256. If `IMG_001.jpg` and `IMG_Copy.jpg` are byte-for-byte identical, one is instantly discarded.
    *   *Visual duplicates:* Checked via perceptual hashing (phash). If two images are 98% similar (e.g., burst fire photos or compressed vs. uncompressed versions), the system flags them for you to pick the best one, or auto-keeps the highest resolution.

### Stage 2: Metadata Extraction (The Skeleton)
*   **Tool:** `ExifTool` (The industry standard, wrapped in Python).
*   **What it does:** Extracts timestamp, GPS coordinates (Lat/Long), camera model, and lens data instantly and locally. 

### Stage 3: Local Facial Recognition (The "Who")
*   **Tool:** `face_recognition` (Python library built on dlib) or `DeepFace` (running locally).
*   **How it works:** 
    1.  You provide a small "Reference Folder" containing 2-3 clear pictures of key people (e.g., @Sean, @Ghada).
    2.  The script scans every photo entirely locally.
    3.  If it finds a match, it tags the photo's metadata database with the person's `@handle`. 
    4.  **Cost:** $0. It uses your computer's CPU/GPU.

### Stage 4: Scene & Object Detection (The "What")
*   **Tool:** Lightweight local models like `YOLOv8` (for objects: "dog", "car", "beach") or `CLIP` (from OpenAI, but running locally, allowing you to search images by text description).
*   **How it works:** Extracts basic keywords and appends them to the image record.

### Stage 5: Reverse Geocoding (The "Where")
*   **Tool:** Local or free-tier OpenStreetMap (Nominatim) API.
*   **What it does:** Converts GPS coordinates (e.g., `48.8584° N, 2.2945° E`) into human words: `"Paris, France, Eiffel Tower"`.

---

## 3. The Database (The Index)

We do not store the photos inside `sean-vault`.
We create a local SQLite database (e.g., `C:\Users\shareuser\OneDrive\sean-pictures\picture-index.db`) that maps:
`[File Hash] -> [Path] | [Timestamp] | [Location] | [People: @Sean, @Ghada] | [Tags: beach, sunset]`

---

## 4. Integration with Sean-Vault (The Brain)

This is how the massive photo database talks to your Markdown second brain without overwhelming it.

### Feature A: The Event Summarizer
Instead of individual files, a script groups photos by Time and Location. 
If you took 400 photos in Paris over 4 days, the script generates **one** file in the vault: `/log/events/2024-05-Paris-Trip.md`.

*Content of that Markdown file:*
```markdown
# 2024-05 Paris Trip
**Date:** May 12-16, 2024
**Location:** Paris, France
**People:** @Sean, @Ghada
**Total Photos:** 423
**Database Query String:** `event:"2024-05-Paris"`
```
If you ever ask Gemini, "When did we go to Paris and who was there?", it reads this summary instantly.

### Feature B: The '@Person' Memory
Since facial recognition maps to your vault handles, we can add a section to your `/tasks/_persons.md`:
*   `@Ghada` -> Total photos in database: 4,502

### Feature C: Agent Access
We build a small script `picture-search.py`. 
When you ask Gemini, *"Find the picture of me and Adel at a coffee shop,"* Gemini translates that into a CLI query: 
`& picture-search.py --people @Sean,@Adel --tags "coffee, cafe"`
The script returns the top 5 file paths on your OneDrive for you to view.

---

## 5. Execution Roadmap

If we decide to build this, we do it in strict phases to avoid breaking anything:

*   **Phase 1: The Sorter.** Build the deduplication and EXIF extraction. Just get the thousands of files into a clean `YYYY/MM` folder structure with a basic SQLite index.
*   **Phase 2: The Face Scanner.** Implement local facial recognition against a known list of `@handles`.
*   **Phase 3: The Vault Bridge.** Build the script that generates Event Markdown summaries and the `picture-search.py` tool for Gemini to use.

This design completely eliminates the need to pay OpenAI or Google for image processing, keeps your raw data private, and connects perfectly to your `sean-vault` philosophy!
