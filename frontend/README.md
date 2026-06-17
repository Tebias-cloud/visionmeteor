# VisionMeteor - Frontend (Dashboard Avanzado)

## 🖥️ Descripción General
El frontend de VisionMeteor es una interfaz de usuario interactiva y moderna construida para el monitoreo, ingesta y visualización de datos satelitales meteorológicos. Está diseñado para ofrecer una Experiencia de Usuario (UX) de nivel "Enterprise" y de alta fidelidad, orientada a operadores e ingenieros.

## 🛠️ Stack Tecnológico
*   **Framework:** Next.js 14+ (App Router).
*   **Lenguaje:** TypeScript (Tipado estático robusto).
*   **Estilos:** Tailwind CSS (Arquitectura de utilidades).
*   **Iconografía:** SVGs en línea minimalistas optimizados.
*   **Diseño UX/UI:** Adopción de filosofías "Glassmorphism" sutil y esquemas de color "Slate/Cyan" oscuros adaptados para entornos de centro de comando.

## 🧩 Componentes Arquitectónicos
*   `page.tsx`: Layout principal. Consume el API de FastAPI mediante `fetch` de forma asíncrona y orquesta el flujo de estado global de la aplicación (estado de carga, errores de conexión, renderizado de resultados).
*   `MetricCard.tsx`: Módulo reutilizable de métricas KPI. Diseñado con bordes simétricos y manejo de estados críticos (ej. borde y sombra roja reactiva si se detecta Nivel de Amenaza ALTA).
*   `Uploader.tsx`: Interfaz de ingesta de datos. Emplea un diseño de *"Dropzone"* intuitivo y realiza peticiones POST `multipart/form-data` al backend para inyectar imágenes al pipeline de Python en milisegundos.

## ✨ Funcionalidades Enterprise Destacadas
1.  **Visor Multipanel Dinámico:** Panel inferior inteligente con pestañas Reactivas que permite a los operadores alternar instantáneamente entre la *"Comparación del Modelo ML"* y el *"Mapa de Calor Térmico (Falso Color INFERNO)"* sin latencia ni recarga.
2.  **Reportabilidad Instantánea:** Generación de un botón interactivo (Glassmorphism effect) que detecta cuando el Backend genera un nuevo PDF y permite descargarlo inmediatamente a nivel de navegador.
3.  **Resiliencia Frontend:** Implementación de manejo de errores en promesas `fetch()`. Si el backend experimenta una excepción no manejada (o si FastAPI está inactivo), la UI de Next.js detendrá la carga y mostrará las alertas del error limpio sin colapsar el árbol de renderizado de React.

## 🚀 Despliegue y Desarrollo
El proyecto utiliza Node.js y NPM.

**Instalación:**
```bash
npm install
```

**Ejecución en Entorno Local:**
```bash
npm run dev
```

**Construcción para Producción:**
```bash
npm run build
npm start
```
El frontend se expone por defecto en `http://localhost:3000`.
