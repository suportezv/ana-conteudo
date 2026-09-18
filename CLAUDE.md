# EITA Reels Studio (memória persistente do projeto)

Este repositório é o **EITA Reels Studio**: edição e agendamento de reels para o Instagram **@anaclaudia.eita** (Anaclaudia Zani, "Neurocientista criadora do método EITA", 363 mil seguidores).

**Antes de editar qualquer vídeo ou escrever qualquer caption, leia `FRAMEWORK.md`** (persona, regras inegociáveis, pilares, assinaturas de edição, fórmula de caption, fluxo por vídeo e todos os gotchas técnicos).

## Regras que valem em qualquer resposta pública

- Nunca usar travessão em texto público (caption, lettering, legenda): reescrever a frase.
- Credencial dela: sempre "Neurocientista criadora do método EITA".

## Working dirs

- Estúdio: este repo (symlink `~/eita-reels-studio` aponta para cá). Projetos em `projects/<nome>/`.
- Ferramentas: `video-use` e `hyperframes` clonados em `/workspace/browser-use/` e `/workspace/heygen-com/` (Linux/cloud) ou `~/video-editor/` (Mac). Skills registradas em `~/.claude/skills/`.
- Composições Remotion em `remotion/` (React). Tokens da marca só em `remotion/src/marca.ts`.
- Ambiente novo (container limpo): rode `bash scripts/setup.sh` e depois `bash scripts/validate.sh`.
- **Em sessão nova, conferir `ls /workspace` antes de contar com video-use ou hyperframes.** O passo de setup do environment nem sempre roda; rodar o script à mão resolve.

## Scripts do estúdio (`scripts/`)

| Script | O que faz |
|---|---|
| `decupar.py` | Decupa vídeo por **âncoras de texto** ("de tal frase até tal frase") casadas contra transcrição com timestamp por palavra. Junta trechos, gira, aplica LUT, normaliza áudio |
| `relatorio_decupagem.py` | Retranscreve as peças finais e monta o relatório do que ficou e do que caiu |
| `gera_lut_slog2.py` | Gera LUT 3D de S-Log2/S-Gamut para Rec.709 a partir das transferências da `colour-science` |
| `zip_index_remoto.py` | Lista e extrai arquivos de um ZIP gigante no Drive por *range request*, sem baixar o ZIP |
| `gera_imagem.py` | Gera imagem pela OpenAI ou pelo Gemini, mesma interface, chaves só do ambiente |
| `sobe_para_drive.py` | Sobe arquivos para uma pasta do Drive com token de acesso |

Nenhum deles aceita chave por argumento: linha de comando vaza em histórico de shell e em lista de processos. Todos leem só de variável de ambiente.

## Chaves de API (variáveis do environment, nunca no repo)

| Variável | Para quê | Como conferir o escopo |
|---|---|---|
| `ELEVENLABS_API_KEY` | TTS, STT (Scribe) e `sound-generation` | chamar o endpoint com parâmetro inválido: `401 missing_permissions` = escopo ausente; `400`/`404` = escopo presente |
| `OPENAI_API_KEY` | geração de imagem | `curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"` |
| `GEMINI_API_KEY` | geração de imagem | `curl https://generativelanguage.googleapis.com/v1beta/models -H "x-goog-api-key: $GEMINI_API_KEY"` |

Três armadilhas já pagas com tempo:

1. **Variável entra na criação do container.** Cadastrar no environment com sessão já aberta não faz a sessão enxergar: é preciso sessão nova. Conferir com `printenv | grep -c API_KEY` antes de acusar o script.
2. **Chave válida não significa quota.** No Gemini, listar modelos funciona no tier gratuito, mas gerar imagem devolve `429` com `limit: 0`. Se o erro cita `quotaId: ...-FreeTier`, o projeto daquela chave não está no faturamento; vincular o pagamento **ao projeto da chave**, não só à conta.
3. **Nem toda chave da ElevenLabs tem todos os escopos.** Sem `user_read` não dá para checar saldo antes de gerar lote. Verificar antes de planejar lote grande.

## Rede do environment

Hosts que o cinto de ferramentas exige na allowlist: `api.elevenlabs.io`, `api.openai.com`, `generativelanguage.googleapis.com`, `www.googleapis.com`, `drive.google.com`, `drive.usercontent.google.com`, `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`, `api.github.com` e GitHub Releases.

- **A allowlist é literal por subdomínio.** `www.googleapis.com` não cobre `generativelanguage.googleapis.com`. Para um site inteiro, usar `*.dominio.com` junto do apex.
- **Diagnóstico em um comando**: `curl -sv https://host/ 2>&1 | grep CONNECT`. `HTTP/1.1 403` no CONNECT é allowlist; qualquer outra resposta significa que a rede passou e o problema é outro (chave, quota, rota).
- `raw.githubusercontent.com` não precisa ser liberado: o `setup.sh` registra as skills do hyperframes a partir do clone local quando o `npx ... skills update` falha.
- **Chromium não contorna a allowlist.** O headless usa o mesmo agent proxy e devolve `ERR_TUNNEL_CONNECTION_FAILED` no host que o `curl` recusa. Navegador só ajuda contra JS/SPA, nunca contra egresso bloqueado.

