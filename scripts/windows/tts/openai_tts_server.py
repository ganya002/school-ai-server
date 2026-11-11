#!/usr/bin/env python3
"""
OpenAI-compatible text-to-speech server for one local engine (VoxCPM2 or Piper).

Exposes:
  POST /v1/audio/speech   {"model": "...", "input": "text", "voice": "...", "response_format": "wav", "speed": 1.0}
  GET  /v1/models         the one model this process serves
  GET  /health            {"status": "ok"} once the model is loaded

Binds to 127.0.0.1 by default. Do not publish an engine port directly; only the
gateway goes through the tunnel (docs/tts-plan.md). Request text and audio are
kept in memory only and never written to disk or logged.

Examples (PowerShell, Windows 11, inside each engine's venv):
  python openai_tts_server.py --engine voxcpm2 --model C:\\tts\\models\\VoxCPM2 --port 18101
  python openai_tts_server.py --engine piper   --model C:\\tts\\models\\piper   --port 18102
  python openai_tts_server.py --engine dummy   --port 18199      # sine tone, for testing clients

Voices:
  voxcpm2  "default" = the model's own voice; any other text is used as a VoxCPM2
           voice-design description, e.g. "a calm adult female voice".
  piper    the voice file stem without language/quality, e.g. "talesyntese" (default),
           or "nvcc:3" for speaker 3 of a multi-speaker voice.

Needs: fastapi, uvicorn. VoxCPM2 also needs voxcpm + soundfile; Piper needs piper-tts.
"""
import argparse, io, math, struct, threading, wave
from pathlib import Path

MAX_CHARS = 2000          # longest accepted input; keeps one request from hogging the GPU


def wav_bytes_int16(pcm: bytes, rate: int) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm)
    return buf.getvalue()


class Dummy:
    """Sine tone whose length follows the text. Lets you test clients without a model."""
    name = "dummy"
    def voices(self): return ["default"]
    def speak(self, text, voice, speed):
        rate, secs = 22050, max(.3, len(text) * .06 / speed)
        n = int(rate * secs)
        pcm = b"".join(struct.pack("<h", int(8000 * math.sin(2 * math.pi * 440 * i / rate))) for i in range(n))
        return wav_bytes_int16(pcm, rate)


class VoxCPM2:
    name = "voxcpm2"
    def __init__(self, model_dir, optimize):
        from voxcpm import VoxCPM  # imported here so the other engines don't need it
        import soundfile
        self.sf = soundfile
        self.m = VoxCPM.from_pretrained(model_dir, load_denoiser=False, optimize=optimize)
        self.rate = self.m.tts_model.sample_rate
    def voices(self): return ["default", "<free-text voice description>"]
    def speak(self, text, voice, speed):
        if voice and voice != "default":
            text = f"({voice}){text}"        # VoxCPM2 voice design syntax
        wav = self.m.generate(text=text, cfg_value=2.0, inference_timesteps=10)
        buf = io.BytesIO()
        self.sf.write(buf, wav, self.rate, format="WAV", subtype="PCM_16")
        return buf.getvalue()             # speed is not supported by VoxCPM2 and is ignored


class Piper:
    name = "piper"
    def __init__(self, model_dir):
        from piper import PiperVoice
        try:
            from piper import SynthesisConfig
        except ImportError:
            from piper.config import SynthesisConfig
        self.Cfg = SynthesisConfig
        self.v = {}
        for onnx in sorted(Path(model_dir).glob("*.onnx")):
            short = onnx.stem.split("-")[1] if onnx.stem.count("-") >= 2 else onnx.stem   # no_NO-talesyntese-medium -> talesyntese
            self.v[short] = PiperVoice.load(str(onnx))
        if not self.v:
            raise SystemExit(f"no .onnx voices found in {model_dir}")
        self.default = "talesyntese" if "talesyntese" in self.v else next(iter(self.v))
    def voices(self): return list(self.v)
    def speak(self, text, voice, speed):
        name, _, spk = (voice or self.default).partition(":")
        if name == "default":
            name = self.default
        if name not in self.v:
            raise ValueError(f"unknown voice '{name}', choose from {self.voices()}")
        cfg = self.Cfg(length_scale=1 / speed, speaker_id=int(spk) if spk else None)
        chunks = list(self.v[name].synthesize(text, syn_config=cfg))
        return wav_bytes_int16(b"".join(c.audio_int16_bytes for c in chunks), chunks[0].sample_rate)


def build_app(engine, model_id):
    from fastapi import FastAPI, HTTPException, Response
    from pydantic import BaseModel, Field

    class Speech(BaseModel):
        model: str = model_id
        input: str = Field(min_length=1, max_length=MAX_CHARS)
        voice: str = "default"
        response_format: str = "wav"
        speed: float = Field(1.0, ge=0.25, le=4.0)

    app = FastAPI(title=f"TTS ({engine.name})", docs_url=None, redoc_url=None)
    lock = threading.Lock()               # one synthesis at a time per engine; the GPU is shared

    @app.get("/health")
    def health(): return {"status": "ok", "engine": engine.name}

    @app.get("/v1/models")
    def models(): return {"object": "list", "data": [{"id": model_id, "object": "model", "owned_by": "local", "voices": engine.voices()}]}

    @app.post("/v1/audio/speech")
    def speech(req: Speech):
        if req.response_format != "wav":
            raise HTTPException(400, "only response_format 'wav' is supported")
        try:
            with lock:
                audio = engine.speak(req.input, req.voice, req.speed)
        except ValueError as e:
            raise HTTPException(400, str(e))
        return Response(audio, media_type="audio/wav")

    return app


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engine", required=True, choices=["voxcpm2", "piper", "dummy"])
    ap.add_argument("--model", help="model folder (VoxCPM2 weights, or a folder of Piper .onnx voices)")
    ap.add_argument("--model-id", help="id reported in /v1/models (default: engine name)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, required=True)
    ap.add_argument("--optimize", action="store_true", help="VoxCPM2: use torch.compile (needs triton-windows)")
    a = ap.parse_args()
    if a.host not in ("127.0.0.1", "localhost", "::1"):
        print(f"WARNING: binding to {a.host}. Engine ports should stay on localhost; publish only the gateway.")
    if a.engine != "dummy" and not a.model:
        ap.error("--model is required for this engine")
    engine = {"voxcpm2": lambda: VoxCPM2(a.model, a.optimize), "piper": lambda: Piper(a.model), "dummy": Dummy}[a.engine]()
    import uvicorn
    uvicorn.run(build_app(engine, a.model_id or a.engine), host=a.host, port=a.port, access_log=False)


if __name__ == "__main__":
    main()
