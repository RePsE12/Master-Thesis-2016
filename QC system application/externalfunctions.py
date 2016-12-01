import os
import ifcopenshell
import shutil
import subprocess

def make_collada():
	FNULL = open(os.devnull, 'w')
	filename = "Situatie_totaal4D.ifc"
	target = ""
	for x in filename:
		if x != ".":
			target = target + x
		else:
			break			
	args = "ifcConvert.exe" + " " + filename + " " + target + ".dae" 
	subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)

def move_file():	
	x = os.getcwd()
	source = os.path.join(x,"Situatie_totaal4D.dae")
	first = os.getcwd()
	destination = ""
	for letter in first:
		if letter != "P":
			destination = destination + letter
		else:	
			break
	second = os.path.join(destination,"flask\static\models\Situatie_totaal4D.dae")
	# move the model to the static folder to be viewed in the web browser (flask)
	shutil.move(source,second)	

def findwallopening():
	file = ifcopenshell.open('Situatie_totaal4D.ifc')
	properties = file.by_type("IFCRELDEFINESBYPROPERTIES")
	materials = file.by_type('IFCRELASSOCIATESMATERIAL')
	external_walls = []
	exterior_material = []
	withopenings = []
	filtered_walls = []
	final_walls = []
	# A function to determine the external walls : (All walls including insulation and beickwork)
	for property in properties:
		for obj in property.RelatedObjects:
			if obj.is_a("IfcWall"):
				for wall_property in property.RelatingPropertyDefinition.HasProperties:
					if wall_property.Name == "[eigenschappen]position":
						if wall_property.NominalValue.wrappedValue == "Exterior":
							external_walls.append(obj.GlobalId)
	# A function to select only walls that have one of the three material types
	for material in properties:
		for obj1 in material.RelatedObjects:
			if obj1.is_a("IfcWall"):
				for wall_material in material.RelatingPropertyDefinition.HasProperties:
					if wall_material.Name == "IfcMaterial":
						value = wall_material.NominalValue.wrappedValue
						if value == "Steen - kalkzandsteen C":
							exterior_material.append(obj1.GlobalId)
						elif value == "Steen - baksteen geeloranje":
							exterior_material.append(obj1.GlobalId)
						elif value == "Steen - baksteen bruin":
							exterior_material.append(obj1.GlobalId)
						elif value == "Steen - baksteen beige grijs":
							exterior_material.append(obj1.GlobalId)
						elif value == "Hout - Eternit Cedral ":	
							exterior_material.append(obj1.GlobalId)	
	# A function to determine which walls have openings based on comparing areas
	for quantity in properties:
		for obj2 in quantity.RelatedObjects:
			if obj2.is_a("IfcWall"):
				for wall_quantity in quantity.RelatingPropertyDefinition.HasProperties:
					if wall_quantity.Name == "[BaseQuantities[IfcElementQuantity/ArchiCAD BIM Base Quantities]]Length":
						leng = wall_quantity.NominalValue.wrappedValue
						length = (leng/1000) # convert from mm to m
					if wall_quantity.Name == "[BaseQuantities[IfcElementQuantity/ArchiCAD BIM Base Quantities]]Height":
						hei = wall_quantity.NominalValue.wrappedValue
						height = (hei/1000) # convert from mm to m
					if wall_quantity.Name == "[BaseQuantities[IfcElementQuantity/ArchiCAD BIM Base Quantities]]GrossSideArea":
						area = wall_quantity.NominalValue.wrappedValue
				if (length * height) > area + 1.5: # allows for some tolerance
					withopenings.append(obj2.GlobalId)
	# Performing the neccessary comparisons
	for wall1 in external_walls:
		for wall2 in exterior_material:
			if wall1 == wall2:
				filtered_walls.append(wall1)
	for wall3 in filtered_walls:
		for wall4 in withopenings:
			if wall3 == wall4:
				final_walls.append(wall3)
	return final_walls	