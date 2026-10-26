import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

GREEN = '#4ade80'; NAVY = '#142f73'; DARKBG = '#0b1220'; LIGHT = '#eef2f8'

def bundle(block, back, back_op):
    return (f'<rect x="128" y="138" width="256" height="150" rx="34" fill="{back}" fill-opacity="{back_op}" transform="rotate(-7 256 213)"/>'
            f'<rect x="104" y="184" width="304" height="176" rx="40" fill="{block}"/>'
            f'<rect x="220" y="168" width="72" height="208" rx="14" fill="{GREEN}"/>')

def icon(bg, block, back_op):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><title>MoSuBi</title>'
            f'<rect width="512" height="512" fill="{bg}"/>{bundle(block, block, back_op)}</svg>')

def mark(block, back_op):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="96 124 320 256"><title>MoSuBi</title>'
            f'{bundle(block, block, back_op)}</svg>')

def text_path(s, size, x0, baseline, tracking=-0.01):
    f = TTFont('font/fredoka600.ttf'); gs = f.getGlyphSet(); cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm; sc = size / upm; x = 0; d = []
    for ch in s:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x0 + x, baseline)))
        d.append(pen.getCommands())
        x += f['hmtx'][g][0] * sc + tracking * size
    return ' '.join(d), x

def wordmark(block, back_op, word):
    # mark 320x256 scaled to height 160, then text cap-aligned
    h = 160; s = h / 256; gap = 36
    d, w = text_path('MoSuBi', 168, 320 * s + gap, 138)
    W = round(320 * s + gap + w + 4)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}"><title>MoSuBi</title>'
            f'<g transform="scale({s}) translate(-96 -124)">{bundle(block, block, back_op)}</g>'
            f'<path d="{d}" fill="{word}"/></svg>')

out = {
  'mosubi-icon.svg': icon(NAVY, '#ffffff', .32),
  'mosubi-icon-dark.svg': icon(DARKBG, LIGHT, .22),
  'mosubi-mark.svg': mark(NAVY, .28),
  'mosubi-mark-on-dark.svg': mark(LIGHT, .25),
  'mosubi-wordmark.svg': wordmark(NAVY, .28, NAVY),
  'mosubi-wordmark-on-dark.svg': wordmark(LIGHT, .25, LIGHT),
}
for k, v in out.items(): open('out/' + k, 'w').write(v)
print('ok')
# Green-text versions (Cuong, 2026-10-26)
open('out/mosubi-wordmark-green.svg', 'w').write(wordmark('#ffffff', .3, GREEN))         # for navy or dark backgrounds
open('out/mosubi-wordmark-green-on-light.svg', 'w').write(wordmark(NAVY, .28, GREEN))   # for white backgrounds
