# EITA Reels Studio

Estúdio de edição e agendamento de reels para **@anaclaudia.eita** (Instagram, 363 mil seguidores).

- **`FRAMEWORK.md`**: contexto editorial completo (persona, pilares, assinaturas de edição, fluxo) + gotchas técnicos. Leia antes de editar qualquer vídeo.
- **`SETUP.md`**: como montar o estúdio numa máquina nova (Mac ou Linux/cloud).
- **`projects/`**: um subdiretório por vídeo (bruto, briefing, transcrição, renders, caption).
- **`assets/fonts/`**: fontes do lettering (Helvetica Neue Condensed Black; copiar de um Mac).
- **`patches/`**: patches conhecidos para as ferramentas (video-use).
- **`scripts/`**: setup automatizado e validação.

## Uso rápido

Numa sessão nova, na raiz deste repositório:

```bash
bash scripts/setup.sh      # instala ffmpeg, video-use, hyperframes, aplica patches
bash scripts/validate.sh   # roda as validações
```

Depois: coloque o bruto e o briefing em `projects/<nome-do-video>/` e peça a edição. O fluxo completo por vídeo está em `FRAMEWORK.md`.

## Conectores necessários (ação humana)

| Conector | Para quê | Como |
|---|---|---|
| Metricool | Agendamento | MCP http `https://ai.metricool.com/mcp` + OAuth no browser. Marca "anaclaudia.eita", blog_id 6707687, timezone America/Sao_Paulo |
| Google Drive | Brutos | Conector oficial de Drive do Claude nas configurações |
| Kairogen | B-roll por IA | Conector MCP oficial + plano Essential ou superior (Free bloqueia vídeo) |
| ElevenLabs | Transcrição Scribe + SFX/trilha | `ELEVENLABS_API_KEY` em `.env` na raiz do video-use |
