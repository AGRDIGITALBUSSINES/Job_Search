# 🚀 Sistema de Búsqueda de Empleos - ¡TODO EN UN SOLO ARCHIVO!

## ✨ Sistema Completo Unificado con Interfaz Personalizada

**¡Ahora con logo AGRDB y sección completa "Acerca de"!** 

### 📁 ¿Qué contiene este folder?

- `job_search_bim.py` - **¡El sistema completo en un solo archivo!**
- `AGRDB_Logo.png` - **Logo oficial integrado en la interfaz**
- `.venv/` - Entorno virtual de Python
- `README.md` - Este archivo de instrucciones

### 🎯 Características del Sistema

- **🖥️ Interfaz gráfica moderna** con tkinter y logo AGRDB
- **📡 APIs reales integradas** (RemoteOK, The Muse) 
- **🔗 LinkedIn e Indeed automáticos** con URLs optimizadas
- **🏢 Sitios especializados** según la categoría del empleo
- **📤 Múltiples formatos de exportación** (JSON, CSV, XML, HTML, TXT)
- **⭐ Sistema de puntuación** y ranking automático
- **⚙️ Configuración personalizable** de salarios y filtros
- **ℹ️ Sección "Acerca de"** con información completa del desarrollador
- **👨‍💻 Footer personalizado** con enlace al perfil AGRDB

### 🚀 Cómo Usar (Para Desarrolladores)

```bash
# 1. Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependencias (incluye Pillow para el logo)
pip install -r requirements.txt

# 3. Ejecutar con interfaz gráfica (recomendado)
python job_search_bim.py

# 4. O en modo consola
python job_search_bim.py --console

# 5. Ver ayuda
python job_search_bim.py --help
```

### 🎮 Modos de Uso

#### 🖥️ **Modo Gráfico (Recomendado)**
```bash
python job_search_bim.py
```
- **Interfaz moderna con logo AGRDB**
- **4 pestañas completas**: Búsqueda, Exportación, Configuración, Acerca de
- Búsqueda visual con resultados
- Exportación con vista previa
- Configuración fácil
- **Información completa del desarrollador con enlaces**

#### 💻 **Modo Consola**
```bash
python job_search_bim.py --console
```
- Búsqueda completa automática
- Búsqueda por palabra clave
- Resultados en terminal

### 🔍 Qué Busca el Sistema

#### **🎯 Búsqueda Inteligente Combinada**
El sistema ahora combina categorías con palabras clave específicas para resultados más precisos:

**Ejemplo 1 - Búsqueda Completa + Filtro:**
- Categorías: ✅ Técnico/Ingeniería, ✅ Software/Tecnología  
- Filtro adicional: "remote"
- **Resultado**: Busca "BIM remote", "AutoCAD remote", "Python remote", "JavaScript remote", etc.

**Ejemplo 2 - Solo Palabra Clave:**
- Filtro adicional: "Senior React Developer"
- **Resultado**: Búsqueda específica solo para ese término

#### **Categorías Técnicas:**
- BIM, AutoCAD, Revit, GIS, ArcGIS
- Python, JavaScript, Software Engineer
- Data Analyst, Data Scientist
- Product Owner, Scrum Master

#### **Ubicaciones:**
- Remote (prioritario)
- Colombia, United States, Canada, Europe

### 📊 Tipos de Resultados

1. **🎯 Empleos Reales** (APIs públicas):
   - RemoteOK: Trabajos remotos con salarios
   - The Muse: Empresas establecidas
   - Datos completos: empresa, salario, descripción

2. **🔗 Enlaces de Búsqueda** (automáticos):
   - LinkedIn Jobs (remotos + ubicaciones)
   - Indeed (salarios + ubicaciones)
   - We Work Remotely
   - AngelList (startups)

### 📤 Exportación de Resultados

El sistema exporta en 5 formatos:
- **JSON**: Para análisis y programación
- **CSV**: Para Excel y hojas de cálculo
- **XML**: Para sistemas empresariales
- **HTML**: Reporte visual navegable
- **TXT**: Texto simple legible

### 🔧 Dependencias

Necesitas:
- **Python 3.7+** 
- **requests** (para APIs)
- **Pillow** (para cargar el logo AGRDB)
- **tkinter** (incluido con Python)

```bash
pip install -r requirements.txt
```



### 🎉 ¡Listo para usar!

1. Activa el entorno virtual
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta `python job_search_bim.py`
4. ¡Comienza a buscar empleos con estilo AGRDB!

### 📥 Descarga la Versión Ejecutable (v1.0.0 para Windows)

**¿No quieres instalar Python? ¡No hay problema!**

Descarga la versión ejecutable desde la sección de **Releases** de GitHub. Incluye todo lo necesario para ejecutar el programa con un solo clic.

- **[➡️ Descargar JobSearchBIM_AGRDB.exe (v1.0.0) ⬅️](https://github.com/AGRDIGITALBUSSINES/Job_Search/releases/download/v1.0.0/JobSearchBIM_AGRDB.exe)**

**Instrucciones:**
1.  Descarga el archivo `JobSearchBIM_AGRDB.exe` usando el enlace anterior.
2.  **Opcional:** Para que el logo se muestre correctamente, descarga también el archivo `AGRDB_Logo.png` desde la misma página de la release y colócalo en la misma carpeta que el `.exe`.
3.  ¡Ejecuta el archivo `.exe` y listo!

Para ver otras versiones o descargar los archivos fuente, visita la [**página de Releases del proyecto**](https://github.com/AGRDIGITALBUSSINES/Job_Search/releases).

---

### 👨‍💻 Desarrollado por AGRDB
**Especialistas en Automatización y Desarrollo BIM**
- 🔗 **Repositorio**: [GitHub/AGRDB](https://github.com/AGRDB)
- 📧 **Contacto**: Soluciones tecnológicas para AEC
- 🎯 **Especialidad**: Python, Dynamo, APIs y Automatización BIM