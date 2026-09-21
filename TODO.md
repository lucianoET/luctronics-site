# TODO — site luctronics.com.br

Pendências do site institucional. Contexto e estado completo em `README-ESTADO.md`
do projeto Claude "luctronics". Não cobre os apps da plataforma — cada um tem sua
própria lista no monorepo.

**Estado:** versão nova no ar desde 18/09/2026, na Netlify. Verificado em 20/09:
todas as páginas 200, redirects de URL limpa funcionando, headers de segurança
aplicados, `og.png` e `sitemap.xml` servidos.

---

## 🔴 Bloqueia outras coisas

- [ ] **Redeploy pendente.** `privacidade.html` mudou depois da publicação (data de
      atualização corrigida para 18/09). O que está no ar ainda diz 20/ago.
- [ ] **Demo pública do PMOC**, com organização genérica e sem dados do CMASM.
      É o que destrava linkar um sistema real na landing — hoje todo CTA de
      "ver funcionando" cai em agendar demonstração, porque o portal do cliente
      carrega dados operacionais reais e identifica a OM.
- [ ] **Decidir como o repo chega à Netlify.** Conferir no painel se o projeto está
      conectado a um repositório git ou se é deploy manual. Se for manual, publicar
      `luctronics-site` no GitHub (org `luctronicserp`) e conectar — cada commit
      passa a publicar sozinho. O token do `gh` na máquina está inválido:
      `gh auth login -h github.com`.

## 🟡 Conteúdo e identidade

- [ ] **E-mail do domínio.** O site usa `luctronics@gmail.com` em contato, privacidade,
      termos e documentação. Um `contato@luctronics.com.br` muda a percepção do
      negócio mais que qualquer ajuste de layout.
- [ ] **Decidir sobre `luctronics.com`.** Não resolve. Registrar e redirecionar para
      o `.com.br`, ou abandonar de vez — hoje está no meio do caminho.
- [ ] **URL fictícia no mockup do hero:** a barra do navegador mostra
      `luctronics.com.br/dashboard`, que não existe. Convenção comum de mockup, mas
      vale trocar por algo verdadeiro quando a demo existir.
- [ ] **Status do AirQ e do Sentinela na landing.** Ambos aparecem como
      "em desenvolvimento". O AirQ tem bloqueador registrado no firmware
      (alimentação do KY-037/038) — quando destravar, atualizar aqui.
- [ ] **Referências de cliente.** A landing diz "referências disponíveis sob
      solicitação". Vale ter pelo menos uma declaração formal pronta antes de a
      primeira pessoa pedir.

## 🟢 Técnico

- [ ] **Self-host das fontes.** Inter e JetBrains Mono vêm do Google Fonts por CDN.
      Custa uma requisição a mais no caminho crítico e, com a política de
      privacidade afirmando que o site não usa rastreamento de terceiros, a fonte
      externa é uma inconsistência defensável mas incômoda. Dois `.woff2` locais
      resolvem os dois problemas.
- [ ] **Lighthouse** com o site já publicado. Nunca foi medido em produção.
- [ ] **Testar o preview de compartilhamento** de verdade no WhatsApp e no LinkedIn.
      O `og.png` está servido e correto, mas o cache dessas plataformas é próprio.
- [ ] **Analytics — decidir se quer.** Hoje não tem nenhum. Se quiser, precisa ser
      sem cookie (Plausible, Umami, ou o próprio painel da Netlify) para não
      contradizer o item 2.3 da política de privacidade, que afirma não haver
      pixel nem perfilamento.
- [ ] **Favicon como arquivo.** Hoje é um SVG inline em data URI no `<head>`.
      Funciona, mas um `favicon.ico` + `apple-touch-icon.png` cobrem os clientes
      antigos e o atalho de tela inicial no iOS.

## 🔵 Manutenção recorrente

- [ ] Revisar os números da landing quando os módulos mudarem. Hoje: 12 módulos,
      171 climatização, ~500 instrumentos, 49 paióis, 150 locais, 206 itens.
      Fonte da verdade é o portal em produção, não este arquivo.
- [ ] Atualizar a data de "Última atualização" em `privacidade.html` e `termos.html`
      sempre que houver mudança material. `termos.html` está em 20/ago e continua
      correto — não foi alterado desde então.
- [ ] `_arquivo/` guarda ~7 MB de imagens órfãs e o backup do index original.
      Está fora do git e do deploy. Limpar quando não fizer mais falta.

---

## Feito

- [x] Publicar a versão nova (estava no ar a de agosto, com o título antigo) — 18/09
- [x] Sincronizar módulos com o sistema em produção: 8 → 12, mais Paióis, Gestão e
      Qualidade, Equipes, Bio e Energia e água — 18/09
- [x] Corrigir link quebrado do GitHub (`luctronics-ET` dava 404) — 18/09
- [x] `og:image`, `twitter:image` e `theme-color` com `og.png` 1200×630 — 18/09
- [x] Acessibilidade: `<main>`, skip link, `scroll-margin-top` nas âncoras,
      animação respeitando `prefers-reduced-motion` — 18/09
- [x] `robots.txt`, `sitemap.xml`, `netlify.toml` com headers e redirects — 18/09
- [x] Corrigir provedores de hospedagem na política de privacidade — 18/09
- [x] Repo git iniciado e ~7 MB de imagens órfãs tiradas do deploy — 18/09
