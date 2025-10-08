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

### 🚀 Cómo Usar (¡Súper Fácil!)

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

#### **Salarios Objetivo:**
- Mínimo: $30,000 USD
- Preferido: $60,000 USD  
- Objetivo: $100,000+ USD

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

### ⚙️ Configuración Incorporada

Todo está pre-configurado, pero puedes ajustar:
- Preferencias salariales
- Filtros de búsqueda (solo remotos, excluir agencias)
- Categorías de empleos
- Ubicaciones preferidas

### ⭐ Sistema de Puntuación Inteligente

El sistema ahora rankea empleos usando múltiples factores:

1. **🎯 Relevancia de Términos** (Nuevo):
   - Título del empleo: +3 puntos por término
   - Empresa: +2 puntos por término  
   - Descripción: +1 punto por término

2. **💰 Puntuación Salarial**:
   - $100K+: +50 puntos
   - $60K-$99K: +30 puntos
   - $30K-$59K: +10 puntos

3. **📍 Ubicación Preferida**:
   - Remote: +10 puntos
   - Colombia: +9 puntos
   - US/Canada/Europe: +8-6 puntos

**Resultado**: Empleos más relevantes aparecen primero

### 💡 Ejemplos de Resultados Reales

El sistema encuentra empleos como:
- **Python Developer Remote** - $80,000-$120,000
- **BIM Coordinator** - $65,000-$90,000  
- **Data Analyst Remote** - $70,000-$100,000
- **Scrum Master** - $90,000-$130,000

### 🔧 Dependencias

Necesitas:
- **Python 3.7+** 
- **requests** (para APIs)
- **Pillow** (para cargar el logo AGRDB)
- **tkinter** (incluido con Python)

```bash
pip install -r requirements.txt
```

### 🎨 Personalización AGRDB

La aplicación incluye:
- **Logo AGRDB** en el header principal
- **Pestaña "Acerca de"** con información completa
- **Footer personalizado** con enlace al desarrollador  
- **Enlaces directos** al repositorio GitHub y perfil
- **Información técnica** y de licencia

### ⚡ ¡Ventajas del Sistema AGRDB!

✅ **Marca personalizada**: Logo y branding AGRDB integrado
✅ **Profesional**: Información completa del desarrollador
✅ **Fácil distribución**: Un solo archivo para compartir
✅ **Sin configuraciones complejas**: Todo integrado
✅ **Portabilidad total**: Funciona en cualquier lugar
✅ **Menos errores**: No hay dependencias entre archivos
✅ **Mantenimiento simple**: Todo en un lugar
✅ **Enlaces directos**: Acceso rápido al repositorio y perfil

### 🎉 ¡Listo para usar!

1. Activa el entorno virtual
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta `python job_search_bim.py`
4. ¡Comienza a buscar empleos con estilo AGRDB!

**¡El sistema está completo, funcional y personalizado con marca AGRDB en un solo archivo!** 🚀

---

### 👨‍💻 Desarrollado por AGRDB
**Especialistas en Automatización y Desarrollo BIM**
- 🔗 **Repositorio**: [GitHub/AGRDB](https://github.com/AGRDB)
- 📧 **Contacto**: Soluciones tecnológicas para AEC
- 🎯 **Especialidad**: Python, Dynamo, APIs y Automatización BIM