import os
import xml.etree.ElementTree as et
import shutil
import sqlite3 as lite
import ifcopenshell
import zipfile
from lxml import etree
from datetime import datetime

full_path = ""
zipped_file = ""

def create_new_bcf_report():
	newpath = r'C:\Users\esper\Desktop\Tue\7cc10\Thesis\Thesis draft\BCF\BCF report program\BCF_report.bcfzip'
	if os.path.exists(newpath):
		i = 1
		corepath = os.path.splitext(newpath)[0]
		while os.path.exists(newpath):
			x = str(i)
			newpath = corepath + x + ".bcfzip"
			determined_path = corepath + x
			i = i + 1
		else:
			os.makedirs(determined_path)
			global full_path	
			full_path = determined_path
			global zipped_file
			zipped_file = determined_path + ".zip"
	else:
		first_path = os.path.split(newpath)[1]
		stree = ""
		for x in first_path:
			if x == ".":
				break
			else:			
				stree = stree + x
		os.makedirs(stree)
		new_path = os.path.join(os.getcwd(),stree)
		global full_path
		full_path = new_path
		global zipped_file
		zipped_file = new_path + ".zip"		
	
def create_topics():
	DATABASE = r'C:\Users\esper\Desktop\Tue\7CC10\Thesis\Thesis draft\program\Asta project,Hendriks ifc\Newexample.db'
	con = lite.connect(DATABASE)
	cur = con.cursor()
	cur.execute("SELECT objects.GUID,results.result,results.Date_of_inspection,objects.Location,objects.Type,results.comments,results.reviewer FROM objects JOIN inspections ON objects.ID = inspections.ObjectID JOIN results ON inspections.ID = results.InspectionID")
	results = cur.fetchall()
	# We only look at the most recent inspection result  for the entry. The assumption is that the older result issues have been resolved
	temp = {}
	for key,number,date,ref,typ,comment,review in results:
		if key not in temp:
			temp[key] = (key,number,date,ref,typ,comment,review)
		else:
			if temp[key][2] < date:
				temp[key] = (key,number,date,ref,typ,comment,review)		
	for key in temp:
		# only rejected inspections are considered
		if temp[key][1] == "0":
			id = temp[key][0]
			reference = temp[key][3]
			topic = temp[key][4]
			reason = temp[key][5]
			date = temp[key][2]
			reviewer = temp[key][6]
			newid = ifcopenshell.guid.split(ifcopenshell.guid.expand(id))
			#remove curly brackets
			newid = newid[1:-1]
			newfolder = os.path.join(full_path,newid)
			if not os.path.exists(newfolder):
				os.makedirs(newfolder)
				create_bcfschema(newfolder)
				create_markup(newfolder,newid,reference,topic,reason,date,reviewer)
				create_viewpoint(newfolder,id)
	shutil.make_archive(full_path,"zip",full_path)			
	path = os.getcwd()
	b = os.path.join(path,full_path)
	base = os.path.splitext(b)[0]
	os.rename(zipped_file,base + ".bcfzip")
	shutil.rmtree(full_path)

def create_bcfschema(folder):
	namespace = "http://www.w3.org/2001/XMLSchema-instance"
	location_attribute = '{%s}noNameSpaceSchemaLocation' % namespace
	root = et.Element("Version",attrib = {location_attribute: 'version.xsd'})
	root.set("VersionId","2.0")
	body = et.SubElement(root,"DetailedVersion")
	body.text = "2.0 RC"
	tree = et.ElementTree(root)
	tree.write("bcf.version",xml_declaration = True ,encoding = 'utf-8')
	path = os.getcwd()
	source = os.path.join(path,"bcf.version")
	destination = os.path.join(folder,"bcf.version")
	shutil.move(source,destination)
		
def create_markup(folder,atr,parameter1,parameter2,parameter3,parameter4,parameter5):
	xsi_ns =  "http://www.w3.org/2001/XMLSchema-instance"
	xsd_ns =  "http://www.w3.org/2001/XMLSchema"
	needed = datetime.strptime(parameter4, '%d-%m-%Y').strftime('%Y-%m-%d')
	needed_string = str(needed)
	root = etree.Element("Markup", nsmap = {"xsi":xsi_ns,"xsd":xsd_ns})
	subroot1 = etree.SubElement(root,"Header")
	subroot2 = etree.SubElement(root,"Topic")
	subroot2.set("Guid",atr)
	subroot3 = etree.SubElement(root,"Comment")
	subroot3.set('Guid',atr)
	internalsubroot1 = etree.SubElement(subroot2,"ReferenceLink")
	internalsubroot1.text = parameter1
	internalsubroot2 = etree.SubElement(subroot2,"Topic")
	internalsubroot2.text = parameter2
	internalsubroot3 = etree.SubElement(subroot3,"Date")
	internalsubroot3.text = needed_string
	internalsubroot4 = etree.SubElement(subroot3,"Author")
	internalsubroot4.text = parameter5
	internalsubroot5 = etree.SubElement(subroot3,"Comment")
	internalsubroot5.text = parameter3
	tree = etree.ElementTree(root)
	tree.write("markup.bcf",xml_declaration = True ,encoding = 'utf-8')
	path = os.getcwd()
	source = os.path.join(path,"markup.bcf")
	destination = os.path.join(folder,"markup.bcf")
	shutil.move(source,destination)

def create_viewpoint(folder,atr):
	xsi =  "http://www.w3.org/2001/XMLSchema-instance"
	xsd =  "http://www.w3.org/2001/XMLSchema"
	root  = etree.Element("VisualizationInfo", nsmap = {"xsi":xsi,"xsd":xsd})
	subroot1 = etree.SubElement(root,"Components")
	subroot2 = etree.SubElement(subroot1,"Component")
	subroot2.set("IfcGuid",atr)
	tree = etree.ElementTree(root)
	tree.write("viewpoint.bcfv",xml_declaration = True ,encoding = 'utf-8')
	path = os.getcwd()
	source = os.path.join(path,"viewpoint.bcfv")
	destination = os.path.join(folder,"viewpoint.bcfv")
	shutil.move(source,destination)
	
create_new_bcf_report()
create_topics()




