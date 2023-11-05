
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey


Base = declarative_base()


class Client(Base):
    __tablename__ = "client_account"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    cpf = Column(String(9), nullable=False)
    
    account = relationship(
        "Account", back_populates="acc_id", cascade="all, delete-orphan")

    def __repr__(self):
        return f"nome={self.name}, fullname={self.fullname}, cpf={self.cpf})"


class Account(Base):
    __tablename__ = "account_bank"
    id = Column(Integer, primary_key=True)
    account_type = Column(String(15), nullable=False)
    bank_branch = Column(String(15), nullable=False)
    agency_number = Column(Integer, nullable=False)
    client_id = Column(Integer, ForeignKey("client_account.id"), nullable=False)

    acc_id = relationship("Client", back_populates="account")

    def __repr__(self):
        return f"""id={self.id}, account_type={self.account_type},
          bank_branch={self.bank_branch}, agency_number={self.agency_number})"""


print(Client.__tablename__)
print(Account.__tablename__)

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)
inspetor_engine = inspect(engine)

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    douglas = Client(
        name = 'douglas',
        fullname = 'Douglas Lucarelli',
        cpf = '123456789',
        account = [Account(
            account_type = 'Corrente',
            bank_branch = 2099,
            agency_number = 1750
        )]
    )

    thais = Client(
        name = 'thais',
        fullname = 'Thais Lima',
        cpf = '333456789',
        account = [Account(
            account_type = 'Poupança',
            bank_branch = 2098,
            agency_number = 1770
        )]
    )

session.add_all([douglas, thais])

session.commit()



stmt_order = select(Account).order_by(Account.id)
for result in session.scalars(stmt_order):
    print(result)


stmt_join = select(Client.fullname, Client.cpf).join_from(Account, Client)
print("\n")
for result in session.scalars(stmt_join):
    print(result)



