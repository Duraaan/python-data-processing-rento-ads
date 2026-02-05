import pandas as pd
import os
from datetime import datetime
from pathlib import Path

# --- CONFIGURACIÓN ---
ARCHIVO_EXTRACCION = "extraccion.xlsx"
ARCHIVO_BD_LIMPIA = "bd_limpia.xlsx"
ARCHIVO_FINAL_CARGA = "carga_leads.xlsx"

def generar_script_carga():
    try:
        print("⏳ Iniciando cruce de datos...")
        
        # Validar existencia de archivos necesarios
        path_extraccion = Path(ARCHIVO_EXTRACCION)
        path_bd = Path(ARCHIVO_BD_LIMPIA)

        if not path_extraccion.exists() or not path_bd.exists():
            print("❌ Faltan archivos de entrada (extraccion.xlsx o bd_limpia.xlsx).")
            return

        # Carga de datos
        df_listas = pd.read_excel(ARCHIVO_EXTRACCION)
        df_bd = pd.read_excel(ARCHIVO_BD_LIMPIA)

        # Normalizar números para comparación
        df_listas['numero'] = df_listas['numero'].astype(str)
        df_bd['numero'] = df_bd['numero'].astype(str)

        # Filtrar los que NO están en la BD maestra
        numeros_en_bd = set(df_bd['numero'].tolist())
        df_nuevos = df_listas[~df_listas['numero'].isin(numeros_en_bd)].copy()

        if df_nuevos.empty:
            print("🙌 No hay leads nuevos para cargar.")
            # Si no hay nuevos, igual borramos la extracción para no procesarla mañana por error
            os.remove(ARCHIVO_EXTRACCION)
            return

        # Construcción del DataFrame final
        df_final = pd.DataFrame({
            'E-mail priv.': df_nuevos['email'],
            'Teléfono celular': df_nuevos['numero'],
            'Nombre del lead': df_nuevos['first_name'],
            'Nombre completo': df_nuevos['full_name'],
            'Etiqueta del lead': f"ADS, CargaGoogle",
            'Usuario responsable': "Rento arriendos",
            'Etapa del lead': "Carga manual"
        })

        # Guardar el archivo que te interesa
        df_final.to_excel(ARCHIVO_FINAL_CARGA, index=False)
        print(f"✅ ARCHIVO LISTO: {ARCHIVO_FINAL_CARGA}")

        # --- LIMPIEZA DE ARCHIVOS BASURA ---
        print("🧹 Limpiando archivos temporales...")
        if path_extraccion.exists():
            os.remove(ARCHIVO_EXTRACCION)
        if path_bd.exists():
            os.remove(ARCHIVO_BD_LIMPIA)
        
        print("✨ Proceso finalizado.")

    except Exception as e:
        print(f"❌ Error en el cruce: {e}")

if __name__ == "__main__":
    generar_script_carga()