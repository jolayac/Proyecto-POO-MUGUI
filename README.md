# Manual de Usuario - MUGUI

Esta aplicación te proporciona tres herramientas esenciales para practicar música:

- **Afinador** - Afina tu guitarra con precisión
- **Metrónomo** - Mantén el ritmo mientras practicas
- **Reproductor** - Escucha tu música favorita mientras practicas


## Primeros Pasos

### Instalación Rápida

1. **Descargar e instalar Python**
   - Asegúrate de tener Python 3.13 o superior
   - Descárgalo desde www.python.org

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar la aplicación**
   ```bash
   python definitivo.py
   ```


## Interfaz Principal

Una vez cargada la aplicación, verás la pantalla principal con tres elementos:

### Menú de Navegación

![alt text](image.png)

En la pantalla inicial tienes acceso a los tres módulos:
- **Afinador** - Abre el módulo de afinación
- **Metrónomo** - Abre el módulo de metrónomo
- **Reproductor** - Abre el módulo de reproductor

También puedes usar el menú superior:
- **Inicio** → Menú Principal (vuelve a esta pantalla)
- **Funciones** → Selecciona cualquier módulo
- **Cuenta** → Gestiona tu sesión de usuario (opcional)

---

## Módulo de Afinación (Tuner)

### ¿Cómo Funciona?

El afinador detecta automáticamente las notas que tocas en tu guitarra. Funciona analizando el sonido del micrófono en tiempo real.

### Requisitos

- Micrófono conectado al equipo
- Guitarra u otro instrumento para afinar
- Lugar sin ruido de fondo

### Cómo Usar

![alt text](image-1.png)


**Afina**
1. Toca una cuerda de tu guitarra
2. Mira la pantalla:
   - **Frecuencia (Hz)** - Número en la parte superior derecha
   - **Nota Musical** - La nota que está detectando (E, A, D, G, B, E)
   - **Desviación en cent** - Cuánto desafinada está la nota
      > Un **cent** es 1/100 de un semitono. Esto significa:
      >- ±5 cents es imperceptible al oído
      >- ±10 cents es una afinación buena
      >- ±20 cents comienza a sonar desafinado


**Paso 3: Ajusta la Tensión**
1. Si la nota está demasiado baja: aprieta la clavija (sube la afinación)
2. Si la nota está demasiado alta: afloja la clavija (baja la afinación)
3. Observa el cambio en tiempo real



### Notas Válidas para Guitarra

| Cuerda | Nota Estándar | Frecuencia (Hz) |
|--------|---------------|-----------------|
| 6 (más grave) | E (Mi) | ~82.4 |
| 5 | A (La) | ~110 |
| 4 | D (Re) | ~146.8 |
| 3 | G (Sol) | ~196 |
| 2 | B (Si) | ~246.9 |
| 1 (más aguda) | E (Mi) | ~329.6 |

---

## Módulo de Metrónomo

### ¿Cómo Funciona?

El metrónomo genera pulsos de audio sincronizados para ayudarte a mantener el ritmo mientras practicas.

### Cómo Usar

![alt text](image-2.png)

1. Presiona **INICIAR** para comenzar
2. El metrónomo emitirá sonidos de pulso
3. Practica manteniendo el ritmo
4. Presiona **PAUSA** para detener en cualquier momento

### Calibración Manual (Tap Tempo)

Si no sabes qué BPM usar, puedes calibrar el tempo:


1. Presiona **TAP** repetidamente al ritmo que deseas
2. El metrónomo detectará automáticamente el BPM
3. Mínimo 3 toques para calibrar




---

## 🎵 Módulo de Reproductor

### ¿Cómo Funciona?

El reproductor te permite escuchar archivos MP3 mientras practicas con el afinador o metrónomo.

### Requisitos

- Archivos en formato MP3
- Altavoces o auriculares conectados

### Cómo Usar

![alt text](image-3.png)

**Paso 1: Agregar Canciones**

1. Haz clic en el **botón de carpeta** (📁)
2. Se abrirá el explorador de archivos
3. Selecciona uno o más archivos MP3
4. Los archivos aparecerán en la lista


**Paso 2: Reproducir**

1. Haz clic en una canción de la lista para seleccionarla
2. Presiona  ▶ para comenzar
3. La canción se reproducirá en los altavoces






### Problema: "Los archivos MP3 no se cargan en el reproductor"

**¿Cuál es el problema?**
- No puedo agregar archivos o no se reproduce nada

**¿Cómo lo soluciono?**

1. **Verifica el formato:**
   - ¿Es un archivo MP3 válido?
   - Prueba con un MP3 diferente

