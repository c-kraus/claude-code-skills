# Layout Templates — Ready-to-Use Coordinate Grids

Copy the template that fits, then fill in text and colors. No coordinate math needed.

All templates use these seeds (just increment by 1 for each new element): start at 100001.

---

## Template A — Assembly Line 3 Boxes
**Use for:** 3-step process, A→B→C flows, cause-and-effect chains
**Canvas:** ~740 × 240

```json
{"type":"rectangle","id":"box1","x":40,"y":80,"width":170,"height":70,"strokeColor":"STROKE","backgroundColor":"FILL","fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100001,"version":1,"versionNonce":100002,"isDeleted":false,"groupIds":[],"boundElements":[{"id":"t1","type":"text"}],"link":null,"locked":false,"roundness":{"type":3}},
{"type":"text","id":"t1","x":50,"y":105,"width":150,"height":20,"text":"LABEL 1","originalText":"LABEL 1","fontSize":16,"fontFamily":3,"textAlign":"center","verticalAlign":"middle","strokeColor":"#333333","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100003,"version":1,"versionNonce":100004,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"containerId":"box1","lineHeight":1.25},

{"type":"arrow","id":"arr1","x":212,"y":115,"width":48,"height":0,"strokeColor":"ARROW_COLOR","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100005,"version":1,"versionNonce":100006,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"points":[[0,0],[48,0]],"startBinding":{"elementId":"box1","focus":0,"gap":2},"endBinding":{"elementId":"box2","focus":0,"gap":2},"startArrowhead":null,"endArrowhead":"arrow"},

{"type":"rectangle","id":"box2","x":262,"y":80,"width":170,"height":70,"strokeColor":"STROKE","backgroundColor":"FILL","fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100007,"version":1,"versionNonce":100008,"isDeleted":false,"groupIds":[],"boundElements":[{"id":"t2","type":"text"}],"link":null,"locked":false,"roundness":{"type":3}},
{"type":"text","id":"t2","x":272,"y":105,"width":150,"height":20,"text":"LABEL 2","originalText":"LABEL 2","fontSize":16,"fontFamily":3,"textAlign":"center","verticalAlign":"middle","strokeColor":"#333333","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100009,"version":1,"versionNonce":100010,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"containerId":"box2","lineHeight":1.25},

{"type":"arrow","id":"arr2","x":434,"y":115,"width":48,"height":0,"strokeColor":"ARROW_COLOR","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100011,"version":1,"versionNonce":100012,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"points":[[0,0],[48,0]],"startBinding":{"elementId":"box2","focus":0,"gap":2},"endBinding":{"elementId":"box3","focus":0,"gap":2},"startArrowhead":null,"endArrowhead":"arrow"},

{"type":"rectangle","id":"box3","x":484,"y":80,"width":170,"height":70,"strokeColor":"STROKE","backgroundColor":"FILL","fillStyle":"solid","strokeWidth":2,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100013,"version":1,"versionNonce":100014,"isDeleted":false,"groupIds":[],"boundElements":[{"id":"t3","type":"text"}],"link":null,"locked":false,"roundness":{"type":3}},
{"type":"text","id":"t3","x":494,"y":105,"width":150,"height":20,"text":"LABEL 3","originalText":"LABEL 3","fontSize":16,"fontFamily":3,"textAlign":"center","verticalAlign":"middle","strokeColor":"#333333","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":1,"strokeStyle":"solid","roughness":0,"opacity":100,"angle":0,"seed":100015,"version":1,"versionNonce":100016,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"containerId":"box3","lineHeight":1.25}
```

**Sub-labels below boxes** (y=162, fontSize=11, strokeColor="#64748b", no container):
- box1 sub: x=40, width=170
- box2 sub: x=262, width=170
- box3 sub: x=484, width=170

---

## Template B — Assembly Line 4 Boxes
**Use for:** 4-step processes, Raw Mat→WIP→Fin.Goods→COGS
**Canvas:** ~960 × 240

Boxes at y=80, height=70. Pitch = 230px (box width 170 + gap 60).

