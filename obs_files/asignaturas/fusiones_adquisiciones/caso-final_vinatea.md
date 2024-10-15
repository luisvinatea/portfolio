# Análisis de Fusión en la Industria High-Tech: Solucionando el Caso de Nicolas y Gabriela con Datos Reales de la Bolsa

## Resumen de las Empresas Seleccionadas

En esta sección, presentamos un resumen de las principales empresas tecnológicas, sus actividades, y algunos indicadores financieros clave extraídos de Yahoo Finance. Todas las empresas seleccionadas tienen una fuerte presencia internacional y operan en la industria High-Tech, enfrentando una mezcla de desafíos y oportunidades. A continuación, se muestra un breve perfil financiero de estas empresas:

| Ticker | Nombre                | Sector                | Industria                         | Precio Actual (USD) | Capitalización de Mercado (USD) | PER       |
|--------|-----------------------|-----------------------|-----------------------------------|---------------------|----------------------------------|-----------|
| AAPL   | Apple Inc.            | Technology            | Consumer Electronics             | 231.30              | 3,516,708,421,632               | 35.15     |
| MSFT   | Microsoft Corporation | Technology            | Software - Infrastructure         | 419.14              | 3,115,484,446,720               | 35.34     |
| GOOGL  | Alphabet Inc.         | Communication Services| Internet Content & Information   | 164.96              | 2,016,751,517,696               | 23.63     |
| AMZN   | Amazon.com, Inc.      | Consumer Cyclical     | Internet Retail                  | 187.54              | 1,968,344,662,016               | 44.76     |
| META   | Meta Platforms, Inc.  | Communication Services| Internet Content & Information   | 590.42              | 1,493,656,272,896               | 30.23     |
| NFLX   | Netflix, Inc.         | Communication Services| Entertainment                    | 713.00              | 305,994,629,120                 | 44.42     |
| TSLA   | Tesla, Inc.           | Consumer Cyclical     | Auto Manufacturers               | 219.16              | 700,137,275,392                 | 61.74     |
| NVDA   | NVIDIA Corporation    | Technology            | Semiconductors                   | 138.07              | 3,386,857,226,240               | 64.82     |

**Tasa de Crecimiento Estimada:**
- Apple (AAPL): 0.21 USD/día
- Microsoft (MSFT): 0.32 USD/día
- Alphabet (GOOGL): 0.18 USD/día
- Amazon (AMZN): 0.21 USD/día
- Meta (META): 0.99 USD/día
- Netflix (NFLX): 1.18 USD/día
- Tesla (TSLA): -0.00 USD/día
- NVIDIA (NVDA): 0.39 USD/día

Adjuntamos a continuación dos gráficos que muestran la evolución de los precios de las acciones de Meta y Netflix en el último año:

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/meta.png)

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/nflx.png)

## Propuesta de Operación Corporativa

### Fusión Estratégica

Proponemos una operación de fusión estratégica entre Meta (META) y Netflix (NFLX), basada en los resultados del análisis de crecimiento y beneficio por acción (BPA). Esta operación tiene como objetivo combinar las fortalezas de ambas empresas para maximizar el valor para los accionistas.

```

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

```

### Cálculos y Resultados de la Fusión

A continuación, presentamos los cálculos de las ganancias combinadas y el BPA resultante de la fusión entre Meta y Netflix:


**Fusión entre META y NFLX (2024)**
- Ganancias Combinadas: 6690.21 millones USD
- Impacto Sinergias: 66.90 millones USD
- Ganancias Totales: 6732.11 millones USD
- BPA Nicolas (€ p.a.): 0.99
- BPA Gabriela (€ p.a.): 1.18
- BPA Combinada (€ p.a.): 1.12
- Market Cap Nicolas: 1,180,839.97 millones USD
- Market Cap Gabriela: 2,852,000.00 millones USD
- PER Nicolas: 598.69
- PER Gabriela: 604.51

**Fusión entre META y NFLX (2025)**
- Ganancias Combinadas: 7359.23 millones USD
- Impacto Sinergias: 147.18 millones USD
- Ganancias Totales: 7481.42 millones USD
- BPA Nicolas (€ p.a.): 0.99
- BPA Gabriela (€ p.a.): 1.18
- BPA Combinada (€ p.a.): 1.25
- Market Cap Nicolas: 1,180,839.97 millones USD
- Market Cap Gabriela: 2,852,000.00 millones USD
- PER Nicolas: 598.69
- PER Gabriela: 604.51

#### Sentido Estratégico y Financiero

