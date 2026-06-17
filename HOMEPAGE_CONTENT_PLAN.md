# Homepage Content Plan

This redesign is now set up so the homepage can be driven through Wagtail content without changing models.

## Recommended homepage structure

Create or edit the homepage as a `GenericPage` and use the following `body` block order:

1. `post`
   - This becomes the full homepage hero automatically.
   - `heading_small`: short eyebrow like `Georgia Tech Rowing`
   - `heading_large`: main headline like `Built on early mornings and team speed.`
   - `paragraph`: 1-2 sentence intro
   - `photo`: use `VM-03.jpg`
   - `page`: optional CTA target such as recruitment/contact page
   - `document`: optional second CTA such as handbook or recruiting packet

2. `section`
   - Add a heading block and paragraph block for a short brand/mission section.
   - Good use for `DSC09298.dng` as a warm atmosphere section.

3. `post`
   - Use this as a secondary feature section.
   - Recommended image: `DSCF0511.jpg`
   - Suggested theme: team culture, training, or race preparation.

4. `section`
   - Add supporting content for alumni support, recruiting, or program values.

## Recommended image mapping

- `VM-03.jpg`
  - Use as the first `post` block photo.
  - This is the strongest homepage hero option.

- `DSC09298.dng`
  - Convert/export to a web-friendly format if needed before uploading.
  - Use in a secondary section focused on early mornings, discipline, or training atmosphere.

- `DSCF0511.jpg`
  - Use as a wide supporting image for team scale and environment.

- `test.mov`
  - Treat as an optional later enhancement.
  - If used, it should replace or support the homepage hero only after visual QA.

## Suggested homepage copy direction

- Eyebrow: `Georgia Tech Rowing`
- Hero headline: `Built on early mornings and team speed.`
- Hero body: `We train, race, and grow together on the water, building a club program rooted in commitment, competition, and community.`

## Suggested CTA targets

- Primary CTA: recruiting or interest form page
- Secondary CTA: donations or member portal depending on audience

## Notes

- The first `post` block on a `GenericPage` now renders as a hero automatically.
- Later `post` blocks render as editorial split sections.
- `section` blocks render as polished content cards in the new visual system.
- Public page templates have been updated to match this same style direction across the site.
