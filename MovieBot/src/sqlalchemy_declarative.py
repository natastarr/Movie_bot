from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


Base = declarative_base()

association_table = Table('association', Base.metadata, Column('movies_id', Integer, ForeignKey('Movies.id_of_movie')),)


class Movies(Base):
    __tablename__ = 'Movies'
    title = Column(Text, nullable=False)
    id_of_movie = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    movie_url = Column(String, nullable=False)


class User(Base):
    __tablename__ = 'Users'
    id_of_user = Column(Integer, primary_key=True)
    rating = Column(String, nullable=False, default='false')


engine = create_engine('sqlite:///movies.db')

Base.metadata.create_all(engine)
with Session(engine) as session:
    film1 = Movies(title='мфти', description='Фильм "От абитуриента к студенту"', movie_url='https://mipt.ru/dcam/abitur/video/aboutfupm.php')
    film2 = Movies(title='Фильм про мгу', description='Документальный фильм Россия об МГУ | Самый умный в мире небоскрёб', movie_url='https://www.youtube.com/watch?v=YnLtw5Yf7JQ')
    film3 = Movies(title='Бузова на кухне', description='Ольга Бузова может всё! Певица, телеведущая, актриса и дизайнер пробует себя в новом амплуа, теперь она – королева кухни. ', movie_url='https://www.youtube.com/watch?v=bDepUHraTNE&list=PLO_oY3U82zHMTmTDRzoh8G4GQ6N9BWjYm&index=11')
    film4 = Movies(title='Алгоритмы MSAI', description='Лекции и вебинары по алгоритмам', movie_url='https://youtube.com/playlist?list=PLH5AUD0BdzX7gO-uSC75GWFKecjb1k3on')
    session.add_all([film1, film2, film3, film4])
    session.commit()
