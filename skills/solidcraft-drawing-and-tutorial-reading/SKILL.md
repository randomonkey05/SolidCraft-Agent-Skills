---
name: solidcraft-drawing-and-tutorial-reading
description: Use when a SolidCraft model must be built from a drawing, PDF, tutorial video or transcript: extract the geometry, plan numerically, build with checkpoints and verify with measure.
---

# Reading drawings, PDFs, videos and transcripts for SolidCraft

Use with `solidcraft-modeling` (commands), `solidcraft-tutorial-recipes` (validated recipes and traps) and `solidcraft-sweep-and-boolean-hangs`.

## 1. Extract the source
- **PDF drawing:** rasterize the page (for example `pdftoppm -r 150`) and also extract its text. Read every dimension, note, fillet callout and the material or density. Anything missing (a density, an undimensioned fillet) is reported as an assumption in the notes you hand over.
- **Video without a transcript:** an agent cannot hear audio, so transcribe it first with any speech-to-text tool you have (for example `faster-whisper`, model `small`, runs on CPU). Where the tool must run depends on your setup: if the machine that holds the video cannot install it, run it somewhere that can. Two practical notes: load the audio as a 16 kHz wav with numpy if the decoder in your `av` version fails, and always hand the `.txt` or `.srt` back to the user.
- **Use both sources:** the transcript gives the ORDER of operations and the intent. Frames give the NUMBERS (`ffmpeg -ss <time> -i file.mp4 -frames:v 1 -vf scale=1100:-1 out.png`, or a contact sheet). Spoken numbers are often wrong ("14 / 18 / 19" for 40 / 80 / 90), and tutorials with similar names can have different dimensions.
- **Video plus a written transcript (.docx):** read it (a .docx is a zip, the text is in `word/document.xml`). Machine translation mangles numbers.
- **Silent videos** give an empty transcript. Read dimensions from frames and measure unlabeled positions in pixels against a known width.
- Work on copies. Keep scratch frames outside the folder that holds your skills.

## 2. Plan in numbers before touching the app
- Write a parameter table and a coordinate list for each profile. Choose the origin to match the drawing's datum.
- Use the fewest features. Put the whole side profile (with concave fillets drawn in 2D) in one sketch, trim with one intersect from a plan sketch, and build holes as ONE clean cut after the solid exists.
- Compute the expected volume or mass and the bounding box so every `measure` can be checked.
- Mark the risky steps (booleans between coincident or curved faces, fillets near thin features, ANY boolean on a swept body) and isolate each in its own call.

## 3. Build safely
- Save a checkpoint before every risky step. The app can hang for more than 60 s and restart, losing the whole design with no crash report.
- Avoid coincident cylindrical faces (do not pre-cut a hole and then add a ring of the same radius). Avoid coplanar booleans: overlap the tool, or make the solid longer and intersect afterwards.
- Do every feature in the drawing, fillets included, rather than skipping them to save time. Pick the fillet regime first (see `solidcraft-robust-build-order`), do one risky fillet per call, and checkpoint first.
- Use `fit:"reduce"` on a fillet only when the exact radius fails, and record the reduced value.
- A failed batch rolls everything back. Fix only the failing step and resend.
- If a call hangs: check `running` once and tell the user. Do not poll with `sleep` and do not queue more commands. After a restart, reopen the checkpoint and never repeat the same boolean more than once.

## 4. Verify and deliver
- `measure` the volume, mass and bounding box against the plan, and take an isometric screenshot (plus the underside if relevant). Fix problems before reporting.
- For timed tests, note the start time at file creation and at the final save. Report the time, the number of features (sketches counted separately), crashes or restarts, missing items and assumptions in a notes file next to the model.
- Suggested delivery convention: one folder per model holding the design file, `.3mf`, `.stl` and a preview image. New versions go in the same folder under a new name (`_v2`). Flag checkpoint files.

## 5. Tutorial builds versus timed tests
- Tutorial authors build step by step, pick whole regions, create a new body first and use one to three booleans. Models built blind for timed tests tend to use many cuts and intersects, which is where hangs and wrong volumes come from. Copy the tutorial habit: new body first, few booleans, parameters for key distances.
- In both cases only the author's video or audio reveals details a blind build misses (a hemisphere instead of a dome, a toroid instead of a second arc). Watch or transcribe it before the final version and compare with `measure`.
