# EITA Reels Studio (memória persistente do projeto)

Este repositório é o **EITA Reels Studio**: edição e agendamento de reels para o Instagram **@anaclaudia.eita** (Anaclaudia Zani, "Neurocientista criadora do método EITA", 363 mil seguidores).

**Antes de editar qualquer vídeo ou escrever qualquer caption, leia `FRAMEWORK.md`** (persona, regras inegociáveis, pilares, assinaturas de edição, fórmula de caption, fluxo por vídeo e todos os gotchas técnicos).

## Regras que valem em qualquer resposta pública

- Nunca usar travessão em texto público (caption, lettering, legenda): reescrever a frase.
- Credencial dela: sempre "Neurocientista criadora do método EITA".

## Working dirs

- Estúdio: este repo (symlink `~/eita-reels-studio` aponta para cá). Projetos em `projects/<nome>/`.
- Ferramentas: `video-use` e `hyperframes` clonados em `/workspace/browser-use/` e `/workspace/heygen-com/` (Linux/cloud) ou `~/video-editor/` (Mac). Skills registradas em `~/.claude/skills/`.
- Ambiente novo (container limpo): rode `bash scripts/setup.sh` e depois `bash scripts/validate.sh`.

## IDs e contas

- Metricool: conta da agência suporte@mentoravirtual.com.br, marca "anaclaudia.eita", **blog_id 6707687**, timezone America/Sao_Paulo. Melhor horário de publicação: 10h da manhã (pico em todos os dias).
- Kairogen: conta suporte@zavi.ag. Precisa plano Essential+ para vídeo; modelo `veo3-1-lite` no Essential.
- ElevenLabs: chave em `.env` na raiz do video-use (transcrição Scribe + SFX/trilha).

## Gotchas essenciais (detalhe completo em FRAMEWORK.md)

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar.
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle.
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- video-use precisa do patch `patches/video-use-is-portrait-source.patch` (senão vertical vira paisagem).
- Metricool MCP: sem delete (cancelar = update draft:true; update devolve id novo); mídia por URL pública (Supabase bucket público funciona).
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: ffmpeg do apt já serve.
- Cloud: conector Drive só baixa arquivos pequenos (3,4 MB ok; 7,7 MB derruba a sessão do MCP) e o proxy do container bloqueia drive.google.com. Para trazer um bruto: deixar o arquivo com link público no Drive e importar com Kairogen `download_audio_from_url` usando `https://drive.google.com/uc?export=download&id=<ID>` (o binário chega salvo em disco). Testado com vídeo de 7,4 MB.
- Cloud: a env var `ELEVENLABS_API_KEY` do ambiente contém um key ID (64 hex), não a chave da API. Scribe exige chave `sk_...` de 51 caracteres. Corrigir o valor na configuração do environment antes de transcrever.
