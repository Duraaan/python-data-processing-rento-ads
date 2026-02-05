import pandas as pd
import re
import os
from pathlib import Path

# --- CONFIGURACIÓN ---
CARPETA_LISTAS = Path(r"C:\Users\__Duraaan\Desktop\python\listas")
ARCHIVO_SALIDA = "extraccion.xlsx"

COL_FECHA = "Hora de envío: GMT-03:00"
COL_TELEFONO = "Número de teléfono"
COL_EMAIL = "Correo electrónico"
COL_FULL = "Nombre completo"
COL_FIRST = "Nombre"
COL_LAST = "Apellidos"

def limpiar_numero(texto):
    """Extrae solo dígitos y valida que no exceda los 11 caracteres."""
    if pd.isna(texto) or str(texto).strip() == '': 
        return ""
    numeros = "".join(re.findall(r'\d+', str(texto)))
    return numeros if len(numeros) <= 11 else ""

def procesar_archivo(ruta):
    try:
        df = pd.read_excel(ruta)
        if COL_FECHA not in df.columns:
            print(f"⚠️ El archivo {ruta.name} no tiene la columna de fecha. Se saltará.")
            return None
        
        temp_df = pd.DataFrame()
        temp_df['fecha'] = pd.to_datetime(df[COL_FECHA], errors='coerce')
        temp_df['email'] = df[COL_EMAIL].fillna('') if COL_EMAIL in df.columns else ""
        temp_df['numero'] = df[COL_TELEFONO].apply(limpiar_numero) if COL_TELEFONO in df.columns else ""
        
        # Lógica de nombres estandarizada
        if COL_FULL in df.columns:
            temp_df['full_name'] = df[COL_FULL].fillna('')
            temp_df['first_name'] = temp_df['full_name'].astype(str).str.split().str[0]
        elif COL_FIRST in df.columns and COL_LAST in df.columns:
            temp_df['first_name'] = df[COL_FIRST].fillna('')
            temp_df['full_name'] = temp_df['first_name'].astype(str) + " " + df[COL_LAST].fillna('').astype(str)
        else:
            temp_df['first_name'] = ""
            temp_df['full_name'] = ""
        
        return temp_df
    except Exception as e:
        print(f"⚠️ Error procesando {ruta.name}: {e}")
        return None

if __name__ == "__main__":
    f_inicio = input("📅 Fecha inicio (AAAA-MM-DD): ")
    f_fin = input("📅 Fecha fin (AAAA-MM-DD): ")

    # Obtener lista de archivos excel
    archivos = list(CARPETA_LISTAS.glob("*.xlsx"))
    
    if not archivos:
        print("❌ No se encontraron archivos .xlsx en la carpeta de listas.")
    else:
        listas_procesadas = []
        for a in archivos:
            res = procesar_archivo(a)
            if res is not None:
                listas_procesadas.append(res)

        if listas_procesadas:
            df_unido = pd.concat(listas_procesadas, ignore_index=True).dropna(subset=['fecha'])
            df_unido = df_unido[df_unido['numero'] != ""] # Filtro estricto
            
            # Filtro de rango de tiempo
            inicio = pd.to_datetime(f_inicio)
            fin = pd.to_datetime(f_fin) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            
            resultado = df_unido[(df_unido['fecha'] >= inicio) & (df_unido['fecha'] <= fin)].copy()
            
            if not resultado.empty:
                resultado = resultado.sort_values(by='fecha')
                resultado['fecha'] = resultado['fecha'].dt.strftime('%Y-%m-%d %H:%M')
                resultado = resultado[['fecha', 'email', 'numero', 'first_name', 'full_name']]
                
                # Guardar el extracto consolidado
                resultado.to_excel(ARCHIVO_SALIDA, index=False)
                print(f"✅ EXTRACCIÓN COMPLETADA. Registros: {len(resultado)}")

                # --- LIMPIEZA DE LOS ARCHIVOS ORIGINALES ---
                print("🧹 Borrando archivos originales de la carpeta 'listas'...")
                for a in archivos:
                    try:
                        os.remove(a)
                    except Exception as e:
                        print(f"⚠️ No se pudo borrar {a.name}: {e}")
                print("✨ Carpeta de listas limpia.")
            else:
                print("❌ No se encontraron registros en ese rango. No se borraron los archivos originales.")
        else:
            print("❌ No se pudo procesar ningún archivo válido.")