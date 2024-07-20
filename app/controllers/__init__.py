from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

# http://0.0.0.0:5000/employee/all?order=name,asc
"""
    Resultado final: 
    filtro = Filter(...)
    filtro.order_data()

    data = filtro.query.all()
"""
class Filter:
    def __init__(self, db: Session, table, request_args: dict = None) -> None:
        self.table = table
        self.query = db.query(table)
        self.request_args = request_args

        self.__order_data()
    
    def __order_data(self):
        if self.request_args is None:
            return

        order_types = {
            "asc": asc,
            "desc": desc
        }

        field_name, order = self.request_args.get("order").split(",")
        self.query = self.query.order_by(order_types[order](field_name))
    
    def get_ordered_data(self):
        return self.query.all()