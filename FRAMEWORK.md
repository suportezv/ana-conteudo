# EITA Reels Studio: FRAMEWORK

Estúdio de edição e agendamento de reels para o perfil Instagram **@anaclaudia.eita** (Anaclaudia Zani, neurocientista criadora do método EITA, 363 mil seguidores).

## Persona e voz

- Tom direto e provocador, coloquial ("vc", "tá").
- Bordões: **"Meus Anjos"** (vocativo), **"Conta pra titia"** (pergunta de engajamento).
- CTA padrão: **"Conversa com a EITA, minha mentora virtual. Link na bio."**

### REGRAS INEGOCIÁVEIS

1. **Nunca usar travessão em texto público.** Se a frase pedir travessão, reescrever a frase.
2. A credencial dela é sempre: **"Neurocientista criadora do método EITA"**.

## Pilares de conteúdo (views típicas)

| Pilar | Formato | Views típicas |
|---|---|---|
| A | Educacional na poltrona, lettering branco caps | 10 a 16 mil |
| B | Split-screen com b-roll embaixo e frase grande | 8 a 12 mil |
| C | Esquetes "Véia da Porsche" com carros e humor | 41 a 155 mil (topo do perfil) |
| D | Cortes de podcast com título amarelo marker e palavra-ênfase branca | 5 a 26 mil |

Sempre que o bruto permitir, **hibridizar educação com humor**.

## Assinaturas de edição

- Hook verbal + título na tela nos **2 primeiros segundos**.
- Lettering **Helvetica Neue Condensed Black** caps branco com sombra (títulos 104px, ênfases 116 a 138px em 1080x1920).
- Acento **amarelo #FFE234** estilo marca-texto nas ênfases.
- Legendas frase a frase em branco (não karaokê), terço inferior.
- Cortes secos, sem transições.
- Punch-ins de zoom **1.10 a 1.18x** centrados no rosto nas frases de ênfase.
- B-roll emocional em P&B.
- Watermark **@ANACLAUDIA.EITA** nos cortes de podcast.
- Duração alvo: **20 a 60s**.
- Trilha discreta (vol ~0.15) com SFX (whoosh, impact-bass, riser) sincronizados aos zooms e entradas.
- Loudness final: **-14 LUFS**.

## Fórmula da caption

1. Hook contraintuitivo em 1 linha
2. 3 parágrafos curtos
3. "Meus Anjos" opcional
4. CTA EITA link na bio
5. Pergunta + "Conta pra titia."

## Fluxo por vídeo

1. Bruto (computador ou Google Drive) + briefing (pilar, mensagem central, duração, data de publicação)
2. Transcrição
3. Decupagem/cortes
4. Cor
5. Lettering/motion
6. **Legendas por último**
7. Trilha + SFX
8. Preview 720p pra aprovação
9. Caption
10. Agendamento no Metricool (melhor horário: **10h da manhã** é o pico em todos os dias desta conta)

## Gotchas técnicos (economizam horas)

### Brutos de iPhone são HLG 10-bit (HDR)

Gere um proxy SDR 1080x1920 **uma vez** com:

```
colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc
```

O filtro não aceita `arib-std-b67`; `bt2020-10` aproxima bem em cena indoor. Edite a partir do proxy.

### Overlays

- Gerar em 1080x1920 RGBA via PIL, PNG sequence, depois `-c:v qtrle` .mov.
- Legendas SEMPRE por último no filter chain.
- Overlays de split-screen: b-roll na metade inferior (960 a 1920) com topo transparente.

### Zoom animado (Ken Burns)

O filtro `crop` não aceita `t` em w/h. Use:

```
zoompan=z='1+K*in_time':d=1:s=1080x1920:fps=60
```

Punch-ins estáticos: crop centrado com bias vertical 0.30 + scale de volta.

### Metricool MCP

- `getScheduledPosts` usa `brandId/fromDate/toDate` (não blogId/start/end).
- `createScheduledPost` usa `date` + `blogId` + `info` (string JSON com media, providers, publicationDate, text, `instagramData:{type:"REEL"}`).
- **Não existe tool de delete.** Cancelar = update para `draft:true` + `autoPublish:false`; o update devolve um id NOVO.
- Mídia entra por URL pública (o Metricool copia para o CDN dele).
- O token OAuth expira em 1h; no Mac o refresh_token fica no Keychain "Claude Code-credentials".
- Conta da agência (suporte@mentoravirtual.com.br): marca "anaclaudia.eita", **blog_id 6707687**, timezone America/Sao_Paulo.

### Mídia pública para agendar

Bucket público no Supabase funciona bem. Chaves novas `sb_secret_...` exigem header `apikey` além do `Authorization: Bearer`.

### BGM

O catálogo do media-use exige login HeyGen (interativo). Sem ele, gerar bed via ElevenLabs sound-generation (endpoint `/v1/sound-generation`, máx ~22s) funciona muito bem.

### Kairogen (b-roll por IA)

- app.kairogen.ai; o plano Free bloqueia TODOS os modelos de vídeo. É preciso Essential ou superior.
- No Essential o modelo liberado é `veo3-1-lite`: 12 créditos por clipe de 6s, só 16:9 e 9:16, durações 4/6/8, saída 720p 24fps.

### ffmpeg

- **Mac**: `brew install ffmpeg-full` (a fórmula `ffmpeg` normal vem SEM libass/zscale). Keg-only: todo render deve rodar com `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
- **Linux (apt)**: o pacote `ffmpeg` padrão do Ubuntu/Debian já inclui `subtitles` (libass), `zscale`, `zoompan` e `colorspace`. Nenhum PATH especial necessário.

### video-use: patch conhecido

Em `video-use/helpers/render.py`, a função `is_portrait_source` quebra com ffprobe que emite CSV com vírgula final ("1080,1920,"): filtrar campos vazios antes do `map(int, ...)`, senão vídeos verticais são tratados como paisagem e os overlays desalinham. Patch pronto em `patches/video-use-is-portrait-source.patch`.

### Fonte

Helvetica Neue Condensed Black é fonte proprietária da Apple (vem no macOS em `/System/Library/Fonts/HelveticaNeue.ttc`). Em Linux não está disponível: copiar o arquivo para `assets/fonts/` a partir de um Mac, ou usar fallback visualmente próximo (Archivo Black ou Liberation Sans Bold condensada via `fontconfig`).
