from sqlalchemy import create_engine, Column, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DataTrain(Base):
    __tablename__ = 'data_train'
    id = Column(Integer, primary_key=True)
    datetime = Column(Integer)
    telemetry_0 = Column(Float)
    telemetry_1 = Column(Float)
    telemetry_2 = Column(Float)
    telemetry_3 = Column(Float)
    telemetry_4 = Column(Float)
    telemetry_5 = Column(Float)
    telemetry_6 = Column(Float)
    telemetry_7 = Column(Float)
    telemetry_8 = Column(Float)
    telemetry_9 = Column(Float)
    telemetry_10 = Column(Float)
    telemetry_11 = Column(Float)
    telemetry_12 = Column(Float)
    telemetry_13 = Column(Float)
    telemetry_14 = Column(Float)
    telemetry_15 = Column(Float)

class Target(Base):
    __tablename__ = 'target'
    id = Column(Integer, primary_key=True)
    datetime = Column(Integer)
    target = Column(Float)

class ORM:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def add_data_train(self, datetime, telemetry_values):
        data_train = DataTrain(datetime=datetime, **telemetry_values)
        self.session.add(data_train)
        self.session.commit()

    def add_target(self, datetime, target_value):
        target = Target(datetime=datetime, target=target_value)
        self.session.add(target)
        self.session.commit()

    def load_data_train(self, data_train_array):
        for data_train in data_train_array:
            datetime = data_train.pop('datetime')  # Извлекаем время из данных
            self.add_data_train(datetime, data_train)

    def load_target(self, target_array):
        for datetime, target in target_array:
            self.add_target(datetime, target)

    def read_data_train_by_id_range(self, start_id, end_id):
        data_train_list = self.session.query(DataTrain).filter(DataTrain.id >= start_id, DataTrain.id <= end_id).all()
        return [[data_train.id, data_train.datetime, data_train.telemetry_0, data_train.telemetry_1, data_train.telemetry_2, data_train.telemetry_3, data_train.telemetry_4, data_train.telemetry_5, data_train.telemetry_6, data_train.telemetry_7, data_train.telemetry_8, data_train.telemetry_9, data_train.telemetry_10, data_train.telemetry_11, data_train.telemetry_12, data_train.telemetry_13, data_train.telemetry_14, data_train.telemetry_15] for data_train in data_train_list]

    def read_target_by_id_range(self, start_id, end_id):
        target_list = self.session.query(Target).filter(Target.id >= start_id, Target.id <= end_id).all()
        return [[target.id, target.datetime, target.target] for target in target_list]

    def read_data_train_by_time_range(self, start_time, end_time):
        data_train_list = self.session.query(DataTrain).filter(DataTrain.datetime >= start_time, DataTrain.datetime <= end_time).all()
        return [[data_train.id, data_train.datetime, data_train.telemetry_0, data_train.telemetry_1, data_train.telemetry_2, data_train.telemetry_3, data_train.telemetry_4, data_train.telemetry_5, data_train.telemetry_6, data_train.telemetry_7, data_train.telemetry_8, data_train.telemetry_9, data_train.telemetry_10, data_train.telemetry_11, data_train.telemetry_12, data_train.telemetry_13, data_train.telemetry_14, data_train.telemetry_15] for data_train in data_train_list]

    def read_target_by_time_range(self, start_time, end_time):
        target_list = self.session.query(Target).filter(Target.datetime >= start_time, Target.datetime <= end_time).all()
        return [[target.id, target.datetime, target.target] for target in target_list]



    def close(self):
        self.session.close()


# Пример использования
'''
if __name__ == "__main__":
    db_url = 'sqlite:///telemetry.db'  # URL базы данных SQLite
    orm = ORM(db_url)
    
    # Пример добавления данных в таблицы
    telemetry_data = {
        'telemetry_0': 1.1,
        'telemetry_1': 2.2,
        # Добавьте остальные значения телеметрии
    }
    target_value = 42.0
    orm.add_data_train(datetime.now(), telemetry_data)
    orm.add_target(datetime.now(), target_value)
    
    orm.close()

    data_train_array = [
        {'datetime': datetime.now(), 'telemetry_0': 1.1, 'telemetry_1': 2.2, 'telemetry_2': 3.3, ...},
        {'datetime': datetime.now(), 'telemetry_0': 4.4, 'telemetry_1': 5.5, 'telemetry_2': 6.6, ...},
        # Добавьте другие данные, если необходимо
    ]

    # Пример массива данных для таблицы target
    target_array = [
        (datetime.now(), 42.0),
        (datetime.now(), 43.0),
        # Добавьте другие данные, если необходимо
    ]

    orm.load_data_train(data_train_array)
    orm.load_target(target_array)
        
    # Пример чтения данных по времени в заданном диапазоне
    start_time = datetime(2022, 1, 1)
    end_time = datetime(2022, 1, 31)
    data_train_by_time_range = orm.read_data_train_by_time_range(start_time, end_time)
    target_by_time_range = orm.read_target_by_time_range(start_time, end_time)

    # Пример чтения данных по идентификаторам в заданном диапазоне
    start_id = 1
    end_id = 100
    data_train_by_id_range = orm.read_data_train_by_id_range(start_id, end_id)
    target_by_id_range = orm.read_target_by_id_range(start_id, end_id)


'''
