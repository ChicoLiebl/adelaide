import sys
import FreeCAD
import importDXF
import Draft
import Import

### Enable legacy importer ###
### Make sure dxf-library addon is installed ###
params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
params.SetBool("dxfUseLegacyImporter", True)


if (len(sys.argv) < 3):
    print("Usage: freecadcmd import_svg.py <input.svg> [Output file name] [extrusion heigh in mm]")
    sys.exit(1)

input_file = sys.argv[2]
output_file = sys.argv[3]
height = float(sys.argv[4])

print(input_file, output_file, height)
# Create a new FreeCAD document
doc = FreeCAD.newDocument("SVG_to_STEP")

# Import SVG into the document as Draft objects
importDXF.insert(input_file, doc.Name)
doc.recompute()

# Collect all imported objects
imported_objs = [obj for obj in doc.Objects]
if not imported_objs:
    print("❌ No objects were imported! Check DXF file or importer settings.")
    sys.exit(1)

# Connect wires
imported_objs, _ = Draft.upgrade(imported_objs, delete=True)

# Convert imported wires into a single sketch
sketch = Draft.makeSketch(imported_objs, autoconstraints=True)

doc.recompute()

# Optionally delete the original Draft wires
for obj in imported_objs:
    doc.removeObject(obj.Name)
doc.recompute()

# Extrude the sketch by 1.4 mm along Z
extrusion = doc.addObject("Part::Extrusion", "Extrusion")
extrusion.Base = sketch
extrusion.Dir = (0, 0, height)  # extrusion vector in mm
extrusion.Solid = True
extrusion.TaperAngle = 0
doc.recompute()

# doc.saveAs(input_file.split(".")[0] + ".FCStd")

# # Export the extrusion as STEP
# print(output_file)
Import.export([extrusion], output_file)

print(f"✅ Imported '{input_file}', extruded 1.4 mm, exported as STEP → '{output_file}'")

sys.exit(0)
