import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from scipy.stats import linregress
from itertools import combinations

# Obtener una vista previa de las principales empresas tecnológicas
tech_companies = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NFLX", "TSLA", "NVDA"]


def obtener_vista_previa_empresas(empresas):
    datos_empresas = []
    for ticker in empresas:
        empresa = yf.Ticker(ticker)
        resumen = empresa.info
        # Obtener el precio de cierre más reciente para asegurar un valor actualizado
        precio_actual = (
            empresa.history(period="1d")["Close"].iloc[-1]
            if not empresa.history(period="1d").empty
            else "N/A"
        )
        datos_empresas.append(
            {
                "Ticker": ticker,
                "Nombre": resumen.get("shortName", "N/A"),
                "Sector": resumen.get("sector", "N/A"),
                "Industria": resumen.get("industry", "N/A"),
                "Precio Actual": precio_actual,
                "Capitalización de Mercado": resumen.get("marketCap", "N/A"),
                "PER": resumen.get("trailingPE", "N/A"),
            }
        )
    return pd.DataFrame(datos_empresas)


# Obtener y mostrar la vista previa de las principales empresas tecnológicas
vista_previa = obtener_vista_previa_empresas(tech_companies)
print(vista_previa)


# Obtener datos históricos de precios para una empresa específica
def obtener_datos_historicos(empresa, periodo="1y"):
    ticker = yf.Ticker(empresa)
    datos_historicos = ticker.history(period=periodo)
    if not datos_historicos.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(
            datos_historicos.index,
            datos_historicos["Close"],
            label=f"Precio de Cierre de {empresa}",
        )
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.title(f"Histórico de Precios de {empresa} ({periodo})")
        plt.legend()
        plt.grid()
        plt.show()
    return datos_historicos


# Obtener la pendiente del crecimiento de precios para estimar la tasa de crecimiento
def calcular_tasa_crecimiento(datos_historicos):
    if not datos_historicos.empty:
        x = np.arange(len(datos_historicos))
        y = datos_historicos["Close"].values
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        return slope
    return 0


# Obtener y mostrar datos históricos para todas las empresas y calcular la tasa de crecimiento
tasas_crecimiento = {}
for empresa in tech_companies:
    datos_historicos = obtener_datos_historicos(empresa, "1y")
    tasa_crecimiento = calcular_tasa_crecimiento(datos_historicos)
    tasas_crecimiento[empresa] = tasa_crecimiento
    print(
        f"Tasa de crecimiento estimada para {empresa}: {tasa_crecimiento:.2f} USD/día\n"
    )


# Cálculo de ganancias combinadas
def calculo_ganancias_combinadas(
    ganancias_2024, ganancias_2025, sinergias, costos_de_integracion, año
):
    ganancias = ganancias_2024 if año == "2024" else ganancias_2025
    ganancias_combinadas = ganancias["Nicolas"] + ganancias["Gabriela"]
    impacto_sinergias = sinergias[año] * ganancias_combinadas
    ganancias_totales = (
        ganancias_combinadas + impacto_sinergias - costos_de_integracion[año]
    )
    return ganancias_totales, ganancias_combinadas, impacto_sinergias