## Gotchas essenciais (detalhe completo em FRAMEWORK.md)

### Câmera e cor

- Brutos de iPhone são HLG 10-bit: gerar proxy SDR uma vez antes de editar.
- **Brutos de Sony em S-Log2 (A7 III): converter, não "filtrar".** O XML lateral de cada clipe (`C00xxM01.XML`) declara `CaptureGammaEquation` e `CaptureColorPrimaries`; quando diz `s-log2`/`s-gamut`, a imagem chega chapada e precisa de conversão para Rec.709. `scripts/gera_lut_slog2.py` gera a LUT (log para linear, primárias, ombro, gama). Dois cuidados que a prática impôs: **exposição −0,5 stop e joelho em 0,65**, senão o branco estoura; e conferir que o ffmpeg aplica a `lut3d` **em RGB, não em YUV** (ele auto-insere `yuvj420p` para `rgb24`; verificar com `-v verbose`). Saída sempre com `out_range=tv` e `-color_range tv`, senão o arquivo sai `yuvj420p` e destoa entre players.
- **Câmera pode gravar na vertical sem gravar a flag de rotação.** O arquivo vem 3840x2160 deitado e o ffprobe não mostra rotação nenhuma; só olhando um frame se descobre. Corrigir com `transpose=1` antes de escalar. Checar um frame de qualquer lote novo antes de planejar o corte.

### Edição

- **Decupagem por âncora de texto, não por timecode.** `scripts/decupar.py` recebe um `edl.json` onde cada trecho é "de tal frase até tal frase" e casa as âncoras contra a transcrição com timestamp por palavra. Revisar um corte vira editar uma frase. O campo `apos` empurra o cursor quando a mesma frase aparece antes.
- Legendas SEMPRE por último no filter chain; overlays via PIL em PNG sequence + qtrle.
- Zoom animado com `zoompan`, não `crop` (crop não aceita `t` em w/h).
- **O patch `video-use-is-portrait-source` foi aposentado.** O upstream reescreveu `is_portrait_source` para ler também o `rotation` do side data, cobrindo mais casos que o patch. O `validate.sh` testa **comportamento** (retrato, paisagem e paisagem com matriz de rotação 90) em vez de procurar o patch no código, porque o que importa é a função acertar.

### Render e ferramentas

- **Remotion renderiza com o `headless_shell`, não com o Chromium do Playwright.** O `chromium-1194` removeu o headless antigo que o Remotion pede e o launch morre com "Old Headless mode has been removed". O binário certo é `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, fixado em `remotion/remotion.config.ts`. Baixar o browser próprio do Remotion não é opção: está fora da allowlist.
- **Licença do Remotion não é MIT**: grátis para indivíduo, organização sem fins lucrativos, empresa de até 3 funcionários e avaliação; acima disso exige Company License paga (remotion.pro). Confirmar o enquadramento antes de usar em produção.
- **Sem rede de fontes no render.** Google Fonts está fora da allowlist e a fonte cai para a sans do sistema. Para usar a fonte da marca, embutir o arquivo em `assets/fonts/` como asset local.
- **A URL do ffmpeg estático tem duas formas parecidas e só uma funciona.** `releases/download/latest/...` é a tag rolante do BtbN e serve o arquivo; `releases/latest/download/...` resolve para a autobuild do dia, cujos assets têm outro nome, e devolve 404. O `setup.sh` tenta as duas em ordem e **confere a assinatura XZ (`fd377a585a00`) antes de extrair**, senão um 404 chega como corpo de texto e o `tar` reclama de "not a tar archive", escondendo a causa.
- **Processo em background com `nohup`/`setsid` é recolhido quando a tool call retorna.** Usar `run_in_background: true` da própria ferramenta Bash, que o harness rastreia, ou deixar estourar o timeout do primeiro plano. Em lote longo, `flock` num arquivo de lock evita a corrida de dois loops escrevendo o mesmo arquivo.
- **Ler o índice de um ZIP gigante no Drive sem baixar o arquivo.** `drive.usercontent.google.com` aceita `Range`: pegar os últimos ~64 KB, achar o EOCD (`PK\x05\x06`) e, em arquivo maior que 4 GB, o ZIP64 EOCD via locator `PK\x06\x07`, ler o central directory e listar tudo. Com entradas `method=0` (stored), cada arquivo sai sozinho por outro `Range` no offset do local header. Evita baixar 11 GB para pegar um vídeo de 90 MB. Script: `scripts/zip_index_remoto.py`.
- Mac: usar ffmpeg-full keg-only com PATH explícito. Linux: ffmpeg do apt já serve.

### Publicação

- Metricool MCP: sem delete (cancelar = update draft:true; update devolve id novo); mídia por URL pública (Supabase bucket público funciona).
- **Metricool, rascunho com data vencida não publica e não avisa.** Um post `draft:true` cuja data passa continua no calendário e aparece em `getScheduledPosts` como se estivesse agendado, mas nunca dispara. Regra: **quem agenda tira do rascunho na mesma sessão e confirma com `getScheduledPosts`**; nunca deixar o flip de `draft` para a sessão seguinte. Tirar do rascunho com data no passado também não resolve, é preciso data nova.
