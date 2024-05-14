import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Создаем случайные реальные данные и предсказанные значения
np.random.seed(0)
x = np.arange(100)
real_data = np.random.normal(0, 1, 100)
predicted_data = np.random.normal(0, 1, 100)

# Создаем DataFrame для хранения данных
df = pd.DataFrame({'x': x, 'Real Data': real_data, 'Predicted Data': predicted_data})

# Страница заголовка
st.title('Аналитика')

# График соответствия реальных данных и предсказанных
st.line_chart(df[['Real Data', 'Predicted Data']])

# График реальных данных и предсказанных
st.line_chart(df[['x', 'Real Data']])
st.line_chart(df[['x', 'Predicted Data']])


