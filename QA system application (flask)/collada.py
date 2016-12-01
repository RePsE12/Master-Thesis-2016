def setup_colorcoding():
	import xml.etree.ElementTree as et
	et.register_namespace("", "http://www.collada.org/2005/11/COLLADASchema")
	import os
	path = os.getcwd()
	file = os.path.join(path,"static\models\Situatie_totaal4D.dae")
	model = et.parse(file)
	root = model.getroot()	
	material = root.find('{http://www.collada.org/2005/11/COLLADASchema}library_materials')
	Boo_app = False
	Boo_rej = False
	Boo_neutral = False
	for child in material:
		if child.attrib['id'] == "approved_material":
			Boo_app = True
		else:
			pass
		if child.attrib['id'] == "rejected_material":	
			Boo_rej = True
		else:
			pass
		if child.attrib['id'] == "neutral_material":	
			Boo_neutral = True
		else:
			pass
	if Boo_app == False:		
		approved = et.SubElement(material,"{http://www.collada.org/2005/11/COLLADASchema}material", id="approved_material")
		instance_green = et.SubElement(approved,"{http://www.collada.org/2005/11/COLLADASchema}instance_effect",url="#approved_material_fx")
	if Boo_rej == False:
		rejected = et.SubElement(material,"{http://www.collada.org/2005/11/COLLADASchema}material",id="rejected_material")
		instance_red = et.SubElement(rejected,"{http://www.collada.org/2005/11/COLLADASchema}instance_effect",url = "#rejected_material_fx")
	if Boo_neutral == False:
		neutr = et.SubElement(material,"{http://www.collada.org/2005/11/COLLADASchema}material",id="neutral_material")
		instance_neutr = et.SubElement(neutr,"{http://www.collada.org/2005/11/COLLADASchema}instance_effect",url = "#neutral_material_fx")
	effects = root.find('{http://www.collada.org/2005/11/COLLADASchema}library_effects')
	Boo_eff1 = False
	Boo_eff2 = False
	Boo_eff3 = False
	for child in effects:	
		if child.attrib['id'] == "approved_material_fx":
			Boo_eff1 = True
		else:
			pass
		if child.attrib['id'] == "rejected_material_fx":
			Boo_eff2 = True
		else:
			pass
		if child.attrib['id'] == "neutral_material_fx":
			Boo_eff3 = True
		else:
			pass
	if Boo_eff1 == False:		
		app_effect = et.SubElement(effects,"{http://www.collada.org/2005/11/COLLADASchema}effect",id ="approved_material_fx")
		app_profile = et.SubElement(app_effect,"{http://www.collada.org/2005/11/COLLADASchema}profile_COMMON")
		app_tech = et.SubElement(app_profile,"{http://www.collada.org/2005/11/COLLADASchema}technique", sid="common")
		app_lamb = et.SubElement(app_tech,"{http://www.collada.org/2005/11/COLLADASchema}lambert")
		app_diff = et.SubElement(app_lamb,"{http://www.collada.org/2005/11/COLLADASchema}diffuse")
		app_col = et.SubElement(app_diff,"{http://www.collada.org/2005/11/COLLADASchema}color")
		app_col.text = "0.2 1 0 1"
		app_spec = et.SubElement(app_lamb,"{http://www.collada.org/2005/11/COLLADASchema}specular")
		app_colo = et.SubElement(app_spec,"{http://www.collada.org/2005/11/COLLADASchema}color")
		app_colo.text = "0.2 1 0 1"
		app_shine = et.SubElement(app_lamb,"{http://www.collada.org/2005/11/COLLADASchema}shininess")
		app_flo = et.SubElement(app_shine,"{http://www.collada.org/2005/11/COLLADASchema}float")
		app_flo.text = "64"
	if Boo_eff2 == False:
		rej_effect = et.SubElement(effects,"{http://www.collada.org/2005/11/COLLADASchema}effect",id = "rejected_material_fx")
		rej_profile = et.SubElement(rej_effect,"{http://www.collada.org/2005/11/COLLADASchema}profile_COMMON")
		rej_tech = et.SubElement(rej_profile,"{http://www.collada.org/2005/11/COLLADASchema}technique",sid ="common")
		rej_lamb = et.SubElement(rej_tech,"{http://www.collada.org/2005/11/COLLADASchema}lambert")
		rej_diff = et.SubElement(rej_lamb,"{http://www.collada.org/2005/11/COLLADASchema}diffuse")
		rej_col = et.SubElement(rej_diff,"{http://www.collada.org/2005/11/COLLADASchema}color")
		rej_col.text = "0.6 0 0 1"
		rej_spec = et.SubElement(rej_lamb,"{http://www.collada.org/2005/11/COLLADASchema}specular")
		rej_colo = et.SubElement(rej_spec,"{http://www.collada.org/2005/11/COLLADASchema}color")
		rej_colo.text = "0.6 0 0 1"
		rej_shine = et.SubElement(rej_lamb,"{http://www.collada.org/2005/11/COLLADASchema}shininess")
		rej_flo = et.SubElement(rej_shine,"{http://www.collada.org/2005/11/COLLADASchema}float")
		rej_flo.text = "64"
	if Boo_eff3 == False:
		neu_effect = et.SubElement(effects,"{http://www.collada.org/2005/11/COLLADASchema}effect",id = "neutral_material_fx")
		neu_profile = et.SubElement(neu_effect,"{http://www.collada.org/2005/11/COLLADASchema}profile_COMMON")
		neu_tech = et.SubElement(neu_profile,"{http://www.collada.org/2005/11/COLLADASchema}technique",sid ="common")
		neu_lamb = et.SubElement(neu_tech,"{http://www.collada.org/2005/11/COLLADASchema}lambert")
		neu_diff = et.SubElement(neu_lamb,"{http://www.collada.org/2005/11/COLLADASchema}diffuse")
		neu_col = et.SubElement(neu_diff,"{http://www.collada.org/2005/11/COLLADASchema}color")
		neu_col.text = "0.9 1 0.9 1"
		neu_spec = et.SubElement(neu_lamb,"{http://www.collada.org/2005/11/COLLADASchema}specular")
		neu_colo = et.SubElement(neu_spec,"{http://www.collada.org/2005/11/COLLADASchema}color")
		neu_colo.text = "0.9 1 0.9 1"
		neu_shine = et.SubElement(neu_lamb,"{http://www.collada.org/2005/11/COLLADASchema}shininess")
		neu_flo = et.SubElement(neu_shine,"{http://www.collada.org/2005/11/COLLADASchema}float")
		neu_flo.text = "64"
	model.write(file)
	
