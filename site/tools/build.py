#!/usr/bin/env python3
"""Gera as páginas estáticas do site Legado Genética em ../ (sem dependências)."""
import os, html

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NAV = [
    ("index.html", "Início"), ("produtos.html", "Produtos"), ("jornada.html", "Jornada"),
    ("consanguinidade-x-heterose.html", "Consanguinidade x Heterose"), ("diagnostico.html", "Diagnóstico"),
    ("legado-connect.html", "Legado Connect"), ("fontes.html", "Fontes"),
]
IMG = {
    "aereo": ("assets/img/pasto-aereo.jpg", "Vaca Nelore branca pastando sozinha, vista aérea de um pasto dourado ao fim da tarde, com anéis de vento no capim"),
    "olho": ("assets/img/vaca-nivel-olho.jpg", "Vaca Nelore olhando para a câmera, com o sol baixo atrás dela e o pasto dourado ao fundo"),
    "sede": ("assets/img/sede-ipe-entardecer.jpg", "Casa de fazenda branca com telhado colonial e um ipê amarelo ao pôr do sol, com uma vaca Nelore pastando em primeiro plano"),
    "curral": ("assets/img/curral-por-do-sol.jpg", "Vaca Nelore iluminada por trás dentro de um curral de madeira ao pôr do sol, com poeira dourada no ar"),
    "rosto": ("assets/img/vaca-rosto-contraluz.jpg", "Retrato de perfil do rosto de uma vaca Nelore contra o sol, com contorno dourado nos pelos"),
}
FAVICON = "assets/favicon.svg"


def layout(fname, title, desc, body, home=False, scripts=(), inline=""):
    nav = "".join(
        f'<a href="{h}">{html.escape(t)}</a>' for h, t in NAV
    )
    foot = "".join(f'<a href="{h}">{html.escape(t)}</a>' for h, t in NAV)
    og = IMG["sede"][0]
    scr = "".join(f'<script src="assets/js/{s}" defer></script>' for s in scripts)
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#14110a">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{FAVICON}" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,700;1,9..144,500&amp;family=DM+Sans:wght@400;500;600&amp;display=swap">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="{'page-home' if home else ''}">
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="index.html" aria-label="Legado Genética, início">Legado <i>Genética</i></a>
    <button class="nav-toggle" type="button" aria-label="Abrir menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Navegação principal">{nav}</nav>
  </div>
</header>
<main id="conteudo">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <a class="brand" href="index.html">Legado <i>Genética</i></a>
    <nav class="foot-nav" aria-label="Navegação do rodapé">{foot}</nav>
    <p>Projeto acadêmico de simulação (APS de Agronomia). Empresa, produtos e dados de demonstração.</p>
    <p>Imagens geradas por IA para fins ilustrativos. Não representam animais ou instalações reais.</p>
    <p>Preservamos a origem. Planejamos o futuro.</p>
  </div>
</footer>
<script src="assets/js/common.js" defer></script>
{scr}
{inline}
</body>
</html>
"""


def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)


def img(key, cls="layer", extra=""):
    src, alt = IMG[key]
    return f'<img class="{cls}" src="{src}" alt="{html.escape(alt)}" width="1080" height="1446" decoding="async" {extra}>'


# ------------------------------------------------------------------ INÍCIO
home = f"""
<div class="story-track" id="story-track">
  <div class="stage">
    {img('aereo', extra='fetchpriority="high"')}
    {img('olho')}
    {img('sede')}
    {img('curral')}
    {img('rosto')}
    <div class="scrim"></div>
    <div class="dots" aria-label="Capítulos da abertura"></div>
    <article class="chapter" id="c0">
      <p class="eyebrow">Programa de melhoramento Nelore</p>
      <h1>Genética que nasce no <span class="accent">pasto</span>.</h1>
      <p class="lead">Consanguinidade planejada para quem cria Nelore de verdade.</p>
      <div class="hint"><i></i>Role para entrar na fazenda</div>
    </article>
    <article class="chapter" id="c1">
      <p class="eyebrow">A matriz</p>
      <h2>Tudo começa com uma <span class="accent">matriz</span>.</h2>
      <p class="lead">Rusticidade, fertilidade e carcaça nascem de uma boa escolha, feita a pasto e com histórico conhecido.</p>
    </article>
    <article class="chapter" id="c2">
      <p class="eyebrow">Consanguinidade planejada</p>
      <h2>Parentesco sob <span class="accent">controle</span>.</h2>
      <p class="lead">Cada acasalamento é simulado antes de acontecer, e o coeficiente de endogamia (F) fica dentro da meta.</p>
      <div class="stats">
        <div><b>6,25%</b><span>F do filho de primos de primeiro grau</span></div>
        <div><b>12,5%</b><span>F do filho de meios-irmãos</span></div>
      </div>
    </article>
    <article class="chapter" id="c3">
      <p class="eyebrow">A fazenda</p>
      <h2>A fazenda é o <span class="accent">laboratório</span>.</h2>
      <p class="lead">Pesagem, prenhez e desmama viram dados. Os dados voltam ao pasto como decisão de acasalamento.</p>
    </article>
    <article class="chapter" id="c4">
      <p class="eyebrow">Diagnóstico</p>
      <h2>Conheça o seu <span class="accent">rebanho</span>.</h2>
      <p class="lead">Informe o perfil da fazenda e veja qual estratégia de consanguinidade planejada se encaixa nela.</p>
      <p><a class="btn" href="diagnostico.html">Iniciar diagnóstico</a></p>
    </article>
  </div>
</div>

