# MUGUI - Gestor Inteligente de Música

**MUGUI** es una aplicación de escritorio multiplataforma desarrollada en Python que proporciona herramientas integradas para músicos y estudiantes de música. La aplicación combina tres módulos principales: un afinador de guitarra automático, un metrónomo interactivo y un reproductor de música, todo en una única interfaz centralizada.

## Características Principales

### Afinador (Tuner)

El módulo de afinación proporciona una detección automática de frecuencias en tiempo real mediante análisis de señales de audio capturadas del micrófono del usuario. Sus características incluyen:

- Detección automática de frecuencias (rango: 30 Hz - 1318 Hz)
- Visualización de la desviación en centavos
- Indicador digital de nota musical y frecuencia
- Representación visual del diapasón de la guitarra
- Evaluación de la afinación en tiempo real

### Metrónomo

El metrónomo proporciona soporte temporal para práctica de música mediante pulsos de metrónomo sincronizados. Incluye:

- Control de velocidad (BPM): rango de 20 a 300 pulsaciones por minuto
- Configuración de compás (1 a 12 tiempos)
- Indicadores visuales de beats sincronizados
- Calibración manual mediante Tap Tempo
- Síntesis de sonido (sonidos diferenciados para primer pulso y pulsos restantes)

### Reproductor de Música

El reproductor integrado permite la gestión y reproducción de archivos de audio:

- Reproducción de archivos en formato MP3
- Gestión de playlist personalizada
- Control de volumen ajustable
- Barra de tiempo interactiva para navegación
- Información dinámica de pista (posición, duración, número de pista)

## Requisitos del Sistema

La aplicación requiere Python 3.13 o superior y las siguientes dependencias principales:

**Librerías de Sistema:**
- tkinter (incluido con Python)

**Librerías Externas:**
- pygame: Reproducción y síntesis de audio
- librosa: Análisis de procesamiento de señales y detección de pitch
- pyaudio: Captura de audio del micrófono
- numpy: Operaciones matemáticas y procesamiento de señales digitales
- mutagen: Lectura de metadatos de archivos de audio
- firebase-admin: Integración con base de datos en tiempo real

## Instalación

### Paso 1: Obtener el código fuente
```bash
git clone https://github.com/jolayac/Proyecto-POO-MUGUI.git
cd Proyecto-POO-MUGUI
```

### Paso 2: Crear un entorno virtual (recomendado)
```bash
python -m venv venv
```

**Activar el entorno virtual:**

En Windows:
```bash
venv\Scripts\activate
```

En Linux o macOS:
```bash
source venv/bin/activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configuración de Firebase (opcional)

Para utilizar las funcionalidades de autenticación y sincronización en línea:

1. Descargar el archivo de credenciales JSON desde la consola de Firebase
2. Definir las variables de entorno:

En Windows (PowerShell):
```bash
$env:FIREBASE_CREDENTIALS_JSON="ruta/a/credenciales.json"
$env:FIREBASE_DB_URL="https://tu-proyecto.firebaseio.com"
```

En Linux/macOS:
```bash
export FIREBASE_CREDENTIALS_JSON="ruta/a/credenciales.json"
export FIREBASE_DB_URL="https://tu-proyecto.firebaseio.com"
```

## Ejecución de la Aplicación

Para iniciar la aplicación, ejecute el siguiente comando desde el directorio raíz del proyecto:

```bash
python definitivo.py
```

La aplicación se iniciará con una pantalla de carga animada y posteriormente mostrará el módulo de afinación como interfaz principal predeterminada.

## Estructura del Proyecto

El proyecto organiza sus componentes siguiendo la arquitectura MVVM (Model-View-ViewModel):

```
Proyecto-POO-MUGUI/
├── definitivo.py                 # Punto de entrada de la aplicación
├── requirements.txt              # Especificación de dependencias
├── README.md                     # Documentación del proyecto
├── mvvm/                         # Directorio principal de la arquitectura MVVM
│   ├── Model/                    # Capa de lógica de negocio
│   │   ├── AudioProcessor.py    # Captura y procesamiento de audio
│   │   ├── PitchAnalyzer.py     # Análisis de pitch y detección de notas
│   │   ├── MetronomeModel.py    # Lógica del metrónomo
│   │   ├── Usuario.py           # Modelo de datos de usuario
│   │   ├── firebase_admin.py    # Gestión de conexión con Firebase
│   │   └── reproductorModel/
│   │       ├── reproductor.py   # Lógica de reproducción pygame
│   │       └── pista.py         # Modelo de pista de audio
│   ├── View/                     # Capa de presentación
│   │   ├── TunerGUI.py          # Interfaz gráfica del afinador
│   │   ├── metronomo.py         # Interfaz gráfica del metrónomo
│   │   ├── reproductorFrame.py  # Marco contenedor del reproductor
│   │   ├── splash_screen.py     # Pantalla de carga inicial
│   │   └── reproductorView/
│   │       ├── reproductorUI.py # Interfaz completa del reproductor
│   │       └── barra_de_tiempo.py # Control de barra de tiempo/posición
│   └── ViewModel/                # Capa de lógica de presentación
│       ├── TunerApp.py          # Coordinador del afinador
│       ├── MetronomeVM.py       # Coordinador del metrónomo
│       ├── reproductor_vm.py    # Coordinador del reproductor
│       ├── authentication_vm.py # Gestor de autenticación
│       └── usuario_vm.py        # Gestor de datos de usuario
├── sonidos/                      # Recursos de audio
│   ├── tic.wav                  # Sonido de pulso normal
│   └── tac.wav                  # Sonido de pulso acentuado
└── imagenes/                     # Recursos gráficos
    ├── icono.ico
    ├── logo.png
    ├── play.png
    ├── pausa.png
    └── [otros recursos visuales]