| Element | x | y | w | h |
|---|---|---|---|---|
| box1 | 40 | 80 | 170 | 70 |
| arr1 | 212 | 115 | 48 | 0 |
| box2 | 262 | 80 | 170 | 70 |
| arr2 | 434 | 115 | 48 | 0 |
| box3 | 484 | 80 | 170 | 70 |
| arr3 | 656 | 115 | 48 | 0 |
| box4 | 706 | 80 | 170 | 70 |

Text inside each box: same containerId pattern as Template A, x = box.x+10, y = box.y+25, width = box.w-20.

---

## Template C — Split Zone (Left/Right with Divider)
**Use for:** Balance Sheet vs Income Statement, Before/After, Asset vs Expense
**Canvas:** ~1060 × 420

Dividing line at x=700. Left zone: x=40..680. Right zone: x=720..1020.

```json
{"type":"line","id":"divider","x":700,"y":40,"width":0,"height":380,"strokeColor":"#64748b","backgroundColor":"transparent","fillStyle":"solid","strokeWidth":2,"strokeStyle":"dashed","roughness":0,"opacity":100,"angle":0,"seed":200001,"version":1,"versionNonce":200002,"isDeleted":false,"groupIds":[],"boundElements":null,"link":null,"locked":false,"points":[[0,0],[0,380]]}
```

Zone title positions:
- Left title: x=50, y=50, fontSize=18, strokeColor="#cc5500"
- Right title: x=720, y=50, fontSize=18, strokeColor="#047857"

Divider label (top): x=706, y=44, fontSize=12, strokeColor="#047857"

Boxes on left: use Template B shifted to start at x=50.
Box on right: x=730, y=80, width=170, height=70 — End/Success color (#a7f3d0/#047857).

Crossing arrow (bold, green): strokeWidth=3, strokeColor="#047857", from right edge of last left box to left edge of right box.

---

## Template D — 2-Column Comparison
**Use for:** FIFO vs Weighted Average, HGB vs IFRS, Method A vs Method B
**Canvas:** ~700 × 380

```
| Left Column (Method A) | Right Column (Method B) |
x=40..320                 x=360..640
```

Column header boxes (y=40, h=50, w=280):
- Left: x=40, y=40, End/Success or Primary color
- Right: x=360, y=40, Secondary color

Row boxes (h=60, gap=10):
- Row 1: y=110, both columns
- Row 2: y=180, both columns
- Row 3: y=250, both columns
- Result row: y=330, h=40, bold

Vertical divider: x=340, y=40 to y=380, dashed, slate.

---

## Template E — Vertical Timeline
**Use for:** Historical sequence, step-by-step process, chronological events
**Canvas:** ~500 × 500

Spine line: x=100, y=60 to y=460 (vertical, strokeColor="#ff6a00", strokeWidth=2).

Each event: dot at (94, y), label at (120, y-8).
Dot template: ellipse, x=94, y=EVENT_Y, width=12, height=12, fill="#ff6a00", stroke="#ff6a00".
Label template: text, x=120, y=EVENT_Y-8, fontSize=15, strokeColor="#333333".
Sub-label: text, x=120, y=EVENT_Y+12, fontSize=11, strokeColor="#64748b".

Event y-positions (evenly spaced, 5 events): 80, 160, 240, 320, 400.

---

## Template F — Hub and Spoke (1 center → N outputs)
**Use for:** One principle driving multiple consequences, root cause → effects
**Canvas:** ~700 × 400

Center box: x=270, y=165, w=160, h=70 (hero size).
Spoke targets at radius ~220px around center (center point 350, 200):
- Top:    x=280, y=20
- Right:  x=530, y=165
- Bottom: x=280, y=310
- Left:   x=20,  y=165

Each spoke: arrow from center box edge to target box edge. Use `points` with slight curve if needed.

---

## Quick Reference: Box Pitch Formula

When placing N boxes in a row with gap G and box width W:
- Box i starts at: `x = MARGIN + i * (W + G)`
- Arrow starts at: `x = MARGIN + i*(W+G) + W + 2` (right edge + gap)
- Arrow ends at: `x = MARGIN + (i+1)*(W+G) - 2` (next box left edge - gap)
- Arrow width: `G - 4`

Standard values: W=170, G=60, MARGIN=40 → pitch=230.