<section class="block">
  <div class="wrap">
    <p class="eyebrow">Uma proposta, três ativos</p>
    <h2>A fazenda já tem o que o programa <span class="accent">precisa</span>.</h2>
    <p class="lead">A Legado Genética oferece informação para decidir: quem avaliar, quais famílias preservar, como planejar acasalamentos e como monitorar resultados, sem prometer ganho automático.</p>
    <div class="grid g3" style="margin-top:1.4rem">
      <article class="card"><span class="tag">Ativo 1</span><h3>Nelore Fumaça</h3><p>Caracterizar geneticamente o fenótipo, mapear famílias e desempenho, e transformar a preferência da proprietária em um programa de seleção estruturado.</p></article>
      <article class="card"><span class="tag">Ativo 2</span><h3>Nelore convencional</h3><p>Reservatório de diversidade e de linhagens complementares. Não desperdiçamos o patrimônio genético que a proprietária já possui.</p></article>
      <article class="card"><span class="tag">Ativo 3</span><h3>Fábrica de ração</h3><p>Organizar os dados de nutrição e avaliar eficiência alimentar com método válido. Seu investimento em nutrição também poderá orientar a seleção.</p></article>
    </div>
    <div class="note gold">A cor Fumaça é um critério de interesse da cliente, não uma garantia de superioridade genética ou produtiva. A seleção equilibra pelagem, fertilidade, saúde, mérito genético e diversidade.</div>
  </div>
</section>

<section class="block" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">O debate técnico</p>
    <h2>Consanguinidade ou <span class="accent">heterose</span>?</h2>
    <p class="lead">O cruzamento rende mais quilos no desmame no curto prazo, e este site mostra isso. A pergunta certa é qual caminho serve ao objetivo desta fazenda: preservar e valorizar a linhagem Fumaça com risco controlado.</p>
    <p><a class="btn ghost" href="consanguinidade-x-heterose.html">Ver o comparador com números</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Preservamos a origem. <span class="accent">Planejamos o futuro.</span></h2>
    <a class="btn" href="diagnostico.html">Iniciar diagnóstico</a>
  </div>
</section>
"""

# ------------------------------------------------------------------ PRODUTOS
PRODUCTS = [
    ("Fumaça DNA", "Genotipagem e registros genéticos; estudo da pelagem.", "Passaporte Genético Digital.", "Caracterizar o rebanho Fumaça com padrão e abrir o mapa genético."),
    ("GeneBank Nelore", "Triagem de convencionais e diversidade genética.", "Mapa de candidatos à seleção.", "Achar reprodutores pouco aparentados e possíveis portadores de alelos de interesse."),
    ("Fumaça Match", "Simula pares e parentesco; estima endogamia quando houver dados.", "Plano de acasalamentos justificado.", "Comparar opções de acasalamento, apontar risco e recusar pares de F alto."),
    ("Núcleo Fumaça Elite", "Matrizes, reprodutores, IA/FIV se indicadas.", "Calendário e metas reprodutivas.", "Organizar o núcleo de seleção e as próximas gerações."),
    ("NutriGen Performance", "Compara desempenho sob condições controladas.", "Boletim zootécnico e alimentar.", "Ligar a fábrica de ração a ganho, consumo e custo alimentar medidos."),
    ("Legado Connect", "Centraliza dados e alertas.", "Painel remoto e relatório executivo.", "Dar à proprietária em São Paulo uma visão simples da fazenda."),
    ("Legado Selection", "Rastreabilidade e preparação comercial.", "Dossiê para animais selecionados.", "Documentar animais avaliados para o posicionamento comercial."),
]
cards = ""
for i, (n, fn, ent, uso) in enumerate(PRODUCTS):
    cards += f"""<article class="card{' hl' if i == 2 else ''}">
  <span class="tag">Solução {i+1}</span><h3>{n}</h3>
  <div class="dl"><b>Função técnica</b>{fn}</div>
  <div class="dl"><b>Entrega</b>{ent}</div>
  <button class="btn ghost small" type="button" data-prod="{html.escape(n)}" data-fn="{html.escape(fn)}" data-ent="{html.escape(ent)}" data-uso="{html.escape(uso)}">Saiba mais</button>
</article>"""
produtos = f"""
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Soluções Legado</p><h1>Sete soluções, um <span class="accent">programa</span>.</h1>
    <p class="lead">Um contrato principal com módulos integrados, em vez de sete serviços desconectados.</p></div>
    <div class="grid g3">{cards}</div>
    <div class="grid g2" style="margin-top:1.6rem">
      <div class="panelbox"><h3>O que estamos realmente vendendo</h3><p>Nossa principal oferta é o <b>Programa Fumaça 360</b>: metodologia de seleção e acasalamentos em um projeto supervisionado por profissionais habilitados. O software é a interface visível desse serviço e não substitui análises laboratoriais ou avaliação profissional.</p></div>
      <div class="panelbox"><h3>Promessa responsável</h3><p>Menos decisões no escuro: mais rastreabilidade, critérios explícitos e acompanhamento. Não prometemos nascimentos de cor específica nem valorização financeira sem validação.</p></div>
    </div>
  </div>
</section>
<dialog id="dlg" aria-labelledby="dlg-t">
  <h3 id="dlg-t"></h3>
  <p><b>Função técnica:</b> <span id="dlg-fn"></span></p>
  <p><b>Entrega:</b> <span id="dlg-ent"></span></p>
  <p><b>Para que serve na fazenda:</b> <span id="dlg-uso"></span></p>
  <p class="small muted">O que não entregamos: laudos de laboratório próprios nem promessa de resultado genético.</p>
  <form method="dialog"><button class="btn">Fechar</button> <a class="btn ghost" href="diagnostico.html">Iniciar diagnóstico</a></form>
