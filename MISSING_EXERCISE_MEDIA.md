# LockIn exercises missing approved media

Active exercises missing approved media: **27** of **155**.

All **176** source exercise records and original IDs remain in `exercises.py`.
Twenty-one records are preserved but excluded from the active recommendation
pool, so they are not assigned as media tasks.

## Active missing media

### Beginner — 2

`128, 161`

### Intermediate — 11

`103, 124, 156, 158, 162, 163, 164, 165, 166, 167, 168`

### Advanced — 14

`152, 153, 154, 155, 157, 159, 160, 169, 170, 172, 173, 174, 175, 176`

## Preserved but inactive records — 21

`62, 63, 64, 73, 74, 77, 84, 87, 90, 97, 104, 112, 113, 114, 117, 119, 126, 132, 133, 135, 136`

ID 132 (Single-leg Ball Pass) remains in the source database but is inactive
because ball equipment is not supported. The other twenty records were removed
from recommendations with approval and coverage validation. No record was
deleted or renumbered.

## Unresolved active Beginner media

IDs `128` and `161` remain active because they are essential to three-exercise
Beginner coverage. They are tracked as unresolved missing media, not as media
tasks assigned to the user.

## Reviewed user-saved files

Validated media is registered for IDs:

`31, 38, 41, 44, 45, 50, 54, 55, 57, 58, 59, 67, 69, 72, 75`

ID `59` now maps to the visually validated `static/exercises/59-replacement.gif`.
The rejected `static/exercises/59.gif` is preserved but remains unmapped because
it demonstrates a cobra press-up rather than the instructed Prone Cobra Hold.
Beginner ID `63` is preserved but is now excluded from recommendations after
the complete coverage simulation passed without it.

Saved files `103.gif` and `124.gif` are preserved but remain unmapped after
visual review. Respectively, they show a moving bear crawl rather than a
stationary hold and an incomplete clock reach without the full 12/3/6 sequence
and leg switch. Matching replacement media is still required for both.

ID `151` now maps to the frame-by-frame validated
`static/exercises/151-replacement.gif`. The old `static/exercises/151.gif` is
preserved but intentionally unused.

The Flask UI handles an active exercise without approved media by returning a
null `media_url` and rendering the exercise without a demonstration.
