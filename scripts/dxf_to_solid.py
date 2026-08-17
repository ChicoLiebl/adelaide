import os
import sys
import FreeCAD
import importDXF
import Part

def solid_extrusion_from_dxf (dxf_file, height, freecad_doc):
    ### Enable legacy DXF importer ###
    params = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
    params.SetBool("dxfUseLegacyImporter", True)

    doc = freecad_doc

    # --- Import DXF into FreeCAD document ---
    importDXF.insert(dxf_file, doc.Name)
    doc.recompute()

    # Collect all imported objects
    imported_objs = [obj for obj in doc.Objects if hasattr(obj, "Shape") and obj.Shape.Edges]
    if not imported_objs:
        print("❌ No objects were imported! Check DXF file or importer settings.")
        sys.exit(1)

    print(f"✅ Imported {len(imported_objs)} objects")

    # --- Collect all edges and sort them into closed wires ---
    edges = []
    for obj in imported_objs:
        edges.extend(obj.Shape.Edges)

    wires = []
    open_loops = 0
    for edge_loop in Part.sortEdges(edges):
        try:
            wire = Part.Wire(edge_loop)
            if wire.isClosed():
                wires.append(wire)
            else:
                open_loops += 1
        except Exception:
            open_loops += 1

    # Cleanup original imported Draft objects
    for obj in imported_objs:
        try:
            doc.removeObject(obj.Name)
        except Exception:
            pass
    doc.recompute()

    print(f"🔹 Closed wires: {len(wires)} (skipped {open_loops} open loops)")
    if not wires:
        print("❌ No closed wires found. Cannot proceed with extrusion.")
        sys.exit(1)

    # --- Build the 2D region with booleans (robust against overlapping
    #     geometry, e.g. courtyard outlines of adjacent components) ---
    faces = []
    for wire in wires:
        try:
            faces.append(Part.Face(wire))
        except Exception as e:
            print(f"⚠️ Skipping wire that could not become a face: {e}")

    # The wire with the largest face is the outline; everything else is a hole
    outline = max(faces, key=lambda f: f.Area)
    holes = [f for f in faces if f is not outline]
    print(f"🔹 Outline area: {outline.Area:.1f} mm², holes: {len(holes)}")

    region = outline
    if holes:
        cut_tool = holes[0] if len(holes) == 1 else holes[0].multiFuse(holes[1:])
        region = outline.cut(cut_tool)
    region = region.removeSplitter()

    # --- Extrude the clean region ---
    print(f"Extruding region by {height} mm...")
    solid_shape = region.extrude(FreeCAD.Vector(0, 0, height))
    if not solid_shape.isValid():
        print("❌ Extruded solid is invalid.")
        sys.exit(1)

    result_solid = doc.addObject("Part::Feature", "Solid")
    result_solid.Shape = solid_shape
    doc.recompute()

    return result_solid



def load_open_wires(dxf_file, freecad_doc):
    """Import a DXF of line segments and chain them into wires (may be open)."""
    doc = freecad_doc
    before = set(obj.Name for obj in doc.Objects)
    importDXF.insert(dxf_file, doc.Name)
    doc.recompute()

    imported = [obj for obj in doc.Objects if obj.Name not in before
                and hasattr(obj, "Shape") and obj.Shape.Edges]
    edges = []
    for obj in imported:
        edges.extend(obj.Shape.Edges)
    for obj in imported:
        try:
            doc.removeObject(obj.Name)
        except Exception:
            pass
    doc.recompute()

    wires = []
    for edge_loop in Part.sortEdges(edges):
        try:
            wires.append(Part.Wire(edge_loop))
        except Exception as e:
            print(f"⚠️ Skipping unchainable split segments: {e}")
    return wires


