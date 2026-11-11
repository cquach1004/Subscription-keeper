# MoSuBi explainer video (phone, 1080x1920, 13.5s)

- `video.src.html` + `build_video_html.py` -> `video.html` (pulls the character art from ../src/app.html). Open video.html to preview; `window.seek(t)` drives every frame.
- `render.js <frames-dir>` captures 30fps frames with Playwright; `make_audio.py` synthesizes music + sound effects to `audio.wav`.
- Mux: `ffmpeg -framerate 30 -i frames/f%04d.jpg -i audio.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -shortest mosubi-explainer-v1.mp4`
- Voiceover: Cuong generates it with an AI voice tool and uploads it; mix it over audio.wav (duck the music a little).

Voiceover script (timings):
- 0.3-3.0  "Subscriptions add up fast."
- 3.6-6.0  "Meet Subi, your pocket coach."
- 6.4-9.8  "Tell Subi what you have, and get a simple game plan to save."
- 10.4-13.2 "MoSuBi. Spend less on subscriptions. It's free."

v2 (2026-11-11): 14.5s, Cuong's AI voiceover (voiceover-original.mp3) cut at its pauses and placed at 0.4, 3.7, 6.4, 10.7, 11.65, 13.4s (voice-timed.wav), music ducked under it (final-audio.wav) -> mosubi-explainer-v2.mp4. ffmpeg commands are in the project memory thread; scene 4 timings moved earlier to match "MoSuBi" being spoken.
