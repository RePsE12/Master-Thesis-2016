from flask import Flask,render_template,session,redirect,url_for,flash,g,request
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField, SubmitField,BooleanField,SelectField,ValidationError
from wtforms.validators import Required
import xml.etree.ElementTree as et
import sqlite3 as lite
import os
import collada
import json
import time


path = r'C:\Users\esper\Desktop\Tue\7CC10\Thesis\Thesis draft\program\Asta project,Hendriks ifc\UITVOERINGSTIJDSCHEMA.xml'
tree = et.parse(path)
root = tree.getroot()
project_name = tree.findtext('{http://schemas.microsoft.com/project}Title')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'esperachkar'
bootstrap = Bootstrap(app)
DATABASE = r'C:\Users\esper\Desktop\Tue\7CC10\Thesis\Thesis draft\program\Asta Project,Hendriks ifc\Newexample.db'
		
class NameForm(Form):
	# check = SelectField('The required checks are:')
	reviewer = StringField ('Checked by:', validators=[Required()])
	# result = BooleanField ('Inspection approved?')
	date = StringField ('Inspection Date: (DD-MM-YYYY Format)',validators=[Required()])
	# comment = SelectField ('Comments/Defects:', choices=())
	# submit = SubmitField('Submit')	

def get_dropdown():
	nested_ans1 =[]
	nested_ans2 = []
	con = lite.connect(DATABASE)
	cur = con.cursor()
	cur.execute("SELECT ELEMENT,GUID FROM objects JOIN inspections WHERE objects.ID = inspections.objectID")
	nested_ans1 = cur.fetchall()
	cur.execute("SELECT Check_required FROM requirements JOIN inspections WHERE requirements.ID = inspections.checkID")
	nested_ans2 = cur.fetchall()
	cur.execute("SELECT objects.ELEMENT,objects.GUID,requirements.Check_required FROM objects JOIN inspections ON objects.ID = inspections.objectID JOIN requirements ON requirements.ID = inspections.checkID JOIN results ON inspections.ID = results.InspectionID WHERE results.result = '1'")
	passed = cur.fetchall()
	ans = zip(nested_ans1,nested_ans2)
	new_list = []
	new1 = ()
	new2 = ()	
	new3 = ()
	new4 = ()
	for x in ans:
		new =  x[0] + x[1]
		new1 = new1 + (new,)	
	if len(passed) == 0:
		new3 = new1
		for x in new3:
			cur.execute("SELECT ID FROM objects WHERE GUID = ?",(x[1],))
			objID = cur.fetchone()
			cur.execute("SELECT ID FROM requirements WHERE Check_required = ?",(x[2],))
			checkID = cur.fetchone()
			z = objID + checkID
			cur.execute("SELECT ID FROM inspections WHERE objectID = ? AND checkID = ?",(z))
			resID = cur.fetchone()
			new2 = resID + (",".join(x),)
			new_list.append(new2)
	else:	
		for x in new1:
			x = [x]
			if set(x) & set(passed):
				pass
			else:
				new3 = new3 + (x,)
		for x in new3:
			y = x[0]
			new4 = new4 + (y,)	
		for x in new4:
			cur.execute("SELECT ID FROM objects WHERE GUID = ?",(x[1],))
			objID = cur.fetchone()
			cur.execute("SELECT ID FROM requirements WHERE Check_required = ?",(x[2],))
			checkID = cur.fetchone()
			z = objID + checkID
			cur.execute("SELECT ID FROM inspections WHERE objectID = ? AND checkID = ?",(z))
			resID = cur.fetchone()
			new2 = resID + (",".join(x),)
			new_list.append(new2)
	return new_list	
	
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
	
