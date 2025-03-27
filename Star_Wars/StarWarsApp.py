import io
import os

from dotenv import load_dotenv

from flask import Flask, render_template, make_response, request, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

import Connection

import modulo_graficas

#creating a flask object with the name of current file
app = Flask(__name__)


load_dotenv()

#getting URI from environment variables
app.config['DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
        os.environ.get('DB_USER'),
        os.environ.get('DB_PASSWORD'),
        os.environ.get('DB_HOST', 'localhost'),
        os.environ.get('DB_PORT', '5432'),
        os.environ.get('DB_NAME')
        )

Connection.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

#example of route function
@app.route('/people/<int:id_people>')
def get_person(id_people):
    db = Connection.get_raw_connection()
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM people WHERE id_people = %s"""
                   ,(id_people, ))

    response = cursor.fetchone()[1]
    return response

@app.route('/graphs/', methods = ['GET', 'POST'])
def get_graphs():
    if request.method == 'POST':
        if request.form['graph'] == "Species":
            fig = create_figure()
            output = io.BytesIO()
            FigureCanvas(fig).print_png(output)
            return Response(output.getvalue(), mimetype='image/png')
    return render_template("graphs.html")

def create_figure():
    connection = Connection.get_raw_connection()
    fig = modulo_graficas.mostrar_graficoEsp(connection)
    return fig


if __name__ == "__main__":
    app.run(debug=True)
