# Normalyze | e-mail HTML de exemplo (mail.normalyze.com.br)

`nr01-convite-demo.html` é um e-mail pronto para disparo pelo domínio `mail.normalyze.com.br`.
Público: gestor de RH e tomador de decisão. Objetivo: agendamento de demonstração (NR-01 e riscos psicossociais).

## Características técnicas

- Layout em tabelas, 600px, com fallback de empilhamento no mobile (media query em `@media screen and (max-width:600px)`).
- CSS inline nos elementos que importam (Gmail descarta parte do `<style>`), com `<style>` só para media queries, dark mode e resets.
- Suporte a dark mode via `prefers-color-scheme` e classes `bg-page`, `bg-card`, `bg-soft`, `t-strong`, `t-body`, `t-muted`, `rule`.
- Botão "bulletproof" em tabela com `bgcolor`, funciona no Outlook desktop.
- Preheader oculto no topo (texto de prévia da caixa de entrada).
- Sem imagens externas: a marca está em texto no cabeçalho. Para usar a logo, troque o link do topo pelo `<img>` já comentado no arquivo e hospede o PNG em `https://mail.normalyze.com.br/assets/`.

## Variáveis a substituir na plataforma de disparo

| Variável | Onde aparece | O que é |
|---|---|---|
| `{{first_name}}` | primeiro parágrafo | primeiro nome do contato |
| `{{campaign_id}}` | link de navegador e CTA | id da campanha para rastreio |
| `{{contact_id}}` | navegador, preferências, descadastro | id do contato |
| `{{sender_address}}` | rodapé | endereço físico do remetente (exigido por CAN-SPAM e boas práticas de entregabilidade) |

Links de descadastro e preferências apontam para `mail.normalyze.com.br`; troque pelos tokens nativos do ESP se ele gerar os próprios (`{{unsubscribe_url}}` e afins).

## Conteúdo

Pilares vindos do planejamento estratégico 2026: adequação à NR-01, privacidade do colaborador como bandeira principal, adesão real pelo WhatsApp com a Norma 24h. CTA do público RH: "Agende uma demonstração".

O depoimento no bloco de prova social é fictício e serve de placeholder. Troque por um depoimento real antes de disparar.