</dialog>
"""
produtos_js = """<script>
(function () {
  var d = document.getElementById('dlg');
  document.querySelectorAll('[data-prod]').forEach(function (b) {
    b.addEventListener('click', function () {
      document.getElementById('dlg-t').textContent = b.dataset.prod;
      document.getElementById('dlg-fn').textContent = b.dataset.fn;
      document.getElementById('dlg-ent').textContent = b.dataset.ent;
      document.getElementById('dlg-uso').textContent = b.dataset.uso;
      if (d.showModal) d.showModal(); else d.setAttribute('open', '');
    });
  });
})();
</script>"""

# ------------------------------------------------------------------ JORNADA
jornada = """
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Jornada de implantação</p><h1>Da visita ao plano de <span class="accent">acasalamento</span>.</h1>
    <p class="lead">Cinco etapas, cada uma com uma entrega clara. Em 90 dias entregamos informação e planejamento. Resultados genéticos exigem gerações.</p></div>
    <ol class="timeline">
      <li><span class="when">Fase 1</span><h3>Diagnóstico</h3><p>Inventário Fumaça e convencional, pedigree, reprodução, manejo e fábrica de ração.</p><p class="muted"><b>A cliente recebe:</b> dossiê com prioridades.</p></li>
      <li><span class="when">Fase 2</span><h3>Mapeamento</h3><p>Amostras de DNA conforme o plano técnico; SNP e pedigree, e avaliação de marcadores pertinentes.</p><p class="muted"><b>A cliente recebe:</b> passaportes e mapa genético.</p></li>
      <li><span class="when">Fase 3</span><h3>Acasalamento</h3><p>Ranking de pares por mérito, pelagem de interesse, parentesco e risco.</p><p class="muted"><b>A cliente recebe:</b> matriz de seleção e alertas.</p></li>
      <li><span class="when">Fase 4</span><h3>Reprodução</h3><p>Monta controlada, IA, TE e FIV quando viável; calendário e acompanhamento.</p><p class="muted"><b>A cliente recebe:</b> plano e registros reprodutivos.</p></li>
      <li><span class="when">Fase 5</span><h3>Monitoramento</h3><p>Coleta de descendência, endogamia, reprodução, ganho e dieta.</p><p class="muted"><b>A cliente recebe:</b> painel e boletins periódicos.</p></li>
    </ol>
    <h2>Critério para avançar de fase</h2>
    <div class="tablewrap"><table><thead><tr><th>Porta de decisão</th><th>Evidência mínima para avançar</th></tr></thead><tbody>
      <tr><td>Diagnóstico → laboratório</td><td>Identificação dos animais, autorização, desenho de amostras e orçamento.</td></tr>
      <tr><td>Laboratório → acasalamentos</td><td>Qualidade dos laudos, genealogia e definição dos objetivos e limites técnicos.</td></tr>
      <tr><td>Acasalamentos → reprodução</td><td>Aprovação do zootecnista e do veterinário responsável, viabilidade e sanidade.</td></tr>
      <tr><td>Reprodução → avaliação</td><td>Registros de nascimentos e protocolo zootécnico comparável.</td></tr>
    </tbody></table></div>
    <h2>Cronograma honesto</h2>
    <div class="tablewrap"><table><thead><tr><th>Período</th><th>Ação principal</th><th>Marco</th></tr></thead><tbody>
      <tr><td>Dias 01 a 15</td><td>Reunião técnica, identificação do núcleo e visita.</td><td>Escopo, acesso a dados e cronograma validados.</td></tr>
      <tr><td>Dias 16 a 30</td><td>Inventário, pedigree, indicadores e amostragem.</td><td>Dossiê inicial e orçamento de análises.</td></tr>
      <tr><td>Dias 31 a 60</td><td>Testes contratados, integração e interpretação conforme prazos.</td><td>Mapa genético e revisão da herança da pelagem.</td></tr>
      <tr><td>Dias 61 a 90</td><td>Ranking de pares, planos reprodutivos e desenho do painel.</td><td>Plano aprovado e demonstração do Connect.</td></tr>
      <tr><td>Após 90 dias</td><td>Execução, reprodução e monitoramento.</td><td>Resultados biológicos registrados.</td></tr>
      <tr><td>Próximas gerações</td><td>Comparação de descendentes e seleção continuada.</td><td>Avaliação dos objetivos de linhagem.</td></tr>
    </tbody></table></div>
    <h2>Pacotes</h2>
    <p class="lead">Uma escada de contratação reduz a resistência e organiza a oferta.</p>
    <div class="grid g3">
      <article class="card"><span class="tag">Entrada</span><h3>Descoberta Genética</h3><p>Visita, inventário, análise de registros, plano de amostragem e diagnóstico.</p><p class="muted small">Entrada de baixo compromisso, com escopo definido.</p></article>
      <article class="card hl"><span class="tag">Oferta principal</span><h3>Fumaça 360</h3><p>Descoberta, mapeamento, Fumaça Match, plano reprodutivo e Connect.</p><p class="muted small">Oferta principal desta APS.</p></article>
      <article class="card"><span class="tag">Premium</span><h3>Fumaça 360 Signature</h3><p>Programa completo, avaliação nutricional ampliada e apoio ao posicionamento do plantel.</p><p class="muted small">Se houver viabilidade técnica e demanda.</p></article>
    </div>
    <div class="note gold"><b>Investimento sob proposta personalizada.</b> O valor final depende do número de animais, testes, visitas, mão de obra, insumos e biotecnologias escolhidas. Nenhum preço, retorno ou valorização é apresentado como resultado observado sem dados reais.</div>
    <p><a class="btn" href="diagnostico.html">Iniciar diagnóstico</a></p>
  </div>