```

## Arquitectura MVVM (Model-View-ViewModel)

MUGUI implementa el patrón arquitectónico Model-View-ViewModel, que proporciona una separación clara de responsabilidades entre la lógica de negocio, la interfaz de usuario y la coordinación entre ambas.

**Componentes de la Arquitectura:**

- **Model**: Contiene la lógica de negocio pura. Incluye procesamiento de audio (AudioProcessor), detección de pitch (PitchAnalyzer), gestión de reproducción (Reproductor), y lógica del metrónomo (MetronomeModel).

- **View**: Capa de presentación responsable de renderizar la interfaz gráfica. Implementada usando Tkinter y presenta tres vistas principales: TunerGUI, MetronomeFrame y ReproductorFrame.

- **ViewModel**: Capa intermedia que coordina las actualizaciones entre Model y View. Maneja eventos del usuario, actualiza el Model según sea necesario, y notifica a la View sobre cambios en el estado.

**Flujo de Datos:**

```
Entrada de Usuario → View → ViewModel → Model
                                 ↓
                            Procesamiento
                                 ↓
                    Cambios de Estado (Callbacks)
                                 ↓
                    ViewModel → View (Actualización UI)
```

**Ventajas del Enfoque MVVM:**

- Código modular y mantenible
- Facilita pruebas unitarias de lógica sin dependencias de UI
- Permite reutilización de componentes
- Simplifica depuración y extensión futura

## Guía de Uso

### Cambiar entre módulos

Para cambiar de módulo (Afinador, Metrónomo, Reproductor):

1. Acceder al menú "Funciones" en la barra de menú superior
2. Seleccionar el módulo deseado
3. La interfaz se actualizará automáticamente

### Módulo de Afinación

**Procedimiento:**

1. Conectar un micrófono al equipo
2. Pulsar una cuerda de la guitarra
3. Observar la lectura de frecuencia en Hz
4. Observar la desviación en centavos
5. Ajustar la tensión de la cuerda hasta que la lectura esté en el rango verde (±10 centavos)

**Interpretación:**

- Verde: Nota correctamente afinada (dentro de ±10 cents)
- Amarillo: Ligeramente desafinada (±10-25 cents)
- Rojo: Significativamente desafinada (>25 cents)

### Módulo de Metrónomo

**Procedimiento:**

1. Establecer la velocidad en BPM (pulsaciones por minuto)
2. Seleccionar el compás deseado (número de tiempos)
3. Presionar el botón "INICIAR"
4. El metrónomo emitirá pulsos sincronizados
5. Presionar "DETENER" para pausar

**Calibración manual (Tap Tempo):**

1. Presionar el botón "TAP TEMPO" repetidamente al ritmo deseado
2. El sistema detectará automáticamente el BPM

### Módulo de Reproductor

**Procedimiento:**

1. Presionar el ícono de carpeta para abrir el explorador de archivos
2. Seleccionar uno o más archivos MP3
3. Los archivos se agregarán a la lista de reproducción
4. Presionar "Play" para iniciar la reproducción
5. Usar los botones de control:
   - Play/Pausa: Controlar reproducción
   - Siguiente: Ir a la siguiente pista
   - Anterior: Ir a la pista anterior
   - Volumen: Ajustar nivel de audio
6. Usar la barra de tiempo para navegar dentro de la pista

## Configuración Avanzada

### Seleccionar dispositivo de micrófono

Para usar un dispositivo de micrófono diferente al predeterminado:

1. Abrir el archivo `mvvm/Model/AudioProcessor.py`
2. Localizar la línea con `self.device_index = 0`
3. Cambiar el índice según el dispositivo deseado
4. Para listar dispositivos disponibles, ejecutar:

```bash
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(i, p.get_device_info_by_index(i)['name']) for i in range(p.get_device_count())]"
```

### Ajustar sensibilidad del micrófono

En el archivo `AudioProcessor.py`, buscar la constante `MIN_ENERGY`:

```python
self.MIN_ENERGY = 0.00004  # Aumentar para reducir sensibilidad
```

Valores más altos requieren más energía de audio para detectar señal.

### Modificar rango de frecuencias de afinación

En el archivo `PitchAnalyzer.py`, en el método `freq_to_note()`:

```python
fmin=30,    # Frecuencia mínima en Hz (actualmente guitarra baja)
fmax=1318,  # Frecuencia máxima en Hz (actualmente guitarra alta)
```

Estos valores definen el rango de detección de la aplicación.

## Tabla de Dependencias

| Librería | Versión Mínima | Propósito |
|----------|-----------------|----------|
| pygame | 2.6.1 | Reproducción y síntesis de audio |
| librosa | 0.10.0 | Análisis de señales y detección de pitch |
| pyaudio | 0.2.13 | Captura de audio del micrófono |
| numpy | 1.24 | Operaciones matemáticas y procesamiento digital de señales |
| mutagen | 1.46 | Lectura de metadatos de archivos MP3 |
| firebase-admin | 6.2 | Conexión con base de datos Firebase |

## Solución de Problemas

### Error: "No se pudo abrir el micrófono"

**Causa:** Permisos insuficientes o micrófono no disponible.

**Soluciones:**
- Verificar que el micrófono funcione en otros programas
- Ejecutar la aplicación con permisos de administrador
- Comprobar que el micrófono esté conectado
- Verificar la configuración de dispositivos de audio del sistema operativo

### Error: "ModuleNotFoundError: librosa"

**Causa:** Librería no instalada correctamente.

**Solución:**
```bash
pip install librosa --upgrade
```

### Problema: El audio del metrónomo se superpone con otro módulo

**Causa:** Las capas de audio no se detienen correctamente al cambiar de módulo.

**Soluciones:**
- Cambiar a otro módulo para detener el audio actual
- Reiniciar la aplicación
- Verificar que no haya múltiples instancias ejecutándose

### Problema: La barra de tiempo del reproductor no se mueve

**Causa:** El archivo no se cargó correctamente o está dañado.

**Soluciones:**
- Esperar a que el archivo se cargue completamente
- Seleccionar un archivo MP3 diferente
- Verificar que el archivo no esté corrompido
- Comprobar que el formato MP3 sea compatible

### Error: "No se puede conectar con Firebase"

**Causa:** Variables de entorno no configuradas o credenciales inválidas.

**Soluciones:**
- Verificar las variables de entorno
- Validar el archivo de credenciales JSON
- Comprobar la conexión a Internet
- Consultar la documentación de Firebase

## Contribución al Proyecto

Las contribuciones son bienvenidas. Para contribuir al proyecto, siga estos pasos:

1. Crear un fork del repositorio
2. Clonar el fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/Proyecto-POO-MUGUI.git
   ```
