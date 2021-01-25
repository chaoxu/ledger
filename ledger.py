from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from metadata import *



class Ledger:

  def __init__(self, db_string):
    self.db_string = db_string
    self.db = create_engine(db_string)
    self.session = sessionmaker(self.db)()


  def build_entry(self, account, change, commodity1, transaction=None, price=None, converted=None, commodity2=None):
    # if we have price, we must set commodity 2
    if price is not None and commodity2 is not None:
      converted = change * price

    # otherwise, default
    if commodity2 is None and converted is None:
      commodity2 = commodity1
      converted = change

    # at this point, if something is none, we meet a problem
    if commodity2 is None:
      raise ValueError('No reasonable commodity2.')
    if converted is None:
      raise ValueError('No reasonable converted.')

    return Entry(account=account, change=change, commodity1=commodity1, converted=converted, commodity2=commodity2, transaction=transaction)

  def is_balanced(self, entries):
    # first create entries
    d = dict()
    for entry in entries:
      if entry.commodity2 not in d:
        d[entry.commodity2] = 0.0
      d[entry.commodity2] += entry.converted

    for x in d.values():
      if x != 0:
        return False
    return True

  # transaction

  def create_transaction_with_entries(self, entries):
    transaction_id = self._create_transaction().id
    self.update_transaction(transaction_id, entries)
    return transaction_id

  def delete_transaction(self, id):
    self._delete_by_ids(Transaction, [id])
    self.session.commit()

  def merge_transaction(self, canonical_id, ids):
    if not ids:
      raise ValueError('No transaction ids')

    # rename transaction to the first transaction in the list
    # just in case merged ids also contain canonical id
    ids = set(ids)
    remove_ids = ids - {canonical_id}
    session = self.session()

    # fist make sure transaction exists
    # We never create new transactions
    if session.query(Transaction).filter_by(id=canonical_id).count() == 0:
      raise ValueError('Canonical ID %d does not exist.' % canonical_id)

    # update entries
    entries = session.query(Entry).filter(Entry.transaction.in_(remove_ids))
    for entry in entries:
      entry.transaction = canonical_id
    session.commit()

    # remove transactions
    self._delete_by_ids(Transaction, remove_ids)
    self.session.commit()

  def update_transaction(self, id, entries):
    if not self.is_balanced(entries):
      raise ValueError("transaction is not balanced")

    self._clear_transaction(id)
    for e in entries:
      e.transaction = id
    self.session.add_all(entries)
    self.session.commit()

  # other random stuff

  def delete_account(self, id):
    self._delete_by_ids(Account, [id])
    self.session.commit()

  def delete_commodity(self, id):
    self._delete_by_ids(Commodity, [id])
    self.session.commit()

  def create_account(self):
    x = Account()
    self.session.add(x)
    self.session.commit()
    return x

  def create_commodity(self):
    x = Commodity()
    self.session.add(x)
    self.session.commit()
    return x

  # private methods, does not commit.
  def _delete_by_ids(self, type, ids):
    x = self.session.query(type).filter(type.id.in_(ids)).one()
    self.session.delete(x)

  def _create_transaction(self):
    x = Transaction()
    self.session.add(x)
    self.session.flush()
    return x

  def _clear_transaction(self, id):
    self.session.query(Entry).filter_by(transaction=id).delete()