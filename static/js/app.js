/**
 * Barbearia App - JavaScript Principal
 * Este arquivo contém todas as funcionalidades JavaScript do sistema
 */

// Aguarda o DOM estar completamente carregado
document.addEventListener('DOMContentLoaded', function() {
    console.log('Barbearia App carregado com sucesso!');
    
    // Inicializa todas as funcionalidades
    initApp();
});

/**
 * Inicializa todas as funcionalidades da aplicação
 */
function initApp() {
    // Inicializa tooltips do Bootstrap
    initTooltips();
    
    // Inicializa validações de formulários
    initFormValidations();
    
    // Inicializa máscaras de input
    initInputMasks();
    
    // Inicializa funcionalidades de agenda
    initAgendaFeatures();
    
    // Inicializa notificações
    initNotifications();
}

/**
 * Inicializa tooltips do Bootstrap
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Inicializa validações de formulários
 */
function initFormValidations() {
    // Validação de formulários com Bootstrap
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Inicializa máscaras de input
 */
function initInputMasks() {
    // Máscara para telefone
    const telefoneInputs = document.querySelectorAll('input[type="tel"], input[name*="telefone"]');
    telefoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = '(' + value;
                if (value.length > 3) {
                    value = value.substring(0, 3) + ') ' + value.substring(3);
                }
                if (value.length > 10) {
                    value = value.substring(0, 10) + '-' + value.substring(10);
                }
                if (value.length > 15) {
                    value = value.substring(0, 15);
                }
            }
            e.target.value = value;
        });
    });
    
    // Máscara para preço
    const precoInputs = document.querySelectorAll('input[name*="preco"]');
    precoInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                value = (parseInt(value) / 100).toFixed(2);
                value = value.replace('.', ',');
                value = 'R$ ' + value;
            }
            e.target.value = value;
        });
    });
}

/**
 * Inicializa funcionalidades de agenda
 */
function initAgendaFeatures() {
    // Seletores de data e hora
    const dataInputs = document.querySelectorAll('input[type="date"]');
    const horaInputs = document.querySelectorAll('input[type="time"]');
    
    // Define data mínima como hoje
    const hoje = new Date().toISOString().split('T')[0];
    dataInputs.forEach(input => {
        input.min = hoje;
    });
    
    // Define horários de funcionamento padrão
    horaInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const hora = e.target.value;
            const [horas, minutos] = hora.split(':');
            
            // Verifica se está dentro do horário comercial (8h às 18h)
            if (parseInt(horas) < 8 || parseInt(horas) >= 18) {
                showNotification('Horário deve estar entre 8h e 18h', 'warning');
                e.target.value = '';
            }
        });
    });
}

/**
 * Inicializa sistema de notificações
 */
function initNotifications() {
    // Cria container para notificações se não existir
    if (!document.getElementById('notification-container')) {
        const container = document.createElement('div');
        container.id = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(container);
    }
}

/**
 * Exibe uma notificação
 * @param {string} message - Mensagem da notificação
 * @param {string} type - Tipo da notificação (success, warning, error, info)
 * @param {number} duration - Duração em milissegundos (padrão: 5000)
 */
