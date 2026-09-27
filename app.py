import streamlit as st
import math
import pandas as pd

st.set_page_config(layout="wide")

st.title("🧪 Assistente de Pré-Formulação v5.0 (Full Expert System)")
st.write("Integração completa: Parâmetros Físico-Químicos, Térmicos, Target e Motor DCS com Termodinâmica de Hansen.")

# Barra Lateral: Perfil Geral
st.sidebar.header("🎯 Perfil da Formulação")
estado_fisico = st.sidebar.selectbox("Estado Físico", 
                                     ["Selecione...", "Sólido (Comprimidos, Cápsulas, ODTs)", "Líquido / Dispersão Coloidal (Suspensões, Emulsões)"])
target = st.sidebar.selectbox("Principal Objetivo", 
                              ["Selecione...", "Melhorar Dissolução", "Absorção Mucosal / Rápido Onset", "Aumentar Permeabilidade", "Estabilidade Física"])

# Colunas Centrais: Parâmetros Moleculares
col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Biofarmacêuticos")
    dose = st.number_input("Dose Terapêutica (mg)", value=50.0, step=10.0)
    solubilidade = st.number_input("Solubilidade (mg/mL)", value=0.05, format="%.4f")
    permeabilidade = st.selectbox("Permeabilidade Intestinal", ["Alta", "Baixa"])
    logp = st.number_input("LogP (Coef. de Partição)", value=2.0, step=0.5)
    pka = st.number_input("pKa principal", value=7.0, step=0.5)

with col2:
    st.header("2. Físico-Químicos")
    tm = st.number_input("Ponto de Fusão (Tm) em °C", value=150, step=10)
    tg = st.number_input("Transição Vítrea (Tg) em °C", value=50, step=5)
    termoestavel = st.checkbox("A molécula é termoestável?", value=True)

with col3:
    st.header("3. Termodinâmica (Hansen)")
    st.write("Insira os valores do IFA (MPa½)")
    dd = st.number_input("Dispersão (δD)", value=18.0)
    dp = st.number_input("Polaridade (δP)", value=10.0)
    dh = st.number_input("Pontes de Hidr. (δH)", value=10.0)

st.divider()
st.subheader("📊 Diagnóstico Farmacotécnico (Motor Avançado)")

if estado_fisico == "Selecione..." or target == "Selecione...":
    st.info("👈 Preencha os parâmetros de 'Perfil da Formulação' na barra lateral para rodar o motor de regras.")
