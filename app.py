import streamlit as st
import math
import pandas as pd

st.set_page_config(layout="wide")

st.title("🧪 Assistente de Pré-Formulação v4.0 (DCS & Hansen)")
st.write("Integração do Developability Classification System (DCS) e termodinâmica de miscibilidade para seleção de polímeros em ASD.")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Parâmetros e Dose")
    dose = st.number_input("Dose Terapêutica (mg)", value=50.0, step=10.0)
    solubilidade = st.number_input("Solubilidade (mg/mL)", value=0.05, format="%.4f")
    permeabilidade = st.selectbox("Permeabilidade Intestinal", ["Alta", "Baixa"])

with col2:
    st.header("2. Térmicos e Físicos")
    tm = st.number_input("Ponto de Fusão (Tm) em °C", value=150, step=10)
    tg = st.number_input("Transição Vítrea (Tg) em °C", value=50, step=5)
    termoestavel = st.checkbox("A molécula é termoestável?", value=True)

with col3:
    st.header("3. Parâmetros de Hansen (HSP)")
    st.write("Insira os valores do IFA (MPa½)")
    dd = st.number_input("Dispersão (δD)", value=18.0)
    dp = st.number_input("Polaridade (δP)", value=10.0)
    dh = st.number_input("Pontes de Hidr. (δH)", value=10.0)

st.divider()
st.subheader("📊 Diagnóstico Farmacotécnico (Motor DCS)")

# Cálculo do Volume de Dissolução (Vd)
if solubilidade > 0:
    vd = dose / solubilidade
else:
    vd = float('inf')

limite_vd = 250.0 # Volume padrão do trato gastrointestinal (ICH)

# Lógica DCS
if vd <= limite_vd:
    if permeabilidade == "Alta":
        st.success(f"**Classe DCS I (Vd: {vd:.1f} mL)** - Molécula ideal. Formulação sólida convencional. O volume necessário para dissolver a dose é menor que 250 mL.")
    else:
        st.warning(f"**Classe DCS III (Vd: {vd:.1f} mL)** - Foco em Permeabilidade. Avaliar promotores de absorção ou pareamento iônico hidrofóbico.")
else:
    if permeabilidade == "Baixa":
        st.error(f"**Classe DCS IV (Vd: {vd:.1f} mL)** - Baixa Solubilidade e Permeabilidade. Alto risco de desenvolvimento.")
    else:
        # Separação DCS IIa e IIb (Limite simplificado de taxa de dissolução vs solubilidade intrínseca)
        if solubilidade > 0.1:
            st.warning(f"**Classe DCS IIa (Vd: {vd:.1f} mL)** - Limitado pela Taxa de Dissolução.")
            st.write("🔬 **Estratégia:** Como a solubilidade intrínseca é razoável (> 0.1 mg/mL), a limitação é a velocidade. **Redução de tamanho de partícula (Micronização/Nanocristais)** costuma ser suficiente, sem necessidade de amorfização.")
        else:
            st.error(f"**Classe DCS IIb (Vd: {vd:.1f} mL)** - Limitado pela Solubilidade Intrínseca.")
            st.write("🔬 **Estratégia:** A barreira é termodinâmica. Reduzir a partícula não será suficiente. É necessária formulação habilitadora como **Dispersão Sólida Amorfa (ASD)** ou Sistemas Lipídicos para gerar e manter a supersaturação.")
            
            # ATIVAÇÃO DO MÓDULO HANSEN PARA ASD
            st.divider()
            st.subheader("🧬 Módulo de Miscibilidade (Seleção de Polímero para ASD)")
            
            # Banco de Dados de Polímeros (HSP)
            polimeros = {
                "Hipromelose (HPMC)": {"dD": 18.0, "dP": 12.0, "dH": 15.0, "Tg": 145},
                "PVP-VA (Kollidon VA64)": {"dD": 17.6, "dP": 9.0, "dH": 6.5, "Tg": 109},
                "Copolímero Enxertado (Soluplus)": {"dD": 17.5, "dP": 6.1, "dH": 7.3, "Tg": 70},
                "HPMCAS": {"dD": 17.5, "dP": 12.2, "dH": 15.3, "Tg": 120}
            }
            
            resultados = []
            for nome, props in polimeros.items():
                # Cálculo da Distância de Ra (Fórmula de Hansen)
                ra = math.sqrt(4 * ((dd - props["dD"])**2) + (dp - props["dP"])**2 + (dh - props["dH"])**2)
                
                # Regra prática: Ra < 7.0 indica provável miscibilidade (interação de Flory-Huggins favorável)
                miscibilidade = "Alta (Miscível)" if ra < 7.0 else "Baixa (Imiscível)"
                
                # Previsão da Tecnologia baseada na Tg e Termoestabilidade
                if termoestavel and props["Tg"] < (tm - 20):
                    tecnologia = "HME (Hot-Melt Extrusion) viável"
                else:
                    tecnologia = "Spray Drying preferencial"
                    
                resultados.append({"Carreador Polimérico": nome, "Distância de Ra (MPa½)": round(ra, 2), "Miscibilidade Predita": miscibilidade, "Processo Predito": tecnologia})
            
            # Exibir resultados em formato de tabela
            df_resultados = pd.DataFrame(resultados)
            st.dataframe(df_resultados, use_container_width=True)
            
            st.info("💡 **Dica de Formulação:** Polímeros com Distância de Ra menor que 7.0 têm maior afinidade com a molécula, estabilizando o estado amorfo e reduzindo a força motriz para a recristalização. Avalie aplicações de hipromelose ou HPMCAS para manutenção da supersaturação gastrointestinal caso a distância de Ra seja favorável.")
