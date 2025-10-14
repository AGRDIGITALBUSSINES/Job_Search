#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 SISTEMA DE BÚSQUEDA DE EMPLEOS BIM/GIS - ÚLTIMAS VACANTES
Optimizado para encontrar las ofertas MÁS RECIENTES

Funcionalidades:
- ✅ Interfaz gráfica moderna
- ✅ APIs públicas integradas (RemoteOK, The Muse) con filtro de fechas
- ✅ LinkedIn e Indeed automáticos - ÚLTIMAS 72 HORAS
- ✅ Sitios especializados BIM/GIS/Colombia - ÚLTIMOS 3 DÍAS
- ✅ Exportación múltiples formatos
- ✅ Configuración personalizable

🎯 ENFOQUE: Búsquedas optimizadas para las vacantes más recientes
- LinkedIn: Últimas 72 horas (f_TPR=r259200)
- Indeed: Últimos 3 días (fromage=3)
- APIs: Filtro automático por fecha de publicación

Uso: python job_search_bim.py
"""

import sys
import os
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote_plus
import threading
import webbrowser

# Dependencias externas
PIL_AVAILABLE = False
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    print("✅ tkinter importado correctamente")
except ImportError as e:
    print(f"❌ Error con tkinter: {e}")
    sys.exit(1)

try:
    import requests
    print("✅ requests importado correctamente")
except ImportError as e:
    print(f"❌ Error: Falta dependencia requests")
    print("📦 Instala con: pip install requests")
    sys.exit(1)

# Intentar importar PIL (opcional para el logo)
try:
    from PIL import Image, ImageTk  # type: ignore
    PIL_AVAILABLE = True
    print("✅ PIL/Pillow disponible - Logo habilitado")
except ImportError:
    print("⚠️ PIL/Pillow no disponible - Logo deshabilitado")
    print("📦 Para habilitar logo: pip install Pillow")
    PIL_AVAILABLE = False

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

# Categorías de empleos optimizadas para perfil BIM/GIS - AMPLIADO Y OPTIMIZADO
JOB_CATEGORIES = {
    "BIM Especialista": [
        # BIM Core
        "BIM Coordinator", "BIM Manager", "BIM Specialist", "Building Information Modeling", 
        "BIM Modeler", "BIM Engineer", "BIM Consultant", "Digital Construction",
        # BIM Avanzado
        "BIM Director", "BIM Lead", "BIM Analyst", "BIM Technician", "BIM Administrator",
        "Virtual Design Construction", "VDC Engineer", "VDC Coordinator", "VDC Manager",
        # BIM Software Específico
        "Revit Specialist", "Revit Developer", "Bentley MicroStation", "ArchiCAD Specialist",
        "BIM 360 Coordinator", "Autodesk Construction Cloud", "BIM Collaboration",
        # Roles Emergentes
        "Digital Twin Specialist", "Smart Building Consultant", "Construction Technology"
    ],
    
    "Software CAD/GIS": [
        # CAD Software
        "Revit", "AutoCAD Civil 3D", "AutoCAD", "MicroStation", "Tekla", "Navisworks", 
        "Infraworks", "Civil 3D", "Plant 3D", "Inventor", "SolidWorks", "CATIA",
        # GIS Software
        "ArcGIS", "QGIS", "GIS Analyst", "GIS Specialist", "GIS Developer", "GIS Coordinator",
        "MapInfo", "PostGIS", "FME", "ArcGIS Enterprise", "ArcGIS Online", "ESRI",
        # Roles Profesionales
        "CAD Designer", "CAD Technician", "CAD Manager", "CAD Coordinator",
        "Civil Engineer", "Structural Engineer", "Architect", "MEP Engineer",
        "Surveyor", "Cartographer", "Remote Sensing Specialist", "Geospatial Analyst",
        # Software Especializado
        "SketchUp", "3ds Max", "Rhino", "Grasshopper", "Bentley STAAD", "SAP2000",
        "ETABS", "Robot Structural Analysis", "Advance Steel"
    ],
    
    "Automatización/Desarrollo": [
        # Lenguajes de Programación
        "Python Developer", "Python Engineer", "C# Developer", ".NET Developer",
        "JavaScript Developer", "Java Developer", "C++ Developer", "VBA Programming",
        # Automatización BIM/CAD
        "Dynamo", "Dynamo Developer", "Grasshopper Developer", "Revit API",
        "AutoCAD LISP", "VBA Excel", "Revit Add-in Developer", "BIM Programming",
        # Roles de Desarrollo
        "Software Engineer", "Software Developer", "Programming", "API Development",
        "Automation Engineer", "DevOps Engineer", "Full Stack Developer",
        "Frontend Developer", "Backend Developer", "Mobile Developer",
        # Tecnologías Emergentes
        "Machine Learning Engineer", "AI Developer", "Data Engineer", "Cloud Engineer",
        "Azure Developer", "AWS Developer", "Docker", "Kubernetes", "Git"
    ],
    
    "Infraestructura/Construcción": [
        # Gestión de Proyectos
        "Project Manager", "Construction Manager", "Program Manager", "PMO",
        "Project Coordinator", "Site Manager", "Construction Supervisor",
        # Ingeniería Civil
        "Civil Engineer", "Civil Engineering", "Infrastructure Engineer",
        "Transportation Engineer", "Water Resources Engineer", "Geotechnical Engineer",
        "Environmental Engineer", "Hydraulic Engineer", "Traffic Engineer",
        # Construcción y Tecnología
        "Construction Technology", "Digital Construction", "Construction Tech",
        "Building Technology", "Construction Innovation", "Prefab Construction",
        # Ciudades Inteligentes
        "Smart Cities", "Digital Twins", "IoT Engineer", "Smart Infrastructure",
        "Urban Planning", "City Planning", "Infrastructure Planning",
        # Sostenibilidad
        "Sustainability Consultant", "Green Building", "LEED", "BREEAM",
        "Energy Efficiency", "Carbon Footprint", "Renewable Energy"
    ],
    
    "Datos/Visualización": [
        # Análisis de Datos
        "Data Analyst", "Data Scientist", "Business Analyst", "Business Intelligence",
        "Data Engineer", "Analytics Engineer", "Reporting Analyst",
        # Herramientas de Visualización
        "Power BI", "Power BI Developer", "Tableau", "Tableau Developer",
        "Data Visualization", "Dashboard Developer", "Excel Expert",
        "SQL Developer", "Database Analyst", "ETL Developer",
        # GIS y Datos Espaciales
        "GIS Analyst", "Spatial Data Analyst", "Geographic Information Systems",
        "Spatial Data", "Geospatial Data", "Remote Sensing", "GPS Specialist",
        # Tecnologías de Datos
        "SQL Server", "Oracle", "PostgreSQL", "MySQL", "MongoDB", "BigQuery",
        "Snowflake", "Azure SQL", "AWS RDS", "Data Warehouse", "Data Lake"
    ],
    
    "Arquitectura/Diseño": [
        # Roles de Arquitectura
        "Architect", "Senior Architect", "Project Architect", "Design Architect",
        "Technical Architect", "Architectural Designer", "Architecture Consultant",
        # Especialidades Arquitectónicas
        "Landscape Architect", "Interior Designer", "Urban Designer",
        "Facade Engineer", "Building Envelope", "Acoustic Consultant",
        # Diseño y Modelado 3D
        "3D Modeler", "3D Designer", "Visualization Specialist", "Rendering Artist",
        "Architectural Visualization", "3D Artist", "Virtual Reality Developer",
        # Software de Diseño
        "SketchUp Specialist", "3ds Max Artist", "V-Ray Artist", "Lumion",
        "Enscape", "Twinmotion", "Unreal Engine", "Unity Developer"
    ],
    
    "Gestión/Consultoría": [
        # Consultoría Técnica
        "Technical Consultant", "BIM Consultant", "Technology Consultant",
        "Digital Transformation", "Process Improvement", "Change Management",
        # Gestión de Activos
        "Asset Management", "Facility Manager", "CAFM Specialist", "CMMS",
        "Building Operations", "Property Management", "Real Estate Technology",
        # Liderazgo Técnico
        "Technical Lead", "Team Lead", "Department Manager", "CTO",
        "Innovation Manager", "Digital Strategy", "Technology Director",
        # Ventas Técnicas
        "Technical Sales", "Pre-Sales Engineer", "Solution Architect", "Sales Engineer"
    ],
    
    "Tecnologías Emergentes": [
        # Realidad Virtual/Aumentada
        "VR Developer", "AR Developer", "Mixed Reality", "Virtual Reality",
        "Augmented Reality", "HoloLens Developer", "Immersive Technology",
        # Inteligencia Artificial
        "AI Engineer", "Machine Learning", "Computer Vision", "Natural Language Processing",
        "Deep Learning", "Neural Networks", "AI Consultant", "ML Engineer",
        # IoT y Sensores
        "IoT Developer", "IoT Engineer", "Sensor Technology", "Smart Sensors",
        "Industrial IoT", "Building Automation", "Smart Building Technology",
        # Blockchain y Web3
        "Blockchain Developer", "Smart Contracts", "Web3 Developer", "DeFi",
        # Robótica y Automatización
        "Robotics Engineer", "Automation Specialist", "RPA Developer", "Drone Technology"
    ]
}

# Preferencias salariales (USD) - Optimizado para mercado global/remoto 2025
SALARY_PREFERENCES = {
    "minimum_usd": 30000,     # ~$2,500 USD/mes - Competitivo para Colombia
    "preferred_usd": 55000,   # ~$4,580 USD/mes - Muy bueno para LATAM/remoto
    "target_usd": 85000       # ~$7,080 USD/mes - Excelente para remoto global
}

# Ubicaciones preferidas (Optimizado para búsqueda global)
PREFERRED_LOCATIONS = [
    # Remoto y Global
    "Remote", "Work from Home", "WFH", "Telecommute", "Virtual", "Distributed",
    # Colombia y LATAM
    "Colombia", "Bogotá", "Bogota", "Medellín", "Medellin", "Cali", "Barranquilla",
    "Mexico", "Chile", "Argentina", "Peru", "Ecuador", "Costa Rica", "Panama",
    "Latinoamérica", "Latin America", "LATAM", "Spanish Speaking",
    # Mercados Principales
    "United States", "USA", "Canada", "United Kingdom", "UK", "Europe", "EU",
    "Australia", "New Zealand", "Germany", "Netherlands", "Spain", "Portugal",
    # Mercados Emergentes Tech
    "Singapore", "Dubai", "Israel", "Ireland", "Switzerland", "Denmark", "Sweden"
]

# APIs habilitadas - Ampliado
ENABLED_APIS = {
    "remoteok": True,
    "themuse": True,
    "stackoverflow": True,
    "github_jobs": False,  # API descontinuada pero mantenemos la estructura
    "adzuna": False        # Para futuras integraciones
}

# Filtros de búsqueda optimizados - Actualizado 2025
SEARCH_FILTERS = {
    "remote_only": False,           # Incluir tanto remotos como presenciales
    "exclude_agencies": True,       # Excluir agencias de reclutamiento
    "min_salary": 25000,           # Salario mínimo más competitivo
    "include_colombia": True,       # Priorizar empleos en Colombia/LATAM
    "include_entry_level": True,    # Incluir posiciones junior/entry-level
    "exclude_unpaid": True,         # Excluir trabajos no remunerados
    "max_job_age_days": 30,        # Empleos máximo 30 días de antigüedad
    "prioritize_tech_companies": True,  # Priorizar empresas tecnológicas
    "include_contract": True,       # Incluir trabajos por contrato
    "include_freelance": True       # Incluir trabajos freelance
}

# ============================================================================
# MOTOR DE BÚSQUEDA
# ============================================================================

class JobSearchEngine:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_jobs(self, keyword):
        """Busca empleos para una palabra clave específica - OPTIMIZADO PARA ÚLTIMAS VACANTES"""
        print(f"🔍 Buscando ÚLTIMAS VACANTES para: '{keyword}'")
        results = []
        
        # 1. APIs reales con filtro de fechas
        if ENABLED_APIS.get("remoteok", True):
            print("  📡 RemoteOK API (últimos 7 días)...")
            remoteok_results = self.search_remoteok(keyword)
            if remoteok_results:
                results.extend(remoteok_results)
            
        if ENABLED_APIS.get("themuse", True):
            print("  📡 The Muse API...")
            themuse_results = self.search_themuse(keyword)
            if themuse_results:
                results.extend(themuse_results)
        
        # 2. Enlaces de LinkedIn optimizados (últimas 72 horas)
        print("  🔗 Generando enlaces LinkedIn (últimas 72h)...")
        linkedin_searches = self.generate_linkedin_searches(keyword)
        results.extend(linkedin_searches)
        
        # 3. Enlaces de Indeed optimizados (últimos 3 días)
        print("  🔗 Generando enlaces Indeed (últimos 3 días)...")
        indeed_searches = self.generate_indeed_searches(keyword)
        results.extend(indeed_searches)
        
        # 4. Sitios especializados con fechas recientes
        print("  🔗 Sitios especializados (vacantes recientes)...")
        specialized_searches = self.generate_specialized_searches(keyword)
        results.extend(specialized_searches)
        
        print(f"✅ {len(results)} empleos/enlaces encontrados")
        return results
    
    def search_remoteok(self, keyword):
        """Busca en RemoteOK API - Filtra por empleos recientes"""
        try:
            response = self.session.get("https://remoteok.io/api", timeout=10)
            if response.status_code == 200:
                jobs = response.json()[1:]  # Saltar metadata
                
                relevant_jobs = []
                for job in jobs:
                    if self.is_relevant_job(job, keyword) and self.is_recent_job(job):
                        relevant_jobs.append(self.normalize_job(job, "RemoteOK"))
                        
                return relevant_jobs[:10]  # Máximo 10 por keyword
                
        except Exception as e:
            print(f"⚠️ Error con RemoteOK: {e}")
            return []
    
    def search_themuse(self, keyword):
        """Busca en The Muse API"""
        try:
            url = f"https://www.themuse.com/api/public/jobs?page=1&api_key=&category={quote_plus(keyword)}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("results", [])
                
                relevant_jobs = []
                for job in jobs[:10]:
                    relevant_jobs.append(self.normalize_job(job, "The Muse"))
                    
                return relevant_jobs
                
        except Exception as e:
            print(f"⚠️ Error con The Muse: {e}")
            return []
    
    def generate_linkedin_searches(self, keyword):
        """Genera enlaces optimizados de LinkedIn Jobs"""
        try:
            base_url = "https://www.linkedin.com/jobs/search/"
            searches = []
            
            # Búsqueda básica remoto - ÚLTIMAS 72 HORAS
            remote_url = f"{base_url}?keywords={quote_plus(keyword)}&location=Worldwide&f_WT=2&f_TPR=r259200"
            searches.append({
                'title': f"LinkedIn: {keyword} (Remote - Últimas 72h)",
                'company': "LinkedIn Jobs", 
                'location': "Remote Worldwide",
                'description': f"Búsqueda en LinkedIn para '{keyword}' - Solo empleos remotos de las ÚLTIMAS 72 HORAS.",
                'url': remote_url,
                'salary_min': 0,
                'salary_max': 0,
                'source': 'LinkedIn (Remote)',
                'posted_date': 'Últimas 72 horas',
                'score': 90
            })
            
            # Búsqueda con ubicaciones específicas - ÚLTIMAS 72 HORAS
            locations = ["United States", "Canada", "United Kingdom"]
            for location in locations[:2]:
                location_url = f"{base_url}?keywords={quote_plus(keyword)}&location={quote_plus(location)}&f_TPR=r259200"
                searches.append({
                    'title': f"LinkedIn: {keyword} ({location} - Últimas 72h)",
                    'company': "LinkedIn Jobs",
                    'location': location,
                    'description': f"Búsqueda en LinkedIn para '{keyword}' en {location} - ÚLTIMAS 72 HORAS.",
                    'url': location_url,
                    'salary_min': 0,
                    'salary_max': 0,
                    'source': 'LinkedIn',
                    'posted_date': 'Últimas 72 horas',
                    'score': 85
                })
            
            return searches
            
        except Exception as e:
            print(f"❌ Error generando enlaces LinkedIn: {e}")
            return []
    
    def generate_indeed_searches(self, keyword):
        """Genera enlaces optimizados de Indeed"""
        try:
            base_url = "https://www.indeed.com/jobs"
            searches = []
            
            # Búsqueda remota - ÚLTIMOS 3 DÍAS
            remote_url = f"{base_url}?q={quote_plus(keyword)}&l=Remote&fromage=3&sort=date"
            searches.append({
                'title': f"Indeed: {keyword} (Remote - Últimos 3 días)",
                'company': "Indeed Jobs",
                'location': "Remote",
                'description': f"Búsqueda en Indeed para '{keyword}' - Empleos remotos, ÚLTIMOS 3 DÍAS.",
                'url': remote_url,
                'salary_min': 0,
                'salary_max': 0,
                'source': 'Indeed (Remote)',
                'posted_date': 'Últimos 3 días',
                'score': 85
            })
            
            # Búsqueda con salario mínimo - ÚLTIMOS 3 DÍAS
            salary_url = f"{base_url}?q={quote_plus(keyword)}&l=&fromage=3&sort=date&salary=%2450%2C000"
            searches.append({
                'title': f"Indeed: {keyword} ($50K+ - Últimos 3 días)",
                'company': "Indeed Jobs", 
                'location': "Any",
                'description': f"Búsqueda en Indeed para '{keyword}' - Salario mínimo $50,000, ÚLTIMOS 3 DÍAS.",
                'url': salary_url,
                'salary_min': 50000,
                'salary_max': 0,
                'source': 'Indeed (Salary)',
                'posted_date': 'Últimos 3 días',
                'score': 80
            })
            
            return searches
            
        except Exception as e:
            print(f"❌ Error generando enlaces Indeed: {e}")
            return []
    
    def generate_specialized_searches(self, keyword):
        """Genera enlaces a sitios especializados según el keyword"""
        try:
            searches = []
            keyword_lower = keyword.lower()
            
            # Para trabajos remotos generales (siempre incluir)
            searches.append({
                'title': f"We Work Remotely: {keyword}",
                'company': "We Work Remotely",
                'location': "Remote Global",
                'description': f"Mayor sitio de empleos remotos para '{keyword}'.",
                'url': f"https://weworkremotely.com/remote-jobs/search?term={quote_plus(keyword)}",
                'salary_min': 0,
                'salary_max': 0,
                'source': 'WeWorkRemotely',
                'score': 55
            })
            
            # Para BIM/CAD/Engineering - ÚLTIMAS VACANTES
            if any(term in keyword_lower for term in ['bim', 'revit', 'autocad', 'civil', 'tekla', 'navisworks', 'engineer', 'cad']):
                searches.extend([
                    {
                        'title': f"Indeed Colombia: {keyword} (Últimos 3 días)",
                        'company': "Indeed Colombia",
                        'location': "Colombia",
                        'description': f"Empleos en Colombia para '{keyword}' - ÚLTIMOS 3 DÍAS.",
                        'url': f"https://co.indeed.com/jobs?q={quote_plus(keyword)}&l=Colombia&fromage=3&sort=date",
                        'salary_min': 0,
                        'salary_max': 0,
                        'source': 'Indeed Colombia',
                        'score': 85
                    },
                    {
                        'title': f"LinkedIn Colombia: {keyword} (Últimas 72h)",
                        'company': "LinkedIn Colombia",
                        'location': "Colombia",
                        'description': f"Red profesional en Colombia para '{keyword}' - ÚLTIMAS 72 HORAS.",
                        'url': f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(keyword)}&location=Colombia&f_TPR=r259200",
                        'salary_min': 0,
                        'salary_max': 0,
                        'source': 'LinkedIn Colombia',
                        'score': 90
                    },
                    {
                        'title': f"ElEmpleo Colombia: {keyword} (Recientes)",
                        'company': "ElEmpleo Colombia",
                        'location': "Colombia",
                        'description': f"Principal sitio de empleos en Colombia para '{keyword}' - VACANTES RECIENTES.",
                        'url': f"https://www.elempleo.com/co/ofertas-empleo?q={quote_plus(keyword)}&l=Colombia",
                        'salary_min': 0,
                        'salary_max': 0,
                        'source': 'ElEmpleo Colombia',
                        'score': 95
                    }
                ])
            
            # Para tech/software/programming
            if any(term in keyword_lower for term in ['software', 'developer', 'engineer', 'python', 'javascript', 'tech', 'programming', 'c#', 'dynamo']):
                searches.extend([
                    {
                        'title': f"AngelList: {keyword}",
                        'company': "AngelList (Startups)",
                        'location': "Global",
                        'description': f"Empleos en startups para '{keyword}'.",
                        'url': f"https://angel.co/jobs#find/f!%7B%22keywords%22%3A%5B%22{quote_plus(keyword)}%22%5D%7D",
                        'salary_min': 0,
                        'salary_max': 0,
                        'source': 'AngelList',
                        'score': 60
                    },
                    {
                        'title': f"Stack Overflow Jobs: {keyword}",
                        'company': "Stack Overflow",
                        'location': "Global",
                        'description': f"Empleos técnicos para '{keyword}'.",
                        'url': f"https://stackoverflow.com/jobs?q={quote_plus(keyword)}&r=true",
                        'salary_min': 0,
                        'salary_max': 0,
                        'source': 'StackOverflow',
                        'score': 65
                    }
                ])
                
            # Para GIS/Data/Analytics
            if any(term in keyword_lower for term in ['gis', 'arcgis', 'qgis', 'data', 'analyst', 'power bi', 'spatial']):
                searches.append({
                    'title': f"GIS Jobs: {keyword}",
                    'company': "GIS Jobs Clearinghouse",
                    'location': "Global",
                    'description': f"Empleos especializados en GIS para '{keyword}'.",
                    'url': f"https://www.gjc.org/jobs/search?query={quote_plus(keyword)}",
                    'salary_min': 0,
                    'salary_max': 0,
                    'source': 'GIS Jobs',
                    'score': 70
                })
            
            # Para empleos en Colombia específicamente
            searches.extend([
                {
                    'title': f"ElEmpleo.com: {keyword}",
                    'company': "ElEmpleo Colombia",
                    'location': "Colombia",
                    'description': f"Principal sitio de empleos en Colombia para '{keyword}'.",
                    'url': f"https://www.elempleo.com/co/ofertas-empleo?q={quote_plus(keyword)}&l=Colombia",
                    'salary_min': 0,
                    'salary_max': 0,
                    'source': 'ElEmpleo Colombia',
                    'score': 80
                },
                {
                    'title': f"Computrabajo Colombia: {keyword}",
                    'company': "Computrabajo",
                    'location': "Colombia",
                    'description': f"Empleos en Colombia y LATAM para '{keyword}'.",
                    'url': f"https://www.computrabajo.com.co/trabajo-de-{quote_plus(keyword)}-en-colombia",
                    'salary_min': 0,
                    'salary_max': 0,
                    'source': 'Computrabajo',
                    'score': 75
                }
            ])
            
            return searches
            
        except Exception as e:
            print(f"❌ Error generando enlaces especializados: {e}")
            return []
    
    def is_relevant_job(self, job, keyword):
        """Verifica si un empleo es relevante para el keyword"""
        text = ""
        if isinstance(job, dict):
            text = f"{job.get('position', '')} {job.get('company', '')} {job.get('description', '')}".lower()
        
        keyword_lower = keyword.lower()
        return keyword_lower in text
    
    def is_recent_job(self, job, max_days=7):
        """Verifica si un empleo es reciente (últimos 7 días por defecto)"""
        try:
            from datetime import datetime, timedelta
            
            # Para RemoteOK, usar el campo 'date'
            if 'date' in job:
                job_date = datetime.fromtimestamp(int(job['date']))
                cutoff_date = datetime.now() - timedelta(days=max_days)
                return job_date >= cutoff_date
            
            # Para otros sitios, asumir que son recientes si no hay fecha
            return True
            
        except Exception:
            # Si hay error procesando la fecha, incluir el empleo
            return True
    
    def calculate_relevance_score(self, job, search_terms):
        """Calcula puntuación de relevancia basada en múltiples términos"""
        if not isinstance(search_terms, list):
            search_terms = [search_terms]
        
        text = ""
        if isinstance(job, dict):
            title_text = job.get('position', job.get('title', '')).lower()
            company_text = job.get('company', '').lower() 
            desc_text = str(job.get('description', '')).lower()
            text = f"{title_text} {company_text} {desc_text}"
        
        score = 0
        for term in search_terms:
            term_lower = term.lower()
            
            # Puntuación por aparición en título (más importante)
            if term_lower in title_text:
                score += 3
            
            # Puntuación por aparición en empresa
            if term_lower in company_text:
                score += 2
            
            # Puntuación por aparición en descripción
            if term_lower in desc_text:
                score += 1
        
        return score
    
    def normalize_job(self, job, source):
        """Normaliza la estructura de datos de diferentes fuentes"""
        if source == "RemoteOK":
            return {
                "title": job.get("position", "N/A"),
                "company": job.get("company", "N/A"),
                "location": job.get("location", "Remote"),
                "salary_min": job.get("salary_min", 0),
                "salary_max": job.get("salary_max", 0),
                "url": f"https://remoteok.io/remote-jobs/{job.get('id', '')}",
                "description": str(job.get("description", ""))[:200],
                "source": source,
                "score": 0
            }
        elif source == "The Muse":
            location = job.get('locations', [{}])[0].get('name', 'Remote') if job.get('locations') else 'Remote'
            return {
                "title": job.get("name", "N/A"),
                "company": job.get("company", {}).get("name", "N/A"),
                "location": location,
                "salary_min": 0,
                "salary_max": 0,
                "url": job.get("refs", {}).get("landing_page", ""),
                "description": str(job.get("contents", ""))[:200],
                "source": source,
                "score": 0
            }
        
        return job
    
    def search_all_categories(self):
        """Busca empleos en todas las categorías configuradas"""
        print("🚀 INICIANDO BÚSQUEDA COMPLETA DE EMPLEOS")
        print("=" * 60)
        
        all_results = []
        
        for category, keywords in JOB_CATEGORIES.items():
            print(f"\n🎯 CATEGORÍA: {category}")
            print("-" * 40)
            
            category_results = []
            for keyword in keywords:  # ✅ TODOS los keywords por categoría
                results = self.search_jobs(keyword)
                category_results.extend(results)
            
            # Procesar resultados de la categoría
            unique_results = self.remove_duplicates(category_results)
            filtered_results = self.apply_filters(unique_results)
            ranked_results = self.rank_jobs(filtered_results, keywords)  # ✅ TODOS los keywords
            
            print(f"📊 {len(ranked_results)} empleos únicos encontrados")
            
            # Mostrar los top 3 de la categoría
            for i, job in enumerate(ranked_results[:3], 1):
                self.display_job(job, f"#{i}")
            
            all_results.extend(ranked_results)
        
        return all_results
    
    def remove_duplicates(self, jobs):
        """Elimina empleos duplicados"""
        seen_urls = set()
        unique_jobs = []
        
        for job in jobs:
            url = job.get('url', '')
            title_company = f"{job.get('title', '')}-{job.get('company', '')}"
            
            if url not in seen_urls and title_company not in seen_urls:
                seen_urls.add(url)
                seen_urls.add(title_company)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def apply_filters(self, jobs):
        """Aplica filtros configurados"""
        filtered = []
        
        for job in jobs:
            # Filtro de salario mínimo
            if SEARCH_FILTERS.get("min_salary", 0) > 0:
                if job.get("salary_min", 0) > 0 and job.get("salary_min", 0) < SEARCH_FILTERS["min_salary"]:
                    continue
            
            # Filtro solo remotos
            if SEARCH_FILTERS.get("remote_only", False):
                location = job.get("location", "").lower()
                if not any(word in location for word in ["remote", "remoto", "worldwide"]):
                    continue
            
            # Excluir agencias
            if SEARCH_FILTERS.get("exclude_agencies", True):
                company = job.get("company", "").lower()
                agency_keywords = ["staffing", "recruiting", "headhunter", "talent acquisition"]
                if any(keyword in company for keyword in agency_keywords):
                    continue
                    
            filtered.append(job)
            
        return filtered
    
    def rank_jobs(self, jobs, search_terms=None):
        """Rankea empleos por relevancia"""
        for job in jobs:
            score = 0
            
            # Puntuación por relevancia de términos de búsqueda
            if search_terms:
                relevance_score = self.calculate_relevance_score(job, search_terms)
                score += relevance_score * 5  # Multiplicar para dar más peso a la relevancia
            
            # Puntuación por salario
            salary_min = job.get("salary_min", 0)
            if salary_min >= SALARY_PREFERENCES.get("target_usd", 100000):
                score += 50
            elif salary_min >= SALARY_PREFERENCES.get("preferred_usd", 60000):
                score += 30
            elif salary_min >= SALARY_PREFERENCES.get("minimum_usd", 30000):
                score += 10
                
            # Puntuación por ubicación
            location = job.get("location", "").lower()
            for i, pref_location in enumerate(PREFERRED_LOCATIONS):
                if pref_location.lower() in location:
                    score += (10 - i)
                    break
                    
            job["score"] = score
            
        return sorted(jobs, key=lambda x: x.get("score", 0), reverse=True)
    
    def display_job(self, job, prefix=""):
        """Muestra información de un empleo en consola"""
        salary_info = ""
        if job.get('salary_min', 0) > 0:
            salary_info = f" | 💰 ${job['salary_min']:,}"
            if job.get('salary_max', 0) > 0:
                salary_info += f"-${job['salary_max']:,}"
        
        print(f"\n🎯 {prefix}")
        print(f"📋 {job['title']}")
        print(f"🏢 {job.get('company', 'N/A')} | 📍 {job.get('location', 'N/A')}{salary_info}")
        print(f"🌐 {job.get('source', 'N/A')}")
        print(f"⭐ Puntuación: {job.get('score', 0)}")
        print(f"🔗 {job.get('url', 'N/A')}")
        if job.get('description'):
            print(f"📝 {job['description'][:100]}...")
        print("-" * 50)

# ============================================================================
# INTERFAZ GRÁFICA
# ============================================================================

class JobSearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Sistema de Búsqueda de Empleos - BIM/GIS")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.search_results = []
        self.searcher = JobSearchEngine()
        self.search_running = False
        
        # Cargar logo si está disponible
        self.logo_image = None
        self.load_logo()
        
        self.setup_ui()
        
    def load_logo(self):
        """Carga el logo AGRDB si está disponible"""
        try:
            if PIL_AVAILABLE:
                logo_path = os.path.join(os.path.dirname(__file__), "AGRDB_Logo.png")
                if os.path.exists(logo_path):
                    # Cargar y redimensionar la imagen
                    image = Image.open(logo_path)
                    # Redimensionar manteniendo proporción (altura máxima 40px)
                    image.thumbnail((120, 40), Image.Resampling.LANCZOS)
                    self.logo_image = ImageTk.PhotoImage(image)
                    print("✅ Logo AGRDB cargado exitosamente")
                else:
                    print("⚠️ Logo AGRDB_Logo.png no encontrado")
            else:
                print("⚠️ PIL no disponible, logo no se puede cargar")
        except Exception as e:
            print(f"⚠️ Error cargando logo: {e}")
            self.logo_image = None
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        
        # Título principal con logo
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        # Contenedor para logo y título
        content_frame = tk.Frame(title_frame, bg='#2c3e50')
        content_frame.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Logo (si está disponible)
        if self.logo_image:
            logo_label = tk.Label(content_frame, image=self.logo_image, bg='#2c3e50')
            logo_label.pack(side='left', padx=(0, 15))
        
        # Título
        title_label = tk.Label(
            content_frame, 
            text="🚀 Sistema de Búsqueda de Empleos - ÚLTIMAS VACANTES",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='left', expand=True)
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pestañas
        self.create_search_tab()
        self.create_export_tab()
        self.create_config_tab()
        self.create_about_tab()
        
        # Footer con información del desarrollador
        self.create_footer()
        
    def create_search_tab(self):
        """Crea la pestaña de búsqueda principal"""
        search_frame = ttk.Frame(self.notebook)
        self.notebook.add(search_frame, text="🔍 Búsqueda")
        
        # Opciones de búsqueda
        options_frame = ttk.LabelFrame(search_frame, text="Opciones de Búsqueda", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        # Tipo de búsqueda
        ttk.Label(options_frame, text="Tipo de búsqueda:").grid(row=0, column=0, sticky='w', pady=2)
        self.search_type = tk.StringVar(value="completa")
        ttk.Radiobutton(options_frame, text="Búsqueda completa", variable=self.search_type, value="completa").grid(row=0, column=1, sticky='w')
        ttk.Radiobutton(options_frame, text="Solo palabra clave", variable=self.search_type, value="keyword").grid(row=0, column=2, sticky='w')
        
        # Campo de palabra clave (siempre activo)
        ttk.Label(options_frame, text="Filtro adicional:").grid(row=1, column=0, sticky='w', pady=2)
        self.keyword_entry = ttk.Entry(options_frame, width=30)
        self.keyword_entry.grid(row=1, column=1, columnspan=2, sticky='ew', pady=2)
        
        # Categorías
        ttk.Label(options_frame, text="Categorías:").grid(row=2, column=0, sticky='w', pady=2)
        self.categories_frame = tk.Frame(options_frame)
        self.categories_frame.grid(row=2, column=1, columnspan=2, sticky='ew', pady=2)
        
        self.category_vars = {}
        for i, category in enumerate(JOB_CATEGORIES.keys()):
            var = tk.BooleanVar(value=True)
            self.category_vars[category] = var
            ttk.Checkbutton(self.categories_frame, text=category, variable=var).grid(
                row=i//2, column=i%2, sticky='w', padx=5
            )
        
        # Botones
        buttons_frame = tk.Frame(options_frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        self.search_button = ttk.Button(buttons_frame, text="🚀 Buscar", command=self.start_search)
        self.search_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(buttons_frame, text="⏹️ Detener", command=self.stop_search, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        ttk.Button(buttons_frame, text="🔄 Limpiar", command=self.clear_results).pack(side='left', padx=5)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(search_frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=10, pady=5)
        
        # Resultados
        results_frame = ttk.LabelFrame(search_frame, text="Resultados", padding=5)
        results_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.summary_label = ttk.Label(results_frame, text="Sin resultados", font=('Arial', 10, 'bold'))
        self.summary_label.pack(anchor='w', pady=2)
        
        # Lista de resultados
        self.results_tree = ttk.Treeview(
            results_frame, 
            columns=('Empresa', 'Ubicación', 'Salario', 'Fuente', 'Score'),
            show='tree headings',
            height=10
        )
        
        self.results_tree.heading('#0', text='Título del Empleo')
        self.results_tree.heading('Empresa', text='Empresa')
        self.results_tree.heading('Ubicación', text='Ubicación')
        self.results_tree.heading('Salario', text='Salario')
        self.results_tree.heading('Fuente', text='Fuente')
        self.results_tree.heading('Score', text='Score')
        
        self.results_tree.column('#0', width=250)
        self.results_tree.column('Empresa', width=120)
        self.results_tree.column('Ubicación', width=100)
        self.results_tree.column('Salario', width=80)
        self.results_tree.column('Fuente', width=80)
        self.results_tree.column('Score', width=50)
        
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.results_tree.bind('<Double-1>', self.open_job_url)
        
    def create_export_tab(self):
        """Crea la pestaña de exportación"""
        export_frame = ttk.Frame(self.notebook)
        self.notebook.add(export_frame, text="📤 Exportación")
        
        # Título
        title_label = ttk.Label(export_frame, text="📤 Exportar Resultados", font=('Arial', 12, 'bold'))
        title_label.pack(pady=10)
        
        # Opciones de formato
        format_frame = ttk.LabelFrame(export_frame, text="Formato", padding=10)
        format_frame.pack(fill='x', padx=10, pady=5)
        
        self.export_format = tk.StringVar(value="json")
        
        formats = [
            ("JSON", "json", "Para análisis"),
            ("CSV", "csv", "Para Excel"),
            ("XML", "xml", "Para sistemas"),
            ("HTML", "html", "Reporte visual"),
            ("TXT", "txt", "Texto simple")
        ]
        
        for i, (name, value, desc) in enumerate(formats):
            frame = ttk.Frame(format_frame)
            frame.grid(row=i, column=0, sticky='ew', pady=2)
            
            ttk.Radiobutton(frame, text=name, variable=self.export_format, value=value).pack(side='left')
            ttk.Label(frame, text=f"- {desc}", font=('Arial', 9)).pack(side='left', padx=10)
        
        # Opciones
        options_frame = ttk.LabelFrame(export_frame, text="Opciones", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.include_description = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Incluir descripciones", variable=self.include_description).pack(anchor='w')
        
        self.filter_by_salary = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Solo con salario", variable=self.filter_by_salary).pack(anchor='w')
        
        # Botones
        export_buttons_frame = ttk.Frame(export_frame)
        export_buttons_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(export_buttons_frame, text="📁 Exportar", command=self.export_results).pack(side='left', padx=5)
        ttk.Button(export_buttons_frame, text="📊 Vista Previa", command=self.preview_export).pack(side='left', padx=5)
        
        # Vista previa
        preview_frame = ttk.LabelFrame(export_frame, text="Vista Previa", padding=5)
        preview_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame, height=8)
        self.preview_text.pack(fill='both', expand=True)
        
    def create_config_tab(self):
        """Crea la pestaña de configuración"""
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuración")
        
        # Contenedor principal
        main_container = tk.Frame(config_frame)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Salarios
        salary_frame = ttk.LabelFrame(main_container, text="Preferencias Salariales (USD)", padding=15)
        salary_frame.pack(fill='x', pady=(0, 15))
        
        ttk.Label(salary_frame, text="Salario mínimo:").grid(row=0, column=0, sticky='w', pady=5)
        self.min_salary = tk.StringVar(value=str(SALARY_PREFERENCES.get('minimum_usd', 30000)))
        ttk.Entry(salary_frame, textvariable=self.min_salary, width=15).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(salary_frame, text="Salario preferido:").grid(row=1, column=0, sticky='w', pady=5)
        self.pref_salary = tk.StringVar(value=str(SALARY_PREFERENCES.get('preferred_usd', 60000)))
        ttk.Entry(salary_frame, textvariable=self.pref_salary, width=15).grid(row=1, column=1, padx=10, pady=5)
        
        # Filtros
        filters_frame = ttk.LabelFrame(main_container, text="Filtros", padding=15)
        filters_frame.pack(fill='x', pady=(0, 15))
        
        self.remote_only = tk.BooleanVar(value=SEARCH_FILTERS.get('remote_only', False))
        ttk.Checkbutton(filters_frame, text="Solo empleos remotos", variable=self.remote_only).pack(anchor='w', pady=5)
        
        self.exclude_agencies = tk.BooleanVar(value=SEARCH_FILTERS.get('exclude_agencies', True))
        ttk.Checkbutton(filters_frame, text="Excluir agencias", variable=self.exclude_agencies).pack(anchor='w', pady=5)
        
        # Botón centrado
        button_frame = tk.Frame(main_container)
        button_frame.pack(fill='x', pady=20)
        
        save_button = ttk.Button(button_frame, text="💾 Guardar", command=self.save_config)
        save_button.pack(anchor='center')
        
        # Spacer para empujar el contenido hacia arriba
        spacer = tk.Frame(main_container)
        spacer.pack(fill='both', expand=True)
    
    def create_about_tab(self):
        """Crea la pestaña Acerca de"""
        about_frame = ttk.Frame(self.notebook)
        self.notebook.add(about_frame, text="ℹ️ Acerca de")
        
        # Contenedor principal centrado
        main_container = tk.Frame(about_frame, bg='white')
        main_container.pack(fill='both', expand=True)
        
        # Frame centrado para el contenido
        centered_frame = tk.Frame(main_container, bg='white')
        centered_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Header con logo grande (si está disponible)
        header_frame = tk.Frame(centered_frame, bg='#2c3e50', width=400, height=120)
        header_frame.pack(pady=(0, 20))
        header_frame.pack_propagate(False)
        
        if self.logo_image:
            # Logo más grande para la página Acerca de
            try:
                if PIL_AVAILABLE:
                    logo_path = os.path.join(os.path.dirname(__file__), "AGRDB_Logo.png")
                    if os.path.exists(logo_path):
                        image = Image.open(logo_path)
                        image.thumbnail((250, 100), Image.Resampling.LANCZOS)
                        large_logo = ImageTk.PhotoImage(image)
                        logo_label = tk.Label(header_frame, image=large_logo, bg='#2c3e50')
                        logo_label.image = large_logo  # type: ignore # Mantener referencia
                        logo_label.pack(expand=True)
            except Exception:
                pass
        
        # Enlaces centrados
        links_frame = ttk.LabelFrame(centered_frame, text="🔗 Enlaces", padding=20)
        links_frame.pack(pady=10)
        
        # Botón para GitHub/Repositorio
        github_button = tk.Button(
            links_frame,
            text="📂 Ver Repositorio en GitHub",
            command=self.open_github_repo,
            bg='#0366d6',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=12,
            width=25
        )
        github_button.pack(pady=8)
        
        # Botón para perfil
        profile_button = tk.Button(
            links_frame,
            text="👤 Perfil del Desarrollador",
            command=self.open_developer_profile,
            bg='#28a745',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief='flat',
            padx=30,
            pady=12,
            width=25
        )
        profile_button.pack(pady=8)
        
        # Información de licencia centrada
        license_frame = ttk.LabelFrame(centered_frame, text="📄 Licencia", padding=20)
        license_frame.pack(pady=(20, 0))
        
        license_info = """📜 MIT License - Uso libre y gratuito