def extend_wire_ends(wire, length):
    """Prolong both free ends of an open wire along their end directions."""
    if wire.isClosed():
        return wire
    verts = [v.Point for v in wire.OrderedVertexes]
    extra = []
    d_start = (verts[0] - verts[1]).normalize()
    extra.append(Part.makeLine(verts[0], verts[0] + d_start * length))
    d_end = (verts[-1] - verts[-2]).normalize()
    extra.append(Part.makeLine(verts[-1], verts[-1] + d_end * length))
    return Part.Wire(Part.sortEdges(list(wire.Edges) + extra)[0])


def split_shape(shape, split_dxf, freecad_doc, extend=10.0):
    """Slice a solid with the (vertical) surface extruded from the split
    polyline in split_dxf. Returns (left, right) shapes sorted by X."""
    import BOPTools.SplitAPI

    wires = load_open_wires(split_dxf, freecad_doc)
    if not wires:
        print(f"❌ No split lines found in {split_dxf}")
        sys.exit(1)

    bb = shape.BoundBox
    knives = []
    for wire in wires:
        wire = extend_wire_ends(wire, extend)
        wire.translate(FreeCAD.Vector(0, 0, bb.ZMin - 1))
        knives.append(wire.extrude(FreeCAD.Vector(0, 0, bb.ZLength + 2)))

    pieces = BOPTools.SplitAPI.slice(shape, knives, "Split").Solids
    if len(pieces) < 2:
        print("❌ Split line did not cut the part in two.")
        sys.exit(1)

    # Group pieces by which side of the knife their center lies on
    knife_x = sum(v.Point.x for w in wires for v in w.Vertexes) / \
              sum(len(w.Vertexes) for w in wires)
    left = [p for p in pieces if p.CenterOfMass.x < knife_x]
    right = [p for p in pieces if p.CenterOfMass.x >= knife_x]
    if not left or not right:
        left = [min(pieces, key=lambda p: p.CenterOfMass.x)]
        right = [p for p in pieces if p is not left[0]]
    fuse = lambda ps: ps[0] if len(ps) == 1 else ps[0].multiFuse(ps[1:])
    return fuse(left), fuse(right)


def export_split_parts(shape, split_dxf, output_file, freecad_doc):
    """Export the two halves of `shape` as <output>-left/right.step."""
    import Import
    left, right = split_shape(shape, split_dxf, freecad_doc)
    base = output_file[:-len(".step")] if output_file.endswith(".step") else output_file
    for name, half in (("left", left), ("right", right)):
        obj = freecad_doc.addObject("Part::Feature", f"Split_{name}")
        obj.Shape = half
        out = f"{base}-{name}.step"
        Import.export([obj], out)
        print(f"✅ Split part saved to {out}")


def main():
    if len(sys.argv) < 5:
        print("Usage: freecadcmd dxf_to_solid.py <input.dxf> <output.step> <extrusion_height_mm> [split_line.dxf]")
        sys.exit(1)

    print(f"Input: {sys.argv[2]}, Output: {sys.argv[3]}, Extrusion Height: {sys.argv[4]}")
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    height = float(sys.argv[4])
    split_file = sys.argv[5] if len(sys.argv) > 5 else None

    doc = FreeCAD.newDocument("Solid_from_DXF")

    solid = solid_extrusion_from_dxf(input_file, height, doc)

    # --- Export to STEP ---
    print(f"Exporting final solid to STEP: {output_file}")
    import Import
    Import.export([solid], output_file)

    if split_file:
        export_split_parts(solid.Shape, split_file, output_file, doc)

    print(f"Done! Result saved to {output_file}")


# freecadcmd may set __name__ to the filename (old versions) or run the
# script twice (once as the filename, once as "__main__" — FreeCAD 1.1+).
# Checking argv[1] ensures main() only runs when THIS script was invoked,
# not when generate_mold.py imports this module; sys.exit prevents the
# second freecadcmd pass from running everything again.
if len(sys.argv) > 1 and os.path.basename(sys.argv[1]).startswith("dxf_to_solid"):
    main()
    sys.exit(0)
