# Setup do EITA Reels Studio numa máquina nova

Siga na ordem. Valide cada etapa antes de seguir. Em Linux/cloud, `bash scripts/setup.sh` faz as etapas 1 a 4 automaticamente.

## 1. ffmpeg

- **Mac**: `brew install ffmpeg-full`. A fórmula `ffmpeg` normal do Homebrew vem SEM libass/zscale. `ffmpeg-full` é keg-only: todo render deve rodar com `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
- **Linux (Ubuntu/Debian)**: `apt-get install -y ffmpeg`. O pacote padrão já tem libass e zscale.

Validar: `ffmpeg -filters | grep -cE "subtitles|zscale"` deve dar 2 ou mais.

## 2. Ferramentas de edição

```bash
# Mac: clonar em ~/video-editor. Linux/cloud: /workspace funciona igual.
git clone https://github.com/browser-use/video-use <destino>/video-use
git clone https://github.com/heygen-com/hyperframes <destino>/hyperframes
```

- **video-use**: siga o `install.md` do repo (`uv sync`, symlink do repo inteiro para `~/.claude/skills/video-use`).
- **Patch obrigatório**: aplique `patches/video-use-is-portrait-source.patch` no video-use (ffprobe de alguns builds emite CSV com vírgula final e vídeos verticais viram paisagem sem o patch).
- **hyperframes + media-use**: `npx --yes hyperframes skills update` instala o core set de skills (requer Node 22+).

## 3. ElevenLabs

Peça ao usuário a `ELEVENLABS_API_KEY` e grave em `.env` na raiz do video-use:

```bash
printf 'ELEVENLABS_API_KEY=%s\n' "$KEY" > <destino>/video-use/.env
chmod 600 <destino>/video-use/.env
```

Usada para transcrição Scribe e geração de SFX/trilha via endpoint `/v1/sound-generation`. Nunca commitar o `.env`.

## 4. Diretório do estúdio

Este repositório É o estúdio. Numa máquina nova:

```bash
git clone <este-repo> ~/eita-reels-studio   # ou clone onde preferir e symlinke
```

Estrutura: `FRAMEWORK.md`, `projects/`, `assets/fonts/`.

## 5. Conectores (cada um exige ação do usuário; peça na hora certa)

- **Metricool** (agendamento): adicionar em `~/.claude.json`:

  ```json
  {"mcpServers": {"metricool": {"type": "http", "url": "https://ai.metricool.com/mcp"}}}
  ```

  Na primeira sessão nova o usuário autoriza via OAuth (browser). Conta da agência (suporte@mentoravirtual.com.br): marca "anaclaudia.eita", **blog_id 6707687**, timezone America/Sao_Paulo.

- **Google Drive** (brutos): conectar o conector oficial de Drive do Claude nas configurações de conectores.

- **Kairogen** (b-roll por IA, app.kairogen.ai): conector MCP oficial + conta com plano **Essential ou superior** (o Free bloqueia TODOS os modelos de vídeo). No Essential o modelo liberado é `veo3-1-lite` (12 créditos por clipe de 6s, só 16:9 e 9:16, durações 4/6/8, saída 720p 24fps).

## 6. Validação final

```bash
bash scripts/validate.sh
```

1. `ffmpeg -filters | grep -cE "subtitles|zscale"` deve dar >= 2.
2. Transcrever 10s de qualquer vídeo com o helper do video-use: JSON com timestamps por palavra (requer ELEVENLABS_API_KEY; gasta créditos Scribe, rodar só uma vez).
3. Metricool: `getBrandSettings` deve listar a marca com Instagram conectado.
4. Kairogen: `get_me_context` deve mostrar plano Essential+ e créditos.
5. Gravar a memória persistente do projeto (neste repo: `CLAUDE.md`).
