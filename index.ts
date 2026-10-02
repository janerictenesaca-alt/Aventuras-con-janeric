import { config as loadEnv } from "dotenv";
import { createHiggsfieldClient } from "@higgsfield/client/v2";

// Server-side only: credentials are read from .env.local and never printed.
loadEnv({ path: ".env.local" });

const MODEL = "bytedance/seedance-2.5/text-to-video";

async function main(): Promise<number> {
  const credentials = process.env.HF_CREDENTIALS;
  if (!credentials || !credentials.includes(":")) {
    console.error("HF_CREDENTIALS is missing or not in key-id:key-secret format. Set it in .env.local.");
    return 1;
  }

  const client = createHiggsfieldClient({ credentials });

  let result;
  try {
    result = await client.subscribe(MODEL, {
      input: {
        prompt: "A cinematic scene at sunset",
        duration: 5,
        resolution: "720p",
        aspect_ratio: "16:9",
      },
      withPolling: true,
    });
  } catch (err) {
    console.error("Request failed:", err instanceof Error ? `${err.name}: ${err.message}` : "unknown error");
    return 1;
  }

  const status = String(result.status);
  switch (status) {
    case "completed": {
      const url = result.video?.url;
      if (!url) {
        console.error(`Request ${result.request_id} completed but returned no video URL.`);
        return 1;
      }
      console.log(`Video URL: ${url}`);
      return 0;
    }
    case "nsfw":
      console.error(`Request ${result.request_id} was rejected by moderation (credits refunded). No video generated.`);
      return 1;
    case "failed":
      console.error(`Request ${result.request_id} failed (credits refunded). No video generated.`);
      return 1;
    case "canceled":
    case "cancelled":
      console.error(`Request ${result.request_id} was canceled. No video generated.`);
      return 1;
    default:
      console.error(`Request ${result.request_id} ended in unexpected status "${status}". No video generated.`);
      return 1;
  }
}

main().then((code) => process.exit(code));