✅ Puedes modificar, distribuir y usar comercialmente
🔄 Contribuciones y mejoras son bienvenidas"""
        
        license_label = tk.Label(license_frame, text=license_info, justify='center', 
                               font=('Arial', 10), wraplength=400, bg='white')
        license_label.pack()
    
    def open_github_repo(self):
        """Abre el repositorio en GitHub"""
        # Puedes cambiar esta URL por tu repositorio real
        repo_url = "https://github.com/AGRDIGITALBUSSINES"
        webbrowser.open(repo_url)
    
    def open_developer_profile(self):
        """Abre el perfil del desarrollador"""
        # Puedes cambiar esta URL por tu perfil real
        profile_url = "https://www.linkedin.com/in/agrdb"
        webbrowser.open(profile_url)
    
    def create_footer(self):
        """Crea el footer con información del desarrollador"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=35)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Texto del desarrollador
        footer_text = "Desarrollado por: AGRDB | Automatización y Desarrollo BIM"
        footer_label = tk.Label(
            footer_frame,
            text=footer_text,
            font=('Arial', 9),
            fg='white',
            bg='#34495e'
        )
        footer_label.pack(expand=True)
        
        # Hacer clickeable el footer para abrir el perfil
        footer_label.bind("<Button-1>", lambda e: self.open_developer_profile())
        footer_label.configure(cursor='hand2')
    
    def start_search(self):
        """Inicia la búsqueda"""
        if self.search_running:
            return
            
        self.search_running = True
        self.search_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        self.progress.start()
        
        search_thread = threading.Thread(target=self._perform_search)
        search_thread.daemon = True
        search_thread.start()
    
    def _perform_search(self):
        """Realiza la búsqueda en segundo plano"""
        try:
            self.search_results = []
            additional_keyword = self.keyword_entry.get().strip()
            
            if self.search_type.get() == "completa":
                # Búsqueda por categorías seleccionadas - TODOS LOS KEYWORDS
                for category, var in self.category_vars.items():
                    if var.get() and category in JOB_CATEGORIES:
                        keywords = JOB_CATEGORIES[category]  # ✅ TODOS los keywords (sin [:2])
                        for keyword in keywords:
                            if not self.search_running:
                                break
                            
                            # Combinar keyword de categoría con filtro adicional
                            search_terms = [keyword]
                            if additional_keyword:
                                # Buscar tanto el keyword original como la combinación
                                combined_keyword = f"{keyword} {additional_keyword}"
                                search_terms.extend([additional_keyword, combined_keyword])
                            
                            for search_term in search_terms:
                                if not self.search_running:
                                    break
                                self.root.after(0, lambda k=search_term: self.summary_label.configure(text=f"🔍 Buscando: {k}..."))
                                results = self.searcher.search_jobs(search_term)
                                self.search_results.extend(results)
            else:
                # Búsqueda solo por palabra clave específica
                if additional_keyword:
                    self.root.after(0, lambda: self.summary_label.configure(text=f"🔍 Buscando: {additional_keyword}..."))
                    results = self.searcher.search_jobs(additional_keyword)
                    self.search_results.extend(results)
                else:
                    self.root.after(0, lambda: self.summary_label.configure(text="⚠️ Ingresa una palabra clave"))
                    return
            
            # Procesar resultados
            if self.search_results:
                search_link_sources = ['LinkedIn (Remote)', 'LinkedIn', 'Indeed (Remote)', 'Indeed (Salary)', 'WeWorkRemotely', 'AngelList']
                real_jobs = [job for job in self.search_results if job.get('source') not in search_link_sources]
                search_links = [job for job in self.search_results if job.get('source') in search_link_sources]
                
                if real_jobs:
                    real_jobs = self.searcher.remove_duplicates(real_jobs)
                    real_jobs = self.searcher.apply_filters(real_jobs)
                    
                    # Preparar términos de búsqueda para ranking
                    ranking_terms = []
                    if self.search_type.get() == "completa":
                        # Incluir palabras clave de categorías seleccionadas
                        for category, var in self.category_vars.items():
                            if var.get() and category in JOB_CATEGORIES:
                                ranking_terms.extend(JOB_CATEGORIES[category])  # ✅ TODOS los keywords
                    if additional_keyword:
                        ranking_terms.append(additional_keyword)
                    
                    real_jobs = self.searcher.rank_jobs(real_jobs, ranking_terms if ranking_terms else None)
                
                self.search_results = real_jobs + search_links
            
            self.root.after(0, self._update_results_ui)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error: {e}"))
        finally:
            self.root.after(0, self._search_completed)
    
    def _update_results_ui(self):
        """Actualiza la interfaz con los resultados"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        search_link_sources = ['LinkedIn (Remote)', 'LinkedIn', 'Indeed (Remote)', 'Indeed (Salary)', 'WeWorkRemotely', 'AngelList']
        real_jobs = [job for job in self.search_results if job.get('source') not in search_link_sources]
        search_links = [job for job in self.search_results if job.get('source') in search_link_sources]
        
        total_jobs = len(self.search_results)
        real_count = len(real_jobs)
        links_count = len(search_links)
        with_salary = len([job for job in real_jobs if job.get('salary_min', 0) > 0])
        
        self.summary_label.configure(text=f"📊 {total_jobs} resultados • {real_count} empleos reales • {links_count} enlaces • {with_salary} con salario")
        
        # Empleos reales
        for i, job in enumerate(real_jobs[:20], 1):
            salary_text = ""
            if job.get('salary_min', 0) > 0:
                salary_text = f"${job['salary_min']:,}"
                if job.get('salary_max', 0) > 0:
                    salary_text += f"-${job['salary_max']:,}"
            
            title_with_icon = f"💼 {job.get('title', 'N/A')}"
            
            self.results_tree.insert('', 'end',
                text=f"{i}. {title_with_icon}",
                values=(
                    job.get('company', 'N/A'),
                    job.get('location', 'N/A'),
                    salary_text,
                    job.get('source', 'N/A'),
                    f"⭐{job.get('score', 0)}"
                ),
                tags=(job.get('url', ''), 'real_job')
            )
        
        # Separador
        if real_jobs and search_links:
            self.results_tree.insert('', 'end',
                text="─── 🔗 ENLACES DE BÚSQUEDA ───",
                values=("", "", "", "", ""),
                tags=("", 'separator')
            )
        
        # Enlaces de búsqueda
        link_start = len(real_jobs) + (1 if real_jobs and search_links else 0)
        for i, link in enumerate(search_links[:10], link_start + 1):
            icon = "🔗"
            if "LinkedIn" in link.get('source', ''):
                icon = "💼"
            elif "Indeed" in link.get('source', ''):
                icon = "🔍"
            elif "Remote" in link.get('source', ''):
                icon = "🏠"
            
            title_with_icon = f"{icon} {link.get('title', 'N/A')}"
            
            self.results_tree.insert('', 'end',
                text=f"{i}. {title_with_icon}",
                values=(
                    link.get('company', 'N/A'),
                    link.get('location', 'N/A'),
                    "Haz clic para buscar",
                    link.get('source', 'N/A'),
                    f"🔗{link.get('score', 0)}"
                ),
                tags=(link.get('url', ''), 'search_link')
            )
        
        # Colores
        self.results_tree.tag_configure('real_job', background='#e8f5e8')
        self.results_tree.tag_configure('search_link', background='#e8f0ff')
        self.results_tree.tag_configure('separator', background='#f0f0f0', font=('Arial', 9, 'bold'))
    
    def _search_completed(self):
        """Finaliza la búsqueda"""
        self.search_running = False
        self.search_button.configure(state='normal')
        self.stop_button.configure(state='disabled')
        self.progress.stop()
    
    def stop_search(self):
        """Detiene la búsqueda"""
        self.search_running = False
    
    def clear_results(self):
        """Limpia los resultados"""
        self.search_results = []
        self._update_results_ui()
        self.preview_text.delete(1.0, tk.END)
    
    def open_job_url(self, event):
        """Abre la URL del empleo"""
        selection = self.results_tree.selection()
        if selection:
            item = self.results_tree.item(selection[0])
            url = item['tags'][0] if item['tags'] else None
            if url:
                webbrowser.open(url)
    
    def export_results(self):
        """Exporta los resultados"""
        if not self.search_results:
            messagebox.showwarning("Sin resultados", "No hay resultados para exportar")
            return
        
        format_type = self.export_format.get()
        
        file_types = {
            'json': [('JSON files', '*.json')],
            'csv': [('CSV files', '*.csv')],
            'xml': [('XML files', '*.xml')],
            'html': [('HTML files', '*.html')],
            'txt': [('Text files', '*.txt')]
        }
        
        filename = filedialog.asksaveasfilename(
            title="Guardar resultados",
            filetypes=file_types[format_type],
            defaultextension=f".{format_type}"
        )
        
        if filename:
            try:
                self._export_to_file(filename, format_type)
                messagebox.showinfo("Éxito", f"Resultados exportados a {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {e}")
    
    def _export_to_file(self, filename, format_type):
        """Exporta los resultados al archivo"""
        results_to_export = self.search_results
        if self.filter_by_salary.get():
            results_to_export = [job for job in results_to_export if job.get('salary_min', 0) > 0]
        
        if format_type == 'json':
            with open(filename, 'w', encoding='utf-8') as f:
                export_data = {
                    'exported_at': datetime.now().isoformat(),
                    'total_jobs': len(results_to_export),
                    'jobs': results_to_export
                }
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        elif format_type == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['title', 'company', 'location', 'salary_min', 'salary_max', 'source', 'url', 'score']
                if self.include_description.get():
                    fieldnames.append('description')
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for job in results_to_export:
                    row = {field: job.get(field, '') for field in fieldnames}
                    writer.writerow(row)
        
        elif format_type == 'xml':
            root = ET.Element('job_search_results')
            ET.SubElement(root, 'exported_at').text = datetime.now().isoformat()
            ET.SubElement(root, 'total_jobs').text = str(len(results_to_export))
            
            jobs_element = ET.SubElement(root, 'jobs')
            for job in results_to_export:
                job_element = ET.SubElement(jobs_element, 'job')
                for key, value in job.items():
                    if key != 'description' or self.include_description.get():
                        ET.SubElement(job_element, key).text = str(value)
            
            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
        
        elif format_type == 'html':
            html_content = self._generate_html_report(results_to_export)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        elif format_type == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"RESULTADOS DE BÚSQUEDA DE EMPLEOS\n")
                f.write(f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total empleos: {len(results_to_export)}\n")
                f.write("="*60 + "\n\n")
                
                for i, job in enumerate(results_to_export, 1):
                    f.write(f"{i}. {job.get('title', 'N/A')}\n")
                    f.write(f"   Empresa: {job.get('company', 'N/A')}\n")
                    f.write(f"   Ubicación: {job.get('location', 'N/A')}\n")
                    
                    if job.get('salary_min', 0) > 0:
                        salary = f"${job['salary_min']:,}"
                        if job.get('salary_max', 0) > 0:
                            salary += f" - ${job['salary_max']:,}"
                        f.write(f"   Salario: {salary}\n")
                    
                    f.write(f"   Fuente: {job.get('source', 'N/A')}\n")
                    f.write(f"   URL: {job.get('url', 'N/A')}\n")
                    
                    if self.include_description.get() and job.get('description'):
                        f.write(f"   Descripción: {job['description'][:200]}...\n")
                    
                    f.write("\n" + "-"*50 + "\n\n")
    
    def _generate_html_report(self, results):
        """Genera un reporte HTML"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Resultados de Búsqueda de Empleos</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .job {{ border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }}
        .job-title {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
        .salary {{ color: #27ae60; font-weight: bold; }}
        .company {{ color: #34495e; }}
        .meta {{ color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Resultados de Búsqueda de Empleos</h1>
        <p>Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total empleos: {len(results)}</p>
    </div>
"""
        
        for i, job in enumerate(results, 1):
            salary_text = ""
            if job.get('salary_min', 0) > 0:
                salary_text = f"<span class='salary'>${job['salary_min']:,}"
                if job.get('salary_max', 0) > 0:
                    salary_text += f" - ${job['salary_max']:,}"
                salary_text += "</span>"
            
            html += f"""
    <div class="job">
        <div class="job-title">{i}. {job.get('title', 'N/A')}</div>
        <div class="company">🏢 {job.get('company', 'N/A')}</div>
        <div>📍 {job.get('location', 'N/A')}</div>
        {f'<div>💰 {salary_text}</div>' if salary_text else ''}
        <div class="meta">
            Fuente: {job.get('source', 'N/A')} | 
            Puntuación: {job.get('score', 0)} | 
            <a href="{job.get('url', '#')}" target="_blank">Ver empleo</a>
        </div>
        {f'<div style="margin-top: 10px; font-size: 14px;">{str(job.get("description", ""))[:300]}...</div>' if self.include_description.get() and job.get('description') else ''}
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def preview_export(self):
        """Muestra una vista previa"""
        if not self.search_results:
            messagebox.showwarning("Sin resultados", "No hay resultados para previsualizar")
            return
        
        format_type = self.export_format.get()
        preview_data = self.search_results[:5]
        
        self.preview_text.delete(1.0, tk.END)
        
        if format_type == 'json':
            preview_content = json.dumps(preview_data, indent=2, ensure_ascii=False)
        elif format_type == 'csv':
            preview_content = "title,company,location,salary_min,salary_max,source,url,score\n"
            for job in preview_data:
                preview_content += f'"{job.get("title","")}",'
                preview_content += f'"{job.get("company","")}",'
                preview_content += f'"{job.get("location","")}",'
                preview_content += f'{job.get("salary_min","")},'
                preview_content += f'{job.get("salary_max","")},'
                preview_content += f'"{job.get("source","")}",'
                preview_content += f'"{job.get("url","")}",'
                preview_content += f'{job.get("score","")}\n'
        else:
            preview_content = f"Vista previa para formato {format_type.upper()}:\n\n"
            for i, job in enumerate(preview_data, 1):
                preview_content += f"{i}. {job.get('title', 'N/A')}\n"
                preview_content += f"   Empresa: {job.get('company', 'N/A')}\n"
                preview_content += f"   Ubicación: {job.get('location', 'N/A')}\n"
                if job.get('salary_min', 0) > 0:
                    preview_content += f"   Salario: ${job['salary_min']:,}\n"
                preview_content += f"   Fuente: {job.get('source', 'N/A')}\n\n"
        
        self.preview_text.insert(tk.END, preview_content)
    
    def save_config(self):
        """Guarda la configuración"""
        try:
            global SALARY_PREFERENCES, SEARCH_FILTERS
            SALARY_PREFERENCES['minimum_usd'] = int(self.min_salary.get())
            SALARY_PREFERENCES['preferred_usd'] = int(self.pref_salary.get())
            SEARCH_FILTERS['remote_only'] = self.remote_only.get()
            SEARCH_FILTERS['exclude_agencies'] = self.exclude_agencies.get()
            messagebox.showinfo("Configuración", "Configuración guardada")
        except ValueError:
            messagebox.showerror("Error", "Los salarios deben ser números")
# ============================================================================
# MODO CONSOLA
# ============================================================================

def console_mode():
    """Ejecuta el sistema en modo consola"""
    print("🎉 SISTEMA DE BÚSQUEDA DE EMPLEOS - ÚLTIMAS VACANTES")
    print("=" * 60)
    print("🕒 CONFIGURADO PARA LAS OFERTAS MÁS RECIENTES:")
    print("   • LinkedIn: Últimas 72 horas")
    print("   • Indeed: Últimos 3 días")
    print("   • APIs: Filtro automático por fecha")
    print("=" * 60)
    
    searcher = JobSearchEngine()
    
    print("\n¿Qué quieres hacer?")
    print("1. Búsqueda completa en todas las categorías (ÚLTIMAS VACANTES)")
    print("2. Búsqueda por palabra clave específica (ÚLTIMAS VACANTES)")
    print("3. 🖥️ Abrir interfaz gráfica")
    
    choice = input("\nSelección (1-3): ").strip()
    
    if choice == "1":
        all_results = searcher.search_all_categories()
        top_jobs = searcher.rank_jobs(all_results)[:10]
        print(f"\n🏆 TOP 10 EMPLEOS RECOMENDADOS:")
        for i, job in enumerate(top_jobs, 1):
            searcher.display_job(job, f"#{i}")
            
    elif choice == "2":
        keyword = input("Ingresa la palabra clave: ").strip()
        if keyword:
            results = searcher.search_jobs(keyword)
            filtered_results = searcher.apply_filters(results)
            ranked_results = searcher.rank_jobs(filtered_results, [keyword])
            
            print(f"\n📊 {len(ranked_results)} empleos encontrados para '{keyword}'")
            for i, job in enumerate(ranked_results[:5], 1):
                searcher.display_job(job, f"#{i}")
                
    elif choice == "3":
        gui_mode()
        
    else:
        print("❌ Selección inválida")

# ============================================================================
# MODO GUI
# ============================================================================

def gui_mode():
    """Ejecuta el sistema en modo GUI"""
    try:
        root = tk.Tk()
        app = JobSearchGUI(root)
        root.mainloop()
    except Exception as e:
        print(f"❌ Error en la interfaz gráfica: {e}")
        print("Ejecutando en modo consola...")
        console_mode()

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--console":
            console_mode()
        elif sys.argv[1] == "--help":
            print("🚀 Sistema de Búsqueda de Empleos")
            print("\nUso:")
            print("  python job_search_bim.py           - Interfaz gráfica")
            print("  python job_search_bim.py --console - Modo consola")
            print("  python job_search_bim.py --help    - Esta ayuda")
        else:
            print(f"❌ Argumento desconocido: {sys.argv[1]}")
    else:
        # Por defecto: interfaz gráfica
        gui_mode()

if __name__ == "__main__":
    main()