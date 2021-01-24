import pandas as pd
import os
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET

def readCSVs(path):
	_, _, filenames = next(os.walk(path))

	headerList = []

	for file in filenames:
		if "csv" in file and "header" not in file:
			df = pd.read_csv(file)
			headerList.append({
					"tableName":file,
					"columns":[column for column in df.columns]
					})			

	return headerList

input("Please copy all your source table into the src_directory, then press ENTER")
os.chdir('src_table')
tables = readCSVs(os.getcwd())
os.chdir('..')



mxGraphModel = ET.Element('mxGraphModel')

gModelAttrbName = ["dx","dy","grid","gridSize","guides","tooltips","connect","arrows","fold","page","pageScale","pageWidth","pageHeight","math","shadow"]
gModelAttrbValue = [1422,762,1,10,1,1,1,1,1,1,1,850,1100,0,0]

for i in range(0,len(gModelAttrbValue)):
	mxGraphModel.set(gModelAttrbName[i], str(gModelAttrbValue[i]))

root = ET.SubElement(mxGraphModel, 'root')

mxCell0 = ET.SubElement(root, 'mxCell', id="0")
mxCell1 = ET.SubElement(root, 'mxCell', id="1", parent="0")

for idx,table in enumerate(tables):
	tableCell = ET.SubElement(root, 'mxCell',parent="1", vertex="1")
	tableCell.set('value', table['tableName'])
	tableCell.set('id', "id_" + str(table['tableName']) )
	tableCell.set('style', "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;")
	geometry = ET.SubElement(tableCell, 'mxGeometry', x=str(idx * 140), y=str(104), width=str(140), height=str(104))
	geometry.set("as","geometry")

	for cID in range(0,len(table['columns'])):
		col = ET.SubElement(root, 'mxCell', id="id_" + str(table['tableName']) + "-"+str(cID), parent="id_" + str(table['tableName']))
		col.set("value",table['columns'][cID])
		col.set("style","text;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;strokeColor=#000000;")
		col.set("vertex","1")
		colGeo = ET.SubElement(col, 'mxGeometry', y=str(26*(cID+1)), width=str(140), height=str(26))
		colGeo.set("as","geometry")


dom = parseString(ET.tostring(mxGraphModel))
export = open(".\\export.drawio", "w")
export.write(dom.toprettyxml())
export.close()
