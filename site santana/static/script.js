function abrirWhatsApp(title, link) {
    const texto = `Veja esta notícia do CIDADE JÁ NEWS: ${title}\n${link}`;
    const url = `https://wa.me/?text=${encodeURIComponent(texto)}`;
    window.open(url, '_blank', 'noopener,noreferrer');
}

function atualizarDataHora() {
    const dataElemento = document.getElementById('data-atual');
    const horaElemento = document.getElementById('hora-atual');

    if (!dataElemento || !horaElemento) {
        return;
    }

    const agora = new Date();
    const formatterData = new Intl.DateTimeFormat('pt-BR', {
        timeZone: 'America/Bahia',
        weekday: 'long',
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });

    const formatterHora = new Intl.DateTimeFormat('pt-BR', {
        timeZone: 'America/Bahia',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    });

    const partesData = formatterData.formatToParts(agora);
    const partesHora = formatterHora.formatToParts(agora);

    const dia = partesData.find((parte) => parte.type === 'day')?.value || '';
    const mes = partesData.find((parte) => parte.type === 'month')?.value || '';
    const ano = partesData.find((parte) => parte.type === 'year')?.value || '';
    let weekday = partesData.find((parte) => parte.type === 'weekday')?.value || '';
    const hora = partesHora.find((parte) => parte.type === 'hour')?.value || '';
    const minuto = partesHora.find((parte) => parte.type === 'minute')?.value || '';
    const segundo = partesHora.find((parte) => parte.type === 'second')?.value || '';

    if (weekday.toLowerCase() === 'sábado' || weekday.toLowerCase() === 'sabado') {
        weekday = 'sexta-feira';
    }

    const dataFormatada = `${weekday.charAt(0).toUpperCase()}${weekday.slice(1)}, ${dia} de ${mes} de ${ano}`;
    const horaFormatada = `${hora}:${minuto}:${segundo}`;

    dataElemento.textContent = dataFormatada;
    horaElemento.textContent = horaFormatada;
}

document.querySelectorAll('.botao-compartilhar').forEach((botao) => {
    botao.addEventListener('click', () => {
        const title = botao.dataset.title || 'Notícia do CIDADE JÁ NEWS';
        const link = botao.dataset.link || window.location.href;
        abrirWhatsApp(title, link);
    });
});

atualizarDataHora();
setInterval(atualizarDataHora, 1000);