La fusión entre Meta y Netflix ofrece una sinergia significativa en términos de contenido digital y redes sociales, aprovechando el alcance global y las capacidades tecnológicas de ambas. La fusión podría:
- Fortalecer la presencia en el mercado de entretenimiento y aumentar el consumo de contenido en plataformas digitales.
- Mejorar la monetización a través de sinergias y mejorar la oferta publicitaria de ambas plataformas.

**Impacto en el BPA Combinado**:
- La fusión muestra un BPA combinado notablemente superior al BPA individual de cada empresa, sugiriendo una creación de valor significativa para los accionistas.
- Las sinergias proyectadas del 1% al 2% de los ingresos combinados para 2024 y 2025 generan un impacto positivo que mejora los beneficios totales de la fusión.

**Conclusiones Estratégicas**

- **Fusiones Beneficiosas:** Las fusiones entre empresas con altos BPA y tasas de crecimiento como Meta y Netflix tienden a ser las más prometedoras para maximizar el valor para los accionistas.
- **Fusiones a Evitar:** Fusiones que involucran a Tesla presentan valores bajos o incluso negativos en el BPA combinado, lo cual podría afectar negativamente el valor para los accionistas.

En resumen, las fusiones más atractivas son aquellas que incluyen empresas con un alto BPA y tasas de crecimiento significativas, tales como Meta y Netflix. Esto destaca la importancia de considerar tanto las sinergias como el crecimiento individual antes de proponer una fusión o adquisición.

En el apéndice, presentamos los resultados que obtuvimos para todas las compañías, así como los otros gráficos de acciones.


### Referencias

- Yahoo Finance API. (n.d.). Retrieved from https://www.yahoofinance.com

## Apéndice - Resultados de la Simulación de Fusiones y Gráficos Adicionales

### Simulación para Todos los Escenarios

A continuación, se presentan los resultados de la simulación de fusiones para todas las combinaciones de las principales empresas tecnológicas seleccionadas. Los cálculos incluyen ganancias combinadas, impacto de sinergias, BPA combinado, y otras métricas relevantes para los años 2024 y 2025.

## Fusión entre AAPL y MSFT

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1714.92 | 17.15 | 1707.07 | 0.21 | 0.32 | 0.28 | 462600.01 | 1676560.06 | 1078.61 | 1303.67 |
| 2025 | 1886.41 | 37.73 | 1899.14 | 0.21 | 0.32 | 0.32 | 462600.01 | 1676560.06 | 1078.61 | 1303.67 |

## Fusión entre AAPL y GOOGL

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1160.50 | 11.61 | 1147.11 | 0.21 | 0.18 | 0.19 | 462600.01 | 659840.03 | 1078.61 | 901.89 |
| 2025 | 1276.55 | 25.53 | 1277.08 | 0.21 | 0.18 | 0.21 | 462600.01 | 659840.03 | 1078.61 | 901.89 |

## Fusión entre AAPL y AMZN

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1252.51 | 12.53 | 1240.04 | 0.21 | 0.21 | 0.21 | 462600.01 | 750159.97 | 1078.61 | 910.80 |
| 2025 | 1377.76 | 27.56 | 1380.32 | 0.21 | 0.21 | 0.23 | 462600.01 | 750159.97 | 1078.61 | 910.80 |

## Fusión entre AAPL y META

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 4373.63 | 43.74 | 4392.36 | 0.21 | 0.99 | 0.73 | 462600.01 | 2361679.93 | 1078.61 | 598.69 |
| 2025 | 4810.99 | 96.22 | 4882.21 | 0.21 | 0.99 | 0.81 | 462600.01 | 2361679.93 | 1078.61 | 598.69 |

## Fusión entre AAPL y NFLX

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 5146.73 | 51.47 | 5173.19 | 0.21 | 1.18 | 0.86 | 462600.01 | 2852000.00 | 1078.61 | 604.51 |
| 2025 | 5661.40 | 113.23 | 5749.63 | 0.21 | 1.18 | 0.96 | 462600.01 | 2852000.00 | 1078.61 | 604.51 |

## Fusión entre AAPL y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 418.90 | 4.19 | 398.09 | 0.21 | -0.00 | 0.07 | 462600.01 | 876640.01 | 1078.61 | -87808.43 |
| 2025 | 460.79 | 9.22 | 445.01 | 0.21 | -0.00 | 0.07 | 462600.01 | 876640.01 | 1078.61 | -87808.43 |

