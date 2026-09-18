/**
 * Paleta e tokens do EITA Reels Studio (@anaclaudia.eita).
 *
 * Canonico (esta no FRAMEWORK.md, nao inventar outro): o amarelo #FFE234 do
 * marca-texto das enfases, o lettering branco caps e o fundo escuro dos cortes.
 * Os outros amarelos sao derivados dele, so para dar profundidade a aurora.
 * Todo o resto do Remotion le daqui: trocar um hex muda o visual inteiro.
 */
export const marca = {
  /** Canonico: amarelo do marca-texto das enfases. */
  amarelo: "#FFE234",
  /** Derivados do amarelo canonico. */
  dourado: "#FFD166",
  ambar: "#F5A524",
  laranja: "#F2751F",
  /** Base dos fundos aurora: o quase preto dos cortes de podcast. */
  auroraBase: "#0E0D0B",
  /** Tinta do lettering: branco caps, a assinatura do perfil. */
  tinta: "#FFFFFF",
  /**
   * Helvetica Neue Condensed Black e proprietaria da Apple e nao existe em
   * Linux; sem rede no render, a cadeia cai para a condensada mais proxima
   * que estiver instalada e, no limite, para a sans do sistema.
   */
  fonte:
    '"Helvetica Neue", "Archivo Black", "Liberation Sans Narrow", "Liberation Sans", system-ui, -apple-system, sans-serif',
} as const;