</section>
"""

# ------------------------------------------------------------------ COMPARADOR
comparador = """
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Debate técnico</p><h1>Consanguinidade ou <span class="accent">heterose</span>?</h1>
    <p class="lead">Mexa nos números e veja o que cada caminho entrega. Esta página não esconde onde o cruzamento ganha: o argumento da Legado Genética aparece quando o objetivo da fazenda entra na conta.</p>
    <div class="note"><b>Leia antes de citar.</b> Valores com <span class="dag">†</span> vieram de resumos de artigos e ainda não foram conferidos no texto original. Os marcados com <span class="ver">‡</span> foram conferidos no texto completo. O preço é de mercado público, não da fazenda. Nada aqui é resultado observado em rebanho real.</div></div>

    <p class="eyebrow">Simulador</p>
    <h2>Quilos por bezerro ao longo dos anos</h2>
    <p class="lead">Compara um bezerro F1 (cruzamento, um ganho de nível) com um núcleo Nelore em seleção (ganho que acumula, menos o custo da endogamia).</p>
    <div class="sim">
      <form class="ctl" onsubmit="return false" aria-label="Premissas do simulador">
        <label class="field" for="touros"><span class="row"><span>Touros no núcleo</span><output id="o-touros"></output></span><input id="touros" type="range" min="3" max="60" step="1" value="20"></label>
        <label class="field" for="matrizes"><span class="row"><span>Matrizes no núcleo</span><output id="o-matrizes"></output></span><input id="matrizes" type="range" min="30" max="400" step="10" value="100"></label>
        <label class="field" for="ger"><span class="row"><span>Intervalo entre gerações</span><output id="o-ger"></output></span><input id="ger" type="range" min="3" max="7" step="0.5" value="4.5"></label>
        <label class="field" for="g"><span class="row"><span>Ganho genético por ano <span class="dag">†</span></span><output id="o-g"></output></span><input id="g" type="range" min="0.2" max="3.5" step="0.1" value="1"></label>
        <label class="field" for="coef">Custo da endogamia por 1% de F
          <select id="coef"><option value="0.38">0,38 kg (Nelore, Pereira 2015 ‡)</option><option value="0.44">0,44 kg (Burrow, corte †)</option><option value="1.33">1,33 kg (pior caso Nelore †)</option></select></label>
        <label class="field" for="f1">Ganho do bezerro F1 no desmame
          <select id="f1"><option value="12.2">+12,2 kg (heterose pura, PR †)</option><option value="18" selected>+18,0 kg (Embrapa, machos †)</option><option value="30.9">+30,9 kg (USP, inclui raça do touro †)</option></select></label>
        <label class="field" for="preco"><span class="row"><span>Bezerro de 7@ em MT (R$/kg) <span class="dag">†</span></span><output id="o-preco"></output></span><input id="preco" type="range" min="10" max="22" step="0.01" value="16.86"></label>
      </form>
      <div class="out">
        <div class="kpis">
          <div class="kpi k-gold"><b id="k-df">–</b><span>endogamia nova por geração (ΔF)</span></div>
          <div class="kpi k-gold"><b id="k-f10">–</b><span>F do núcleo em 10 anos</span></div>
          <div class="kpi k-clay"><b id="k-f1">–</b><span>ganho do F1 por bezerro</span></div>
          <div class="kpi k-moss"><b id="k-sel">–</b><span>ganho líquido do núcleo em 10 anos</span></div>
        </div>
        <div class="chart">
          <svg id="svg" viewBox="0 0 640 340" role="img" aria-label="Gráfico: ganho do F1 contra ganho líquido do núcleo selecionado, por ano"></svg>
          <div class="legend"><span><i style="background:var(--clay)"></i>Cruzamento F1 (nível, enquanto cruzar)</span><span><i style="background:var(--moss)"></i>Núcleo Nelore (seleção menos endogamia)</span><span><i style="background:var(--gold);height:2px"></i>Custo da endogamia</span></div>
        </div>
        <div class="read" id="read" aria-live="polite"></div>
      </div>
    </div>
  </div>
</section>

<section class="block" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">Placar por critério</p>
    <h2>A fazenda real, critério a critério</h2>
    <p class="lead">Grande fazenda Nelore em Mato Grosso, proprietária em São Paulo, preferência pelo Fumaça, Nelore convencional no plantel, fábrica de ração própria e zootecnista especializado. Rebanho, pedigree e produtividade ainda não são conhecidos.</p>
    <div class="tablewrap"><table style="min-width:44rem">
      <thead><tr><th>Critério</th><th>Consanguinidade planejada</th><th>Heterose</th><th>Ponto</th></tr></thead>
      <tbody>
        <tr><td>Objetivo: valorizar o Fumaça</td><td>Preserva e fixa a linhagem</td><td>Dilui o fenótipo na 1ª geração</td><td class="w-c">Consanguinidade</td></tr>
        <tr><td>Quilos no desmame, curto prazo</td><td>Perde 2 a 8 kg a F = 6,25% <span class="ver">‡</span><span class="dag">†</span></td><td>Ganha 12 a 31 kg <span class="dag">†</span></td><td class="w-h">Heterose</td></tr>
        <tr><td>Permanência do ganho</td><td>Herdável, soma geração a geração</td><td>Cai a cerca de 50% em F2 <span class="dag">†</span> e exige raças puras</td><td class="w-c">Consanguinidade</td></tr>
        <tr><td>Ambiente (calor, carrapato)</td><td>Nelore adaptado</td><td>Taurino: tristeza parasitária <span class="ver">‡</span> e mais consumo <span class="dag">†</span></td><td class="w-c">Consanguinidade</td></tr>
        <tr><td>Gestão à distância</td><td>Um sistema, exige dados e laudos</td><td>Duas ou mais raças, IATF, reposição</td><td class="w-t">Depende</td></tr>
        <tr><td>Risco biológico</td><td>Controlável com F e triagem; grave sem controle</td><td>Baixo</td><td class="w-h">Heterose</td></tr>
        <tr><td>Qualidade de carcaça</td><td>Sem ganho de heterose</td><td>Área de olho de lombo +25,65% e carne mais macia (Angus x Nelore) <span class="ver">‡</span></td><td class="w-h">Heterose</td></tr>
        <tr><td>Fábrica de ração</td><td>Mede GMD e CAR e seleciona eficiência</td><td>Cruzadas pedem dieta de maior consumo <span class="dag">†</span></td><td class="w-c">Leve: consanguinidade</td></tr>
        <tr><td>Mercado</td><td>Leilões de touros Nelore (média de R$ 13,8 mil <span class="dag">†</span>); ágio do Fumaça não encontrado</td><td>Bonificação existe, concentrada em castrados <span class="dag">†</span></td><td class="w-t">Indefinido</td></tr>
      </tbody></table></div>
    <div class="note gold">Placar: consanguinidade leva 4 critérios, heterose leva 3, e 2 ficam em aberto. O placar não é o argumento: os pesos mudam com o objetivo da cliente.</div>
  </div>
</section>

