"""
Builds the thesis-defence video: slides (HTML -> PNG, 1920x1080, Chromium) + Turkish narration (Piper TTS, offline,
voice tr_TR-dfki-medium; nothing leaves the machine) + soft subtitles -> thesis_exp/video/SAVUNMA.mp4
Usage: python3 thesis_exp/video/build_video.py --voice /path/tr_TR-dfki-medium.onnx
"""
import sys, json, subprocess, argparse, pathlib, html, re, wave
H = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(H))
from slides import SLIDES
ap = argparse.ArgumentParser(); ap.add_argument("--voice", required=True); a = ap.parse_args()
B = H / "build"; B.mkdir(exist_ok=True)

CSS = """
*{box-sizing:border-box} body{margin:0;width:1920px;height:1080px;font-family:'DejaVu Sans',sans-serif;background:#fbfbf8;color:#1b1f24}
.bar{height:14px;background:#1f4e79} .wrap{padding:56px 90px} h1{font-size:54px;color:#1f4e79;margin:10px 0 30px}
ul{font-size:34px;line-height:1.5;padding-left:40px} li{margin-bottom:14px} ul.small{font-size:26px} ul.concl{font-size:34px}
pre{font-family:'DejaVu Sans Mono',monospace;font-size:24px;background:#0f1720;color:#e6edf3;padding:28px 32px;border-radius:10px;line-height:1.45;white-space:pre}
.file{font-family:'DejaVu Sans Mono',monospace;font-size:22px;color:#5b6470;margin-bottom:10px}
.def{font-size:30px;background:#eef4fa;border-left:8px solid #1f4e79;padding:18px 24px;margin-top:22px}
.eq{font-size:44px;text-align:center;margin:30px 0 40px;color:#1f4e79}
img{display:block;margin:0 auto;max-width:1600px;max-height:720px} .cap{font-size:26px;color:#3b4450;text-align:center;margin-top:18px}
table.t{border-collapse:collapse;margin:10px auto;font-size:30px} table.t th,table.t td{border:1px solid #c9d1da;padding:12px 20px;text-align:left}
table.t th{background:#eef2f6} table.t.sm{font-size:24px} table.t.sm td{padding:10px 16px}
.title{display:flex;flex-direction:column;justify-content:center;height:1066px;padding:0 120px}
.title h1{font-size:68px} .sub{font-size:40px;color:#3b4450;margin-bottom:40px} .who{font-size:30px;color:#5b6470}
.src{position:absolute;bottom:22px;right:40px;font-size:18px;color:#8a929c} .num{position:absolute;bottom:22px;left:40px;font-size:18px;color:#8a929c}
"""
shot_js = B / "shot.js"
shot_js.write_text("""const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1920,height:1080}});
  for (const f of process.argv.slice(2)) { await p.goto('file://' + f, {waitUntil:'load'}); await p.screenshot({path: f.replace('.html','.png')}); }
  await b.close(); })();""")
htmls = []
for i, s in enumerate(SLIDES, 1):
    inner = (f'<div class="title"><h1>{html.escape(s["title"])}</h1>{s["body"]}</div>' if s["kind"] == "title"
             else f'<div class="wrap"><h1>{html.escape(s["title"])}</h1>{s["body"]}</div>')
    src = f'<div class="src">Kaynak: {html.escape(s["src"])}</div>' if s["src"] else ""
    page = f'<!doctype html><html lang="tr"><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="bar"></div>{inner}{src}<div class="num">{i} / {len(SLIDES)}</div></body></html>'
    f = B / f"s{i:02d}.html"; f.write_text(page.replace('src="../img/', f'src="{H}/img/')); htmls.append(str(f))
subprocess.run(["node", str(shot_js), *htmls], check=True)

srt, t, clips = [], 0.0, []
fmt = lambda x: f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(x * 1000) % 1000:03d}"
for i, s in enumerate(SLIDES, 1):
    wav = B / f"s{i:02d}.wav"
    subprocess.run([sys.executable, "-m", "piper", "-m", a.voice, "-f", str(wav), "--sentence-silence", "0.35"], input=s["say"].encode(), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with wave.open(str(wav)) as w:
        dur = w.getnframes() / w.getframerate()
    clip = B / f"s{i:02d}.mp4"; total = dur + 1.2
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(B / f"s{i:02d}.png"), "-i", str(wav),
                    "-af", "apad=pad_dur=1.2", "-t", f"{total:.2f}", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                    "-r", "25", "-c:a", "aac", "-b:a", "128k", str(clip)], check=True)
    clips.append(clip)
    # subtitles: one cue per sentence, time proportional to length
    sents = [x for x in re.split(r"(?<=[.?!])\s+", s["say"].replace("\n", " ")) if x.strip()]
    L = sum(len(x) for x in sents); tt = t
    for x in sents:
        d = dur * len(x) / L
        srt.append(f"{len(srt) + 1}\n{fmt(tt)} --> {fmt(tt + d)}\n{x}\n"); tt += d
    t += total
    print(f"slide {i}: {dur:.1f} s", flush=True)
(B / "list.txt").write_text("".join(f"file '{c}'\n" for c in clips))
(H / "SAVUNMA.srt").write_text("\n".join(srt))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(B / "list.txt"), "-i", str(H / "SAVUNMA.srt"),
                "-map", "0", "-map", "1", "-c", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=tur", str(H / "SAVUNMA.mp4")], check=True)
(H / "ANLATIM.md").write_text("# Savunma videosu: anlatım metni\n\n" + "\n\n".join(f"## {i}. {s['title']}\n\n{s['say']}" for i, s in enumerate(SLIDES, 1)) + "\n")
print(f"wrote SAVUNMA.mp4 ({t / 60:.1f} min)")
