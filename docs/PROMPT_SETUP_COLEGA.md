# Prompt: montar o EITA Reels Studio nesta máquina

> Cole tudo abaixo desta linha numa sessão nova do Claude Code no computador da colega (Mac). Se possível, copie junto a pasta `~/eita-reels-studio` do computador original (dá histórico e exemplos), mas o prompt funciona sem ela.

---

Você vai montar nesta máquina o **EITA Reels Studio**: um estúdio de edição e agendamento de reels para o perfil Instagram **@anaclaudia.eita** (Anaclaudia Zani, neurocientista criadora do método EITA, 363 mil seguidores). Este setup já roda em outro computador; siga as etapas na ordem, valide cada uma antes de seguir, e ao final grave uma memória persistente do projeto. Quando terminar, me entregue um checklist do que passou e do que ficou pendente.

## 1. Contexto editorial (grave isso em `~/eita-reels-studio/FRAMEWORK.md`)

**Persona e voz**: tom direto e provocador, coloquial ("vc", "tá"). Bordões: "Meus Anjos" (vocativo), "Conta pra titia" (pergunta de engajamento). CTA padrão: "Conversa com a EITA, minha mentora virtual. Link na bio." REGRAS INEGOCIÁVEIS: nunca usar travessão (—) em texto público (reescrever a frase); credencial dela é sempre "Neurocientista criadora do método EITA".

**Pilares de conteúdo** (views típicas): A) educacional na poltrona, lettering branco caps (10 a 16 mil); B) split-screen com b-roll embaixo e frase grande (8 a 12 mil); C) esquetes "Véia da Porsche" com carros e humor (41 a 155 mil, o topo do perfil); D) cortes de podcast com título amarelo marker e palavra-ênfase branca (5 a 26 mil). Sempre que o bruto permitir, hibridizar educação com humor.

**Assinaturas de edição**: hook verbal + título na tela nos 2 primeiros segundos; lettering Helvetica Neue Condensed Black caps branco com sombra (títulos 104px, ênfases 116 a 138px em 1080x1920); acento amarelo #FFE234 estilo marca-texto nas ênfases; legendas frase a frase em branco (não karaokê), terço inferior; cortes secos sem transições; punch-ins de zoom 1.10 a 1.18x centrados no rosto nas frases de ênfase; b-roll emocional P&B; watermark @ANACLAUDIA.EITA nos cortes de podcast; duração alvo 20 a 60s; trilha discreta (vol ~0.15) com SFX (whoosh, impact-bass, riser) sincronizados aos zooms e entradas; loudness final -14 LUFS.

**Fórmula da caption**: hook contraintuitivo em 1 linha → 3 parágrafos curtos → "Meus Anjos" opcional → CTA EITA link na bio → pergunta + "Conta pra titia."

**Fluxo por vídeo**: bruto (computador ou Google Drive) + briefing (pilar, mensagem central, duração, data de publicação) → transcrição → decupagem/cortes → cor → lettering/motion → legendas por último → trilha+SFX → preview 720p pra aprovação → caption → agendamento no Metricool (melhor horário: 10h da manhã é o pico em todos os dias desta conta).

## 2. Ferramentas locais

1. `brew install ffmpeg-full` (a fórmula `ffmpeg` normal do Homebrew vem SEM libass/zscale). Ela é keg-only: todo render deve rodar com `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
2. Clone em `~/video-editor`: `https://github.com/browser-use/video-use` e `https://github.com/heygen-com/hyperframes`. No video-use, siga o `install.md` (uv sync, symlink da skill para `~/.claude/skills/video-use`). Instale as skills do hyperframes e a media-use conforme os READMEs.
3. Peça ao usuário a `ELEVENLABS_API_KEY` e grave em `.env` na raiz do video-use (transcrição Scribe + geração de SFX/trilha via endpoint `/v1/sound-generation`).
4. **Patch conhecido**: em `video-use/helpers/render.py`, a função `is_portrait_source` quebra com o ffprobe do ffmpeg-full, que emite CSV com vírgula final ("1080,1920,"); filtre campos vazios antes do `map(int, ...)`, senão vídeos verticais são tratados como paisagem e os overlays desalinham.
5. Crie `~/eita-reels-studio/` com `FRAMEWORK.md` (conteúdo da seção 1 + gotchas da seção 4), `projects/` e `assets/fonts/`.

## 3. Conectores (cada um exige ação do usuário; peça na hora certa)

- **Metricool** (agendamento): adicione em `~/.claude.json` → `"mcpServers": {"metricool": {"type": "http", "url": "https://ai.metricool.com/mcp"}}`. Na primeira sessão nova o usuário autoriza via OAuth (browser). Se for a mesma conta da agência (suporte@mentoravirtual.com.br): marca "anaclaudia.eita", **blog_id 6707687**, timezone America/Sao_Paulo.
- **Google Drive** (brutos): conectar o conector oficial de Drive do Claude nas configurações de conectores.
- **Kairogen** (b-roll por IA, app.kairogen.ai): conta com plano Essential ou superior (o Free bloqueia TODOS os modelos de vídeo). Conector MCP oficial deles. No Essential o modelo liberado é `veo3-1-lite` (12 créditos por clipe de 6s, só 16:9 e 9:16, durações 4/6/8, saída 720p 24fps).

## 4. Gotchas técnicos (economizam horas)

- **Brutos de iPhone são HLG 10-bit** (HDR): gere um proxy SDR 1080x1920 uma vez com `colorspace=all=bt709:itrc=bt2020-10:iprimaries=bt2020:ispace=bt2020nc` (o filtro não aceita `arib-std-b67`; bt2020-10 aproxima bem em cena indoor) e edite a partir do proxy.
- **Overlays**: gerar em 1080x1920 RGBA via PIL → PNG sequence → `-c:v qtrle` .mov; legendas SEMPRE por último no filter chain; overlays de split-screen = b-roll na metade inferior (960 a 1920) com topo transparente.
- **Zoom animado (Ken Burns)**: o filtro `crop` não aceita `t` em w/h; use `zoompan=z='1+K*in_time':d=1:s=1080x1920:fps=60`. Punch-ins estáticos: crop centrado com bias vertical 0.30 + scale de volta.
- **Metricool MCP**: `getScheduledPosts` usa `brandId/fromDate/toDate` (não blogId/start/end); `createScheduledPost` usa `date` + `blogId` + `info` (string JSON com media, providers, publicationDate, text, instagramData:{type:"REEL"}); não existe tool de delete (cancelar = update para draft:true + autoPublish:false; o update devolve um id NOVO); mídia entra por URL pública (o Metricool copia para o CDN dele); o token OAuth expira em 1h e o refresh_token fica no Keychain "Claude Code-credentials".
- **Mídia pública para agendar**: bucket público no Supabase funciona bem; chaves novas `sb_secret_...` exigem header `apikey` além do `Authorization: Bearer`.
- **BGM**: catálogo do media-use exige login HeyGen (interativo); sem ele, gerar bed via ElevenLabs sound-generation (máx ~22s) funciona muito bem.

## 5. Validação final (rode e me reporte)

1. `ffmpeg -filters | grep -cE "subtitles|zscale"` com o PATH do ffmpeg-full → deve dar 2.
2. Transcreva 10s de qualquer vídeo com o helper do video-use → JSON com timestamps por palavra.
3. Metricool: chame `getBrandSettings` → deve listar a marca com Instagram conectado.
4. Kairogen: `get_me_context` → plano e créditos.
5. Grave a memória persistente do projeto (working dir, framework, ids, gotchas) e me diga o que ficou pendente de ação humana.
