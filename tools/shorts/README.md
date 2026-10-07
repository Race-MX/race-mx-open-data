# Race MX YouTube Shorts tooling

Builds the vertical Shorts for the Race MX channel (@race-mx). Facts come only from `data/` in this repo.

Pipeline per Short:
1. Script: 5-6 short lines, facts checked against `data/*.csv`. Save as `<batch>/segments.json` (`{name: [line, ...]}`).
2. Voice: ElevenLabs, voice "Bill Belcamino 1", model eleven_multilingual_v2, 1 generation. Save as `<batch>/<name>.mp3`.
3. Frames: `python3 -I tools/shorts/frames.py <batch>/frames.json <batch>/frames` (one page per script line; themes desert / night / electric; keep text in the top half).
4. Video: `python3 -I tools/shorts/slideshow.py <batch> <name> [frame_order]` -> `<batch>/<name>.mp4` (scene cuts snapped to pauses in the voiceover).
5. Captions: upload the MP4 to Descript, Agent Underlord adds Manrope captions at y=1400 (orange #D9541E active word), publish privately.
6. Post: Metricool (brand 7295174, America/Phoenix), YouTube type "short", category SPORTS, madeForKids false, isAiGeneratedContent true.

`specs/` holds the batch 1 and 2 frame and script specs, so new batches can avoid repeating topics.
