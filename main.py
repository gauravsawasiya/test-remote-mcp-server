from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__),"expense.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__),'categories.json')

mcp = FastMCP(name = "Expense Tracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
                create table if not exists expenses(
                  id integer primary key autoincrement,
                  date text not null,
                  amount real not null,
                  category text not null,
                  subcategory text default "",
                  note text default "" )

""")
        
init_db()


@mcp.tool
def add_expense(date, amount, category, subcategory="", note=""):

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "insert into expenses(date, amount, category, subcategory, note) values(?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {'status':'ok', "id": cur.lastrowid}

@mcp.tool
def list_exepnse():

    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("select id, date, amount, category, subcategory, note from expenses order by id asc")
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()]
    


@mcp.tool
def summarize(stat_date, end_date, category = None):

    with sqlite3.connect(DB_PATH) as c:

        query = (
            """
            select category , sum(amount) as total_amount
            from expenses
            where date between ? and ?
            """
        )

        params = [stat_date, end_date]

        if category:
            query += " and category = ?"
            params.append(category)

        query += " group by category order by category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols,r)) for r in cur.fetchall()] 


@mcp.resource("expense://categories",mime_type="application/json")
def categories():

    with open(CATEGORIES_PATH,"r", encoding="utf-8") as f:
        return f.read()



if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "127.0.0.1")
    port = int(os.getenv("MCP_PORT", "8001"))
    mcp.run(transport="http", host=host, port=port)
