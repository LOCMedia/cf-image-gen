const ALLOWED_MODELS = new Set([
    "@cf/black-forest-labs/flux-1-schnell",
    "@cf/black-forest-labs/flux-2-dev",
    "@cf/black-forest-labs/flux-2-klein-4b",
    "@cf/black-forest-labs/flux-2-klein-9b",
    "@cf/leonardo/lucid-origin",
    "@cf/leonardo/phoenix-1.0",
]);

const DEFAULT_MODEL = "@cf/black-forest-labs/flux-1-schnell";

export default {
    async fetch(request, env) {
        const API_KEY = env.API_KEY;
        const url = new URL(request.url);
        const auth = request.headers.get("Authorization");

        if (auth !== `Bearer ${API_KEY}`) {
            return json({ error: "Unauthorized" }, 401);
        }

        if (request.method !== "POST" || url.pathname !== "/") {
            return json({ error: "Not allowed" }, 405);
        }

        try {
            const { prompt, model, ...rest } = await request.json();

            if (!prompt) return json({ error: "Prompt is required" }, 400);

            const selectedModel = model ?? DEFAULT_MODEL;
            if (!ALLOWED_MODELS.has(selectedModel)) {
                return json({
                    error: "Invalid model",
                    allowed: [...ALLOWED_MODELS],
                }, 400);
            }

            const inputs = selectedModel.startsWith("@cf/black-forest-labs/flux-2-")
                ? await buildMultipart({ prompt, ...rest })
                : { prompt, ...rest };

            const result = await env.AI.run(selectedModel, inputs);

            const { bytes, contentType } = await normalizeImage(result);

            return new Response(bytes, {
                headers: {
                    "Content-Type": contentType,
                    "X-Model": selectedModel,
                },
            });
        } catch (err) {
            return json({ error: "Failed to generate image", details: err.message }, 500);
        }
    },
};

async function buildMultipart(fields) {
    const form = new FormData();
    for (const [key, value] of Object.entries(fields)) {
        if (value === undefined || value === null) continue;
        form.append(key, String(value));
    }
    const wrapper = new Response(form);
    return {
        multipart: {
            body: wrapper.body,
            contentType: wrapper.headers.get("content-type"),
        },
    };
}

async function normalizeImage(result) {
    if (result instanceof ReadableStream) {
        return { bytes: result, contentType: "image/jpeg" };
    }
    if (result instanceof ArrayBuffer || result instanceof Uint8Array) {
        return { bytes: result, contentType: "image/jpeg" };
    }
    if (result && typeof result === "object" && typeof result.image === "string") {
        const bytes = Uint8Array.from(atob(result.image), (c) => c.charCodeAt(0));
        return { bytes, contentType: "image/jpeg" };
    }
    throw new Error("Unrecognized model response shape");
}

function json(data, status = 200) {
    return new Response(JSON.stringify(data), {
        status,
        headers: { "Content-Type": "application/json" },
    });
}
