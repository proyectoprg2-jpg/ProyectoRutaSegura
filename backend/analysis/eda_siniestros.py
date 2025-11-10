"""
Análisis Exploratorio de Datos (EDA)
Sistema de Siniestros Viales - La Rioja
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# =================================================
# 1. CARGA DE DATOS
# =================================================

def cargar_datos():
    """Carga todos los CSVs"""
    print(" Cargando datos...")
    
    avenidas = pd.read_csv('AVENIDAS.csv')
    tipos = pd.read_csv('TIPOS_SINIESTRO.csv')
    usuarios = pd.read_csv('USUARIOS.csv')
    siniestros = pd.read_csv('SINIESTROS.csv')
    vehiculos = pd.read_csv('VEHICULOS_INVOLUCRADOS.csv')
    
    # Convertir tipos de datos
    siniestros['fecha'] = pd.to_datetime(siniestros['fecha'])
    siniestros['es_fin_de_semana'] = siniestros['es_fin_de_semana'].map({'False': False, 'True': True})
    vehiculos['es_fallecido'] = vehiculos['es_fallecido'].map({'False': False, 'True': True})
    
    print(f"  ✓ Avenidas: {len(avenidas)} registros")
    print(f"  ✓ Tipos de siniestro: {len(tipos)} registros")
    print(f"  ✓ Siniestros: {len(siniestros)} registros")
    print(f"  ✓ Vehículos: {len(vehiculos)} registros")
    
    return avenidas, tipos, usuarios, siniestros, vehiculos

# =================================================
# 2. ANÁLISIS DESCRIPTIVO
# =================================================

def analisis_descriptivo(siniestros, vehiculos):
    """Estadísticas descriptivas generales"""
    print("\n" + "="*60)
    print(" ANÁLISIS DESCRIPTIVO GENERAL")
    print("="*60)
    
    # Período de análisis
    print(f"\n Período: {siniestros['fecha'].min()} a {siniestros['fecha'].max()}")
    
    # Totales
    print(f"\n Total de siniestros: {len(siniestros)}")
    print(f" Total de fallecidos: {siniestros['victimas_fatales'].sum()}")
    print(f" Total de heridos: {siniestros['heridos'].sum()}")
    print(f" Total de vehículos involucrados: {len(vehiculos)}")
    
    # Promedios
    print(f"\n Promedio de siniestros por mes: {len(siniestros)/6:.2f}")
    print(f" Promedio de víctimas por siniestro: {(siniestros['victimas_fatales'].sum() + siniestros['heridos'].sum())/len(siniestros):.2f}")
    
    # Por gravedad
    print("\n Distribución por gravedad:")
    print(siniestros['nivel_gravedad'].value_counts().to_string())
    
    # Fin de semana vs entre semana
    print("\n Siniestros en fin de semana:")
    fin_semana = siniestros['es_fin_de_semana'].sum()
    print(f"  Fin de semana: {fin_semana} ({fin_semana/len(siniestros)*100:.1f}%)")
    print(f"  Entre semana: {len(siniestros)-fin_semana} ({(len(siniestros)-fin_semana)/len(siniestros)*100:.1f}%)")

# =================================================
# 3. ANÁLISIS POR UBICACIÓN
# =================================================

def analisis_ubicacion(siniestros, avenidas):
    """Análisis por zona y avenida"""
    print("\n" + "="*60)
    print(" ANÁLISIS POR UBICACIÓN")
    print("="*60)
    
    # Merge con avenidas
    df = siniestros.merge(avenidas, left_on='avenida_id', right_on='id', suffixes=('', '_av'))
    
    # Top 5 avenidas más peligrosas
    print("\n TOP 5 AVENIDAS MÁS PELIGROSAS:")
    top_avenidas = df.groupby('nombre').agg({
        'id': 'count',
        'victimas_fatales': 'sum',
        'heridos': 'sum'
    }).rename(columns={'id': 'total_siniestros'})
    top_avenidas['total_victimas'] = top_avenidas['victimas_fatales'] + top_avenidas['heridos']
    top_avenidas = top_avenidas.sort_values('total_victimas', ascending=False).head()
    print(top_avenidas.to_string())
    
    # Por zona
    print("\n SINIESTROS POR ZONA:")
    por_zona = df.groupby('zona').agg({
        'id': 'count',
        'victimas_fatales': 'sum',
        'heridos': 'sum'
    }).rename(columns={'id': 'total_siniestros'})
    print(por_zona.to_string())
    
    # Por tipo de vía
    print("\n SINIESTROS POR TIPO DE VÍA:")
    por_tipo = df.groupby('tipo').agg({
        'id': 'count',
        'victimas_fatales': 'sum',
        'heridos': 'sum'
    }).rename(columns={'id': 'total_siniestros'})
    print(por_tipo.to_string())
    
    return df

# =================================================
# 4. ANÁLISIS TEMPORAL
# =================================================

def analisis_temporal(siniestros):
    """Análisis de patrones temporales"""
    print("\n" + "="*60)
    print(" ANÁLISIS TEMPORAL")
    print("="*60)
    
    # Por mes
    siniestros['mes'] = siniestros['fecha'].dt.month
    siniestros['mes_nombre'] = siniestros['fecha'].dt.strftime('%B')
    
    print("\n SINIESTROS POR MES:")
    por_mes = siniestros.groupby('mes_nombre').agg({
        'id': 'count',
        'victimas_fatales': 'sum',
        'heridos': 'sum'
    }).rename(columns={'id': 'total'})
    print(por_mes.to_string())
    
    # Por día de la semana
    print("\n SINIESTROS POR DÍA DE LA SEMANA:")
    por_dia = siniestros.groupby('dia_semana').agg({
        'id': 'count',
        'victimas_fatales': 'sum',
        'heridos': 'sum'
    }).rename(columns={'id': 'total'})
    print(por_dia.to_string())
    
    # Por hora
    siniestros['hora_num'] = pd.to_datetime(siniestros['hora'], format='%H:%M').dt.hour
    
    print("\n HORARIOS MÁS CRÍTICOS:")
    por_hora = siniestros.groupby('hora_num')['id'].count().sort_values(ascending=False).head(5)
    print(por_hora.to_string())

# =================================================
# 5. ANÁLISIS DE VEHÍCULOS
# =================================================

def analisis_vehiculos(vehiculos, siniestros):
    """Análisis de tipos de vehículos"""
    print("\n" + "="*60)
    print(" ANÁLISIS DE VEHÍCULOS INVOLUCRADOS")
    print("="*60)
    
    # Por tipo de vehículo
    print("\n VEHÍCULOS POR TIPO:")
    por_tipo = vehiculos.groupby('tipo_vehiculo').agg({
        'vehiculo_id': 'count',
        'es_fallecido': 'sum'
    }).rename(columns={'vehiculo_id': 'total', 'es_fallecido': 'fallecidos'})
    por_tipo['tasa_mortalidad_%'] = (por_tipo['fallecidos'] / por_tipo['total'] * 100).round(2)
    print(por_tipo.sort_values('total', ascending=False).to_string())
    
    # Marcas más involucradas
    print("\n TOP 10 MARCAS MÁS INVOLUCRADAS:")
    top_marcas = vehiculos[vehiculos['tipo_vehiculo'].isin(['auto', 'camion', 'camioneta'])]
    top_marcas = top_marcas['marca'].value_counts().head(10)
    print(top_marcas.to_string())

# =================================================
# 6. VISUALIZACIONES
# =================================================

def crear_visualizaciones(siniestros, avenidas, vehiculos):
    """Genera gráficos de análisis"""
    print("\n Generando visualizaciones...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Análisis de Siniestros Viales - La Rioja 2024', fontsize=16, fontweight='bold')
    
    # 1. Siniestros por mes
    siniestros['mes'] = siniestros['fecha'].dt.month
    mes_count = siniestros.groupby('mes').size()
    axes[0, 0].bar(mes_count.index, mes_count.values, color='steelblue')
    axes[0, 0].set_title('Siniestros por Mes', fontweight='bold')
    axes[0, 0].set_xlabel('Mes')
    axes[0, 0].set_ylabel('Cantidad')
    axes[0, 0].set_xticks(range(1, 7))
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # 2. Distribución por gravedad
    gravedad_count = siniestros['nivel_gravedad'].value_counts()
    colors = {'alta': '#d62728', 'media': '#ff7f0e', 'baja': '#2ca02c'}
    axes[0, 1].pie(gravedad_count.values, labels=gravedad_count.index, 
                   autopct='%1.1f%%', colors=[colors[g] for g in gravedad_count.index],
                   startangle=90)
    axes[0, 1].set_title('Distribución por Gravedad', fontweight='bold')
    
    # 3. Top 5 avenidas
    df = siniestros.merge(avenidas, left_on='avenida_id', right_on='id')
    top5 = df['nombre'].value_counts().head(5)
    axes[1, 0].barh(top5.index, top5.values, color='coral')
    axes[1, 0].set_title('Top 5 Avenidas con Más Siniestros', fontweight='bold')
    axes[1, 0].set_xlabel('Cantidad')
    axes[1, 0].invert_yaxis()
    
    # 4. Vehículos involucrados por tipo
    vehiculos_count = vehiculos['tipo_vehiculo'].value_counts().head(6)
    axes[1, 1].bar(range(len(vehiculos_count)), vehiculos_count.values, color='teal')
    axes[1, 1].set_title('Vehículos Más Involucrados', fontweight='bold')
    axes[1, 1].set_xticks(range(len(vehiculos_count)))
    axes[1, 1].set_xticklabels(vehiculos_count.index, rotation=45, ha='right')
    axes[1, 1].set_ylabel('Cantidad')
    
    plt.tight_layout()
    plt.savefig('analisis_siniestros.png', dpi=300, bbox_inches='tight')
    print("  ✓ Gráfico guardado: analisis_siniestros.png")
    plt.show()

# =================================================
# 7. INSIGHTS Y RECOMENDACIONES
# =================================================

def generar_insights(siniestros, avenidas, vehiculos):
    """Genera insights clave del análisis"""
    print("\n" + "="*60)
    print(" INSIGHTS Y HALLAZGOS CLAVE")
    print("="*60)
    
    df = siniestros.merge(avenidas, left_on='avenida_id', right_on='id')
    
    # Avenida más peligrosa
    avenida_peligrosa = df.groupby('nombre')['victimas_fatales'].sum().idxmax()
    fallecidos_av = df.groupby('nombre')['victimas_fatales'].sum().max()
    
    print(f"\n Zona crítica: '{avenida_peligrosa}' con {fallecidos_av} fallecidos")
    
    # Horario más peligroso
    df['hora_num'] = pd.to_datetime(df['hora'], format='%H:%M').dt.hour
    hora_critica = df.groupby('hora_num').size().idxmax()
    print(f" Horario más crítico: {hora_critica}:00 hrs")
    
    # Día más peligroso
    dia_critico = df['dia_semana'].value_counts().idxmax()
    print(f" Día más peligroso: {dia_critico}")
    
    # Tipo de siniestro más mortal
    tipo_mortal = df.groupby('tipo_id')['victimas_fatales'].sum().idxmax()
    print(f" Tipo más mortal: Tipo #{tipo_mortal}")
    
    # Vehículo con mayor tasa de mortalidad
    vehiculos_mortalidad = vehiculos.groupby('tipo_vehiculo').agg({
        'vehiculo_id': 'count',
        'es_fallecido': 'sum'
    })
    vehiculos_mortalidad['tasa'] = vehiculos_mortalidad['es_fallecido'] / vehiculos_mortalidad['vehiculo_id'] * 100
    vehiculo_peligroso = vehiculos_mortalidad['tasa'].idxmax()
    tasa = vehiculos_mortalidad['tasa'].max()
    print(f" Vehículo con mayor mortalidad: {vehiculo_peligroso} ({tasa:.1f}%)")
    
    print("\n RECOMENDACIONES:")
    print("  1. Reforzar controles en Av. Peron y Ruta 38")
    print("  2. Intensificar patrullaje en horario pico (7-9 AM y 5-7 PM)")
    print("  3. Campañas de seguridad vial enfocadas en vuelcos")
    print("  4. Mayor control de velocidad en rutas provinciales")
    print("  5. Mejorar señalización en zonas de alto riesgo")

# =================================================
# FUNCIÓN PRINCIPAL
# =================================================

def main():
    """Ejecuta todo el análisis"""
    print("="*60)
    print("  ANÁLISIS EXPLORATORIO DE DATOS")
    print("  Sistema de Siniestros Viales - La Rioja")
    print("="*60)
    
    # Cargar datos
    avenidas, tipos, usuarios, siniestros, vehiculos = cargar_datos()
    
    # Análisis descriptivo
    analisis_descriptivo(siniestros, vehiculos)
    
    # Análisis por ubicación
    df_ubicacion = analisis_ubicacion(siniestros, avenidas)
    
    # Análisis temporal
    analisis_temporal(siniestros)
    
    # Análisis de vehículos
    analisis_vehiculos(vehiculos, siniestros)
    
    # Visualizaciones
    crear_visualizaciones(siniestros, avenidas, vehiculos)
    
    # Insights
    generar_insights(siniestros, avenidas, vehiculos)
    
    print("\n" + "="*60)
    print("  ✓ ANÁLISIS COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()