<section class="block" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">O ponto central</p>
    <h2>Por que cruzar acaba com o <span class="accent">Fumaça</span></h2>
    <p class="lead">Pelo modelo didático do dossiê, A é o alelo do Nelore convencional (dominante) e a é o alelo recessivo do Fumaça. É uma hipótese de aula, não uma prova de que a pelagem real dependa de um único gene.</p>
    <div class="grid g2" style="max-width:34rem">
      <label class="field" for="mae">Mãe<select id="mae"><option value="aa">aa (Fumaça)</option><option value="Aa">Aa (portadora)</option><option value="AA">AA (convencional)</option></select></label>
      <label class="field" for="pai">Pai<select id="pai"><option value="aa">aa (Fumaça)</option><option value="Aa">Aa (portador)</option><option value="AA" selected>AA (outra raça ou convencional)</option></select></label>
    </div>
    <div class="bars" id="bars" aria-live="polite" style="max-width:34rem"></div>
    <p id="gen-note" style="color:var(--soft);margin-top:.8rem"></p>
  </div>
</section>

<section class="block" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">Dados conferidos no texto completo</p>
    <h2>O que já está <span class="accent">verificado</span></h2>
    <div class="tablewrap"><table style="min-width:40rem"><thead><tr><th>Dado</th><th>Valor <span class="ver">‡</span></th><th>Fonte</th></tr></thead><tbody>
      <tr><td>Custo da endogamia no peso à desmama (210 d), por 1% de F</td><td>−0,38 kg (IC 95%: −0,40 a −0,36); materno −0,16 kg</td><td>Pereira et al. 2015, 892.199 Nelore (ABCZ/UFMT/Embrapa)</td></tr>
      <tr><td>Idade ao primeiro parto, por 1% de F</td><td>+1,43 dia (IC 95%: 1,27 a 1,60)</td><td>Pereira et al. 2015, 831.766 Nelore</td></tr>
      <tr><td>Peso ao sobreano e ganho desmama-sobreano, por 1% de F</td><td>−1,00 kg e −2,02 g/dia</td><td>Pereira et al. 2015</td></tr>
      <tr><td>F médio do Nelore do estudo</td><td>cerca de 3%; 96,71% dos animais endogâmicos, só 0,29% com F acima de 25%</td><td>Pereira et al. 2015</td></tr>
      <tr><td>Heterose individual no peso aos 270 dias, Marchigiana x Nelore</td><td>+16,2 ± 4,9 kg; Canchim x Nelore: −6,9 ± 6,8 kg (não significativa)</td><td>Alencar et al., Embrapa Pecuária Sudeste, 962 bezerros em MS</td></tr>
      <tr><td>Carcaça Angus x Nelore (55 novilhos)</td><td>Área de olho de lombo +25,65%; carne mais macia (força de cisalhamento −13,46%)</td><td>Teixeira et al. 2012, Embrapa/UFPel</td></tr>
      <tr><td>Tristeza parasitária</td><td>Limitante principalmente em rebanhos taurinos ou com alta porcentagem de sangue taurino</td><td>Embrapa, Circular Técnica 48</td></tr>
      <tr><td>Rebanho brasileiro</td><td>Cerca de 80% é zebu ou tem alguma mestiçagem de zebu</td><td>Alencar, Embrapa, "Cruzamento em gado de corte"</td></tr>
    </tbody></table></div>
    <p>Os demais números (por exemplo, o +30,9 kg do bezerro F1 da USP) ainda estão a conferir. A lista completa e os links estão em <a href="fontes.html">Fontes</a>, e o <a href="assets/docs/Legado_Genetica_Anexo_Analitico_Consanguinidade_x_Heterose.pdf">anexo analítico em PDF</a> traz o modelo de cálculo.</p>
  </div>
</section>

<section class="block" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">Recomendação</p>
    <h2>Consanguinidade como programa principal, heterose como apoio</h2>
    <div class="grid g3">
      <article class="card"><h3>Núcleo Fumaça</h3><p>Consanguinidade planejada, nunca cruzar. Pelo menos 20 touros por 100 matrizes como ponto de partida. F máximo e triagem de haplótipos deletérios definidos pelo geneticista.</p></article>
      <article class="card"><h3>Lote comercial</h3><p>Se o zootecnista aprovar, cruzamento industrial só aqui. Reposição de matrizes e adaptação ao cerrado entram na conta.</p></article>
      <article class="card"><h3>Quando a heterose vence</h3><p>Se o único objetivo for quilo de bezerro ou de boi no curto prazo. Nesse caso o programa entra só nas matrizes que geram as fêmeas.</p></article>
    </div>
    <p style="margin-top:1.2rem"><a class="btn" href="diagnostico.html">Fazer o diagnóstico da minha fazenda</a></p>
  </div>
