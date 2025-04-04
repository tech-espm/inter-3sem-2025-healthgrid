// Menu Mobile
const menuIcon = document.querySelector('.menu-icon');
const mainNav = document.querySelector('.main-nav');

menuIcon.addEventListener('click', () => {
    mainNav.classList.toggle('active');
});

// Fechar menu ao clicar fora
document.addEventListener('click', (e) => {
    if (!mainNav.contains(e.target) && !menuIcon.contains(e.target)) {
        mainNav.classList.remove('active');
    }
});

// Scroll suave para as seções
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            mainNav.classList.remove('active');
        }
    });
});

// Animação dos cards ao rolar
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.service-card, .team-member, .dashboard-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
});

// Atualização do Dashboard com dados reais
async function updateDashboardData() {
    try {
        const response = await fetch('http://localhost:5000/api/dashboard/data');
        const data = await response.json();

        if (data.success) {
            // Atualizar total de pacientes
            document.querySelector('#total-pacientes').textContent = data.total_pacientes;

            // Atualizar leitos ocupados
            document.querySelector('#leitos-ocupados').textContent = data.leitos_ocupados;

            // Atualizar tempo médio de espera
            const tempoMedio = data.tempo_medio;
            document.querySelector('#tempo-medio').textContent = 
                tempoMedio > 60 
                    ? `${Math.floor(tempoMedio / 60)}h ${tempoMedio % 60}min`
                    : `${tempoMedio}min`;

            // Atualizar gráfico de atendimentos
            updateAtendimentosChart(data.grafico_atendimentos);
        } else {
            console.error('Erro ao buscar dados:', data.error);
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
    }
}

function updateAtendimentosChart(dados) {
    const chart = document.querySelector('#atendimentos-chart');
    if (!chart) return;

    // Criar barras do gráfico
    const maxTotal = Math.max(...dados.map(d => d.total));
    const chartHtml = dados.map(d => {
        const altura = (d.total / maxTotal) * 100;
        return `
            <div class="chart-bar-container">
                <div class="chart-bar" style="height: ${altura}%"></div>
                <div class="chart-label">${d.hora}h</div>
                <div class="chart-value">${d.total}</div>
            </div>
        `;
    }).join('');

    chart.innerHTML = chartHtml;
}

// Atualizar dados a cada 30 segundos
setInterval(updateDashboardData, 30000);

// Efeito de hover nos botões de serviço
document.querySelectorAll('.service-btn').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
        btn.style.transform = 'translateY(-5px)';
        btn.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.15)';
    });
    
    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translateY(0)';
        btn.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
    });
});

// Header fixo com mudança de cor ao rolar
const header = document.querySelector('header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    // Apenas adiciona a classe scrolled para efeitos visuais
    if (currentScroll > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Carrossel de Serviços
const carousel = document.querySelector('.services-carousel');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
const cardWidth = 320; // Largura do card + gap

prevButton.addEventListener('click', () => {
    carousel.scrollBy({
        left: -cardWidth,
        behavior: 'smooth'
    });
});

nextButton.addEventListener('click', () => {
    carousel.scrollBy({
        left: cardWidth,
        behavior: 'smooth'
    });
});

// Atualizar visibilidade dos botões do carrossel
function updateCarouselButtons() {
    const isAtStart = carousel.scrollLeft === 0;
    const isAtEnd = carousel.scrollLeft >= (carousel.scrollWidth - carousel.clientWidth);
    
    prevButton.style.opacity = isAtStart ? '0.5' : '1';
    nextButton.style.opacity = isAtEnd ? '0.5' : '1';
    
    prevButton.style.pointerEvents = isAtStart ? 'none' : 'auto';
    nextButton.style.pointerEvents = isAtEnd ? 'none' : 'auto';
}

carousel.addEventListener('scroll', updateCarouselButtons);
updateCarouselButtons();

// Animação do heatmap
const heatmapBlocks = document.querySelectorAll('.heatmap-placeholder');
heatmapBlocks.forEach(block => {
    block.addEventListener('mouseenter', () => {
        block.style.transform = 'scale(1.05)';
        block.style.transition = 'transform 0.3s ease';
    });
    
    block.addEventListener('mouseleave', () => {
        block.style.transform = 'scale(1)';
    });
});

// Adicionar efeito de parallax suave nas imagens da equipe
document.querySelectorAll('.member-avatar img').forEach(img => {
    window.addEventListener('scroll', () => {
        const rect = img.getBoundingClientRect();
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.1;
        
        if (rect.top <= window.innerHeight && rect.bottom >= 0) {
            img.style.transform = `translateY(${rate}px)`;
        }
    });
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Atualizar dados iniciais do dashboard
    updateDashboardData();
    
    // Adicionar classe active ao link atual
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.main-nav a');
    
    window.addEventListener('scroll', () => {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (window.pageYOffset >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href').slice(1) === current) {
                link.classList.add('active');
            }
        });
    });
}); 