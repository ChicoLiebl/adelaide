import sys
import FreeCAD
import importDXF
import Draft
import Import

### Enable legacy importer ###
### Make sure dxf-library addon is installed ###
params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
params.SetBool("dxfUseLegacyImporter", True)

# ------------------------------
# CLI args validation
# ------------------------------
if len(sys.argv) < 5:
    print("Usage: freecadcmd import_svg.py <input.dxf> <output.step> <mold cavity height> <mold thickness>")
    sys.exit(1)

input_file = sys.argv[2]
output_file = sys.argv[3]
height = float(sys.argv[4])
thickness = float(sys.argv[5])

print(f"Input: {input_file}, Output: {output_file}, Cavity Height: {height}mm, Thickness: {sys.argv[4]}mm")
# exit(0)
# ------------------------------
# Create a new FreeCAD document
# ------------------------------
doc = FreeCAD.newDocument("SVG_to_STEP")

# ------------------------------
# Import SVG
# ------------------------------
importDXF.insert(input_file, doc.Name)
doc.recompute()

# Collect all imported objects
imported_objs = [obj for obj in doc.Objects]
if not imported_objs:
    print("❌ No objects were imported! Check DXF file or importer settings.")
    sys.exit(1)

# Connect wires
imported_objs, _ = Draft.upgrade(imported_objs, delete=True)

# ------------------------------
# Create a sketch from imported geometry
# ------------------------------
svg_sketch = Draft.makeSketch(imported_objs, autoconstraints=True)
doc.recompute()


# Optionally remove the original imported objects (we keep only the sketch)
for obj in imported_objs:
    try:
        doc.removeObject(obj.Name)
    except Exception:
        pass
doc.recompute()

# ------------------------------
# Compute bounding box of the imported sketch
# ------------------------------
# Use the Sketch's Shape BoundBox; ensure the sketch shape is up-to-date
try:
    bb = svg_sketch.Shape.BoundBox
except Exception as e:
    print("Could not compute bounding box of sketch:", e)
    sys.exit(1)

min_x, min_y, max_x, max_y = bb.XMin, bb.YMin, bb.XMax, bb.YMax
print(f"Sketch bounding box: X[{min_x}, {max_x}] Y[{min_y}, {max_y}]")

# ------------------------------
# Create a new sketch with a rectangle that fits the bounding box + margin
# ------------------------------
margin = thickness  # mm to add on each side

rect_min_x = min_x - margin
rect_min_y = min_y - margin
rect_width = (max_x - min_x) + 2.0 * margin
rect_height = (max_y - min_y) + 2.0 * margin

print(f"Rectangle origin: ({rect_min_x}, {rect_min_y}), width: {rect_width}, height: {rect_height}")

# Placement for the rectangle: lower-left corner at (rect_min_x, rect_min_y, 0)
placement = FreeCAD.Placement(FreeCAD.Vector(rect_min_x, rect_min_y, 0), FreeCAD.Rotation(0, 0, 0))

# Draft.makeRectangle(length, height, placement=...) creates a Draft rectangle object.
rect = Draft.makeRectangle(rect_width, rect_height, placement=placement, face=False)
doc.recompute()

# Convert the Draft rectangle to a Sketch so we have a Sketch object for extrusion
# Draft.makeSketch accepts a list of objects (we pass the rectangle)
rect_sketch = Draft.makeSketch([rect], autoconstraints=False)
doc.recompute()

# Remove the intermediate Draft rectangle object (we'll keep rect_sketch)
try:
    doc.removeObject(rect.Name)
except Exception:
    pass
doc.recompute()

# ------------------------------
# Extrude the rectangle sketch
# ------------------------------
base_extrusion = doc.addObject("Part::Extrusion", "Extrusion")
base_extrusion.Base = rect_sketch
base_extrusion.Dir = (0, 0, height + thickness)  # Z-direction
base_extrusion.Solid = True
base_extrusion.TaperAngle = 0
doc.recompute()

slot_extrusion = doc.addObject("Part::Extrusion", "SlotExtrusion")
slot_extrusion.Base = svg_sketch
slot_extrusion.Dir = (0, 0, height)  # Negative Z so it cuts downward
slot_extrusion.Solid = True
slot_extrusion.TaperAngle = 0
doc.recompute()

# ------------------------------
# Cut the slot from the base solid
# ------------------------------
cut_obj = doc.addObject("Part::Cut", "FinalSolid")
cut_obj.Base = base_extrusion
cut_obj.Tool = slot_extrusion
doc.recompute()
# ------------------------------
# Save intermediate FreeCAD project
# ------------------------------
project_name = input_file.split(".")[0] + ".FCStd"
# doc.saveAs(project_name)

# ------------------------------
# Export to STEP
# ------------------------------
Import.export([cut_obj], output_file)
print(f"✅ Imported '{input_file}', created mold with cavity height {height}mm and thickness {thickness}mm, exported as STEP → '{output_file}'")