</section>
"""

# ------------------------------------------------------------------ DIAGNÓSTICO
diagnostico = """
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Diagnóstico</p><h1>Qual estratégia de consanguinidade serve à sua <span class="accent">fazenda</span>?</h1>
    <p class="lead">Responda sobre o seu objetivo, o plantel e os dados que você tem. O diagnóstico aponta a melhor opção de consanguinidade planejada para esse perfil, calcula o risco de endogamia e diz o que falta coletar.</p>
    <div class="note">Triagem orientativa por regras do grupo. Não substitui a avaliação do zootecnista e do geneticista. Nenhum dado é enviado a ninguém: o resultado fica na sua tela, e você pode copiar ou baixar.</div></div>
    <div class="diag">
      <form id="diag-form" class="panelbox grid" style="gap:1rem" novalidate>
        <fieldset><legend>Objetivo principal</legend><div class="radios">
          <label><input type="radio" name="objetivo" value="fumaca" checked> Fixar e valorizar o Fumaça</label>
          <label><input type="radio" name="objetivo" value="reprodutores"> Formar e vender reprodutores</label>
          <label><input type="radio" name="objetivo" value="comercial"> Produzir bezerro ou boi gordo</label>
        </div></fieldset>
        <label class="field" for="matrizes">Matrizes no plantel<input id="matrizes" name="matrizes" type="number" inputmode="numeric" min="1" max="20000" value="120"></label>
        <label class="field" for="touros">Touros em uso por estação<input id="touros" name="touros" type="number" inputmode="numeric" min="1" max="500" value="6"></label>
        <label class="field" for="fumaca">Animais Fumaça no plantel<input id="fumaca" name="fumaca" type="number" inputmode="numeric" min="0" max="20000" value="25"><span class="hint">Classificação visual, ainda sem confirmação por DNA.</span></label>
        <label class="field" for="genealogia">Genealogia (pai e mãe)<select id="genealogia" name="genealogia"><option value="completa">Completa</option><option value="parcial" selected>Parcial</option><option value="nenhuma">Não há</option></select></label>
        <label class="field" for="genotipagem">Genotipagem<select id="genotipagem" name="genotipagem"><option value="sim">Sim</option><option value="parcial">Parcial</option><option value="nao" selected>Não</option></select></label>
        <label class="field" for="desempenho">Registros de peso e prenhez<select id="desempenho" name="desempenho"><option value="sim">Sim</option><option value="parcial" selected>Parcial</option><option value="nao">Não</option></select></label>
        <label class="field" for="racao">Fábrica de ração registra dieta e consumo por lote<select id="racao" name="racao"><option value="sim" selected>Sim</option><option value="nao">Não</option></select></label>
        <label class="field" for="fmedio">F médio já conhecido (%), se houver<input id="fmedio" name="fmedio" type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="Deixe em branco se não souber"></label>
        <div class="actions"><button class="btn" type="submit">Gerar diagnóstico</button><button class="btn ghost" type="button" id="b-example">Ver exemplo</button></div>
      </form>
      <div id="result" class="result" aria-live="polite">
        <div class="panelbox"><h3>O resultado aparece aqui</h3><p class="muted">Preencha o perfil e toque em "Gerar diagnóstico". Você recebe a estratégia indicada, o risco de endogamia, os alertas, o pacote sugerido e a lista do que falta coletar.</p></div>
      </div>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ LEGADO CONNECT
INV = [
    ("FUM-001", "Fumaça (classificação visual)", "Fêmea", "Matriz", "Em verificação", "Não realizada", "Validar pedigree e definir amostragem"),
    ("FUM-002", "Fumaça (classificação visual)", "Fêmea", "Matriz", "Registrado", "Amostra planejada", "Coletar amostra"),
    ("FUM-003", "Fumaça (classificação visual)", "Fêmea", "Novilha", "Em verificação", "Não realizada", "Validar pedigree"),
    ("FUM-004", "Fumaça (classificação visual)", "Macho", "Reprodutor", "Registrado", "Amostra planejada", "Exame andrológico e coleta"),
    ("FUM-005", "Fumaça (classificação visual)", "Fêmea", "Matriz", "Em verificação", "Não realizada", "Validar pedigree"),
    ("CONV-001", "Convencional", "Fêmea", "Matriz", "Registrado", "Não realizada", "Triagem no GeneBank"),
    ("CONV-002", "Convencional", "Macho", "Reprodutor", "Registrado", "Amostra planejada", "Avaliar como portador provável"),
    ("CONV-003", "Convencional", "Fêmea", "Matriz", "Em verificação", "Não realizada", "Validar pedigree"),
]
rows = "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in INV)
n = len(INV)
gen_ok = sum(1 for r in INV if r[4] == "Registrado")
geno_pl = sum(1 for r in INV if r[5] == "Amostra planejada")
connect = f"""
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Legado Connect</p><h1>A fazenda no <span class="accent">seu celular</span>.</h1>
    <p class="lead">Protótipo clicável do painel para a proprietária que acompanha a fazenda de São Paulo. Inventário, genética, reprodução, nutrição e visão executiva em um lugar.</p></div>
    <div class="sim-banner"><b>Dados simulados</b> Esta tela é uma demonstração. Não mostra laudos, autenticação nem integrações reais, e os animais abaixo são exemplos fictícios.</div>
    <div role="tablist" class="tabs" aria-label="Módulos do painel">
      <button role="tab" id="t1" aria-controls="p1" aria-selected="true">Inventário</button>
      <button role="tab" id="t2" aria-controls="p2" aria-selected="false">Genética</button>
      <button role="tab" id="t3" aria-controls="p3" aria-selected="false">Reprodução</button>
      <button role="tab" id="t4" aria-controls="p4" aria-selected="false">Nutrição</button>
      <button role="tab" id="t5" aria-controls="p5" aria-selected="false">Executivo</button>
    </div>

    <div role="tabpanel" id="p1" aria-labelledby="t1">
      <div class="kpis"><div class="kpi k-ink"><b>{n}</b><span>animais no exemplo</span></div><div class="kpi k-moss"><b>{gen_ok} de {n}</b><span>com genealogia registrada</span></div><div class="kpi k-gold"><b>{geno_pl} de {n}</b><span>com amostra de DNA planejada</span></div></div>
      <label class="field" for="filtro" style="max-width:22rem;margin-top:1rem">Filtrar<input id="filtro" type="search" placeholder="Digite um código, grupo ou ação"></label>
      <div class="tablewrap"><table id="inv" style="min-width:48rem"><thead><tr><th>ID</th><th>Grupo / pelagem</th><th>Sexo</th><th>Categoria</th><th>Pai e mãe</th><th>Genotipagem</th><th>Próxima ação</th></tr></thead><tbody>{rows}</tbody></table></div>
    </div>

    <div role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <h2>Passaporte genético <span class="accent">(exemplo)</span></h2>
      <div class="passport"><dl>
        <dt>Identificação</dt><dd>FUM-001 | fêmea | Nelore | cadastro fictício</dd>
        <dt>Pelagem registrada</dt><dd>Fumaça (classificação visual, não validada por DNA)</dd>
        <dt>Pai e mãe</dt><dd>Em verificação</dd>
        <dt>Genotipagem</dt><dd>Não realizada</dd>
        <dt>Parentesco genômico</dt><dd>Não calculável sem laudos</dd>
        <dt>DEPs e desempenho</dt><dd>Aguardando registros comparáveis</dd>
        <dt>Próxima ação</dt><dd>Validar pedigree e definir amostragem</dd>
      </dl></div>
      <h3 style="margin-top:1.4rem">Alertas de exemplo</h3>
      <ul><li>Sem cadastro validado, o sistema não recomenda acasalamento.</li><li>Sem genótipo confirmado, exibe probabilidade condicional e nunca certeza.</li><li>Com parentesco calculável, emite alerta para endogamia elevada, sem limite arbitrário universal.</li></ul>
    </div>

    <div role="tabpanel" id="p3" aria-labelledby="t3" hidden>
      <div class="tablewrap"><table><thead><tr><th>Matriz</th><th>Reprodutor</th><th>Hipótese de pelagem</th><th>Parentesco esperado</th><th>Decisão</th></tr></thead><tbody>
        <tr><td>FUM-001</td><td>REP-101</td><td>aa x aa</td><td>Dados pendentes</td><td><span class="chip warn">Revisar</span></td></tr>
        <tr><td>FUM-002</td><td>REP-102</td><td>aa x Aa</td><td>Dados pendentes</td><td><span class="chip warn">Revisar</span></td></tr>
        <tr><td>FUM-003</td><td>REP-103</td><td>Sem genótipo confirmado</td><td>Dados pendentes</td><td><span class="chip bad">Aguardar</span></td></tr>
      </tbody></table></div>
      <p class="muted">Calendário de protocolos, monta controlada, IA e TE/FIV só aparecem depois da aprovação do zootecnista e do veterinário.</p>
    </div>

    <div role="tabpanel" id="p4" aria-labelledby="t4" hidden>
      <div class="tablewrap"><table><thead><tr><th>Indicador</th><th>Como medir</th><th>Status</th></tr></thead><tbody>
        <tr><td>Ganho médio diário (GMD)</td><td>Pesagens padronizadas por período</td><td><span class="chip warn">A medir</span></td></tr>
        <tr><td>Consumo individual</td><td>Cochos eletrônicos ou mensuração individual confiável</td><td><span class="chip warn">A medir</span></td></tr>
        <tr><td>Consumo alimentar residual (CAR)</td><td>Consumo observado ajustado a manutenção e ganho</td><td><span class="chip warn">A medir</span></td></tr>
        <tr><td>Custo alimentar por kg de ganho</td><td>Custo da dieta e ganho por animal ou lote</td><td><span class="chip warn">A medir</span></td></tr>
      </tbody></table></div>
      <p class="muted">A fábrica própria é um diferencial operacional, mas não comprova sozinha a eficiência alimentar individual.</p>
    </div>

    <div role="tabpanel" id="p5" aria-labelledby="t5" hidden>
      <div class="grid g3">
        <article class="card"><h3>Decisões pendentes</h3><p>Validar pedigree dos animais Fumaça. Aprovar a amostragem para genotipagem. Definir o número de touros do núcleo.</p></article>
        <article class="card"><h3>Próximo marco</h3><p>Dias 31 a 60: testes contratados e mapa genético. Dias 61 a 90: plano de acasalamentos aprovado.</p></article>
        <article class="card"><h3>Relatório executivo</h3><p>Resumo da evolução, decisões pendentes e riscos, em linguagem simples para a proprietária.</p></article>
      </div>
    </div>
  </div>
</section>
"""

