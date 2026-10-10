/* Diagnóstico de consanguinidade planejada: triagem orientativa por regras.
   Não substitui avaliação de zootecnista e geneticista. Nada é enviado a ninguém. */
(function () {
  var form = document.getElementById('diag-form');
  if (!form) return;
  var out = document.getElementById('result');
  var nf = function (x, d) { return x.toFixed(d).replace('.', ','); };
  var lastText = '';

  var LABEL = {
    objetivo: { fumaca: 'Fixar e valorizar o Fumaça', reprodutores: 'Formar e vender reprodutores', comercial: 'Produzir bezerro ou boi gordo' },
    gen: { completa: 'Completa', parcial: 'Parcial', nenhuma: 'Não há' },
    geno: { sim: 'Sim', parcial: 'Parcial', nao: 'Não' },
    desemp: { sim: 'Sim', parcial: 'Parcial', nao: 'Não' },
    racao: { sim: 'Sim', nao: 'Não' }
  };

  function ne(m, f) { return 4 * m * f / (m + f); }
  function minSires(f, neMin) {
    if (4 * f <= neMin) return null;
    var m = Math.ceil(neMin * f / (4 * f - neMin));
    return m > Math.max(2, f / 2) ? null : m;
  }

  function read() {
    var d = new FormData(form);
    var num = function (k, def) { var v = parseFloat(String(d.get(k)).replace(',', '.')); return isFinite(v) ? v : def; };
    var fm = String(d.get('fmedio')).trim();
    return {
      objetivo: d.get('objetivo') || 'fumaca',
      f: Math.max(1, Math.round(num('matrizes', 100))),
      m: Math.max(1, Math.round(num('touros', 5))),
      fum: Math.max(0, Math.round(num('fumaca', 0))),
      gen: d.get('genealogia'), geno: d.get('genotipagem'), desemp: d.get('desempenho'), racao: d.get('racao'),
      fmedio: fm === '' ? null : parseFloat(fm.replace(',', '.'))
    };
  }

  function readiness(p) {
    var s = { completa: 40, parcial: 20, nenhuma: 0 }[p.gen] + { sim: 25, parcial: 12, nao: 0 }[p.geno] + { sim: 20, parcial: 10, nao: 0 }[p.desemp] + (p.racao === 'sim' ? 15 : 0);
    return s;
  }

  function strategy(p, rd, sires) {
    if (p.gen === 'nenhuma') return {
      id: 'E0', title: 'Etapa 0: inventário e validação do pedigree antes de acasalar com intenção', pack: 'Descoberta Genética',
      bullets: [
        'Sem genealogia, o parentesco entre os animais é desconhecido e a endogamia pode subir sem que ninguém perceba.',
        'Identificar cada animal e reconstruir pai e mãe pelo livro de monta, pelas inseminações e pelo registro de sêmen.',
        'Enquanto o parentesco for desconhecido, acasalar sem aproximação: touros distintos e sem repetir o mesmo touro na mesma família.',
        'Genotipar uma amostra para checar parentesco e abrir o mapa genético.'
      ] };
    if (p.objetivo === 'comercial') return {
      id: 'COM', title: 'Núcleo Fumaça com consanguinidade controlada e cruzamento só no lote comercial', pack: 'Descoberta Genética',
      bullets: [
        'Se o objetivo é quilo de bezerro ou de boi no curto prazo, o cruzamento (heterose) tende a render mais. Veja o comparador, que mostra isso sem esconder.',
        'Separar um núcleo pequeno com consanguinidade planejada para preservar o Fumaça e a base de matrizes Nelore.',
        'Cruzamento industrial apenas no lote comercial, com aprovação do zootecnista e plano para carrapato, calor e nutrição.',
        'Medir os dois lotes com as mesmas pesagens para comparar com dados da própria fazenda.'
      ] };
    if (p.fum < 15) return {
      id: 'BASE', title: 'Ampliar a base de fundadores do Fumaça antes de estreitar o núcleo', pack: 'Fumaça 360 (foco em mapeamento)',
      bullets: [
        'Com poucos animais Fumaça, consanguinidade intensa agora é arriscada: poucos fundadores fazem F subir rápido.',
        'Usar o GeneBank Nelore para procurar portadores entre os convencionais. O modo de herança da pelagem é hipótese e precisa de genotipagem.',
        'Formar ao menos 30 matrizes Fumaça ou portadoras, de famílias diferentes, com touros de linhagens distintas.',
        'Só depois aproximar parentes de forma planejada, com F da cria dentro da meta.'
      ] };
    if (p.fum < 40 || rd < 70 || p.gen === 'parcial') return {
      id: 'MOD', title: 'Linebreeding moderado, com F da cria limitado', pack: 'Fumaça 360',
      bullets: [
        'Acasalar com parentesco leve, com F da cria de até 6,25% (filho de primos de primeiro grau), para fixar famílias de interesse.',
        'Meta de ΔF abaixo de 1% por geração, com revisão de cada acasalamento no Fumaça Match.',
        sires ? 'Usar ao menos ' + sires + ' touros para as ' + p.f + ' matrizes, ou sêmen de touros não aparentados.' : 'Com este número de matrizes, usar inseminação com touros externos e não aparentados.',
        'Mapear antes de apertar: genotipar para medir F genômico e triar haplótipos deletérios.'
      ] };
    var sig = p.racao === 'sim' && p.desemp === 'sim' && p.objetivo === 'reprodutores';
    return {
      id: 'OPT', title: 'Consanguinidade planejada otimizada (Fumaça Match completo)', pack: sig ? 'Fumaça 360 Signature' : 'Fumaça 360',
      bullets: [
        'Há dados para acasalamento otimizado: minimizar o parentesco médio do núcleo e controlar ΔF a cada ciclo.',
        'Meta de ΔF abaixo de 0,5% por geração e F da cria de até 6,25%. Chegar a 12,5% só por exceção justificada e aprovada.',
        'Triagem de haplótipos deletérios e de portadores antes de cada estação de monta.',
        'Selecionar também por eficiência alimentar, usando os registros da fábrica de ração.'
      ] };
  }

  function render() {
    var p = read();
    var N = ne(p.m, p.f), dF = 1 / (2 * N);
    var F3 = 1 - Math.pow(1 - dF, 3), F5 = 1 - Math.pow(1 - dF, 5);
    var m1 = minSires(p.f, 50), m05 = minSires(p.f, 100);
    var rd = readiness(p);
    var rdLabel = rd >= 70 ? 'Alta' : rd >= 40 ? 'Média' : 'Baixa';
    var st = strategy(p, rd, m1);
    var risk = dF * 100 > 1 ? ['bad', 'Acima do limite'] : dF * 100 > 0.5 ? ['warn', 'Dentro de 1%'] : ['ok', 'Dentro de 0,5%'];
    var cost = function (F) { return [F * 0.38, F * 1.33]; };
    var c5 = cost(F5 * 100);

    var alerts = [];
    if (dF * 100 > 1) alerts.push(['bad', 'ΔF estimado de ' + nf(dF * 100, 2) + '% por geração, acima do limite de 1% (FAO†). ' + (m1 ? 'Subir para pelo menos ' + m1 + ' touros ou usar sêmen de touros não aparentados.' : 'Com ' + p.f + ' matrizes, touros próprios não bastam para segurar ΔF: usar inseminação com sêmen de touros externos e não aparentados, ou ampliar o plantel.')]);
    else if (dF * 100 > 0.5) alerts.push(['warn', 'ΔF de ' + nf(dF * 100, 2) + '% por geração está dentro de 1%, mas acima da meta ideal de 0,5%' + (m05 ? ' (' + m05 + ' touros).' : '.')]);
    else alerts.push(['ok', 'ΔF de ' + nf(dF * 100, 2) + '% por geração, dentro de 0,5%.']);
    if (p.fmedio !== null && !isNaN(p.fmedio)) {
      if (p.fmedio >= 12.5) alerts.push(['bad', 'F médio informado de ' + nf(p.fmedio, 1) + '%: pausar acasalamentos entre parentes até revisar o plano com o geneticista.']);
      else if (p.fmedio >= 7) alerts.push(['warn', 'F médio informado de ' + nf(p.fmedio, 1) + '%: já na faixa de 7 a 11% em que há perda de desempenho em Nelore†. Evitar novos acasalamentos entre parentes próximos.']);
      else alerts.push(['ok', 'F médio informado de ' + nf(p.fmedio, 1) + '%: sem alerta por este critério.']);
    }
    if (p.f < 30) alerts.push(['warn', 'Plantel pequeno (' + p.f + ' matrizes): o tamanho efetivo fica limitado a no máximo ' + 4 * p.f + '. Inseminação com touros externos ajuda a segurar F.']);
    if (p.objetivo === 'comercial') alerts.push(['warn', 'Objetivo comercial: em quilos de desmame no curto prazo, o cruzamento costuma superar a consanguinidade (veja o comparador).']);

    var todo = [];
    if (p.gen !== 'completa') todo.push('Completar a genealogia (pai e mãe) de todos os animais do núcleo.');
    if (p.geno !== 'sim') todo.push('Definir a amostra para genotipagem: reprodutores, matrizes Fumaça e portadores prováveis.');
    if (p.desemp !== 'sim') todo.push('Padronizar pesagens (nascimento, desmama, sobreano) e o diagnóstico de prenhez.');
    if (p.racao !== 'sim') todo.push('Registrar dieta e consumo por lote na fábrica de ração.');
    if (p.fum < 15) todo.push('Classificar e fotografar os animais Fumaça com o mesmo padrão.');
    if (!todo.length) todo.push('Dados completos: a próxima etapa é a visita técnica e a validação dos números com o zootecnista.');

    var chip = function (t, s) { return '<span class="chip ' + t + '">' + s + '</span>'; };
    var html = '' +
      '<div class="panelbox"><p class="eyebrow">Estratégia indicada</p><h3>' + st.title + '</h3><ul>' + st.bullets.map(function (b) { return '<li>' + b + '</li>'; }).join('') + '</ul>' +
      '<p style="margin-top:.8rem"><b>Pacote sugerido:</b> <span class="accent">' + st.pack + '</span></p></div>' +
      '<div class="kpis">' +
        '<div class="kpi k-gold"><b>' + nf(N, 0) + '</b><span>tamanho efetivo (Ne)</span></div>' +
        '<div class="kpi k-gold"><b>' + nf(dF * 100, 2) + '%</b><span>ΔF por geração ' + chip(risk[0], risk[1]) + '</span></div>' +
        '<div class="kpi k-clay"><b>' + nf(F5 * 100, 1) + '%</b><span>F do núcleo em 5 gerações</span></div>' +
        '<div class="kpi k-moss"><b>' + rdLabel + '</b><span>prontidão dos dados (' + rd + '/100)</span></div>' +
      '</div>' +
      '<div class="panelbox"><h3>Alertas</h3><ul>' + alerts.map(function (a) { return '<li>' + chip(a[0], a[0] === 'ok' ? 'ok' : a[0] === 'warn' ? 'atenção' : 'crítico') + ' ' + a[1] + '</li>'; }).join('') + '</ul></div>' +
      '<div class="panelbox"><h3>O que a endogamia custa nesta estratégia</h3><p>Com F de ' + nf(F5 * 100, 1) + '% após 5 gerações, a perda estimada no peso à desmama é de <b>' + nf(c5[0], 1) + ' a ' + nf(c5[1], 1) + ' kg por bezerro</b> (0,38 kg por 1% de F‡ até o pior caso de 1,33 kg†). Conta do grupo, não resultado observado na fazenda.</p>' +
      '<p class="small muted">Referências de limite: ΔF abaixo de 1% por geração (FAO†). Touros mínimos para esse limite com ' + p.f + ' matrizes: ' + (m1 || 'não alcançável só com touros') + '.</p></div>' +
      '<div class="panelbox"><h3>O que falta coletar</h3><ul>' + todo.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul></div>' +
      '<p class="small muted">Triagem orientativa por regras do grupo. Não substitui a avaliação do zootecnista e do geneticista, e nenhum dado foi enviado a ninguém. Valores com † são a conferir; com ‡, conferidos no texto completo.</p>' +
      '<div class="actions"><button class="btn" type="button" id="b-copy">Copiar resumo</button><button class="btn ghost" type="button" id="b-down">Baixar .txt</button><button class="btn ghost" type="button" id="b-print">Imprimir</button></div>';
    out.innerHTML = html;

    lastText = 'LEGADO GENÉTICA | DIAGNÓSTICO DE CONSANGUINIDADE PLANEJADA (simulação acadêmica)\n\n' +
      'Perfil: ' + LABEL.objetivo[p.objetivo] + ' | ' + p.f + ' matrizes | ' + p.m + ' touros | ' + p.fum + ' animais Fumaça\n' +
      'Genealogia: ' + LABEL.gen[p.gen] + ' | Genotipagem: ' + LABEL.geno[p.geno] + ' | Desempenho: ' + LABEL.desemp[p.desemp] + ' | Ração por lote: ' + LABEL.racao[p.racao] + '\n\n' +
      'ESTRATÉGIA: ' + st.title + '\n' + st.bullets.map(function (b) { return '- ' + b; }).join('\n') + '\nPacote sugerido: ' + st.pack + '\n\n' +
      'Ne = ' + nf(N, 0) + ' | ΔF = ' + nf(dF * 100, 2) + '% por geração | F em 5 gerações = ' + nf(F5 * 100, 1) + '% | Prontidão: ' + rdLabel + ' (' + rd + '/100)\n' +
      'ALERTAS:\n' + alerts.map(function (a) { return '- ' + a[1]; }).join('\n') + '\n\nO QUE FALTA:\n' + todo.map(function (t) { return '- ' + t; }).join('\n') +
      '\n\nTriagem orientativa. Não substitui avaliação profissional. Nenhum dado foi enviado.';

    var copy = document.getElementById('b-copy');
    copy.addEventListener('click', function () {
      var done = function () { copy.textContent = 'Copiado'; setTimeout(function () { copy.textContent = 'Copiar resumo'; }, 1800); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(lastText).then(done, function () { copy.textContent = 'Selecione e copie manualmente'; });
      else copy.textContent = 'Use o botão Baixar';
    });
    document.getElementById('b-down').addEventListener('click', function () {
      var url = URL.createObjectURL(new Blob([lastText], { type: 'text/plain;charset=utf-8' }));
      var a = document.createElement('a'); a.href = url; a.download = 'diagnostico-legado-genetica.txt'; a.click(); URL.revokeObjectURL(url);
    });
    document.getElementById('b-print').addEventListener('click', function () { window.print(); });
    out.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  form.addEventListener('submit', function (e) { e.preventDefault(); render(); });
  var ex = document.getElementById('b-example');
  if (ex) ex.addEventListener('click', function () { form.reset(); render(); });
})();
