from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base

engine = create_engine('sqlite:///futsalBruno.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()


class Jogador(Base):
    __tablename__ = 'jogador'
    id_jogador = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(40), nullable=False)
    sobrenome = Column(String(40), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    numero = Column(Integer, nullable=False)
    id_clube = Column(Integer, nullable=False)

    def serialize_jogador(self):
        return {
            "id_jogador": self.id_jogador,
            "nome": self.nome,
            "sobrenome": self.sobrenome,
            "cpf": self.cpf,
            "numero": self.numero,
            "id_clube": self.id_clube,
        }

    def save(self):
        db_session.add(self)
        db_session.commit()

class Clube(Base):
    __tablename__ = 'clube'
    id_clube = Column(Integer, primary_key=True, autoincrement=True)
    nome_clube = Column(String(40), nullable=False)

    def serialize_clube(self):
        return {"id_clube": self.id_clube, "nome_clube": self.nome_clube}

    def save(self):
        db_session.add(self)
        db_session.commit()

class Campeonato(Base):
    __tablename__ = 'campeonato'
    id_campeonato = Column(Integer, primary_key=True, autoincrement=True)
    nome_campeonato = Column(String(40), nullable=False)
    descricao_campeonato = Column(String(100), nullable=False)

    def serialize_campeonato(self):
        return {
            "id_campeonato": self.id_campeonato,
            "nome_campeonato": self.nome_campeonato,
            "descricao_campeonato": self.descricao_campeonato,
        }

    def save(self):
        db_session.add(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