2. **Verifica la ruta del archivo:**
   - Si la ruta tiene caracteres especiales, puede causar problemas
   - Intenta renombrar el archivo con caracteres simples

3. **Espera a que cargue:**
   - Los archivos grandes pueden tardar
   - Espera unos segundos

---

### Problema: "Error de módulo no encontrado"

**¿Cuál es el problema?**
```
ModuleNotFoundError: No module named 'pygame'
```

**¿Cómo lo soluciono?**

1. Reinstala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Si persiste, instala manualmente:
   ```bash
   pip install pygame librosa pyaudio numpy mutagen
   ```

---

### Problema: "La aplicación se congela"

**¿Cuál es el problema?**
- MUGUI no responde a los clics

**¿Cómo lo soluciono?**

1. **Espera un momento:**
   - A veces procesa audio en segundo plano
   - Espera 5-10 segundos

2. **Cambia de módulo:**
   - Abre el menú "Funciones"
   - Selecciona otro módulo
   - Vuelve al anterior

3. **Reinicia la aplicación:**
   - Presiona Ctrl+C en la terminal
   - Abre nuevamente

---
### Instalación Completa

**1. Clonar el repositorio:**
```bash
git clone https://github.com/jolayac/Proyecto-POO-MUGUI.git
cd Proyecto-POO-MUGUI
```

**3. Instalar dependencias:**
```bash
pip install -r requirements.txt
```

**4. Ejecutar:**
```bash
python definitivo.py
```

### Dependencias del Proyecto

| Librería | Función |
|----------|---------|
| **pygame** | Reproducción de audio y síntesis de sonidos |
| **librosa** | Análisis de FFT y detección de pitch |
| **pyaudio** | Captura de audio del micrófono |
| **numpy** | Procesamiento de señales digitales |
| **mutagen** | Lectura de metadatos de MP3 |
| **firebase-admin** | Base de datos y autenticación |

### Arquitectura del Proyecto

```
Proyecto-POO-MUGUI/
├── definitivo.py              # Punto de entrada
├── MainApp.py                 # Orquestador principal
├── mvvm/
│   ├── Model/                 # Lógica de negocio
│   │   ├── AudioProcessor.py
│   │   ├── PitchAnalyzer.py
│   │   ├── MetronomeModel.py
│   │   └── reproductorModel/
│   │       ├── reproductor.py
│   │       └── pista.py
│   ├── View/                  # Interfaz gráfica
│   │   ├── FrameManager.py
│   │   ├── MenuManager.py
│   │   ├── AuthenticationView.py
│   │   ├── TunerGUI.py
│   │   ├── metronomo.py
│   │   ├── reproductorFrame.py
│   │   └── reproductorView/
│   │       └── reproductorUI.py
│   └── ViewModel/             # Coordinación
│       ├── FrameNavigationViewModel.py
│       ├── MenuViewModel.py
│       ├── TunerApp.py
│       ├── MetronomeVM.py
│       └── reproductor_vm.py
├── sonidos/
│   ├── tic.wav
│   └── tac.wav
└── imagenes/
    └── [recursos gráficos]
```


### Configuración Avanzada

**Cambiar dispositivo de micrófono:**

1. Abre `mvvm/Model/AudioProcessor.py`
2. Busca `device_index = 0`
3. Cambia el número según tus dispositivos

**Listar dispositivos disponibles:**
```bash
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(i, p.get_device_info_by_index(i)['name']) for i in range(p.get_device_count())]"
```

**Ajustar sensibilidad de micrófono:**

En `AudioProcessor.py`, modifica:
```python
self.MIN_ENERGY = 0.00004  # Mayor valor = menos sensible
```

**Cambiar rango de detección:**

En `PitchAnalyzer.py`, modifica:
```python
fmin=30,     # Frecuencia mínima (Hz)
fmax=1318,   # Frecuencia máxima (Hz)
```

## Información de cuentas

Para manejar las opciones de inici de seción y registrar, se tiene que crear un archivo .env con las siguientes variables:
Para habilitar el inicio de sesión y registro de usuarios, debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
client_id=TU_CLIENT_ID
client_secret=TU_CLIENT_SECRET
```

**¿Cómo obtener estos datos?**
1. Ingresa a [Google Cloud Console](https://console.cloud.google.com/)
2. Desde tu proyecto (crea uno si aun no lo tienes), ve a "APIs y servicios" → "Credenciales"
3. Crea un nuevo ID de cliente OAuth 2.0 (tipo: aplicación de escritorio)
4. Copia el `client_id` y el `client_secret` que te proporciona Google
5. Pégalos en el archivo `.env` como se muestra arriba


Con esto podrás utilizar las funciones de inicio de sesión y registro en la aplicación.