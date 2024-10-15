import pandas as pd
import numpy as np

# Datos del Ejercicio
acciones_nicolas = 2000  # en millones
acciones_gabriela = 4000  # en millones
precio_por_accion_nicolas = 3.5  # euros
precio_por_accion_gabriela = 4.0  # euros
ganancias_2024 = {"Nicolas": 350, "Gabriela": 1100}  # en millones
ganancias_2025 = {"Nicolas": 400, "Gabriela": 1300}  # en millones
margen_neta_nicolas = 0.07
margen_neta_gabriela = 0.10
sinergias = {"2024": 0.01, "2025": 0.02}  # porcentaje de ingreso total
costos_de_integracion = {"2024": 25, "2025": 25}  # en millones


# Cálculo de ganancias combinadas
def calculo_ganancias_combinadas(año):
    ganancias = ganancias_2024 if año == "2024" else ganancias_2025
    ganancias_combinadas = ganancias["Nicolas"] + ganancias["Gabriela"]
    impacto_sinergias = sinergias[año] * (
        ganancias_combinadas / (margen_neta_gabriela + margen_neta_nicolas)
    )
    ganancias_totales = (
        ganancias_combinadas + impacto_sinergias - costos_de_integracion[año]
    )
    return ganancias_totales, ganancias_combinadas, impacto_sinergias


# Cálculo del EPS (BPA) antes y después de la fusión
def calculo_eps(año):
    acciones_combinadas = acciones_nicolas + acciones_gabriela
    ganancias_totales, ganancias_combinadas, impacto_sinergias = (
        calculo_ganancias_combinadas(año)
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
    print(output)
    return output


# Aplicando las funciones para 2024 y 2025
summary = ""
summary += calculo_eps("2024")
summary += calculo_eps("2025")


# Cálculo de ecuación de canje para Gabriela absorbiendo a Nicolas
def ecuacion_canje_gabriela_absorbe_nicolas():
    valor_nicolas = acciones_nicolas * precio_por_accion_nicolas
    valor_gabriela = acciones_gabriela * precio_por_accion_gabriela
    nuevas_acciones_gabriela = valor_nicolas / precio_por_accion_gabriela
    ecuacion_canje = nuevas_acciones_gabriela / acciones_nicolas
    acciones_combinadas = acciones_gabriela + nuevas_acciones_gabriela
    bpa_combinada_post_sinergias = (
        valor_nicolas + valor_gabriela
    ) / acciones_combinadas

    output = (
        f"Valor Nicolas: {valor_nicolas:.2f} millones\n"
        f"Valor Gabriela: {valor_gabriela:.2f} millones\n"
        f"Nuevas Acciones Gabriela: {nuevas_acciones_gabriela:.2f}\n"
        f"Ecuación de Canje (Gabriela absorbe a Nicolas): {ecuacion_canje:.2f}\n"
        f"Acciones Combinadas: {acciones_combinadas:.2f}\n"
        f"BPA Combinada Post Sinergias (€ p.a.): {bpa_combinada_post_sinergias:.2f}\n\n"
    )
    print(output)
    return output


# Cálculo de ecuación de canje para Nicolas absorbiendo a Gabriela
def ecuacion_canje_nicolas_absorbe_gabriela():
    valor_gabriela = acciones_gabriela * precio_por_accion_gabriela
    valor_nicolas = acciones_nicolas * precio_por_accion_nicolas
    nuevas_acciones_nicolas = valor_gabriela / precio_por_accion_nicolas
    ecuacion_canje = nuevas_acciones_nicolas / acciones_gabriela
    acciones_combinadas = acciones_nicolas + nuevas_acciones_nicolas
    bpa_combinada_post_sinergias = (
        valor_nicolas + valor_gabriela
    ) / acciones_combinadas

    output = (
        f"Valor Gabriela: {valor_gabriela:.2f} millones\n"
        f"Valor Nicolas: {valor_nicolas:.2f} millones\n"
        f"Nuevas Acciones Nicolas: {nuevas_acciones_nicolas:.2f}\n"
        f"Ecuación de Canje (Nicolas absorbe a Gabriela): {ecuacion_canje:.2f}\n"
        f"Acciones Combinadas: {acciones_combinadas:.2f}\n"
        f"BPA Combinada Post Sinergias (€ p.a.): {bpa_combinada_post_sinergias:.2f}\n\n"
    )
    print(output)
    return output


# Aplicando las funciones de ecuación de canje
summary += ecuacion_canje_gabriela_absorbe_nicolas()
summary += ecuacion_canje_nicolas_absorbe_gabriela()


# Guardar el resumen en un archivo de texto
def guardar_resumen(summary):
    with open("summary.txt", "w") as file:
        file.write(summary)


# Guardar el archivo de resumen
guardar_resumen(summary)