# Cálculo del EPS (BPA) antes y después de la fusión
def calculo_eps(
    acciones_nicolas,
    acciones_gabriela,
    precio_por_accion_nicolas,
    precio_por_accion_gabriela,
    ganancias_2024,
    ganancias_2025,
    sinergias,
    costos_de_integracion,
    año,
):
    acciones_combinadas = acciones_nicolas + acciones_gabriela
    ganancias_totales, ganancias_combinadas, impacto_sinergias = (
        calculo_ganancias_combinadas(
            ganancias_2024, ganancias_2025, sinergias, costos_de_integracion, año
        )
    )
    eps_post_fusion = ganancias_totales / acciones_combinadas
    eps_pre_fusion_nicolas = ganancias_2024["Nicolas"] / acciones_nicolas
    eps_pre_fusion_gabriela = ganancias_2024["Gabriela"] / acciones_gabriela
    market_cap_nicolas = acciones_nicolas * precio_por_accion_nicolas
    market_cap_gabriela = acciones_gabriela * precio_por_accion_gabriela
    per_nicolas = precio_por_accion_nicolas / (
        ganancias_2024["Nicolas"] / acciones_nicolas
    )
    per_gabriela = precio_por_accion_gabriela / (
        ganancias_2024["Gabriela"] / acciones_gabriela
    )

    output = (
        f"Año: {año}\n"
        f"Ganancias Combinadas: {ganancias_combinadas:.2f} millones\n"
        f"Impacto Sinergias: {impacto_sinergias:.2f} millones\n"
        f"Ganancias Totales: {ganancias_totales:.2f} millones\n"
        f"BPA Nicolas (€ p.a.): {eps_pre_fusion_nicolas:.2f}\n"
        f"BPA Gabriela (€ p.a.): {eps_pre_fusion_gabriela:.2f}\n"
        f"BPA Combinada (€ p.a.): {eps_post_fusion:.2f}\n"
        f"Market Cap Nicolas: {market_cap_nicolas:.2f} millones\n"
        f"Market Cap Gabriela: {market_cap_gabriela:.2f} millones\n"
        f"PER Nicolas: {per_nicolas:.2f}\n"
        f"PER Gabriela: {per_gabriela:.2f}\n\n"
    )
    return output


# Simulación de fusiones entre todas las combinaciones de empresas
def simular_fusiones(tech_companies, vista_previa):
    resumen_fusiones = ""
    for empresa_1, empresa_2 in combinations(tech_companies, 2):
        datos_1 = vista_previa[vista_previa["Ticker"] == empresa_1].iloc[0]
        datos_2 = vista_previa[vista_previa["Ticker"] == empresa_2].iloc[0]

        acciones_nicolas = 2000  # Utilizando un número fijo para simplificar
        acciones_gabriela = 4000
        precio_por_accion_nicolas = datos_1["Precio Actual"]
        precio_por_accion_gabriela = datos_2["Precio Actual"]
        ganancias_2024 = {
            "Nicolas": tasas_crecimiento[empresa_1] * acciones_nicolas,
            "Gabriela": tasas_crecimiento[empresa_2] * acciones_gabriela,
        }
        ganancias_2025 = {
            "Nicolas": ganancias_2024["Nicolas"] * 1.1,
            "Gabriela": ganancias_2024["Gabriela"] * 1.1,
        }  # Suposición de un 10% de crecimiento
        sinergias = {"2024": 0.01, "2025": 0.02}
        costos_de_integracion = {"2024": 25, "2025": 25}

        summary_2024 = calculo_eps(
            acciones_nicolas,
            acciones_gabriela,
            precio_por_accion_nicolas,
            precio_por_accion_gabriela,
            ganancias_2024,
            ganancias_2025,
            sinergias,
            costos_de_integracion,
            "2024",
        )
        summary_2025 = calculo_eps(
            acciones_nicolas,
            acciones_gabriela,
            precio_por_accion_nicolas,
            precio_por_accion_gabriela,
            ganancias_2024,
            ganancias_2025,
            sinergias,
            costos_de_integracion,
            "2025",
        )

        resumen_fusiones += f"Fusión entre {empresa_1} y {empresa_2}:"
        resumen_fusiones += summary_2024
        resumen_fusiones += summary_2025
        resumen_fusiones += "\n"
    return resumen_fusiones


# Ejecutar la simulación de fusiones
resumen_fusiones = simular_fusiones(tech_companies, vista_previa)
print(resumen_fusiones)


# Guardar el resumen de fusiones en un archivo de texto
def guardar_resumen_fusiones(resumen):
    with open("resumen_fusiones.txt", "w") as file:
        file.write(resumen)


# Guardar el archivo de resumen de fusiones
guardar_resumen_fusiones(resumen_fusiones)
