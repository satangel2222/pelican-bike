import subprocess, time, os
from PIL import Image
import numpy as np

# Start new Chrome tab with the HTML file
subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-Command",
    'Start-Process "file:///D:/test ai/pelican-bike.html"'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2.5)

# Screenshot twice with gap
subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command",
    r"& 'C:/Users/Casp/.claude/skills/desktop-window-shot/shot-window.ps1' -Match Chrome -Out 'D:/test ai/fr9.png'"],
    capture_output=True, timeout=20000)
time.sleep(0.4)
subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command",
    r"& 'C:/Users/Casp/.claude/skills/desktop-window-shot/shot-window.ps1' -Match Chrome -Out 'D:/test ai/fr10.png'"],
    capture_output=True, timeout=20000)

img9 = np.array(Image.open(r"D:\test ai\fr9.png"))
img10 = np.array(Image.open(r"D:\test ai\fr10.png"))

# Check top-left counter region (x=8-180, y=8-45)
c1 = img9[8:50, 8:200]
c2 = img10[8:50, 8:200]

# Green text pixels (R=0-80, G>150, B=0-80)
g1 = c1[:,:,1]
g2 = c2[:,:,1]
r1 = c1[:,:,0]
r2 = c2[:,:,0]
green1 = (g1 > 150) & (r1 < 80)
green2 = (g2 > 150) & (r2 < 80)

print(f"Frame 9 green pixels: {green1.sum()}")
print(f"Frame 10 green pixels: {green2.sum()}")
print(f"Counter region diff: {(green1 != green2).sum()} px")

# Save counter region
region = img9[8:50, 8:220]
Image.fromarray(region).save(r"D:\test ai\counter_region.png")
print("Counter region saved: D:/test ai/counter_region.png")

# Overall diff
diff = np.abs(img9.astype(int) - img10.astype(int))
pct = (diff.max(axis=2) > 5).mean() * 100
print(f"Overall frame diff: {pct:.2f}%")

# Brightness analysis of wheel area
w1 = img9[340:445, 450:560]
w2 = img10[340:445, 450:560]
wdiff = np.abs(w1.astype(int) - w2.astype(int)).max(axis=2)
print(f"Wheel region changed pixels: {(wdiff>3).mean()*100:.2f}%")
