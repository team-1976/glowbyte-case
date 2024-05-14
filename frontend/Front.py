import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




# Заголовок приложения
st.caption('1976сантиметровые')
st.title('GlowByte-Внедряем решения BI и Big Data в России')
st.caption('Помогаем Бизнесу принимать взвешенные решения на основе данных')


# Загрузка CSV файла
uploaded_file = st.file_uploader("Target_train", type="csv", key="unique_key_1", accept_multiple_files=False, help="Пожалуйста, загрузите CSV файл.")
uploaded2_file = st.file_uploader("Predicditions", type="csv", key="unique_key_2", accept_multiple_files=False, help="Пожалуйста, загрузите CSV файл.")

if (uploaded_file is not None) and (uploaded2_file is not None):
    # Преобразование загруженного файла в DataFrame
    df = pd.read_csv(uploaded_file)
    df2 = pd.read_csv(uploaded2_file)

    # Объединение DataFrame по ключу (предположим, что 'ключ' - это столбец, по которому вы хотите объединить)
    target_column = df['target']
    prediction_column = df2['Predictions']

    # Создание нового DataFrame с этими столбцами
    combined_df = pd.concat([target_column, prediction_column], axis=1)

    combined_df = combined_df.iloc[::100]

    # Выбор нужных столбцов 'target' и 'Prediction'
    st.line_chart(combined_df[['target', 'Predictions']])

    # Если размер графика изменяется, перезапустите приложение
    if st.session_state.get('prev_shape', None) != combined_df.shape:
        st.session_state['prev_shape'] = combined_df.shape
        st.experimental_rerun()