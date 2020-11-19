import os
import re

mp4path = '2020-11-16'
ffmpegpath = 'D:\\blackbox\\ffmpeg\\bin\\ffmpeg.exe'

parse = r'REC_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+)_(.)\.MP4'

frontmp4s = []
rearmp4s = []

print('list of mp4 files..')

files = os.listdir(mp4path)
for f in files:
    print(f)
    m = re.match(parse, f)
    if not m:
        continue
    fr = m.group(7)
    timestamp = ''
    for i in range(1, 7):
        timestamp += m.group(i)
    timestamp = int(timestamp)
    print(timestamp)
    lpath = mp4path+'/'+f
    tp = (lpath, timestamp)
    if fr == 'F':
        frontmp4s.append(tp)
    elif fr == 'R':
        rearmp4s.append(tp)
frontmp4s = sorted(frontmp4s, key=lambda x: x[1])
rearmp4s = sorted(rearmp4s, key=lambda x: x[1])

with open('tmp.txt', 'w+') as f:
    for (fp, _) in frontmp4s:
        f.write("file '"+fp+"'\n")

os.system(f'{ffmpegpath} -f concat -safe 0 -i tmp.txt -c copy results/{mp4path}_F.mp4')

with open('tmp.txt', 'w+') as f:
    for (fp, _) in rearmp4s:
        f.write("file '"+fp+"'\n")

os.system(f'{ffmpegpath} -f concat -safe 0 -i tmp.txt -c copy results/{mp4path}_R.mp4')

print('concatenation done. clean up tmp.txt')
os.remove('tmp.txt')
