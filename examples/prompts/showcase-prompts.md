# Showcase Prompts

Six generic prompts demonstrating range across the six allowlisted models. Each prompt is paired with a model whose strengths suit the brief. Resulting images live in `examples/sample_images/`.

Use these as starting points - copy, edit, and swap models freely.

---

## 1. Abstract geometric hero: `flux-1-schnell`

Fast iteration, low cost. Good for ideation and bulk variants.

**Prompt:**
> Editorial isometric illustration of floating translucent glass cubes stacked in an off-axis tower on a soft cream background, each cube refracting pale teal and warm peach light at the edges, minimalist Swiss-design composition, generous negative space, soft directional studio lighting from upper-left, no text, no people.

**Flags:** `--model @cf/black-forest-labs/flux-1-schnell --width 1024 --height 1024`

---

## 2. Editorial product still: `flux-2-klein-4b`

Mid-tier Flux 2 quality at low cost.

**Prompt:**
> Hyperreal product photograph of a single matte-ceramic coffee cup centered on a white seamless backdrop, soft cinematic key light raking from the upper right, subtle wisp of steam, shallow depth of field, faint warm shadow pooling beneath the cup, magazine-cover composition, no text, no logo.

**Flags:** `--model @cf/black-forest-labs/flux-2-klein-4b --width 1024 --height 1024`

---

## 3. Architectural cinematic: `flux-2-klein-9b`

Top-tier Flux 2 quality. Worth the cost for hero images that need to hold up at full resolution.

**Prompt:**
> Cinematic exterior render of a brutalist concrete observatory perched on a windswept cliff at blue hour, sky in muted indigo and slate grey, single warm interior light glowing through a slit window, low-hanging sea fog wrapping the base of the structure, distant horizon line, wide cinematic aspect, architectural photography, no people, no text.

**Flags:** `--model @cf/black-forest-labs/flux-2-klein-9b --width 1280 --height 720`

---

## 4. Conceptual illustration: `flux-2-dev`

Step-tunable. Bump `--steps` to 40+ when you need finer detail; drop to 15–20 for drafts.

**Prompt:**
> Conceptual editorial illustration of a hand gently releasing a paper origami crane into a gradient sky transitioning from dusty rose to pale lavender, soft watercolor texture, hand-painted feel, minimalist composition with the crane positioned in the upper-right third, faint negative-space cloud forms, gentle and contemplative mood.

**Flags:** `--model @cf/black-forest-labs/flux-2-dev --steps 30 --width 1024 --height 1024`

---

## 5. Photoreal macro: `leonardo/lucid-origin`

Photorealism specialist. Excels at texture-heavy macro and natural light.

**Prompt:**
> Macro photograph of a single dew-covered fern frond against a soft out-of-focus forest background in early morning light, individual water droplets catching the cool blue ambient light and a single warm highlight from off-frame sunrise, extreme shallow depth of field, naturalistic colors, no people, no text.

**Flags:** `--model @cf/leonardo/lucid-origin --width 1024 --height 1024`

---

## 6. Stylized illustration: `leonardo/phoenix-1.0`

Painterly and illustrative - leans into stylization over realism.

**Prompt:**
> Stylized digital illustration of a small wooden sailboat drifting across a calm dawn lake, distant mountains rendered in flat layered silhouettes of teal and rose, soft brush-textured sky with two small high clouds, painterly Studio-Ghibli-influenced light, warm and tranquil mood, square composition.

**Flags:** `--model @cf/leonardo/phoenix-1.0 --width 1024 --height 1024`

---

## Writing your own prompts

Effective prompts name **six** things:

1. **Subject**: what is depicted
2. **Style**: illustration / photoreal / isometric / editorial / painterly
3. **Palette**: name the colors, or anchor with hex if brand-bound
4. **Lighting**: directional, time-of-day, mood
5. **Composition**: centered / rule-of-thirds / isometric / macro / wide
6. **Negatives**: append `no text, no people, no [unwanted thing]` inline (Workers AI has no separate negative-prompt flag)

Detailed and specific beats short and vague every time.
