# EITA Reels Studio — memória do projeto

Estúdio de edição e agendamento de reels do Instagram **@anaclaudia.eita**
(Anaclaudia Zani). Leia **FRAMEWORK.md** antes de editar qualquer vídeo: persona,
pilares, assinaturas de edição, fórmula de caption, fluxo de trabalho e gotchas
técnicos estão lá — inclusive as regras inegociáveis (nunca usar travessão em
texto público; credencial sempre "Neurocientista criadora do método EITA").

## Layout da máquina (recriar se o container for novo)

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
  America/Sao_Paulo. MCP http em `https://ai.metricool.com/mcp` (configurado em
  `~/.claude.json`; exige OAuth do usuário na primeira sessão).
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

- `ELEVENLABS_API_KEY` real no `.env` do video-use. Neste ambiente remoto,
  `api.elevenlabs.io` está bloqueada pela política de rede — transcrição e SFX
  só funcionam após liberar o domínio ou rodando em máquina local.
- OAuth do Metricool (browser, primeira sessão com o MCP ativo).
- Fonte Helvetica Neue Condensed Black em `~/eita-reels-studio/assets/fonts/`
  (proprietária; copiar do Mac original ou da máquina da colega).