def colorcode_model():
	import xml.etree.ElementTree as et
	et.register_namespace("", "http://www.collada.org/2005/11/COLLADASchema")
	import sqlite3 as lite
	import ifcopenshell
	import os
	path = os.getcwd()
	file = os.path.join(path,"static\models\Situatie_totaal4D.dae")
	model = et.parse(file)
	root = model.getroot()	
	con = lite.connect(r'C:\Users\esper\Desktop\Tue\7CC10\Thesis\Thesis draft\Program\Asta project,hendriks ifc\Newexample.db')
	cur = con.cursor()
	cur.execute("SELECT objects.GUID,results.result FROM objects JOIN inspections ON objects.ID = inspections.ObjectID JOIN results ON inspections.ID = results.InspectionID WHERE result = 0 OR result = 1 ")
	trial = cur.fetchall()		
	# change all elements to the base color of the neutral condition	
	for node in root.iter("{http://www.collada.org/2005/11/COLLADASchema}node"):
		x = node[1][0][0][0]
		x.attrib['symbol'] = "neutral_material"
		x.attrib['target'] = "#neutral_material"
	for node in root.iter("{http://www.collada.org/2005/11/COLLADASchema}node"):
		id = node.attrib['id']
		if id.startswith("product-"):
			id = id[8:]
		if id.endswith("-body"):
			id = id[:-5]
		id = ifcopenshell.guid.compress(id.replace("-", ""))
		for x in trial:
			if x[0] == id:
				element = node[1][0][0][0]
				if x[1] == "0":
					element.attrib['symbol'] = "rejected_material"
					element.attrib['target'] = "#rejected_material"
				if x[1] == "1":
					element.attrib['symbol'] = "approved_material"
					element.attrib['target'] = "#approved_material"
	model.write(file)

# Run the color coding app
setup_colorcoding()
colorcode_model()	
	
