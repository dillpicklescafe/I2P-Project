# Static fallback frontend integration

No functional frontend change is required for the new fallback images.

The Flask library and recommendation payloads already expose `media_url` and
`media_type`. The existing frontend behavior provides the required priority:

1. `exercise_media.get_exercise_media()` selects an existing GIF/MP4 first.
2. It selects an approved static fallback when animated media is unavailable.
3. It returns `None` when neither exists, preserving `Demo coming soon`.

`static/app.js` already:

- accepts `jpg` and `png` in exercise payload validation;
- renders MP4 media with a `<video>` element;
- renders GIF and static image URLs with an `<img>` element;
- avoids animated-frame extraction for non-GIF/non-MP4 workout thumbnails;
- keeps the complete ordered exercise instructions in the preview's **How to
  Perform** section.

The new files use `media_type: "jpg"`, so they are displayed as ordinary
static `<img>` elements in both the Exercise Library and Generated Workout
Plan. They are not treated as animated demonstrations.

## Optional semantic improvement requiring frontend ownership approval

The current shared image alt text says “demonstration” for every `<img>`. A
future teammate-owned frontend change could distinguish static illustrations:

```javascript
const isStaticIllustration = ["jpg", "png", "webp"].includes(exercise.media_type);
image.alt = isStaticIllustration
  ? `${exercise.name} key-position illustration`
  : `${exercise.name} demonstration`;
```

This accessibility wording improvement is not required for rendering and was
not applied here.
