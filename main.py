import streamlit as st
from get_twittes_toxicity import run
import pandas as pd
import statistics

if 'output' not in st.session_state:
  st.session_state['output'] = None

st.set_page_config(
    page_title="Medidor de Toxidade do Twitter",
    page_icon="☠",
    menu_items={
      'About': """ 
      ### Projeto desenvolvido na disciplina de Redes Neurais da UFAPE 2022.1 

      Professor: Luís Filipe 

      Alunos: [Gustavo Sales](https://www.linkedin.com/in/gust4vo-sales/) e [Joanne Silva](https://www.linkedin.com/in/joannegsilva/)

      [Github](https://github.com/Gust4voSales/twitter-toxicity)
      """
    }
)

st.title("Medidor de Toxidade do Twitter")

with st.form("my_form"):
  user = st.text_input("Usuário do twitter")
  twittes_amount = st.number_input(label='Quantidade de twittes', value=25, min_value=1, max_value=500)

  submitted = st.form_submit_button("Enviar")

  if submitted:
    try:
      result = run(user, twittes_amount)
      st.session_state['output'] = result 
    except: 
      st.error("Ocorreu um erro ao busca o usuário, tente novamente.")
      st.session_state['output'] = None

if st.session_state['output'] != None:
  output = st.session_state['output']
  if len(output) > 0:
    toxic_avg = statistics.mean([twitte_result[1] for twitte_result in output])
    st.header(f"Nível de toxidade: {round(toxic_avg,2)}%")
    with st.expander("Ver resultados"):
      df = pd.DataFrame([[f'{twitte_result[1]}%', f'{twitte_result[0]}', ] for twitte_result in st.session_state['output']],
                        columns=('Tóxidade', 'Twittes'))
      st.table(df)
  else:
    st.error("Usuário não encontrado")

st.markdown('Desenvolvido por [Gustavo Sales](https://www.linkedin.com/in/gust4vo-sales/) e [Joanne Silva](https://www.linkedin.com/in/joannegsilva/). Veja mais informações no Menu.')  