#!/usr/bin/env python3
"""Gera as páginas de cada app (sistema/*.html, produtos/*.html), os cartões da
seção "O que faz" do index.html e o sitemap.xml a partir da lista APPS abaixo.

Fonte única de nome, situação e números de cada app: mudou um status ou um número,
edite aqui e rode `python3 tools/paginas.py` na raiz do site. Sem dependências.

Regra do conteúdo: linguagem de quem cuida da manutenção, sem jargão técnico, e
nenhum dado que identifique cliente (nome, órgão, local, números exatos de inventário).
"""
from datetime import date
from html import escape
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://luctronics.com.br"
WA = "5521991398668"

# situação → (classe da página, classe do cartão, rótulo)
STATUS = {
    "uso":  ("st-uso",  "ms-active", "Em uso"),
    "disp": ("st-uso",  "ms-active", "Disponível"),
    "beta": ("st-beta", "ms-beta",   "Beta"),
    "impl": ("st-impl", "ms-impl",   "Em implantação"),
    "demo": ("st-demo", "ms-demo",   "Demonstração"),
    "dev":  ("st-dev",  "ms-beta",   "Em desenvolvimento"),
}

# grupo: "uso" = em uso hoje · "impl" = em implantação · "prod" = equipamentos e sensores
APPS = [
    dict(slug="ar-condicionado", pasta="sistema", grupo="uso", status="uso",
         nome="Ar-condicionado", titulo="Ar-condicionado com o PMOC em dia",
         resumo="Plano de manutenção (PMOC) de cada aparelho, serviços do pedido ao pagamento e etiqueta com QR code.",
         lead="Cada aparelho com ficha, histórico e agenda de manutenção. Você vê o que vence, o que está parado e quanto vai custar.",
         num=("170+", "aparelhos acompanhados hoje"),
         feats=[
             ("Ficha de cada aparelho", "Marca, capacidade, local, histórico de serviços e situação atual, num lugar só."),
             ("Agenda das preventivas", "O sistema monta o calendário do PMOC e avisa o que está para vencer."),
             ("Do pedido ao pagamento", "Orçamento, execução, fiscalização e aceite do serviço registrados, prontos para prestação de contas."),
             ("Etiqueta com QR code", "Aponte o celular para o aparelho e abra a ficha dele na hora."),
             ("Prioridade automática", "Os aparelhos mais críticos aparecem primeiro."),
             ("Relatórios para imprimir", "Situação do parque e serviços do período, sem montar planilha."),
         ],
         rel=["eletrica", "predial", "gestao"]),
    dict(slug="calibracao", pasta="sistema", grupo="uso", status="uso",
         nome="Calibração", titulo="Nenhum instrumento com a calibração vencida",
         resumo="Avisa o vencimento de cada instrumento, guarda os certificados e organiza o recolhimento.",
         lead="O sistema avisa antes de um instrumento vencer e guarda todos os certificados, prontos para qualquer auditoria.",
         num=("Centenas", "de instrumentos controlados"),
         feats=[
             ("Lista de instrumentos", "Busque por tipo, local ou situação e veja na hora o que está em dia e o que venceu."),
             ("Aviso de vencimento", "Você fica sabendo com antecedência, não depois."),
             ("Certificados guardados", "Cada calibração registrada com o certificado anexado."),
             ("Laboratórios e contratos", "Quem calibra o quê e quanto ainda resta do contrato."),
             ("Etiqueta com QR code", "A ficha do instrumento a um toque do celular."),
         ],
         rel=["gestao", "ar-condicionado"]),
    dict(slug="predial", pasta="sistema", grupo="uso", status="uso",
         nome="Predial", titulo="Vistoria predial pelas normas, sem papel",
         resumo="Vistoria do prédio pelas normas da ABNT, com prioridade de cada problema e laudo pronto.",
         lead="Organiza a vistoria do prédio pelas normas da ABNT (NBR 5674 e 16747) e mostra o que precisa ser corrigido primeiro.",
         num=("200+", "itens de verificação prontos"),
         feats=[
             ("Prédio organizado", "Locais em árvore: prédio, andar, sala. Cada problema fica no lugar certo."),
             ("Lista de verificação pronta", "Modelos por tipo de local, com os itens que a norma pede."),
             ("O que corrigir primeiro", "Cada problema recebe uma prioridade pela gravidade, urgência e tendência de piorar."),
             ("Laudo pronto", "O sistema monta o laudo da vistoria."),
             ("Aprovação registrada", "Quem vistoriou, quem revisou e quem aprovou, com data."),
         ],
         rel=["gestao", "mapa"]),
    dict(slug="eletrica", pasta="sistema", grupo="uso", status="uso",
         nome="Elétrica", titulo="Geradores e quadros revisados na hora certa",
         resumo="Geradores, quadros elétricos, nobreaks e iluminação, com revisão pelas horas de uso.",
         lead="Geradores, quadros elétricos, nobreaks e iluminação revisados pelas horas de uso, com peças e compras organizadas.",
         num=None,
         feats=[
             ("Contador de horas", "Cada equipamento com as horas de uso; a revisão é avisada quando chega a hora."),
             ("Plano por tipo de equipamento", "O que fazer em cada revisão, de cada tipo de máquina."),
             ("Registro de falhas", "Cada pedido de serviço guarda o que falhou e o que foi feito."),
             ("Estoque mínimo", "Avisa quando uma peça importante está acabando."),
             ("Lista de compras pronta", "O que precisa comprar, já montado para o processo de compra."),
         ],
         rel=["ar-condicionado", "maquinas"]),
    dict(slug="maquinas", pasta="sistema", grupo="uso", status="uso",
         nome="Máquinas de corte", titulo="Roçadeiras e tratores sempre prontos",
         resumo="Roçadeiras, motosserras e tratores: revisão pelas horas de uso, peças com preço e combustível.",
         lead="Roçadeiras, motosserras e tratores revisados pelas horas de uso, com o custo de peças e combustível na mão.",
         num=("25+", "máquinas acompanhadas"),
         feats=[
             ("Revisão pelas horas de uso", "Cada máquina avisa quando precisa de revisão."),
             ("Peças com preço", "Catálogo de peças, estoque e custo de cada troca."),
             ("Combustível por operador", "Quanto cada máquina consome e quem abasteceu."),
             ("Onde vai o dinheiro", "As máquinas que mais custam aparecem primeiro."),
             ("Quadro de serviços", "O que está na fila, em andamento e pronto, num quadro simples."),
             ("Guia de defeitos", "Do sintoma à causa provável, para acertar no conserto."),
         ],
         rel=["frota", "areas-verdes"]),
    dict(slug="frota", pasta="sistema", grupo="uso", status="uso",
         nome="Frota", titulo="Saiba o que está rodando e o que vai parar",
         resumo="Veículos, agenda de viagens, manutenção por quilometragem e relatórios de uso.",
         lead="Cada veículo com agenda de viagens, manutenção por quilometragem ou horas e o histórico completo.",
         num=("40+", "veículos acompanhados"),
         feats=[
             ("Cadastro da frota", "Cada veículo com documentos, situação e histórico."),
             ("Agenda de viagens", "Quem vai, quando e com qual veículo."),
             ("Manutenção por quilometragem", "A revisão é avisada pelos quilômetros ou pelas horas de uso."),
             ("Peças e serviços", "Pedidos de serviço e peças usadas em cada veículo."),
             ("Indicadores da frota", "Disponibilidade, custos e uso, num painel."),
         ],
         rel=["maquinas", "rastreador"]),
    dict(slug="aviso-sonoro", pasta="sistema", grupo="uso", status="uso",
         nome="Aviso sonoro", titulo="Sirenes e alto-falantes que funcionam quando precisa",
         resumo="Amplificadores, alto-falantes e sirenes, com testes periódicos e registro de falhas.",
         lead="Amplificadores, alto-falantes e sirenes testados com regularidade, para não falharem na hora da emergência.",
         num=None,
         feats=[
             ("Cadastro por tipo", "Amplificadores, mesas, alto-falantes, linhas e sirenes."),
             ("Testes periódicos", "O sistema lembra quando testar cada equipamento."),
             ("Registro de falhas", "O que falhou no teste e o que foi feito para corrigir."),
             ("Peças de reposição", "O que tem em estoque para trocar."),
         ],
         rel=["eletrica", "gestao"]),
    dict(slug="gestao", pasta="sistema", grupo="uso", status="uso",
         nome="Gestão e qualidade", titulo="Uma visão única da manutenção",
         resumo="Indicadores num painel, plano de ação por prioridade e um calendário com os prazos de todas as áreas.",
         lead="Os números da manutenção num painel só: o que está atrasado, o que vence e o que fazer primeiro.",
         num=None,
         feats=[
             ("Painel de indicadores", "Os indicadores de manutenção que a norma ABNT NBR 5674 pede, atualizados sozinhos."),
             ("Plano de ação", "O que fazer, por quê, quem, quando e quanto custa, em ordem de prioridade."),
             ("Calendário único", "Os prazos de todas as áreas da manutenção num calendário só."),
             ("Ferramentas da qualidade", "Gráficos para achar as causas que mais pesam e acompanhar a evolução."),
             ("Procedimentos padrão", "Como cada serviço deve ser feito, à mão da equipe."),
         ],
         rel=["equipes", "predial", "ar-condicionado"]),
    dict(slug="equipes", pasta="sistema", grupo="impl", status="impl",
         nome="Equipes", titulo="Quem faz o quê, e se dá tempo",
         resumo="Pessoas, especialidades, escala por turno e horas de trabalho disponíveis.",
         lead="Pessoas, especialidades e turnos num cadastro só, com as horas da equipe comparadas aos serviços previstos.",
         num=None,
         feats=[
             ("Pessoas e especialidades", "Eletricista, mecânico, refrigeração: cada um no seu ofício."),
             ("Turnos e escala", "Escala semanal por turno, sem planilha."),
             ("Horas disponíveis", "Quantas horas a equipe tem contra quantas o serviço pede."),
             ("Cadastro único", "As mesmas pessoas aparecem em todas as áreas do sistema."),
         ],
         rel=["gestao"]),
    dict(slug="mapa", pasta="sistema", grupo="impl", status="beta",
         nome="Mapa", titulo="Cada equipamento no mapa",
         resumo="Mapa e imagem de satélite da instalação, mostrando onde fica cada equipamento.",
         lead="Veja no mapa onde fica cada equipamento e cada ocorrência da instalação.",
         num=None,
         feats=[
             ("Mapa e satélite", "Alterne entre mapa e imagem de satélite."),
             ("Camadas por área", "Ligue e desligue ar-condicionado, elétrica, árvores e o que mais precisar."),
             ("Zonas desenhadas", "Marque áreas, setores e rotas direto no mapa."),
             ("Exportação", "Leve o mapa para outros programas de mapa."),
         ],
         rel=["areas-verdes", "predial"]),
    dict(slug="areas-verdes", pasta="sistema", grupo="impl", status="beta",
         nome="Áreas verdes", titulo="Árvores, animais e pragas sob controle",
         resumo="Árvores com QR code, registro de animais e pragas, e agenda de poda e controle.",
         lead="Árvores identificadas, ocorrência de animais e pragas registrada e agenda de poda e controle em dia.",
         num=None,
         feats=[
             ("Fichas prontas", "Fichas de animais, pragas e árvores comuns, para registrar sem digitar tudo."),
             ("Árvore com QR code", "Cada árvore identificada, com histórico de poda e vistoria."),
             ("Ocorrência no mapa", "Onde o animal ou a praga apareceu."),
             ("Agenda de serviços", "Poda e controle de pragas com periodicidade."),
         ],
         rel=["mapa", "maquinas"]),
    dict(slug="depositos", pasta="sistema", grupo="impl", status="demo",
         nome="Depósitos", titulo="Temperatura e umidade dos depósitos vigiadas",
         resumo="Temperatura e umidade de depósitos e almoxarifados, com alarme e boletim diário.",
         lead="Depósitos e almoxarifados com temperatura e umidade acompanhadas, alarme quando passa do limite e boletim do dia pronto.",
         num=None,
         feats=[
             ("Situação de cada depósito", "Um mapa mostra quais estão bem e quais pedem atenção."),
             ("Alarme", "Aviso quando a temperatura ou a umidade passa do limite."),
             ("Leitura na ronda", "Quem faz a ronda anota a leitura pelo celular."),
             ("Histórico", "Como cada depósito se comportou ao longo dos dias."),
             ("Boletim diário", "Pronto para imprimir e assinar."),
             ("Tela para a portaria", "Painel em tela cheia para acompanhar de longe."),
         ],
         nota="Em demonstração: as telas estão prontas; a ligação com os sensores está em teste.",
         rel=["mapa", "gestao"]),
    dict(slug="energia", pasta="sistema", grupo="impl", status="demo",
         nome="Energia e água", titulo="Consumo de energia e água num painel",
         resumo="Painel de consumo de energia e água, com metas. Os medidores ainda estão sendo instalados.",
         lead="Consumo de energia e água acompanhado num painel, com metas para economizar.",
         num=None,
         feats=[
             ("Consumo e demanda", "Quanto se gasta de energia e água, por período."),
             ("Metas", "Defina metas de economia e acompanhe."),
             ("Indicadores", "Os números de eficiência num painel só."),
         ],
         nota="Em demonstração: a tela já existe e mostra dados de exemplo; os medidores ainda estão sendo instalados.",
         rel=["aguada", "eletrica"]),

    # equipamentos e sensores
    dict(slug="aguada", pasta="produtos", grupo="prod", status="disp",
         nome="Aguada", titulo="Aguada: a água sob controle",
         resumo="Nível das caixas d'água e estado das bombas em tempo real, com sensores sem fio.",
         lead="Sensores sem fio nas caixas d'água mostram o nível e o estado das bombas em tempo real, no celular ou no computador. Funciona sozinho ou junto com o resto do sistema.",
         num=None,
         feats=[
             ("Nível na hora", "Painel ao vivo com o nível de cada caixa d'água."),
             ("Bombas e válvulas", "Uma tela mostra a rede inteira: caixas, bombas e válvulas."),
             ("Alerta de nível", "Aviso quando o nível passa do limite que você definir."),
             ("Histórico e relatório", "Gráficos do nível e relatório diário em PDF."),
             ("Sem Wi-Fi no local", "Os sensores conversam entre si sem fio; um com defeito não derruba os outros."),
             ("Manutenção junto", "Serviços nas bombas e laudos da qualidade da água no mesmo sistema."),
         ],
         rel=["energia", "depositos"]),
    dict(slug="airq", pasta="produtos", grupo="prod", status="dev",
         nome="AirQ", titulo="AirQ: o ar do ambiente e o ar-condicionado medidos",
         resumo="Mede o ar do ambiente e mostra se o ar-condicionado está trabalhando direito.",
         lead="Um sensor pequeno que mede o ar do ambiente e mostra se o ar-condicionado está entregando o que deveria.",
         num=None,
         feats=[
             ("Temperatura e umidade", "Do ambiente, o tempo todo."),
             ("Qualidade do ar", "Gás carbônico (CO₂) e outros gases que pesam no ar parado."),
             ("Luz e ruído", "Iluminação e barulho do ambiente."),
             ("O ar-condicionado está gelando?", "Compara a temperatura do ar que entra e que sai do aparelho."),
             ("Consumo do compressor", "Mostra quando o compressor liga e quanto puxa de energia."),
             ("Tela própria", "Acesse as leituras direto pelo Wi-Fi do sensor, sem internet."),
         ],
         nota="Em desenvolvimento: os primeiros sensores estão em teste de bancada.",
         rel=["ar-condicionado"]),
    dict(slug="cameras", pasta="produtos", grupo="prod", status="dev",
         nome="Câmeras inteligentes", titulo="Câmeras que avisam sozinhas",
         resumo="Usa as câmeras de segurança que você já tem para avisar de pessoas, fogo e drones.",
         lead="Aproveita as câmeras de segurança que você já tem para avisar quando algo fora do normal aparece.",
         num=None,
         feats=[
             ("Usa as câmeras existentes", "Sem trocar o sistema de segurança."),
             ("Pessoas em área restrita", "Aviso quando alguém entra onde não deveria."),
             ("Fogo", "Câmeras térmicas ajudam a ver o fogo cedo."),
             ("Drones", "Detecção de objetos voando sobre a instalação."),
             ("Alarmes do seu jeito", "Você escolhe onde, quando e como avisar."),
             ("Painel único", "Todas as câmeras numa tela."),
         ],
         nota="Em desenvolvimento: protótipo em teste.",
         rel=["mapa"]),
    dict(slug="rastreador", pasta="produtos", grupo="prod", status="dev",
         nome="Rastreador de veículos", titulo="Por onde cada veículo andou, sem chip de celular",
         resumo="Grava o trajeto dos veículos mesmo sem sinal e envia quando encontra uma rede conhecida.",
         lead="Grava o trajeto do veículo o tempo todo e envia os dados sozinho quando encontra uma rede conhecida. Não usa chip de celular.",
         num=None,
         feats=[
             ("Nenhum trecho se perde", "O trajeto fica gravado mesmo sem sinal."),
             ("Envio automático", "Os dados sobem quando o veículo chega a uma rede Wi-Fi conhecida."),
             ("Trajeto no mapa", "Veja por onde o veículo passou e onde parou."),
             ("Bateria de reserva", "Continua funcionando com o veículo desligado."),
         ],
         nota="Em desenvolvimento: protótipo em teste de bancada.",
         rel=["frota"]),
]

