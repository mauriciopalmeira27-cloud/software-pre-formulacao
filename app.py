import streamlit as st

# Título e descrição
st.title("🧪 Assistente de Pré-Formulação v2.0")
st.write("Insira as características da molécula para receber uma recomendação tecnológica.")

# Menu lateral para os inputs do usuário
st.sidebar.header("Parâmetros Físico-Químicos")
# O parâmetro 'key' previne o erro de elementos duplicados
solubilidade = st.sidebar.selectbox("Solubilidade Aquosa", ["Selecione...", "Alta", "Baixa"], key="sol_key")
permeabilidade = st.sidebar.selectbox("Permeabilidade Intestinal", ["Selecione...", "Alta", "Baixa"], key="perm_key")

st.sidebar.header("Parâmetros Térmicos e Físicos")
tm = st.sidebar.number_input("Ponto de Fusão (Tm) em °C", value=150, step=10, key="tm_key")
termoestavel = st.sidebar.checkbox("A molécula é termoestável?", value=True, key="termo_key")

st.sidebar.header("Objetivo (Target)")
target = st.sidebar.selectbox("Qual o principal desafio ou objetivo?", 
                              ["Selecione...", "Melhorar Dissolução", "Absorção Mucosal / Rápido Onset", "Aumentar Permeabilidade"], 
                              key="target_key")

st.subheader("Diagnóstico e Recomendação Tecnológica")

# O Motor de Regras Atualizado
if solubilidade == "Selecione..." or permeabilidade == "Selecione..." or target == "Selecione...":
    st.info("👈 Preencha os parâmetros na barra lateral para rodar o motor de regras.")

else:
    # Regra 1: Foco em absorção mucosal
    if target == "Absorção Mucosal / Rápido Onset":
        st.success("**Estratégia Recomendada: Comprimidos Orodispersíveis (ODTs) ou Filmes Sublinguais**")
        st.write("Para targets de rápida absorção mucosal, a rápida desintegração é a via de escolha. **Ponto de atenção crítico:** avaliar o amargor do IFA e a necessidade de tecnologias de mascaramento de sabor na formulação.")
        
    # Regra 2: BCS II (Baixa Solubilidade)
    elif solubilidade == "Baixa" and permeabilidade == "Alta":
        st.warning("**Classe BCS II: Barreira de Dissolução**")
        
        if tm > 200:
            st.write("🔬 **Recomendação: Redução de Tamanho de Partícula**")
            st.write(f"Como o Ponto de Fusão é alto ({tm} °C), a barreira principal é a alta energia da rede cristalina. Tecnologias de amorfização consumiriam muita energia ou degradariam a molécula. Foque em **nanocristais** ou moagem a úmido.")
        else:
            st.write("🔬 **Recomendação: Dispersão Sólida Amorfa (ASD)**")
            if termoestavel:
                st.write("A molécula tem Tm favorável e é termoestável. A técnica de escolha é **Hot-Melt Extrusion (HME)** utilizando carreadores poliméricos adequados.")
            else:
                st.write("A molécula tem Tm favorável, mas é termolábil. Evite a extrusão a quente e utilize **Spray Drying** para a formação da ASD a partir de solução.")
            
    # Regra 3: BCS III (Baixa Permeabilidade)
    elif solubilidade == "Alta" and permeabilidade == "Baixa":
        st.warning("**Classe BCS III: Barreira de Permeabilidade**")
        st.write("🔬 **Recomendação: Pareamento Iônico Hidrofóbico (HIP)**")
        st.write("Para aumentar o coeficiente de partição aparente e facilitar a travessia das membranas biológicas, avalie o pareamento iônico com contra-íons apropriados (ex: **salcaprozato de sódio** ou desoxicolato de sódio).")
        
    # Regra 4: BCS IV
    elif solubilidade == "Baixa" and permeabilidade == "Baixa":
        st.error("**Classe BCS IV: Baixa Solubilidade e Permeabilidade**")
        st.write("Desenvolvimento complexo. Recomenda-se revisitar o design molecular (prodrogas) ou explorar sistemas de entrega nanoestruturados (nanopartículas poliméricas/lipídicas).")
        
    # Regra 5: BCS I
    elif solubilidade == "Alta" and permeabilidade == "Alta":
        st.success("**Classe BCS I**")
        st.write("Molécula com excelente perfil. Seguir com formas sólidas convencionais (compressão direta) focando em otimização de processo e Quality by Design (QbD).")