else:
    # Cálculo do Volume de Dissolução (Vd)
    vd = (dose / solubilidade) if solubilidade > 0 else float('inf')
    limite_vd = 250.0 # Volume padrão do trato gastrointestinal (ICH)

    # ---------------------------------------------------------
    # LÓGICA PARA SISTEMAS LÍQUIDOS E COLOIDAIS
    # ---------------------------------------------------------
    if estado_fisico == "Líquido / Dispersão Coloidal (Suspensões, Emulsões)":
        st.success("**Estratégia Recomendada: Sistemas Dispersos e Nanotecnologia**")
        
        if vd > limite_vd: # Análogo a Baixa Solubilidade
            st.write(f"🔬 **Foco: Nanosuspensões ou Emulsões (Vd da Dose: {vd:.1f} mL)**")
            if logp > 3:
                st.write(f"- **SMEDDS / Microemulsões:** O alto LogP ({logp}) favorece a solubilização natural em carreadores lipídicos.")
            else:
                st.write(f"- **Nanosuspensões Coloidais:** Como o LogP é mais baixo ({logp}), recomenda-se a redução do tamanho de partícula (ex: moagem a úmido).")
                
            st.warning("⚠️ **Atenção Físico-Química (Estabilidade Física):** É imperativo avaliar a energia livre interfacial e a Pressão de Laplace do sistema disperso. Altos gradientes de pressão podem induzir *Ostwald ripening* ou *crystal bridging*. Recomenda-se modular a viscosidade do veículo baseando-se na Lei de Stokes.")
        else:
            st.write("🔬 **Foco: Soluções Orais Convencionais**")
            st.write(f"A molécula é solúvel na dose desejada. Foco no controle de pH (baseado no pKa de {pka}) e sistemas tampão para garantir a estabilidade na prateleira.")

    # ---------------------------------------------------------
    # LÓGICA PARA SISTEMAS SÓLIDOS
    # ---------------------------------------------------------
    elif estado_fisico == "Sólido (Comprimidos, Cápsulas, ODTs)":
        
        if target == "Absorção Mucosal / Rápido Onset":
            st.success("**Estratégia Recomendada: Comprimidos Orodispersíveis (ODTs)**")
            st.write("A rápida desintegração é a via de escolha. Ponto crítico de desenvolvimento: mascaramento de sabor de ativos amargos e otimização da absorção pré-gástrica.")
            
        else:
            # Lógica DCS Integrada
            if vd <= limite_vd:
                if permeabilidade == "Alta":
                    st.success(f"**Classe DCS I (Vd: {vd:.1f} mL)** - Molécula ideal. Formulação sólida convencional. Foco em otimização de processo e QbD.")
                else:
                    st.warning(f"**Classe DCS III (Vd: {vd:.1f} mL)** - Barreira de Permeabilidade.")
                    st.write("🔬 **Recomendação: Pareamento Iônico Hidrofóbico (HIP)**")
                    st.write(f"Como o IFA possui pKa em {pka}, module o micro-pH da matriz para garantir a ionização e utilize contra-íons lipofílicos (ex: salcaprozato de sódio).")
            else:
                if permeabilidade == "Baixa":
                    st.error(f"**Classe DCS IV (Vd: {vd:.1f} mL)** - Baixa Solubilidade e Baixa Permeabilidade.")
                    st.write("Alto risco de desenvolvimento. Considerar matrizes lipídicas sólidas ou nanopartículas poliméricas.")
                else:
                    if solubilidade > 0.1:
                        st.warning(f"**Classe DCS IIa (Vd: {vd:.1f} mL)** - Limitado pela Taxa de Dissolução.")
                        st.write("🔬 **Estratégia:** Como a solubilidade intrínseca é razoável (> 0.1 mg/mL), **Redução de tamanho de partícula** (nanocristais) costuma ser suficiente, sem amorfização.")
                    else:
                        st.error(f"**Classe DCS IIb (Vd: {vd:.1f} mL)** - Limitado pela Solubilidade Intrínseca.")
                        st.write("🔬 **Estratégia:** Reduzir a partícula não será suficiente. É necessária formulação habilitadora como **Dispersão Sólida Amorfa (ASD)** para gerar e manter a supersaturação.")
                        
                        # Alerta de Estabilidade (Zona IVb)
                        if tg < 50:
                            st.error(f"⚠️ **Alerta de Estabilidade (Zona Climática IVb):** A Tg do IFA ({tg} °C) é criticamente baixa para 40°C/75% HR. Risco severo de plastificação por umidade e recristalização. Obrigatório uso de embalagem Alu-Alu e polímero de alta Tg.")
                        
                        # ATIVAÇÃO DO MÓDULO HANSEN PARA ASD
                        st.divider()
                        st.subheader("🧬 Módulo de Miscibilidade (Seleção de Polímero para ASD)")
                        
                        polimeros = {
                            "Hipromelose (HPMC)": {"dD": 18.0, "dP": 12.0, "dH": 15.0, "Tg": 145},
                            "PVP-VA (Kollidon VA64)": {"dD": 17.6, "dP": 9.0, "dH": 6.5, "Tg": 109},
                            "Copolímero Enxertado (Soluplus)": {"dD": 17.5, "dP": 6.1, "dH": 7.3, "Tg": 70},
                            "HPMCAS": {"dD": 17.5, "dP": 12.2, "dH": 15.3, "Tg": 120}
                        }
                        
                        resultados = []
                        for nome, props in polimeros.items():
                            # Distância de Ra de Hansen
                            ra = math.sqrt(4 * ((dd - props["dD"])**2) + (dp - props["dP"])**2 + (dh - props["dH"])**2)
                            miscibilidade = "Alta (Miscível)" if ra < 7.0 else "Baixa (Imiscível)"
                            
                            # Decisão de Processo
                            if termoestavel and props["Tg"] < (tm - 20):
                                tecnologia = "Hot-Melt Extrusion (HME)"
                            else:
                                tecnologia = "Spray Drying"
                                
                            resultados.append({
                                "Carreador Polimérico": nome, 
                                "Distância de Ra (MPa½)": round(ra, 2), 
                                "Miscibilidade Predita": miscibilidade, 
                                "Processo Indicado": tecnologia
                            })
                        
                        df_resultados = pd.DataFrame(resultados)
                        st.dataframe(df_resultados, use_container_width=True)
                        st.info("💡 **Dica QbD:** Polímeros com Distância de Ra menor que 7.0 têm maior afinidade termodinâmica com a molécula e previnem a separação de fases (demistura).")
