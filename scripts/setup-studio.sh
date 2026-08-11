#!/usr/bin/env bash
# Recria o EITA Reels Studio num container novo do Claude Code Remote (Ubuntu).
# Uso: bash scripts/setup-studio.sh   (a partir da raiz deste repositório)
# Idempotente: pode rodar de novo sem estragar nada.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "==> Repo: $REPO_DIR"

echo "==> ffmpeg"
command -v ffmpeg >/dev/null || { apt-get update -qq && apt-get install -y -qq ffmpeg; }
# grep sem -q: com pipefail, -q encerra cedo e o SIGPIPE no ffmpeg falharia o pipeline
ffmpeg -hide_banner -filters 2>/dev/null | grep -E " subtitles " >/dev/null || echo "AVISO: filtro subtitles ausente"
ffmpeg -hide_banner -filters 2>/dev/null | grep -E " zscale "    >/dev/null || echo "AVISO: filtro zscale ausente"

echo "==> Clones"
mkdir -p ~/video-editor
[ -d ~/video-editor/video-use ]   || git clone --depth 1 https://github.com/browser-use/video-use ~/video-editor/video-use
[ -d ~/video-editor/hyperframes ] || git clone --depth 1 https://github.com/heygen-com/hyperframes ~/video-editor/hyperframes

echo "==> Deps do video-use (uv sync)"
(cd ~/video-editor/video-use && uv sync >/dev/null)

echo "==> Patch is_portrait_source"
if git -C ~/video-editor/video-use apply --check "$REPO_DIR/patches/video-use-is-portrait-source.patch" 2>/dev/null; then
  git -C ~/video-editor/video-use apply "$REPO_DIR/patches/video-use-is-portrait-source.patch"
  echo "    aplicado"
else
  echo "    já aplicado (ou upstream mudou — conferir helpers/render.py)"
fi

echo "==> Skills"
mkdir -p ~/.claude/skills
ln -sfn ~/video-editor/video-use ~/.claude/skills/video-use
for s in hyperframes hyperframes-core hyperframes-animation hyperframes-cli \
         hyperframes-creative hyperframes-keyframes hyperframes-registry media-use; do
  ln -sfn ~/video-editor/hyperframes/skills/$s ~/.claude/skills/$s
done

echo "==> Estúdio"
mkdir -p ~/eita-reels-studio/projects ~/eita-reels-studio/assets/fonts
ln -sfn "$REPO_DIR/FRAMEWORK.md" ~/eita-reels-studio/FRAMEWORK.md

echo "==> Fontes"
mkdir -p /usr/local/share/fonts/eita
cp "$REPO_DIR"/assets/fonts/*.ttf ~/eita-reels-studio/assets/fonts/ 2>/dev/null || true
cp "$REPO_DIR"/assets/fonts/*.ttf /usr/local/share/fonts/eita/ 2>/dev/null || true
fc-cache -f >/dev/null 2>&1 || true

echo "==> ELEVENLABS_API_KEY"
if [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  printf 'ELEVENLABS_API_KEY=%s\n' "$ELEVENLABS_API_KEY" > ~/video-editor/video-use/.env
  chmod 600 ~/video-editor/video-use/.env
  echo "    gravada no .env a partir da variável de ambiente"
elif grep -q '^ELEVENLABS_API_KEY=..' ~/video-editor/video-use/.env 2>/dev/null; then
  echo "    já presente no .env"
else
  echo "    PENDENTE: exportar ELEVENLABS_API_KEY (env var do ambiente) ou colar no .env"
fi

echo "==> Teste de rede: api.elevenlabs.io"
code=$(curl -sS -o /dev/null -w "%{http_code}" --max-time 10 https://api.elevenlabs.io/v1/models 2>/dev/null || true)
if [ "$code" = "000" ] || [ -z "$code" ]; then
  echo "    BLOQUEADA pela network policy deste ambiente (transcrição/SFX indisponíveis)"
else
  echo "    acessível (HTTP $code)"
fi

echo "==> Metricool"
echo "    conector da conta claude.ai (ai.metricool.com/mcp) — validar com getBrandSettings na sessão"

echo
echo "Setup concluído. Ler FRAMEWORK.md antes de editar qualquer vídeo."