# ------------------------------------------------------------------ FONTES
fontes = """
<section class="block" style="padding-top:0">
  <div class="wrap">
    <div class="page-head"><p class="eyebrow">Fontes e limites</p><h1>De onde vêm os <span class="accent">números</span>.</h1>
    <p class="lead">Este site é uma simulação acadêmica. Cada dado de literatura aparece com um marcador de verificação, e o que ninguém encontrou aparece como lacuna.</p></div>
    <div class="grid g3">
      <article class="card"><span class="ver">‡ Conferido</span><p>Valor lido no texto completo da fonte.</p></article>
      <article class="card"><span class="dag">† A conferir</span><p>Valor visto só em resumo de busca. Abra a fonte antes de citar.</p></article>
      <article class="card"><span class="tag">Cálculo do grupo</span><p>Depende de premissas declaradas ao lado de cada tabela. Não é resultado observado na fazenda.</p></article>
    </div>
    <h2 style="margin-top:2rem">Documentos para download</h2>
    <ul>
      <li><a href="assets/docs/Legado_Genetica_Anexo_Analitico_Consanguinidade_x_Heterose.pdf">Anexo analítico: consanguinidade x heterose (PDF)</a></li>
      <li><a href="assets/docs/Legado_Genetica_Anexo_Analitico_Consanguinidade_x_Heterose.docx">Anexo analítico (Word, editável)</a></li>
    </ul>

    <h2 style="margin-top:2rem">Fontes conferidas <span class="ver">‡</span></h2>
    <ul>
      <li>Pereira, R. J. et al. (2015). Depressão por endogamia em características reprodutivas e de crescimento na raça Nelore. XI Simpósio Brasileiro de Melhoramento Animal. <a href="https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1029206/1/AVEK.pdf">Texto completo</a></li>
      <li>Alencar, M. M. et al. Estimativas de efeitos aditivos e heteróticos para peso à desmama de bezerros cruzados Canchim x Nelore e Marchigiana x Nelore. Embrapa Pecuária Sudeste. <a href="https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/42654/1/EstimativasEfeitosAditivosHeteroticos-OK.pdf">Texto completo</a></li>
      <li>Teixeira, B. B. M. et al. (2012). Influência da composição racial e da heterose sobre características da carcaça e da carne de novilhos puros e cruzados. IX SBMA. <a href="https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/936212/3/Teixeiraetal2012.pdf">Texto completo</a></li>
      <li>Embrapa. Circular Técnica 48, tristeza parasitária bovina. <a href="https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1113867/1/CirTec48.pdf">Texto completo</a></li>
      <li>Alencar, M. M. Cruzamento em gado de corte. Embrapa. <a href="https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/47823/1/id16989.pdf">Texto completo</a></li>
    </ul>

    <h2 style="margin-top:2rem">Fontes ainda a conferir <span class="dag">†</span></h2>
    <ul>
      <li>Burrow (1993), revisão de depressão endogâmica em gado de corte (−0,44 kg na desmama e −0,69 kg ao ano por 1% de F, via fichas técnicas).</li>
      <li>Leroy (2014), meta-análise de depressão endogâmica (−0,137% da média por 1% de F). <a href="https://hal.archives-ouvertes.fr/hal-01193843">Link</a></li>
      <li>Doekes et al. (2021), "How depressing is inbreeding?", Genes. <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8234567/">Link</a></li>
      <li>Mota et al. (2024), BMC Genomics 25:738, endogamia em Nelore fechado (até −1,33 kg por 1% de F_ROH). <a href="https://bmcgenomics.biomedcentral.com/articles/10.1186/s12864-024-10641-3">Link</a></li>
      <li>Santana Jr. et al. (2010), Livestock Science 131:212-217 (dano com F acima de 7 a 11%). <a href="https://doi.org/10.1016/j.livsci.2010.04.003">Link</a></li>
      <li>Oliveira et al. (2011), linha Lemgruber, Pesq. Agropec. Bras. 46. <a href="https://doi.org/10.1590/S1678-3921.pab2011.v46.9820">Link</a></li>
      <li>Haplótipos candidatos a letais em Nelore, Scientific Reports (2023). <a href="https://doi.org/10.1038/s41598-023-37586-z">Link</a></li>
      <li>Trigo et al. (2021), ASIP e pelagem em Nelore, Genet. Sel. Evol. 53:40. <a href="https://doi.org/10.1186/s12711-021-00633-2">Link</a></li>
      <li>Koger (1980) e Cundiff et al. (1994), via UF/IFAS (heterose em zebu x taurino). <a href="https://journals.flvc.org/edis/article/download/116132/114304/167171">Link</a></li>
      <li>Thrift, Hersom e Yelich (2017), BIF. <a href="https://www.bifconference.com/bif2017/proceedings/04B-thrift-hersom-yelich.pdf">Link</a></li>
      <li>Mangucci (2023), dissertação USP, bezerro F1 contra Nelore em MT, MS e GO (231,6 contra 200,7 kg). <a href="https://teses.usp.br/teses/disponiveis/10/10131/tde-27072023-125523/?lang=en">Link</a></li>
      <li>FAO, estratégias de melhoramento e taxa de endogamia. <a href="https://www.fao.org/4/x5538e/x5538e09.htm">Link</a></li>
      <li>Index ASBIA, Cepea/Esalq e Imea-MT (mercado e preços, 2026).</li>
    </ul>

    <h2 style="margin-top:2rem">Lacunas</h2>
    <ul>
      <li>Nenhuma fonte encontrou o termo "Nelore Fumaça": não há dado de mercado para essa pelagem.</li>
      <li>Modo de herança da pelagem escura: depende de ler o artigo completo de Trigo et al. (2021).</li>
      <li>Ágio atual do Angus, custo atual de genotipagem e percentual de heterose Nelore x Angus em fontes nacionais.</li>
      <li>Dados reais da fazenda (rebanho, pedigree, produtividade): só com a visita técnica.</li>
    </ul>
    <div class="note">Regra de credibilidade: nenhuma tabela de preços, retorno, valorização ou produtividade é apresentada como resultado observado na fazenda sem dados reais.</div>
  </div>
</section>
"""

