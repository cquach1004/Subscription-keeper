# Fills video.src.html with the character art from ../src/app.html -> video.html
import os
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, '..', 'src', 'app.html')).read().split('\n')
want = ['const MARK =', 'const N =', 'const SUBI_BASE', 'const armL', 'const eyes', 'const cheeks', 'const COACH_BASE', 'const COACH_OUTLINE', 'const SHORTS', 'const REF_STRIPES']
art = [l for l in src if any(l.startswith(w) for w in want)]
assert len(art) == len(want), len(art)
def block(name):
    i = next(k for k, l in enumerate(src) if l.startswith('const ' + name + ' = {'))
    j = next(k for k in range(i, len(src)) if src[k] == '};')
    return src[i:j + 1]
art += block('SUBI_POSE') + block('COACH_GEAR')
open(os.path.join(H, 'video.html'), 'w').write(open(os.path.join(H, 'video.src.html')).read().replace('/*__ART__*/', '\n'.join(art)))
print('video.html built')
