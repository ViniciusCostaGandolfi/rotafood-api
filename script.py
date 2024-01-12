import pytz
from sqlalchemy import text

from config.database import get_db


db = get_db()

# ...

# Defina o timezone desejado (por exemplo, America/Sao_Paulo)
br_tz = pytz.timezone('America/Sao_Paulo')

# Query para alterar o tipo da coluna e converter os valores para o novo tipo e timezone
alter_query = text("""
    ALTER TABLE orders
    ALTER COLUMN order_timing TYPE TIMESTAMP WITHOUT TIME ZONE
    USING (order_timing AT TIME ZONE 'UTC' AT TIME ZONE :br_tz)
""")
db.execute(alter_query, {'br_tz': br_tz.zone})