3. Crear una rama para la nueva funcionalidad:
   ```bash
   git checkout -b feature/MiNuevaFuncionalidad
   ```
4. Realizar cambios y commits descriptivos:
   ```bash
   git commit -m "Descripción clara del cambio"
   ```
5. Subir los cambios a la rama remota:
   ```bash
   git push origin feature/MiNuevaFuncionalidad
   ```
6. Abrir un Pull Request en el repositorio principal

**Directrices para contribuciones:**
- Seguir las convenciones de código existentes
- Incluir comentarios explicativos en código complejo
- Probar los cambios antes de enviar
- Escribir mensajes de commit claros y descriptivos

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulte el archivo LICENSE para más detalles.

## Información del Autor

**Desarrollador:** José Layac

**Repositorio:** https://github.com/jolayac/Proyecto-POO-MUGUI

## Contacto y Soporte

Para reportar errores, solicitar funcionalidades o enviar sugerencias, abra un ticket de issue en el repositorio:

https://github.com/jolayac/Proyecto-POO-MUGUI/issues

## Conceptos Técnicos Implementados

A lo largo del desarrollo de este proyecto se implementaron los siguientes conceptos de programación e ingeniería de software:

- Programación Orientada a Objetos (POO): Encapsulación, herencia y polimorfismo
- Patrones de Diseño: Implementación del patrón MVVM
- Procesamiento Digital de Señales: Análisis de FFT, detección de pitch, filtrado
- Programación Multi-thread: Hilos daemon, sincronización, gestión de recursos
- Interfaz Gráfica de Usuario: Tkinter, widgets personalizados, gestión de eventos
- Integración de Servicios Externos: Firebase para autenticación y base de datos
- Manejo de Excepciones: Gestión robusta de errores
- Reproducción de Multimedia: Síntesis de audio, control de reproducción

## Roadmap Futuro

Las siguientes características están planificadas para versiones futuras:

- Soporte para afinación de instrumentos adicionales (violín, bajo, viento-madera)
- Grabación y reproducción de loops de práctica
- Análisis armónico avanzado con visualización de espectro
- Sincronización con Digital Audio Workstations (DAWs)
- Aplicación móvil complementaria (iOS y Android)
- Análisis automático de ritmo y detección de swing
- Interfaz multiidioma (internacionalización)
- Exportación de análisis y reportes de práctica

---

**Última actualización:** Diciembre 2, 2025

Para soporte técnico o preguntas, contacte al autor o abra un issue en el repositorio.
