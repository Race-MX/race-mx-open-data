"""Render a captionless Race.mx Short: frames timed to VO pauses, slow push-in, crossfades, VO + 1s hold."""
import json, re, subprocess, sys
work, name = sys.argv[1], sys.argv[2]
order = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
segs = json.load(open(f"{work}/segments.json"))[name]
mp3 = f"{work}/{name}.mp3"
out = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-30dB:d=0.09", "-f", "null", "-"], capture_output=True, text=True).stderr
dur = float(re.search(r"Duration: (\d+):(\d+):([\d.]+)", out).groups()[2]) + 60 * int(re.search(r"Duration: (\d+):(\d+)", out).group(2))
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
pauses = [(a + b) / 2 for a, b in zip(st, en) if 0.5 < (a + b) / 2 < dur - 0.3]
def spoken(s):
    s = re.sub(r'\d{4}', 'x' * 12, s)
    return len(re.sub(r'\d', 'x' * 5, s))
total = sum(spoken(s) for s in segs); targets = []; cum = 0
for s in segs[:-1]:
    cum += spoken(s); targets.append(dur * cum / total)
# DP: assign each boundary to a distinct, increasing pause, minimising squared error
import functools
P = pauses; T = targets
@functools.lru_cache(None)
def best(i, j):  # boundary i onward, pauses from index j
    if i == len(T): return (0.0, ())
    if len(P) - j < len(T) - i: return (1e9, ())
    take = best(i + 1, j + 1); take = ((P[j] - T[i]) ** 2 + take[0], (P[j],) + take[1])
    skip = best(i, j + 1)
    return min(take, skip)
cost, picks = best(0, 0)
starts = [0.0] + [round(p, 2) for p in picks]
END = dur + 1.0; X = 0.3
n = len(segs); frames = [f"{work}/frames/{name}_p{(order[k] if order else k + 1)}.png" for k in range(n)]
lens = [(END if k == n - 1 else starts[k + 1] + X / 2) - (0 if k == 0 else starts[k] - X / 2) for k in range(n)]
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"]
for f, L in zip(frames, lens): cmd += ["-loop", "1", "-framerate", "30", "-t", f"{L:.3f}", "-i", f]
cmd += ["-i", mp3]; fc = []
for k, L in enumerate(lens):
    fr = int(round(L * 30))
    fc.append(f"[{k}:v]scale=2160:3840,zoompan=z='1+0.05*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{k}]")
prev = "v0"
for k in range(1, n):
    fc.append(f"[{prev}][v{k}]xfade=transition=fade:duration={X}:offset={starts[k] - X / 2:.3f}[x{k}]"); prev = f"x{k}"
fc.append(f"[{n}:a]apad,atrim=0:{END:.3f}[a]")
cmd += ["-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", f"{END:.3f}", "-movflags", "+faststart", f"{work}/{name}.mp4"]
subprocess.run(cmd, check=True)
print(name, "dur", round(dur, 2), "starts", starts, "targets", [round(t, 1) for t in targets])