@app.route('/', methods =['GET',"POST"])
def index():
	if request.method == "GET":
		list_of_defects = {'Controle aanvoer kozijnen':['packaging not intact','delivery not complete'],'Hebben de sparingen de juiste afmetingen (inclusief tolerentie)?':['Insuffucent tolerance','Dimensions are not correct','opening is not perpendicular'],
		'Zitten de sparingen op de juiste plaats?':['Vertical position of opening is not correct','Horizontal position of opening is not correct'],'Kozijnen en beglazing volledig afplakken':['Foil damaged','Foil is missing'],
		'Kwaliteit (let op beschadigingen) bij plaatsen':['Foil is damanged','Glass is damanged','Bottom sill is damaged','Wooden frame is damaged','Hinges and Frames are damaged','Vent damaged'],
		'Kwaliteit (let op beschadigingen) bij oplevering':['Glass is damaged','Bottom sill is damaged','Wooden frame is damaged','Hinges and locks are damaged','Vent is damaged','Joints are not sealed correctly','Paint is not OK','Window is not clean','Window does not open/close correctly'],
		'Zijn attesten aanwezig': ['Yes','No'],'Binnenkozijnen schoongemaakt':['Not cleaned']}
		length = get_dropdown()
		list_length = len(length)
		if list_length == 0:
			return redirect(url_for('complete'))
		class DynamicForm(NameForm): pass
		count = 1
		for el in length:
			num = str(count)
			setattr(DynamicForm, "check" + num, StringField("Inspection" +" " + num + ":",default = el[1]) )
			setattr(DynamicForm, "result" + num, BooleanField ('Inspection approved?') )
			setattr(DynamicForm, "comment" + num, SelectField ('Comments/Defects:', choices=()) )
			setattr(DynamicForm , "Submit" , SubmitField ("Submit"))
			count +=1
		form = DynamicForm()
		try: form.reviewer.data = session['rev']
		except: pass
		form.date.data = time.strftime("%d-%m-%Y")
		return render_template('index_finalalt2.1.html', form=form,list_of_defects=list_of_defects,project_name = project_name)		
	if request.method =="POST":
		elements = get_dropdown()
		elements_length = len(elements)
		if elements_length == 0:
			return redirect(url_for('complete'))
		class DynamicForm(NameForm): pass
		count = 1
		trav = 1
		for el in elements:
			num = str(count)
			setattr(DynamicForm, "check" + num, StringField("Inspection" +" " + num + ":",default = el[1]) )
			setattr(DynamicForm, "result" + num, BooleanField ('Inspection approved?') )
			setattr(DynamicForm, "comment" + num, SelectField ('Comments/Defects:', choices=()) )
			setattr(DynamicForm , "Submit" , SubmitField ("Submit"))
			count +=1
		form = DynamicForm()
		session['rev'] = form.reviewer.data
		session['dat'] = form.date.data
		while trav <= elements_length:
			x = str(trav)
			check = "check" + x
			result = "result" + x
			comment = "comment" + x
			session['che'] = request.form[check]
			session['com'] = request.form[comment]
			session['res'] = request.form.get(result, 0)
			if session.get('res') == "y":
				session['res'] = 1
			object = len(session.get('che'))
			if object > 0:
				obj1 = session.get('che')
				obj2 = obj1.split(",")
				obj3 = obj2[1]
				obj4 = obj2[2]
				with lite.connect(DATABASE) as con:
					cur = con.cursor()
					cur.execute("SELECT ID FROM objects WHERE GUID = ?",(obj3,))
					item1 = cur.fetchone()
					item2 = item1[0]
					cur.execute("SELECT ID FROM requirements WHERE Check_required = ?",(obj4,))
					item3 = cur.fetchone()
					item4 = item3[0]
					cur.execute("SELECT ID FROM inspections WHERE ObjectID = ? AND CheckID = ?",(item2,item4))
					item5 = cur.fetchone()
					item6 = item5[0]
					validate_name(form,session.get('res'),session.get('com'))
					cur.execute("INSERT INTO results VALUES (NULL,?,?,?,?,?)",(item6,session.get('rev'),session.get('res'),session.get('com'),session.get('dat')))
					con.commit()
			else:
				break
				flash("Record added successfully")
			trav +=1	
		collada.setup_colorcoding()
		collada.colorcode_model()
		flash("Record added successfully")
		return redirect(url_for('index'))
		
@app.route('/complete')
def complete():
	return render_template('complete.html')
	
@app.route('/location/<name>')
def location(name):
		processed = name.split(",")
		id = processed[1]
		return render_template('location.html', id = id)
	
	
def validate_name(form, field1,field2):
		if field1 == 0 and field2 == "":
			raise ValidationError('Rejected inspection always require comments')			
			
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'),404

if __name__ == "__main__":
	app.run(debug=True)