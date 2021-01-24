# ledger
A ledger supports multiple commodity. So in some sense it is also a inventory management system. 

# Design

There are 4 different things:
 - account
 - transaction
 - entry
 - commodity

A transaction is a list of entries that is balanced. 

That is summing everything by converted commodity, we obtain 0 in each commodity. 

An entry is a change in the account, and a conversion. 
So it requires a 5 tuple.
`account, change, commodity_type_1, converted, commodity_type_2`
This means for an account, change the amount of commodity_type_1 by change.
It also convert `change commodity_type_1` into `converted commodity_type_2`.

If there is no conversion, then `change=converted`, and `commodity_type_1 = commodity_type_2`.

Note we do not have any checks on conversions, so one should be aware about entering conversions.

The API would include creating writing a transaction, creating an account, creating an commodity.
Transaction updates need to be very careful, as it requires the transaction to be balanced.
