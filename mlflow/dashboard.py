
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


source = '../data/ds_salaries.csv'

# st.title('Salariés')
# st.write('Études sur les différences de salaires en IA')
# data = pd.read_csv(source)
# st.write(data)
# st.line_chart(data, x='job_title', y='salary_in_usd')


st.set_page_config(layout='wide')


#### ---- ---- > FUNCTIONS ---- ---- ####

@st.cache_data
def load_data():
    return pd.read_csv(source)


def display_dashboard(display='containers'):
    if display == 'containers':
        selected_cols = st.multiselect('Sélectionnez les colonnes à afficher :', cols, default=cols)
        with st.container():
            st.dataframe(data[selected_cols], use_container_width=True)
        get_cols()
    else: 
        tab1, tab2 = st.tabs(['Dataframe', 'Graphiques'])
        with tab1:
            selected_cols = st.multiselect('Sélectionnez les colonnes à afficher :', cols, default=cols)
            st.dataframe(data[selected_cols], use_container_width=True)
        with tab2:
            get_cols()

    
def get_cols():
    selected_var = st.selectbox('Sélectionnez une variable pour les graphiques :', cols_for_graphs)
    col1, col2 = st.columns(2)
    with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 8), tight_layout=True)
        data[selected_var].value_counts().plot(kind='bar', ax=ax1) 
        ax1.set_title(f'Distribution de {selected_var}', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(fontsize=10)
        plt.tight_layout()
        st.pyplot(fig1)
    with col2:
        fig2, ax2 = plt.subplots(figsize=(10, 8), tight_layout=True)
        labels = data[selected_var].value_counts().index
        sizes = data[selected_var].value_counts().values  
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 10})
        ax2.set_title(f'Proportion de {selected_var}', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig2)


#### ---- ---- > SCRIPT ---- ---- ####

data = load_data()

cols = [
    
    'work_year', 
    'experience_level', 
    'employment_type',
    'job_title',
    'salary',  
    'salary_currency', 
    'salary_in_usd', 
    'employee_residence', 
    'remote_ratio', 
    'company_location', 
    'company_size'
    
]

cols_for_graphs = [
    
    'work_year', 
    'experience_level', 
    'employment_type', 
    'remote_ratio', 
    'company_size'
    
]

st.title('Salariés')
st.write('Ce dashboard interactif permet d\'explorer les données des salariés')

# default is 'containers', could be 'containers' or 'tabs'
display_dashboard()
