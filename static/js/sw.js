/**
 * Service Worker para Barbearia App
 * Este arquivo permite que o app funcione offline e seja instalável
 */

const CACHE_NAME = 'barbearia-app-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalação do Service Worker
self.addEventListener('install', function(event) {
    console.log('Service Worker instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Cache aberto');
                return cache.addAll(urlsToCache);
            })
            .then(function() {
                console.log('Todos os recursos foram cacheados');
                return self.skipWaiting();
            })
    );
});

// Ativação do Service Worker
self.addEventListener('activate', function(event) {
    console.log('Service Worker ativando...');
    
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(function() {
            console.log('Service Worker ativado');
            return self.clients.claim();
        })
    );
});

// Interceptação de requisições
self.addEventListener('fetch', function(event) {
    // Ignora requisições para APIs
    if (event.request.url.includes('/api/') || event.request.url.includes('/agendar') || event.request.url.includes('/verificar-disponibilidade')) {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Retorna do cache se disponível
                if (response) {
                    return response;
                }
                
                // Se não estiver no cache, busca da rede
                return fetch(event.request).then(function(response) {
                    // Verifica se a resposta é válida
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Clona a resposta para armazenar no cache
                    const responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                });
            })
            .catch(function() {
                // Se offline e não estiver no cache, retorna página offline
                if (event.request.destination === 'document') {
                    return caches.match('/offline.html');
                }
            })
    );
});

// Sincronização em background
self.addEventListener('sync', function(event) {
    console.log('Sincronização em background:', event.tag);
    
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

// Função para sincronização em background
function doBackgroundSync() {
    // Aqui você pode implementar sincronização de dados offline
    console.log('Executando sincronização em background...');
    
    // Exemplo: sincronizar agendamentos pendentes
    return Promise.resolve();
}

// Notificações push (para futuras implementações)
self.addEventListener('push', function(event) {
    console.log('Notificação push recebida:', event);
    
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/img/icon-192x192.png',
            badge: '/static/img/icon-72x72.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Ver Detalhes',
                    icon: '/static/img/icon-72x72.png'
                },
                {
                    action: 'close',
                    title: 'Fechar',
                    icon: '/static/img/icon-72x72.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Clique em notificação
self.addEventListener('notificationclick', function(event) {
    console.log('Notificação clicada:', event);
    
    event.notification.close();
    
    if (event.action === 'explore') {
        // Abre a aplicação
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Mensagens do cliente
self.addEventListener('message', function(event) {
    console.log('Mensagem recebida do cliente:', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Tratamento de erros
self.addEventListener('error', function(event) {
    console.error('Erro no Service Worker:', event.error);
});

// Tratamento de rejeições não tratadas
self.addEventListener('unhandledrejection', function(event) {
    console.error('Promise rejeitada não tratada:', event.reason);
});