POR_SLUG = {a["slug"]: a for a in APPS}
GRUPOS = [
    ("uso",  "g-prod", "Em uso hoje"),
    ("impl", "g-dev",  "Em implantação"),
    ("prod", "g-dev",  "Equipamentos e sensores"),
]


def url(a):
    return f"/{a['pasta']}/{a['slug']}.html"


def wa_link(texto):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(texto)}"


NAV = """<a class="skip-link" href="#conteudo">Ir para o conteúdo</a>

<nav>
  <a class="nav-logo" href="/">
    <div class="logo-icon">
      <svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
    </div>
    <span class="logo-name">luc<span>tronics</span></span>
  </a>
  <div class="nav-links">
    <a href="/#producao">Resultados</a>
    <a href="/#modulos">O que faz</a>
    <a href="/#produto">Sensores</a>
    <a href="/#quem">Quem somos</a>
    <a href="/#contato" class="nav-cta">Agendar demonstração</a>
  </div>
  <button class="nav-mobile-btn" aria-label="Abrir menu" aria-expanded="false" aria-controls="mobile-menu" id="menu-btn">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
  </button>
</nav>
<div class="nav-mobile-panel" id="mobile-menu">
  <a href="/#producao">Resultados</a>
  <a href="/#modulos">O que faz</a>
  <a href="/#produto">Sensores</a>
  <a href="/#quem">Quem somos</a>
  <a href="/#contato">Agendar demonstração</a>
</div>"""

