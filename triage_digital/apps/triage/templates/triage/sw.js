// Service Worker para Triage Digital
// Funcionalidad offline para emergencias médicas

const CACHE_NAME = 'triage-digital-v1';
const OFFLINE_URL = '/triage/';

// Archivos críticos para funcionamiento offline
const CRITICAL_FILES = [
  '/triage/',
  '/triage/triage-completo/',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.min.css'
];

// Instalar Service Worker
self.addEventListener('install', event => {
  console.log('🏥 Service Worker instalado - Triage Digital offline ready');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(CRITICAL_FILES))
      .then(() => self.skipWaiting())
  );
});

// Activar Service Worker
self.addEventListener('activate', event => {
  console.log('🚀 Service Worker activado - Sistema médico listo');
  event.waitUntil(self.clients.claim());
});

// Estrategia de cache: Network First para datos médicos críticos
self.addEventListener('fetch', event => {
  // Solo interceptar requests del mismo origen
  if (!event.request.url.startsWith(self.location.origin)) return;
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Si la respuesta es exitosa, guardar en cache
        if (response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME)
            .then(cache => cache.put(event.request, responseClone));
        }
        return response;
      })
      .catch(() => {
        // Si no hay red, usar cache
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            // Fallback a página principal para navegación
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});

// Notificación de actualización disponible
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});