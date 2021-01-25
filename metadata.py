# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Account(Base):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)


class Commodity(Base):
    __tablename__ = 'commodity'

    id = Column(Integer, primary_key=True)


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)


class Entry(Base):
    __tablename__ = 'entry'

    id = Column(Integer, primary_key=True)
    account = Column(ForeignKey('account.id'), nullable=False, index=True)
    change = Column(Numeric(18, 4), nullable=False)
    commodity1 = Column(ForeignKey('commodity.id'), nullable=False, index=True)
    converted = Column(Numeric(18, 4), nullable=False)
    commodity2 = Column(ForeignKey('commodity.id'), nullable=False, index=True)
    transaction = Column(ForeignKey('transaction.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    account1 = relationship('Account')
    commodity = relationship('Commodity', primaryjoin='Entry.commodity1 == Commodity.id')
    commodity3 = relationship('Commodity', primaryjoin='Entry.commodity2 == Commodity.id')
    transaction1 = relationship('Transaction')