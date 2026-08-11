# EITA Reels Studio — Framework Editorial

Estúdio de edição e agendamento de reels para o perfil Instagram **@anaclaudia.eita**
(Anaclaudia Zani, neurocientista criadora do método EITA, 363 mil seguidores).

## Persona e voz

- Tom direto e provocador, coloquial ("vc", "tá").
- Bordões: **"Meus Anjos"** (vocativo), **"Conta pra titia"** (pergunta de engajamento).
- CTA padrão: **"Conversa com a EITA, minha mentora virtual. Link na bio."**
- **REGRAS INEGOCIÁVEIS**:
  - NUNCA usar travessão (—) em texto público. Reescrever a frase.
  - A credencial dela é sempre **"Neurocientista criadora do método EITA"**.

## Pilares de conteúdo (views típicas)

| Pilar | Formato | Views típicas |
|---|---|---|
| A | Educacional na poltrona, lettering branco caps | 10 a 16 mil |
| B | Split-screen com b-roll embaixo e frase grande | 8 a 12 mil |
| C | Esquetes "Véia da Porsche" com carros e humor | 41 a 155 mil (topo do perfil) |
| D | Cortes de podcast com título amarelo marker e palavra-ênfase branca | 5 a 26 mil |

Sempre que o bruto permitir, **hibridizar educação com humor**.

## Assinaturas de edição

- Hook verbal + título na tela nos 2 primeiros segundos.
- Lettering **Helvetica Neue Condensed Black** caps branco com sombra
  (títulos 104px, ênfases 116 a 138px em 1080x1920).
  - Fallback enquanto a fonte original não vier do Mac (proprietária): **Anton**
    é a substituta principal (grotesca condensada black, caps); alternativas
    **Archivo Black** (não condensada) e **Oswald** (pesos variáveis).
    Arquivos OFL em `assets/fonts/` do repo, instalados em
    `~/eita-reels-studio/assets/fonts/` e no fontconfig do sistema.
- Acento amarelo **#FFE234** estilo marca-texto nas ênfases.
- Legendas frase a frase em branco (não karaokê), terço inferior.
- Cortes secos, sem transições.
- Punch-ins de zoom **1.10 a 1.18x** centrados no rosto nas frases de ênfase.
- B-roll emocional em P&B.
- Watermark **@ANACLAUDIA.EITA** nos cortes de podcast.
- Duração alvo: **20 a 60s**.
- Trilha discreta (vol ~0.15) com SFX (whoosh, impact-bass, riser) sincronizados
  aos zooms e entradas.
- Loudness final: **-14 LUFS**.

## Fórmula da caption

1. Hook contraintuitivo em 1 linha
2. 3 parágrafos curtos
3. "Meus Anjos" (opcional)
4. CTA EITA link na bio
5. Pergunta + "Conta pra titia."

## Fluxo por vídeo

bruto (computador ou Google Drive) + briefing (pilar, mensagem central, duração,
data de publicação) → transcrição → decupagem/cortes → cor → lettering/motion →
legendas por último → trilha+SFX → preview 720p pra aprovação → caption →
agendamento no Metricool.

**Melhor horário de publicação: 10h da manhã** (pico em todos os dias desta conta).

## Contas e IDs

- Metricool: conta da agência (suporte@mentoravirtual.com.br), marca **anaclaudia.eita**,
  **blog_id 6707687**, timezone **America/Sao_Paulo**.
- Kairogen (app.kairogen.ai): plano Essential ou superior (o Free bloqueia TODOS os
  modelos de vídeo). No Essential o modelo liberado é `veo3-1-lite`
  (12 créditos por clipe de 6s, só 16:9 e 9:16, durações 4/6/8, saída 720p 24fps).

## Gotchas técnicos (economizam horas)

### ffmpeg
- **Mac**: usar `ffmpeg-full` do Homebrew (a fórmula `ffmpeg` normal vem SEM
  libass/zscale). É keg-only: todo render deve rodar com
  `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
- **Linux (Ubuntu)**: o ffmpeg do apt já inclui `subtitles` (libass) e `zscale`.

### HDR de iPhone
- Brutos de iPhone são **HLG 10-bit** (HDR): gerar um proxy SDR 1080x1920 uma vez com
  `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc`
  (o filtro não aceita `arib-std-b67`; bt2020-10 aproxima bem em cena indoor)
  e editar a partir do proxy.

### Overlays
- Gerar em 1080x1920 RGBA via PIL → PNG sequence → `-c:v qtrle` .mov.
- Legendas SEMPRE por último no filter chain.
- Overlays de split-screen = b-roll na metade inferior (960 a 1920) com topo transparente.

### Zoom animado (Ken Burns)
- O filtro `crop` não aceita `t` em w/h; usar
  `zoompan=z='1+K*in_time':d=1:s=1080x1920:fps=60`.
- Punch-ins estáticos: crop centrado com bias vertical 0.30 + scale de volta.

### video-use — patch conhecido
- Em `video-use/helpers/render.py`, `is_portrait_source` quebra com o ffprobe do
  ffmpeg-full, que emite CSV com vírgula final ("1080,1920,"); filtrar campos vazios
  antes do `map(int, ...)`, senão vídeos verticais são tratados como paisagem e os
  overlays desalinham. Patch em `patches/video-use-is-portrait-source.patch`.

### Metricool MCP
- `getScheduledPosts` usa `brandId/fromDate/toDate` (NÃO blogId/start/end).
- `createScheduledPost` usa `date` + `blogId` + `info` (string JSON com media,
  providers, publicationDate, text, instagramData:{type:"REEL"}).
- NÃO existe tool de delete: cancelar = update para draft:true + autoPublish:false;
  o update devolve um id NOVO.
- Mídia entra por URL pública (o Metricool copia para o CDN dele).
- O token OAuth expira em 1h; no Mac o refresh_token fica no Keychain
  "Claude Code-credentials".

### Mídia pública para agendar
- Bucket público no Supabase funciona bem; chaves novas `sb_secret_...` exigem
  header `apikey` além do `Authorization: Bearer`.

### BGM
- O catálogo do media-use exige login HeyGen (interativo); sem ele, gerar bed via
  ElevenLabs sound-generation (`/v1/sound-generation`, máx ~22s) funciona muito bem.
