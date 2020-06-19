from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Float, DateTime, MetaData
from sqlalchemy.sql import select
from sqlalchemy import desc


app = Flask(__name__)

engine = create_engine('sqlite:///../pickles/college.db', echo = True)
meta = MetaData()

predictions = Table(
    'predictions', meta, 
    Column('id', Integer, primary_key = True), 
    Column('p_date', DateTime), 
    Column('p_price', Float(asdecimal=False)), 
    Column('f_price', Float(asdecimal=False)),  
)


@app.route('/')
def index():
    query = select([predictions]).order_by(desc(predictions.c.p_date)).limit(1)
    conn = engine.connect()
    results = conn.execute(query)
    for result in results:
        next_price = "{:.2f}".format(round(result.f_price, 2))
        p_date = result.p_date.strftime('%d-%m-%Y')
    return render_template('index.html', next_price=next_price, p_date=p_date)

@app.route('/history')
def history():
    query = select([predictions]).order_by(desc(predictions.c.id))
    conn = engine.connect()
    results = conn.execute(query)
    return render_template('history.html', results=results)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title = '404'), 404

if __name__ == "__main__":
    app.run(debug=True)
