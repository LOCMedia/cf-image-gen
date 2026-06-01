---
name: cf-image-gen
description: Generate images via Cloudflare Workers AI (Flux family, Leonardo Lucid Origin, Leonardo Phoenix). Use when the user asks to "generate an image", "create an image", "make an image", or invokes /cf-image-gen. Free-plan friendly, routes through a private CF Worker. Supports model selection, aspect-ratio tuning, batch generation, and reference-prompt iteration.
---

# Cloudflare Image Generation Skill

Generate custom images via a private Cloudflare Worker that proxies Workers AI image-gen models. Use for hero illustrations, social posts, blog headers, slide assets, etc.

## Prerequisites

Two environment variables must be set in `~/.claude/settings.json` under `env`:

- `CF_IMAGE_URL` - Worker endpoint (POST `/`)
- `CF_IMAGE_API_KEY` - Bearer token expected by the worker

Verify before any call:

```bash
[ -n "${CF_IMAGE_URL:-}" ] && [ -n "${CF_IMAGE_API_KEY:-}" ] && echo "OK" || echo "MISSING"
```

If MISSING, tell the user and stop - do not attempt fallback.

## Available Models

| Model ID | Best for | Notes |
|---|---|---|
| `@cf/black-forest-labs/flux-1-schnell` | **Default.** Fast iterations, low cost. | 4-step turbo. ~$0.0001/step. Returns base64. |
| `@cf/black-forest-labs/flux-2-klein-4b` | Higher quality, still cheap. | Distilled 4B Flux 2. |
| `@cf/black-forest-labs/flux-2-klein-9b` | Highest Flux quality, high-res. | $0.015 per first MP. |
| `@cf/black-forest-labs/flux-2-dev` | Step-tunable Flux 2, full control. | Bills per-step input+output. |
| `@cf/leonardo/lucid-origin` | Photoreal, cinematic. | $0.007 per 512² tile. |
| `@cf/leonardo/phoenix-1.0` | Illustration, stylized. | $0.0058 per 512² tile. |

Default to `flux-1-schnell` unless the user asks for higher quality or a specific style.

## Workflow

### Step 1: Verify env

```bash
[ -n "${CF_IMAGE_URL:-}" ] && [ -n "${CF_IMAGE_API_KEY:-}" ] && echo "OK" || echo "MISSING"
```

### Step 2: Generate

Use the helper script (Python 3.8+, stdlib only - runs on macOS, Linux, Windows):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/cf-image-gen/scripts/generate.py \
  --prompt "Your detailed image description" \
  --output "/absolute/path/to/output.jpg"
```

On Windows PowerShell, use `python` instead of `python3`. `${CLAUDE_PLUGIN_ROOT}` is the plugin's root directory (set automatically by Claude Code when the plugin is enabled).

**Required flags:**
- `--prompt` - image description (write detailed, specific prompts - see Crafting Prompts)
- `--output` - absolute output path

**Optional flags:**
- `--model <id>` - full model ID (see table above). Default: `@cf/black-forest-labs/flux-1-schnell`.
- `--steps <N>` - sampling steps. Defaults: schnell=4, others=20–50. Higher = better but slower/costlier.
- `--width <px>` / `--height <px>` - image size. Default: 1024×1024. Common: 512, 768, 1024, 1280.
- `--seed <int>` - reproducible generation.
- `--guidance <float>` - CFG scale (3–10 typical, model-dependent).

### Step 3: Multiple images

For batch generation (e.g. 3 variants), fire parallel Bash calls in a single message. Each writes to a distinct `--output` path. Do NOT serialize - they are independent.

### Step 4: Integrate

Reference generated images in HTML/React/CSS by absolute or relative path. Worker returns `image/jpeg` regardless of source model (base64 from flux is decoded server-side).

## Crafting Effective Prompts

Detailed and specific beats short and vague.

**Good:**
> Editorial conceptual illustration of an exploded isometric vault with brushed-steel chevron panels and cyan-edged glass faces on a pure white background, modernist Swiss-design influence, cool architectural studio lighting from upper-left.

**Bad:**
> A security image.

**Include:**
1. **Subject**: what is depicted
2. **Style**: minimalist, hyperreal, illustrated, isometric, photoreal, etc.
3. **Palette**: exact hex anchors if brand-bound
4. **Mood**: corporate, playful, brutalist, editorial
5. **Composition**: centered/off-axis, isometric/orthographic, negative-space placement
6. **Lighting**: directional, studio, soft, dramatic
7. **Negatives**: append "no text, no people, no [unwanted thing]" inline; Workers AI does not have a separate `--no` flag

### Brand-aligned prompts

For brand-consistent imagery, build a single brand-prompt template (palette hex codes, aesthetic anchors, forbidden tropes, motifs) and reference it on every generation. The template acts as a style guard - every prompt should reuse its palette, lighting, and composition vocabulary. See `examples/prompts/showcase-prompts.md` for prompt-structure patterns.

## Errors

| HTTP | Meaning | Action |
|---|---|---|
| 401 | Bad/missing `CF_IMAGE_API_KEY` | Re-check settings.json env |
| 400 | `Invalid model` or `Prompt is required` | Read error JSON, fix payload |
| 405 | Wrong method/path | Ensure POST to `/` |
| 500 | Worker exception | Read `details` field; often a model-specific input mismatch |

## Notes

- Worker route: `POST ${CF_IMAGE_URL}` with JSON body `{prompt, model?, width?, height?, num_steps?, seed?, guidance?}`.
- Response header `X-Model` echoes the model that ran - verify if uncertain.
- For img2img / inpainting, the current worker does not support reference images. If the user needs it, extend the worker.
