from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Cargar los datos de los estudiantes, cursos y notas desde el archivo JSON
with open('datos.json', 'r') as f:
    data = json.load(f)

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    estudiantes = data['estudiantes']
    if request.method == 'POST':
        nombre = request.form['nombre']
        # Buscamos al estudiante por nombre
        estudiante = next((e for e in estudiantes if e['nombre'].lower() == nombre.lower()), None)

        if estudiante:
            # Obtener las notas del estudiante
            notas_estudiante = [
                {'curso': next(c['nombre'] for c in data['cursos'] if c['id'] == n['curso_id']), 'nota': n['nota']}
                for n in data['notas'] if n['estudiante_id'] == estudiante['id']
            ]
            return render_template('index.html', nombre=nombre, resultados=notas_estudiante, estudiantes=estudiantes)
        else:
            return render_template('index.html', mensaje="Estudiante no encontrado", estudiantes=estudiantes)

    return render_template('index.html', estudiantes=estudiantes)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
