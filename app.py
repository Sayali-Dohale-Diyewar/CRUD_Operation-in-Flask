from flask  import Flask, render_template, request, redirect, flash, url_for
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sayali'

con = sqlite3.connect('searching.db',check_same_thread=False)
cur=con.cursor()

@app.route('/')

def index():
    cur.execute('select * from students')
    list_users = cur.fetchall()
    return render_template('index.html',list_users=list_users)
@app.route('/add_student',methods=['POST'])
def add_student():
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        cur.execute('insert into students(fname,lname,email) values (?,?,?)',(fname,lname,email))
        con.commit()
        flash('Student Added Successfully!')
        return redirect(url_for('index'))

@app.route('/edit/<id>',methods=['POST','GET'])
def get_student(id):
    cur.execute('select * from students where id=?',(id,))
    data = cur.fetchall()
    return render_template('edit.html',student=data)


@app.route('/update/<id>',methods=['POST'])
def update_students(id):
    if request.method=='POST':
        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        cur.execute('update students set fname=?, lname=?, email=? where id=?',(fname,lname,email,id))
        con.commit()
        flash('Student Updated Successfully!')
        return redirect(url_for('index'))

@app.route('/delete/<id>',methods=['POST','GET'])
def delete_students(id):
    cur.execute('delete from students where id=?', (id,))
    con.commit()
    flash('Student Removed Successfully!')
    return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)