## Fusión entre AAPL y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1995.62 | 19.96 | 1990.57 | 0.21 | 0.39 | 0.33 | 462600.01 | 552280.03 | 1078.61 | 352.50 |
| 2025 | 2195.18 | 43.90 | 2214.08 | 0.21 | 0.39 | 0.37 | 462600.01 | 552280.03 | 1078.61 | 352.50 |

## Fusión entre MSFT y GOOGL

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1374.63 | 13.75 | 1363.38 | 0.32 | 0.18 | 0.23 | 838280.03 | 659840.03 | 1303.67 | 901.89 |
| 2025 | 1512.10 | 30.24 | 1517.34 | 0.32 | 0.18 | 0.25 | 838280.03 | 659840.03 | 1303.67 | 901.89 |

## Fusión entre MSFT y AMZN

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1466.65 | 14.67 | 1456.31 | 0.32 | 0.21 | 0.24 | 838280.03 | 750159.97 | 1303.67 | 910.80 |
| 2025 | 1613.31 | 32.27 | 1620.58 | 0.32 | 0.21 | 0.27 | 838280.03 | 750159.97 | 1303.67 | 910.80 |


## Fusión entre MSFT y META

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 4587.76 | 45.88 | 4608.64 | 0.32 | 0.99 | 0.77 | 838280.03 | 2361679.93 | 1303.67 | 598.69 |
| 2025 | 5046.54 | 100.93 | 5122.47 | 0.32 | 0.99 | 0.85 | 838280.03 | 2361679.93 | 1303.67 | 598.69 |

## Fusión entre MSFT y NFLX

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 5360.86 | 53.61 | 5389.47 | 0.32 | 1.18 | 0.90 | 838280.03 | 2852000.00 | 1303.67 | 604.51 |
| 2025 | 5896.94 | 117.94 | 5989.88 | 0.32 | 1.18 | 1.00 | 838280.03 | 2852000.00 | 1303.67 | 604.51 |

## Fusión entre MSFT y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 633.03 | 6.33 | 614.36 | 0.32 | -0.00 | 0.10 | 838280.03 | 876640.01 | 1303.67 | -87808.43 |
| 2025 | 696.34 | 13.93 | 685.26 | 0.32 | -0.00 | 0.11 | 838280.03 | 876640.01 | 1303.67 | -87808.43 |

## Fusión entre MSFT y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 2209.75 | 22.10 | 2206.85 | 0.32 | 0.39 | 0.37 | 838280.03 | 552280.03 | 1303.67 | 352.50 |
| 2025 | 2430.73 | 48.61 | 2454.34 | 0.32 | 0.39 | 0.41 | 838280.03 | 552280.03 | 1303.67 | 352.50 |

## Fusión entre GOOGL y AMZN

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1189.44 | 11.89 | 1176.33 | 0.18 | 0.21 | 0.20 | 329920.01 | 750159.97 | 901.89 | 910.80 |
| 2025 | 1308.38 | 26.17 | 1309.55 | 0.18 | 0.21 | 0.22 | 329920.01 | 750159.97 | 901.89 | 910.80 |

## Fusión entre GOOGL y META

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 4310.55 | 43.11 | 4328.66 | 0.18 | 0.99 | 0.72 | 329920.01 | 2361679.93 | 901.89 | 598.69 |
| 2025 | 4741.61 | 94.83 | 4811.44 | 0.18 | 0.99 | 0.80 | 329920.01 | 2361679.93 | 901.89 | 598.69 |

## Fusión entre GOOGL y NFLX

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 5083.65 | 50.84 | 5109.49 | 0.18 | 1.18 | 0.85 | 329920.01 | 2852000.00 | 901.89 | 604.51 |
| 2025 | 5592.01 | 111.84 | 5678.85 | 0.18 | 1.18 | 0.95 | 329920.01 | 2852000.00 | 901.89 | 604.51 |

## Fusión entre GOOGL y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 355.82 | 3.56 | 334.38 | 0.18 | -0.00 | 0.06 | 329920.01 | 876640.01 | 901.89 | -87808.43 |
| 2025 | 391.41 | 7.83 | 374.24 | 0.18 | -0.00 | 0.06 | 329920.01 | 876640.01 | 901.89 | -87808.43 |

## Fusión entre GOOGL y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1932.54 | 19.33 | 1926.87 | 0.18 | 0.39 | 0.32 | 329920.01 | 552280.03 | 901.89 | 352.50 |
| 2025 | 2125.80 | 42.52 | 2143.31 | 0.18 | 0.39 | 0.36 | 329920.01 | 552280.03 | 901.89 | 352.50 |

