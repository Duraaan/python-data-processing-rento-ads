# 📊 Scripts de Limpieza de Datos

Un par de scripts Python para procesar y validar leads de Google Ads. Nada complicado, solo automatización de tareas repetitivas.

## 🚀 Qué hace esto

### 1. `extracto_listas.py`
Agarra todos los excels de la carpeta `listas/`, los limpia, los filtra por fecha y genera un archivo consolidado. Después borra los originales para no acumular basura.

**Uso:**
```bash
python extracto_listas.py
```
Te va a pedir fecha inicio y fin en formato `AAAA-MM-DD`.

### 2. `limpieza_bd.py`
Toma tu base de datos maestra (`bd.xlsx`), limpia los números de teléfono y genera una versión limpia para comparar después.

**Uso:**
```bash
python limpieza_bd.py
```

### 3. `cruze_y_validacion.py`
Cruza los leads nuevos con la base de datos limpia. Solo te deja los que NO están repetidos y genera el archivo final listo para cargar a tu CRM.

**Uso:**
```bash
python cruze_y_validacion.py
```

## 📦 Dependencias

```bash
pip install pandas openpyxl
```

## 📁 Estructura esperada

```
python/
├── listas/              # Aquí van los excels de Google Ads
├── bd.xlsx              # Tu base de datos maestra
├── extracto_listas.py
├── limpieza_bd.py
└── cruze_y_validacion.py
```

## 🔧 Flujo de trabajo

1. Tira los excels de Google Ads en la carpeta `listas/`
2. Corre `extracto_listas.py` → genera `extraccion.xlsx`
3. Corre `limpieza_bd.py` → genera `bd_limpia.xlsx`
4. Corre `cruze_y_validacion.py` → genera `carga_leads.xlsx` (este es el que importas)

Los archivos intermedios se borran automáticamente para no dejar mugre.

## ⚠️ Notas

- Los números de teléfono se limpian automáticamente (máximo 11 dígitos)
- Los duplicados se filtran comparando números de teléfono
- Las etiquetas de leads incluyen la fecha del día de la carga

---

*Hecho con ☕ para automatizar cosas aburridas*
