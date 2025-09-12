import sys
import FreeCAD
import importDXF
import Draft
import Import
import Part

def solid_extrusion_from_dxf (dxf_file, height, freecad_doc):
    ### Enable legacy DXF importer ###
    params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    params.SetBool("dxfUseLegacyImporter", True)

    doc = freecad_doc;

    # --- Import DXF into FreeCAD document ---
    importDXF.insert(dxf_file, doc.Name)
    doc.recompute()

    # Collect all imported objects
    imported_objs = [obj for obj in doc.Objects if hasattr(obj, "Shape") and obj.Shape.Edges]
    if not imported_objs:
        print("❌ No objects were imported! Check DXF file or importer settings.")
        sys.exit(1)

    print(f"✅ Imported {len(imported_objs)} objects")

    # --- Separate circles and non-circles ---
    circle_objs = []
    non_circle_objs = []

    for obj in imported_objs:
        shape = obj.Shape
        is_circle = False

        # Detect circles by checking if they are a single edge and a closed shape
        if len(shape.Edges) == 1:
            edge = shape.Edges[0]
            if isinstance(edge.Curve, Part.Circle) and shape.Closed:
                is_circle = True

        if is_circle:
            circle_objs.append(obj)
        else:
            non_circle_objs.append(obj)

    print(f"🔹 Circles detected: {len(circle_objs)}")
    print(f"🔹 Other geometry: {len(non_circle_objs)}")

    if not non_circle_objs:
        print("❌ No non-circle geometry found. Cannot proceed with extrusion.")
        sys.exit(1)

    # --- Create two separate sketches ---
    print("Creating Sketch for non-circle geometry...")
    sketch_main = Draft.makeSketch(non_circle_objs, autoconstraints=True)
    doc.recompute()

    print("Creating Sketch for circle geometry...")
    sketch_circles = None
    if circle_objs:
        sketch_circles = Draft.makeSketch(circle_objs, autoconstraints=True)
        doc.recompute()

    # Cleanup original imported Draft wires
    for obj in imported_objs:
        try:
            doc.removeObject(obj.Name)
        except Exception:
            pass
    doc.recompute()

    # --- Extrude the main sketch ---
    print(f"Extruding main sketch by {height} mm...")
    extrusion = doc.addObject("Part::Extrusion", "MainExtrusion")
    extrusion.Base = sketch_main
    extrusion.Dir = (0, 0, height)
    extrusion.Solid = True
    extrusion.TaperAngle = 0
    doc.recompute()

    result_solid = extrusion

    # doc.saveAs(input_file.split(".")[0] + ".FCStd")

    # --- Cut circular holes (if any) ---
    CUT_DEPTH = height # depth for circle cut
    if sketch_circles:
        print(f"Cutting circular holes with {CUT_DEPTH} mm depth...")

        # Extrude circle sketch DOWNWARDS to cut material
        cut_tool = doc.addObject("Part::Extrusion", "CircleCutExtrusion")
        cut_tool.Base = sketch_circles
        cut_tool.Dir = (0, 0, CUT_DEPTH)  # negative Z direction
        cut_tool.Solid = True
        cut_tool.TaperAngle = 0
        doc.recompute()

        # Perform the cut
        cut_obj = doc.addObject("Part::Cut", "FinalCut")
        cut_obj.Base = result_solid
        cut_obj.Tool = cut_tool
        doc.recompute()

        result_solid = cut_obj

    return result_solid



def main():
    if len(sys.argv) < 5:
        print("Usage: freecadcmd process_dxf.py <input.dxf> <output.step> <extrusion_height_mm>")
        sys.exit(1)

    print(f"Input: {sys.argv[2]}, Output: {sys.argv[3]}, Extrusion Height: {sys.argv[4]}")
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    height = float(sys.argv[4])

    doc = FreeCAD.newDocument("Solid_from_DXF")

    solid = solid_extrusion_from_dxf(input_file, height, doc)

    # --- Export to STEP ---
    print(f"Exporting final solid to STEP: {output_file}")
    Import.export([solid], output_file)

    print(f"Done! Result saved to {output_file}")


""" When running with freecadcmd name is set to filename """
if __name__ == "__main__" or __name__ == "dxf_to_solid":
    main()