FOOTER = """<footer>
  <div class="footer-inner">
    <div class="footer-top">
      <div>
        <a class="footer-logo" href="/">
          <div class="fl-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg></div>
          <span class="fl-name">luc<span>tronics</span></span>
        </a>
        <p class="footer-desc">Sistema de manutenção, calibração e monitoramento de instalações. Feito no Rio de Janeiro, RJ.</p>
      </div>
      <div class="footer-col">
        <h5>Sistema</h5>
        <a href="/#modulos">O que faz</a>
        <a href="/#produto">Sensores</a>
        <a href="/#producao">Resultados</a>
        <a href="/#quem">Quem somos</a>
      </div>
      <div class="footer-col">
        <h5>Materiais</h5>
        <a href="/documentacao.html">Documentação técnica</a>
      </div>
      <div class="footer-col">
        <h5>Contato</h5>
        <a href="mailto:luctronics@gmail.com">luctronics@gmail.com</a>
        <a href="https://wa.me/5521991398668" target="_blank" rel="noopener">WhatsApp</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2026 Luctronics · Rio de Janeiro, RJ</p>
      <div style="display:flex;gap:1.5rem">
        <a href="/privacidade.html">Política de Privacidade</a>
        <a href="/termos.html">Termos de Uso</a>
      </div>
    </div>
  </div>
</footer>"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' "
           "rx='7' fill='%230057FF'/%3E%3Cpolyline points='27 16 22 16 18 26 12 6 9 16 5 16' fill='none' stroke='%23fff' "
           "stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E")


def pagina(a):
    st_cls, _, st_txt = STATUS[a["status"]]
    titulo = f"{a['nome']} — Luctronics"
    desc = a["resumo"]
    canon = SITE + url(a)
    e = escape
    num = ""
    if a.get("num"):
        num = f'    <div class="app-num"><b>{e(a["num"][0])}</b>{e(a["num"][1])}</div>\n'
    nota = f'    <p class="app-note">{e(a["nota"])}</p>\n' if a.get("nota") else ""
    feats = "\n".join(
        f'      <div class="feat"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in a["feats"])
    rel = "\n".join(f'      <a href="{url(POR_SLUG[s])}">{e(POR_SLUG[s]["nome"])} →</a>' for s in a["rel"])
    wa = wa_link(f"Olá, vim pelo site da Luctronics e quero ver o {a['nome']} funcionando.")
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Luctronics">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0057FF">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<!-- Gerado por tools/paginas.py — edite lá, não aqui. -->

{NAV}

<main id="conteudo">

<div class="app-hero">
  <p class="crumbs"><a href="/">Início</a> · <a href="/#modulos">O que faz</a> · {e(a['nome'])}</p>
  <div class="st {st_cls}">{st_txt}</div>
  <h1>{e(a['titulo'])}</h1>
  <p class="lead">{e(a['lead'])}</p>
{num}  <div class="hero-actions">
    <a href="{e(wa)}" class="btn-blue" target="_blank" rel="noopener">Ver funcionando</a>
    <a href="/#modulos" class="btn-outline">Ver todas as áreas</a>
  </div>
</div>

<div class="section-wrap bg-gray">
  <div class="section-inner">
    <div class="section-eyebrow">O que faz</div>
    <h2>Na prática</h2>
    <div class="feat-grid">
{feats}
    </div>
{nota}  </div>
</div>

<div class="section-wrap">
  <div class="section-inner">
    <div class="section-eyebrow">Funciona junto</div>
    <h2>Combina com</h2>
    <p class="lead">Tudo no mesmo sistema e com o mesmo acesso: os equipamentos, as pessoas e os pedidos de serviço são compartilhados.</p>
    <div class="related">
{rel}
    </div>
  </div>
</div>

<div class="cta-wrap" id="contato">
  <div class="cta-inner">
    <h2>Quer ver o {e(a['nome'])} funcionando?</h2>
    <p>Demonstração sem compromisso, com dados de exemplo. Você conversa direto com quem fez o sistema.</p>
    <div class="cta-btns">
      <a href="{e(wa)}" class="btn-white" target="_blank" rel="noopener">Falar no WhatsApp</a>
      <a href="mailto:luctronics@gmail.com?subject={e(a['nome'])}%20%E2%80%94%20Luctronics" class="btn-outline-white">Enviar e-mail</a>
    </div>
    <p class="cta-sub">Resposta em até 1 dia útil · Rio de Janeiro, RJ</p>
  </div>
</div>

</main>

{FOOTER}

<script src="/assets/menu.js" defer></script>
</body>
</html>
"""


