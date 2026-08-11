# EITA Reels Studio — memória do projeto

Estúdio de edição e agendamento de reels do Instagram **@anaclaudia.eita**
(Anaclaudia Zani). Leia **FRAMEWORK.md** antes de editar qualquer vídeo: persona,
pilares, assinaturas de edição, fórmula de caption, fluxo de trabalho e gotchas
técnicos estão lá — inclusive as regras inegociáveis (nunca usar travessão em
texto público; credencial sempre "Neurocientista criadora do método EITA").

## Layout da máquina (recriar se o container for novo)

Num container novo, rodar `bash scripts/setup-studio.sh` (idempotente): instala
ffmpeg, clona e prepara video-use/hyperframes, aplica o patch, registra skills,
instala fontes e grava o `.env` a partir da env var `ELEVENLABS_API_KEY` (se o
ambiente do claude.ai/code tiver essa variável configurada).

- `~/eita-reels-studio/` — working dir do estúdio: `FRAMEWORK.md` (symlink para o
  deste repo), `projects/` (um subdiretório por vídeo), `assets/fonts/`.
- `~/video-editor/video-use` — editor conversacional (clone de
  github.com/browser-use/video-use, deps via `uv sync`). Skill registrada em
  `~/.claude/skills/video-use`. **Patch obrigatório** já aplicado:
  `patches/video-use-is-portrait-source.patch` (deste repo) sobre
  `helpers/render.py`.
- `~/video-editor/hyperframes` — clone de github.com/heygen-com/hyperframes;
  skills core + `media-use` symlinkadas em `~/.claude/skills/`.
- ffmpeg: no Linux/Ubuntu o do apt serve (tem `subtitles` e `zscale`). No Mac,
  usar `ffmpeg-full` do Homebrew com `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
- `~/video-editor/video-use/.env` — precisa de `ELEVENLABS_API_KEY` real
  (transcrição Scribe + SFX/trilha via `/v1/sound-generation`). Nunca commitar.

## Contas e IDs

- Conta da agência: suporte@mentoravirtual.com.br
- Metricool: marca **anaclaudia.eita**, **blog_id 6707687**, timezone
  America/Sao_Paulo. Conectado como conector custom da conta claude.ai
  (URL `https://ai.metricool.com/mcp`), autorizado com
  suporte@mentoravirtual.com.br — validado em 11/08/2026 via `getBrandSettings`
  (Instagram anaclaudia.eita conectado). Cuidado: se o OAuth for refeito logado
  em outra conta Metricool (ex.: suporte@zavi.ag), as marcas erradas aparecem.
- Kairogen: plano Essential; modelo de vídeo liberado `veo3-1-lite` (12 créditos
  por clipe de 6s, 16:9/9:16, durações 4/6/8, 720p 24fps).
- Google Drive: conector oficial do Claude, mesma conta; brutos ficam lá.
- Melhor horário de publicação: **10h da manhã** (todos os dias).

## Regras operacionais

- Fluxo por vídeo: bruto + briefing → transcrição → decupagem → cor →
  lettering/motion → legendas POR ÚLTIMO → trilha+SFX → preview 720p pra
  aprovação → caption → agendamento no Metricool.
- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez e editar do proxy
  (comando exato no FRAMEWORK.md).
- Gotchas do Metricool MCP (nomes de parâmetros, sem delete, id novo no update,
  mídia por URL pública) estão no FRAMEWORK.md — ler antes de agendar.

## Pendências conhecidas (exigem ação humana ou rede)

- `ELEVENLABS_API_KEY` já gravada em `~/video-editor/video-use/.env`, mas
  `api.elevenlabs.io` está bloqueada pela política de rede deste ambiente —
  transcrição e SFX só funcionam após liberar o domínio na network policy do
  ambiente (claude.ai/code) ou rodando em máquina local.
- Fonte Helvetica Neue Condensed Black (proprietária; copiar do Mac original).
  Enquanto isso, fallback OFL instalado: **Anton** (principal), Archivo Black e
  Oswald — em `assets/fonts/` do repo e no fontconfig.
