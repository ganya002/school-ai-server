# Client guide (TTS gateway)

> How a student or an app calls this team's text-to-speech service. The public URL below is a **placeholder**. Never commit a real tailnet, hostname, domain or API key.

The gateway is planned to be reachable from **any network** (school, home, mobile hotspot) at:

`https://tts-gateway.example-tailnet.ts.net`

That shape is a Tailscale Funnel URL (`https://<machine>.<tailnet>.ts.net`). Students should not need to install Tailscale. Going live needs school IT and teacher approval (see the public-access issue).

## 1. Authenticate every request

Every call must send a **per-student API key**. Without a key the gateway must refuse the request.

```bash
# Placeholders only — do not paste a real key or host into the repo or an issue
curl.exe -sS -X POST "https://tts-gateway.example-tailnet.ts.net/v1/audio/speech" \
  -H "Authorization: Bearer $TTS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"MODEL_ID\",\"voice\":\"VOICE_ID\",\"input\":\"Hei! Dette er en test.\"}" \
  --output speech.mp3
```

Ask a team admin for a key. Do not share keys. If a key leaks, it will be revoked (kill switch).

## 2. Pick a voice or model

The `model` and `voice` fields choose a backend on Node A or Node B (for example VoxCPM2, Qwen3-TTS, Phonon, Kokoro, or Piper Norwegian). Call `GET /v1/models` with your key to see the current list. Draft IDs (#250): `voxcpm2` (Norwegian + English; `voice` is `default` or a short voice description), `piper-b` / `piper-a` (Norwegian; voices `talesyntese`, `nvcc:0`–`nvcc:9`), and the Node A English engines once they are installed. Add `"stream": true` to start receiving audio before the whole sentence is done. Languages in the main lineup are **Norwegian and English**.

## 3. Limits

The gateway will enforce rate limits, quotas and a maximum request size. If you hit a limit, wait or ask an admin. Do not retry in a tight loop.

## 4. Privacy

The service is not meant to store your text or the audio it returns. Do not send personal data you would not say in class.

## 5. When it is down

If the URL does not answer, the public path may be switched off (maintenance or the kill switch). Use a team admin, not a public issue, to report problems that include keys or personal details.