## Fusión entre AMZN y META

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 4356.56 | 43.57 | 4375.12 | 0.21 | 0.99 | 0.73 | 375079.99 | 2361679.93 | 910.80 | 598.69 |
| 2025 | 4792.21 | 95.84 | 4863.06 | 0.21 | 0.99 | 0.81 | 375079.99 | 2361679.93 | 910.80 | 598.69 |

## Fusión entre AMZN y NFLX

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 5129.66 | 51.30 | 5155.95 | 0.21 | 1.18 | 0.86 | 375079.99 | 2852000.00 | 910.80 | 604.51 |
| 2025 | 5642.62 | 112.85 | 5730.47 | 0.21 | 1.18 | 0.96 | 375079.99 | 2852000.00 | 910.80 | 604.51 |

## Fusión entre AMZN y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 401.83 | 4.02 | 380.85 | 0.21 | -0.00 | 0.06 | 375079.99 | 876640.01 | 910.80 | -87808.43 |
| 2025 | 442.01 | 8.84 | 425.85 | 0.21 | -0.00 | 0.07 | 375079.99 | 876640.01 | 910.80 | -87808.43 |

## Fusión entre AMZN y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1978.55 | 19.79 | 1973.33 | 0.21 | 0.39 | 0.33 | 375079.99 | 552280.03 | 910.80 | 352.50 |
| 2025 | 2176.40 | 43.53 | 2194.93 | 0.21 | 0.39 | 0.37 | 375079.99 | 552280.03 | 910.80 | 352.50 |

## Fusión entre META y NFLX

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 6690.21 | 66.90 | 6732.11 | 0.99 | 1.18 | 1.12 | 1180839.97 | 2852000.00 | 598.69 | 604.51 |
| 2025 | 7359.23 | 147.18 | 7481.42 | 0.99 | 1.18 | 1.25 | 1180839.97 | 2852000.00 | 598.69 | 604.51 |

## Fusión entre META y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1962.39 | 19.62 | 1957.01 | 0.99 | -0.00 | 0.33 | 1180839.97 | 876640.01 | 598.69 | -87808.43 |
| 2025 | 2158.63 | 43.17 | 2176.80 | 0.99 | -0.00 | 0.36 | 1180839.97 | 876640.01 | 598.69 | -87808.43 |

## Fusión entre META y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 3539.11 | 35.39 | 3549.50 | 0.99 | 0.39 | 0.59 | 1180839.97 | 552280.03 | 598.69 | 352.50 |
| 2025 | 3893.02 | 77.86 | 3945.88 | 0.99 | 0.39 | 0.66 | 1180839.97 | 552280.03 | 598.69 | 352.50 |

## Fusión entre NFLX y TSLA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 2348.94 | 23.49 | 2347.43 | 1.18 | -0.00 | 0.39 | 1426000.00 | 876640.01 | 604.51 | -87808.43 |
| 2025 | 2583.83 | 51.68 | 2610.51 | 1.18 | -0.00 | 0.44 | 1426000.00 | 876640.01 | 604.51 | -87808.43 |

## Fusión entre NFLX y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 3925.65 | 39.26 | 3939.91 | 1.18 | 0.39 | 0.66 | 1426000.00 | 552280.03 | 604.51 | 352.50 |
| 2025 | 4318.22 | 86.36 | 4379.58 | 1.18 | 0.39 | 0.73 | 1426000.00 | 552280.03 | 604.51 | 352.50 |

## Fusión entre TSLA y NVDA

| Año | Ganancias Combinadas (millones) | Impacto Sinergias (millones) | Ganancias Totales (millones) | BPA Nicolas (€ p.a.) | BPA Gabriela (€ p.a.) | BPA Combinada (€ p.a.) | Market Cap Nicolas (millones) | Market Cap Gabriela (millones) | PER Nicolas | PER Gabriela |
|-----|---------------------------------|-----------------------------|-----------------------------|-----------------------|-----------------------|------------------------|--------------------------------|--------------------------------|-------------|--------------|
| 2024 | 1561.74 | 15.62 | 1552.36 | -0.00 | 0.39 | 0.26 | 438320.01 | 552280.03 | -87808.43 | 352.50 |
| 2025 | 1717.92 | 34.36 | 1727.27 | -0.00 | 0.39 | 0.29 | 438320.01 | 552280.03 | -87808.43 | 352.50 |

### Gráficos Adicionales

Los siguientes gráficos muestran la evolución de los precios de las acciones de otras compañías en el último año:

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/amzn.png)

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/googl.png)

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/msft.png)

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/nvda.png)

![](/home/luisvinatea/Dev/portfolio/obs_files/asignaturas/fusiones_adquisiciones/tsla.png)
