import pandas as pd
import re
from pathlib import Path

# --- CONFIGURACIÓN ---
RUTA_BD_ORIGEN = Path(r"C:\Users\__Duraaan\Desktop\python\bd.xlsx")
ARCHIVO_SALIDA = "bd_limpia.xlsx"

COL_NOMBRE = 'Contacto principal'
COL_OFICINA = 'Teléfono oficina (contacto)'
COL_CELULAR = 'Teléfono celular (contacto)'
COL_NUMERO_LIMPIO = 'numero'

def limpiar_numero(texto):
    """Extrae solo dígitos y valida que no exceda los 11 caracteres."""
    if pd.isna(texto) or str(texto).strip() == '': 
        return ""
    numeros = "".join(re.findall(r'\d+', str(texto)))
    return numeros if len(numeros) <= 11 else ""

def procesar_base_datos():
    try:
        print(f"⏳ Cargando base de datos: {RUTA_BD_ORIGEN.name}...")
        columnas_a_leer = [COL_NOMBRE, COL_OFICINA, COL_CELULAR]
        df = pd.read_excel(RUTA_BD_ORIGEN, usecols=columnas_a_leer)
        
        # Limpieza inicial de nulos y espacios
        df[COL_CELULAR] = df[COL_CELULAR].astype(str).replace('nan', '').str.strip()
        df[COL_OFICINA] = df[COL_OFICINA].astype(str).replace('nan', '').str.strip()
        
        # Prioridad Celular > Oficina
        df[COL_NUMERO_LIMPIO] = df[COL_CELULAR].where(df[COL_CELULAR] != '', df[COL_OFICINA])

        # Aplicar limpieza estricta
        df[COL_NUMERO_LIMPIO] = df[COL_NUMERO_LIMPIO].apply(limpiar_numero)
        
        # Filtrar registros sin número válido
        df_final = df[df[COL_NUMERO_LIMPIO] != ''].copy()
        df_final = df_final[[COL_NOMBRE, COL_NUMERO_LIMPIO]]

        # Exportar
        df_final.to_excel(ARCHIVO_SALIDA, index=False)
        print(f"✅ Proceso completado. Registros válidos: {len(df_final)}")
        print(f"📁 Archivo generado: {ARCHIVO_SALIDA}")

    except Exception as e:
        print(f"❌ Error al procesar la BD: {e}")

if __name__ == "__main__":
    procesar_base_datos()