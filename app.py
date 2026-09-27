import streamlit as st

# Título e descrição
st.title("🧪 Assistente de Pré-Formulação v3.0")
st.write("Insira as características da molécula e o estado físico desejado para receber uma recomendação tecnológica avançada.")

# Menu lateral para os inputs do usuário
st.sidebar.header("Parâmetros Físico-Químicos")
solubilidade = st.sidebar.selectbox("Solubilidade Aquosa", ["Selecione...", "Alta", "Baixa"], key="sol_key")
permeabilidade = st.sidebar.selectbox("Permeabilidade Intestinal", ["Selecione...", "Alta", "Baixa"], key="perm_key")
logp = st.sidebar.number_input("LogP (Coeficiente de Partição)", value=2.0, step=0.5, key="logp_key")
pka = st.sidebar.number_input("pKa principal", value=7.0, step=0.5, key="pka_key")

st.sidebar.header("Parâmetros Térmicos e Físicos")
tm = st.sidebar.number_input("Ponto de Fusão (Tm) em °C", value=150, step=10, key="tm_key")
tg = st.sidebar.number_input("Transição Vítrea (Tg) em °C", value=50, step=5, key="tg_key")
termoestavel = st.sidebar.checkbox("A molécula é termoestável?", value=True, key="termo_key")

st.sidebar.header("Perfil da Formulação")
estado_fisico = st.sidebar.selectbox("Estado Físico", 
                                     ["Selecione...", "Sólido (Comprimidos, Cápsulas, ODTs)", "Líquido / Dispersão Coloidal (Suspensões, Emulsões)"], 
                                     key="estado_key")
target = st.sidebar.selectbox("Principal Objetivo", 
                              ["Selecione...", "Melhorar Dissolução", "Absorção Mucosal / Rápido Onset", "Aumentar Permeabilidade", "Estabilidade Física"], 
                              key="target_key")

st.subheader("Diagnóstico e Recomendação Tecnológica")

if solubilidade == "Selecione..." or permeabilidade == "Selecione..." or target == "Selecione..." or estado_fisico == "Selecione...":
    st.info("👈 Preencha os parâmetros na barra lateral para rodar o motor de regras.")
else:
    # ---------------------------------------------------------
    # LÓGICA PARA SISTEMAS LÍQUIDOS E COLOIDAIS
    # ---------------------------------------------------------
    if estado_fisico == "Líquido / Dispersão Coloidal (Suspensões, Emulsões)":
        st.success("**Estratégia Recomendada: Sistemas Dispersos e Nanotecnologia**")
        
        if solubilidade == "Baixa":
            st.write("🔬 **Foco: Nanosuspensões ou Emulsões**")
            st.write(f"Como a molécula possui Baixa Solubilidade e LogP de {logp}:")
            
            if logp > 3:
                st.write("- **SMEDDS / Microemulsões:** O alto LogP favorece a solubilização em carreadores lipídicos.")
            else:
                st.write("- **Nanosuspensões Coloidais:** Recomendada a redução do tamanho de partícula (ex: moagem a úmido).")
                
            st.warning("⚠️ **Atenção Físico-Química (Estabilidade Física):** É imperativo avaliar a energia livre interfacial e a Pressão de Laplace do sistema disperso. Altos gradientes de pressão podem induzir *Ostwald ripening* ou *crystal bridging*. Recomenda-se modular a viscosidade do veículo baseando-se na Lei de Stokes para mitigar a sedimentação.")
        else:
            st.write("Soluções orais convencionais. Foco no controle de pH (baseado no pKa da molécula) para garantir estabilidade em solução.")

    # ---------------------------------------------------------
    # LÓGICA PARA SISTEMAS SÓLIDOS
    # ---------------------------------------------------------
    elif estado_fisico == "Sólido (Comprimidos, Cápsulas, ODTs)":
        
        if target == "Absorção Mucosal / Rápido Onset":
            st.success("**Estratégia Recomendada: Comprimidos Orodispersíveis (ODTs)**")
            st.write("A rápida desintegração é a via de escolha. Ponto crítico de desenvolvimento: mascaramento de sabor de ativos amargos e otimização da absorção pré-gástrica.")
            
        elif solubilidade == "Baixa" and permeabilidade == "Alta":
            st.warning("**Classe BCS II: Barreira de Dissolução**")
            
            if tm > 200:
                st.write("🔬 **Recomendação: Redução de Tamanho de Partícula**")
                st.write(f"O Ponto de Fusão alto ({tm} °C) indica uma alta energia da rede cristalina. Foque em nanocristais ao invés de amorfização.")
            else:
                st.write("🔬 **Recomendação: Dispersão Sólida Amorfa (ASD)**")
                
                # Regra de Estabilidade Baseada na Tg e Zona IVb
                if tg < 50:
                    st.error(f"⚠️ **Alerta de Estabilidade:** A Tg reportada ({tg} °C) é criticamente baixa para testes de estabilidade em clima da Zona IVb (40°C/75% HR). Há elevado risco de recristalização. É mandatório incorporar carreadores poliméricos de alto peso molecular e alta Tg (ex: HPMCAS, PVP) na formulação.")
                
                if termoestavel:
                    st.write("- **Técnica Produtiva:** Hot-Melt Extrusion (HME).")
                else:
                    st.write("- **Técnica Produtiva:** Spray Drying a partir de solvente orgânico.")
                
        elif solubilidade == "Alta" and permeabilidade == "Baixa":
            st.warning("**Classe BCS III: Barreira de Permeabilidade**")
            st.write("🔬 **Recomendação: Pareamento Iônico Hidrofóbico (HIP)**")
            st.write(f"Modular o pH da matriz em função do pKa ({pka}) para garantir a ionização da molécula e utilizar contra-íons (como salcaprozato de sódio ou desoxicolato de sódio) para forçar a formação de complexos lipofílicos absorvíveis.")
            
        elif solubilidade == "Baixa" and permeabilidade == "Baixa":
            st.error("**Classe BCS IV: Baixa Solubilidade e Permeabilidade**")
            st.write("Desenvolvimento de altíssimo risco. Considerar sistemas lipídicos sólidos ou matrizes nanoestruturadas se o target biológico compensar o custo tecnológico.")
            
        else:
            st.success("**Classe BCS I (Alta/Alta)**")
            st.write("Formas sólidas convencionais (compressão direta) são adequadas. Focar na qualidade por design (QbD).")