def cartoes():
    e = escape
    out = []
    for grupo, cls, rotulo in GRUPOS:
        apps = [a for a in APPS if a["grupo"] == grupo]
        n = f'<span class="mod-group-n">{len(apps)} {"áreas" if grupo != "prod" else "produtos"}</span>'
        out.append(f'    <h3 class="mod-group {cls}"><span class="mg-dot"></span>{rotulo} {n}</h3>')
        out.append('    <div class="mod-grid">')
        for a in apps:
            _, ms, st_txt = STATUS[a["status"]]
            ativo = " active" if a["status"] in ("uso", "disp") else ""
            if a.get("num"):
                metric = f'<div class="mod-metric">{e(a["num"][0])}<span>{e(a["num"][1])}</span></div>'
            else:
                metric = ""
            out.append(
                f'      <a class="mod-card{ativo}" href="{url(a)}">'
                f'<div class="mod-status {ms}"><span class="ms-dot"></span>{st_txt}</div>'
                f'<h4>{e(a["nome"])}</h4>{metric}<p>{e(a["resumo"])}</p>'
                f'<span class="mod-more">Ver detalhes →</span></a>')
        out.append('    </div>')
    return "\n".join(out)


def main():
    for a in APPS:
        destino = RAIZ / a["pasta"] / f"{a['slug']}.html"
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(pagina(a), encoding="utf-8")

    idx = RAIZ / "index.html"
    s = idx.read_text(encoding="utf-8")
    ini, fim = "<!-- APPS:INICIO (gerado por tools/paginas.py) -->", "<!-- APPS:FIM -->"
    a, b = s.index(ini) + len(ini), s.index(fim)
    s = s[:a] + "\n" + cartoes() + "\n    " + s[b:]
    idx.write_text(s, encoding="utf-8")

    hoje = date.today().isoformat()
    fixas = [("/", "1.0", "monthly"), ("/documentacao.html", "0.6", "monthly"),
             ("/privacidade.html", "0.3", "yearly"), ("/termos.html", "0.3", "yearly")]
    linhas = [f'  <url><loc>{SITE}{u}</loc><lastmod>{hoje}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>'
              for u, p, f in fixas]
    linhas += [f'  <url><loc>{SITE}{url(a)}</loc><lastmod>{hoje}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>'
               for a in APPS]
    (RAIZ / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(linhas) + "\n</urlset>\n", encoding="utf-8")

    # ponytail: checagem mínima — todo "rel" aponta para app existente e nenhum termo do cliente vazou.
    # Os termos ficam fora do repositório (ele é público): um por linha em ~/.config/luctronics/termos_proibidos.txt
    lista = Path.home() / ".config/luctronics/termos_proibidos.txt"
    proibidos = [t.strip() for t in lista.read_text(encoding="utf-8").splitlines() if t.strip()] if lista.exists() else []
    if not proibidos:
        print(f"aviso: {lista} ausente, termos do cliente não conferidos")
    for a in APPS:
        assert all(r in POR_SLUG for r in a["rel"]), a["slug"]
        html = (RAIZ / a["pasta"] / f"{a['slug']}.html").read_text(encoding="utf-8")
        assert not any(p in html for p in proibidos), a["slug"]
    print(f"{len(APPS)} páginas, cartões do index.html e sitemap.xml gerados")


if __name__ == "__main__":
    main()