function showNotification(message, type = 'info', duration = 5000) {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    
    // Define classes baseadas no tipo
    const alertClass = `alert-${type === 'error' ? 'danger' : type}`;
    const iconClass = getIconForType(type);
    
    notification.className = `alert ${alertClass} alert-dismissible fade show`;
    notification.innerHTML = `
        <i class="${iconClass} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Adiciona à página
    container.appendChild(notification);
    
    // Remove automaticamente após o tempo definido
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
    
    // Remove ao clicar no X
    notification.querySelector('.btn-close').addEventListener('click', function() {
        notification.remove();
    });
}

/**
 * Retorna o ícone apropriado para cada tipo de notificação
 * @param {string} type - Tipo da notificação
 * @returns {string} Classe do ícone
 */
function getIconForType(type) {
    const icons = {
        'success': 'fas fa-check-circle',
        'warning': 'fas fa-exclamation-triangle',
        'error': 'fas fa-times-circle',
        'info': 'fas fa-info-circle'
    };
    return icons[type] || icons.info;
}

/**
 * Função para fazer requisições AJAX
 * @param {string} url - URL da requisição
 * @param {Object} options - Opções da requisição
 * @returns {Promise} Promise com a resposta
 */
async function makeRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        showNotification('Erro na comunicação com o servidor', 'error');
        throw error;
    }
}

/**
 * Função para verificar disponibilidade de horário
 * @param {Object} dados - Dados do agendamento
 * @returns {Promise<boolean>} True se disponível, False caso contrário
 */
async function verificarDisponibilidade(dados) {
    try {
        const response = await makeRequest('/verificar-disponibilidade', {
            method: 'POST',
            body: JSON.stringify(dados)
        });
        
        return response.disponivel;
    } catch (error) {
        return false;
    }
}

/**
 * Função para fazer agendamento
 * @param {Object} dados - Dados do agendamento
 * @returns {Promise<Object>} Resposta do agendamento
 */
async function fazerAgendamento(dados) {
    try {
        const response = await makeRequest('/agendar', {
            method: 'POST',
            body: JSON.stringify(dados)
        });
        
        if (response.success) {
            showNotification(response.message, 'success');
            return response;
        } else {
            showNotification('Erro ao fazer agendamento', 'error');
            return null;
        }
    } catch (error) {
        showNotification('Erro ao fazer agendamento', 'error');
        return null;
    }
}

/**
 * Função para formatar data e hora
 * @param {string} dataHora - String de data e hora
 * @param {string} formato - Formato desejado
 * @returns {string} Data formatada
 */
function formatarDataHora(dataHora, formato = 'dd/MM/yyyy HH:mm') {
    const data = new Date(dataHora);
    
    if (isNaN(data.getTime())) {
        return 'Data inválida';
    }
    
    const dia = String(data.getDate()).padStart(2, '0');
    const mes = String(data.getMonth() + 1).padStart(2, '0');
    const ano = data.getFullYear();
    const hora = String(data.getHours()).padStart(2, '0');
    const minuto = String(data.getMinutes()).padStart(2, '0');
    
    return formato
        .replace('dd', dia)
        .replace('MM', mes)
        .replace('yyyy', ano)
        .replace('HH', hora)
        .replace('mm', minuto);
}

/**
 * Função para formatar preço
 * @param {number} preco - Preço em centavos ou decimal
 * @returns {string} Preço formatado
 */
function formatarPreco(preco) {
    if (typeof preco === 'string') {
        preco = parseFloat(preco.replace(/[^\d,.-]/g, '').replace(',', '.'));
    }
    
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(preco);
}

/**
 * Função para confirmar ações
 * @param {string} mensagem - Mensagem de confirmação
 * @returns {boolean} True se confirmado, False caso contrário
 */
function confirmarAcao(mensagem = 'Tem certeza que deseja continuar?') {
    return confirm(mensagem);
}

/**
 * Função para mostrar/esconder elementos
 * @param {string} elementId - ID do elemento
 * @param {boolean} mostrar - True para mostrar, False para esconder
 */
function toggleElement(elementId, mostrar = true) {
    const element = document.getElementById(elementId);
    if (element) {
        element.style.display = mostrar ? 'block' : 'none';
    }
}

/**
 * Função para adicionar classe CSS
 * @param {string} elementId - ID do elemento
 * @param {string} className - Nome da classe CSS
 */
function addClass(elementId, className) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.add(className);
    }
}

/**
 * Função para remover classe CSS
 * @param {string} elementId - ID do elemento
 * @param {string} className - Nome da classe CSS
 */
function removeClass(elementId, className) {
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.remove(className);
    }
}

// Exporta funções para uso global (se necessário)
window.BarbeariaApp = {
    showNotification,
    makeRequest,
    verificarDisponibilidade,
    fazerAgendamento,
    formatarDataHora,
    formatarPreco,
    confirmarAcao,
    toggleElement,
    addClass,
    removeClass
};





