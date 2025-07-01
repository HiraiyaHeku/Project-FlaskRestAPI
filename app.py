from flask import Flask, jsonify, request, render_template_string, send_from_directory
from flask_mysqldb import MySQL
import sqlite3
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'racing'
mysql = MySQL(app)

@app.route('/')
def index():
    with open('index.html', 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/person')
def person():
	return jsonify({'name' : 'Andre',
                    'region' : 'Jawa'})

@app.route('/pembalap', methods=['GET', 'POST'])
def pembalap():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM PEMBALAP")

        column_names = [i[0] for i in cursor.description]

        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        return jsonify(data)

        cursor.close()

    elif request.method == 'POST':
        nama = request.json['nama']
        mobil = request.json['mobil']
        region = request.json['region']

        cursor = mysql.connection.cursor()
        sql = "INSERT INTO PEMBALAP (nama, mobil, region) VALUES (%s, %s, %s)"
        val = (nama, mobil, region)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'message': 'data added successfully'})
        cursor.close()


@app.route('/infopembalap/')
def infopembalap():

    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM PEMBALAP WHERE pembalap_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        column_names = [i[0] for i in cursor.description]

        pembalap = cursor.fetchall()

        return jsonify(pembalap)

        cursor.close()

@app.route('/deletepembalap', methods=['DELETE'])
def deletepembalap():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM pembalap WHERE pembalap_id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()

        return jsonify({'message': 'data deleted successfully'})
        cursor.close()

@app.route('/editpembalap', methods=['PUT'])
def editpembalap():

    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE pembalap SET nama=%s, mobil=%s, region=%s WHERE pembalap_id = %s"
        val = (data['nama'], data['mobil'], data['region'], request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        return jsonify({'message': 'Data updated successfully'})
        cursor.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)
