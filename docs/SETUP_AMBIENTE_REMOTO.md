# Setup no ambiente remoto (Claude Code na nuvem) — o que muda vs. Mac

Este repositório foi montado a partir do `docs/PROMPT_SETUP_COLEGA.md` num container
Linux (Ubuntu 24.04) do Claude Code Remote. Diferenças em relação ao setup de Mac:

## Adaptações feitas

| Item do prompt (Mac) | Neste ambiente (Linux) |
|---|---|
| `brew install ffmpeg-full` + PATH keg-only | `apt-get install ffmpeg` (6.1.1) — já inclui `subtitles` (libass) e `zscale`; nenhum PATH especial necessário |
| Clones em `~/video-editor` | Igual: `/root/video-editor/{video-use,hyperframes}` |
| Skill via symlink em `~/.claude/skills` | Igual — video-use + skills core do hyperframes + media-use |
| Patch `is_portrait_source` | Aplicado e testado (vídeo 1080x1920 → `portrait: True`); diff versionado em `patches/` |
| `~/eita-reels-studio/` | Criado; `FRAMEWORK.md` é symlink para o deste repo (fonte única) |
| Keychain "Claude Code-credentials" (token Metricool) | Não existe no Linux; o token fica onde o Claude Code guardar credenciais MCP no container |

## Limitações deste ambiente

- **Container efêmero**: tudo fora do repositório git se perde quando o container é
  reciclado. Por isso FRAMEWORK.md, CLAUDE.md, patch e docs estão versionados aqui.
  Ao abrir sessão nova, recriar o layout com os passos do CLAUDE.md.
- **Política de rede**: `api.elevenlabs.io` está BLOQUEADA pelo proxy deste ambiente
  (CONNECT 403). Transcrição Scribe e sound-generation não funcionam daqui até o
  domínio ser liberado na network policy do ambiente, ou rodando em máquina local.
- **Metricool**: o MCP http foi adicionado em `~/.claude.json`, mas o servidor só é
  carregado em sessão nova e o OAuth exige browser do usuário. Em sessões do
  claude.ai/code, alternativamente conectar via conectores da conta.
- **Fonte Helvetica Neue Condensed Black**: proprietária, não disponível no Linux.
  Copiar o arquivo da fonte do Mac original para `~/eita-reels-studio/assets/fonts/`
  (e idealmente para `assets/fonts/` deste repo, se o licenciamento permitir).

## Recriando o ambiente num container novo

```bash
apt-get update && apt-get install -y ffmpeg
mkdir -p ~/video-editor ~/eita-reels-studio/projects ~/eita-reels-studio/assets/fonts
git clone --depth 1 https://github.com/browser-use/video-use ~/video-editor/video-use
git clone --depth 1 https://github.com/heygen-com/hyperframes ~/video-editor/hyperframes
cd ~/video-editor/video-use && uv sync
git apply /caminho/deste/repo/patches/video-use-is-portrait-source.patch
mkdir -p ~/.claude/skills
ln -sfn ~/video-editor/video-use ~/.claude/skills/video-use
for s in hyperframes hyperframes-core hyperframes-animation hyperframes-cli \
         hyperframes-creative hyperframes-keyframes hyperframes-registry media-use; do
  ln -sfn ~/video-editor/hyperframes/skills/$s ~/.claude/skills/$s
done
ln -sfn /caminho/deste/repo/FRAMEWORK.md ~/eita-reels-studio/FRAMEWORK.md
printf 'ELEVENLABS_API_KEY=%s\n' "$CHAVE" > ~/video-editor/video-use/.env && chmod 600 ~/video-editor/video-use/.env
```