PAGES = [
    ("index.html", "Legado Genética | Programa Fumaça 360", "Consanguinidade planejada e tecnologia genética para quem cria Nelore: o Programa Fumaça 360, em uma abertura com scroll.", home, True, ["story.js"], ""),
    ("produtos.html", "Produtos | Legado Genética", "Sete soluções integradas do Programa Fumaça 360: DNA, Match, GeneBank, NutriGen, Núcleo Elite, Connect e Selection.", produtos, False, [], produtos_js),
    ("jornada.html", "Jornada de implantação | Legado Genética", "Cinco fases, critérios de avanço, cronograma de 90 dias e pacotes do Programa Fumaça 360.", jornada, False, [], ""),
    ("consanguinidade-x-heterose.html", "Consanguinidade x Heterose | Legado Genética", "Simulador e placar que comparam consanguinidade planejada e heterose para uma grande fazenda Nelore, com fontes e marcadores de verificação.", comparador, False, ["comparador.js"], ""),
    ("diagnostico.html", "Diagnóstico de consanguinidade | Legado Genética", "Triagem que aponta a melhor opção de consanguinidade planejada para o perfil da sua fazenda, com risco de endogamia e próximos passos.", diagnostico, False, ["diagnostico.js"], ""),
    ("legado-connect.html", "Legado Connect | Legado Genética", "Protótipo clicável do painel Legado Connect, com dados simulados: inventário, genética, reprodução, nutrição e visão executiva.", connect, False, ["connect.js"], ""),
    ("fontes.html", "Fontes e limites | Legado Genética", "Fontes da literatura, o que foi conferido no texto completo, o que ainda falta e downloads do anexo analítico.", fontes, False, [], ""),
]

for name, title, desc, body, is_home, scripts, inline in PAGES:
    write(name, layout(name, title, desc, body, is_home, scripts, inline))

write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#14110a"/><text x="32" y="44" font-family="Georgia,serif" font-size="38" font-weight="700" font-style="italic" fill="#efb04a" text-anchor="middle">LG</text></svg>')
write("vercel.json", '{\n  "cleanUrls": false,\n  "headers": [\n    { "source": "/assets/(.*)", "headers": [ { "key": "Cache-Control", "value": "public, max-age=86400" } ] }\n  ]\n}\n')
write("robots.txt", "User-agent: *\nAllow: /\n")
print("ok:", ", ".join(p[0] for p in PAGES))
