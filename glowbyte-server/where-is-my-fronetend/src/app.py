import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier
import plotly.express as px
from some_ml import *


def accept_user_data():
	duration = st.text_input("Введите длительность поездки: ")
	start_station = st.text_input("Введите номер станции начала поездки: ")
	end_station = st.text_input("Введите номер станции конца поездки: ")
	user_prediction_data = np.array([duration,start_station,end_station]).reshape(1,-1)

	return user_prediction_data


@st.cache
def showMap():
	plotData = pd.read_csv("./data/Trip history with locations.csv")
	Data = pd.DataFrame()
	Data['lat'] = plotData['lat']
	Data['lon'] = plotData['lon']

	return Data


def visualize(st, data):
	
	choose_viz = st.sidebar.selectbox("Выберите визуализацию",
		["NONE","Общее количество транспортных средств из различных отправных точек", "Общее количество транспортных средств из различных конечных точек",
		"Количество типов покемонов в природе"])
	
	if(choose_viz == "Общее количество транспортных средств из различных отправных точек"):
		fig = px.histogram(data['Start station'], x ='Start station')
		st.plotly_chart(fig)
	elif(choose_viz == "Общее количество транспортных средств из различных конечных точек"):
		fig = px.histogram(data['End station'], x ='End station')
		st.plotly_chart(fig)
	elif(choose_viz == "Количество типов покемонов в природе"):
		fig = px.histogram(data['Member type'], x ='Member type')
		st.plotly_chart(fig)


def main():
	st.title("Предсказываем поездочки")
	data = loadData()
	X_train, X_test, y_train, y_test, le = preprocessing(data)

	# ML Section
	choose_model = st.sidebar.selectbox("Выберите ML модель",
		["NONE","Дерево принятия решений", "Нейроная сетОчка", "Метод K ближайших соседей"])

	if(choose_model == "Дерево принятия решений"):
		score, report, tree = decisionTree(X_train, X_test, y_train, y_test)
		st.text("Точность дерева принятия решений: ")
		st.write(score,"%")
		st.text("Отчет: ")
		st.write(report)

		try:
			if(st.checkbox("Если хочется на своих данных потыкать - тыкни меня")):
				user_prediction_data = accept_user_data() 		
				pred = tree.predict(user_prediction_data)
				st.write(le.inverse_transform(pred)) 
		except:
			pass

	elif(choose_model == "Нейроная сетОчка"):
		score, report, clf = neuralNet(X_train, X_test, y_train, y_test)
		st.text("Точность нейронной сетки: ")
		st.write(score,"%")
		st.text("Отчет: ")
		st.write(report)

		try:
			if(st.checkbox("Если хочется на своих данных потыкать - тыкни меня")):
				user_prediction_data = accept_user_data()
				scaler = StandardScaler()  
				scaler.fit(X_train)  
				user_prediction_data = scaler.transform(user_prediction_data)	
				pred = clf.predict(user_prediction_data)
				st.write(le.inverse_transform(pred)) # Inverse transform to get the original dependent value. 
		except:
			pass

	elif(choose_model == "Метод K ближайших соседей"):
		score, report, clf = Knn_Classifier(X_train, X_test, y_train, y_test)
		st.text("Точность модельки: ")
		st.write(score,"%")
		st.text("Отчет: ")
		st.write(report)

		try:
			if(st.checkbox("Если хочется на своих данных потыкать - тыкни меня")):
				user_prediction_data = accept_user_data() 		
				pred = clf.predict(user_prediction_data)
				st.write(le.inverse_transform(pred)) # Inverse transform to get the original dependent value. 
		except:
			pass
	
	


	# Визуализация
	visualize(st, data)
	

if __name__ == "__main__":
	main()
