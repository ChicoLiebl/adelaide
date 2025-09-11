

BASE_DIR=$(git rev-parse --show-toplevel)
PCB_FILE="$BASE_DIR/$1"
PROJECT_NAME=$(echo $PCB_FILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long) 
OUT_DIR="$BASE_DIR/FAB-OUTPUTS/$PROJECT_NAME-case-$(date +%y-%m-%d)-$GIT_VERSION"

mkdir -p $OUT_DIR

OUT_DIR_2D="$OUT_DIR/2D"
mkdir -p $OUT_DIR_2D


kicad-cli pcb export dxf --layers "F.Courtyard,Edge.Cuts" --udo --ou mm --drill-shape-opt 0 --cl "" --mode-single -o "$OUT_DIR_2D/top-spacer.dxf" "$PCB_FILE"
kicad-cli pcb export dxf --layers "User.Eco1,Edge.Cuts" --udo --ou mm --drill-shape-opt 0 --cl "" --mode-single -o "$OUT_DIR_2D/top-plate.dxf" "$PCB_FILE"
kicad-cli pcb export dxf --layers "B.Courtyard,Edge.Cuts" --udo --ou mm --drill-shape-opt 0 --cl "" --mode-single -o "$OUT_DIR_2D/bottom-spacer.dxf" "$PCB_FILE"
kicad-cli pcb export dxf --layers "User.Eco1" --udo --ou mm --drill-shape-opt 0 --cl "" --mode-single -o "$OUT_DIR_2D/holes.dxf" "$PCB_FILE"
kicad-cli pcb export dxf --layers "Edge.Cuts" --udo --ou mm --drill-shape-opt 0 --cl "" --mode-single -o "$OUT_DIR_2D/edge.dxf" "$PCB_FILE"

OUT_DIR_3D="$OUT_DIR/3D"
mkdir -p "$OUT_DIR_3D"

# Top plate
freecadcmd "$BASE_DIR/scripts/svg_to_solid.py" "$OUT_DIR_2D/top-plate.dxf" "$OUT_DIR_3D/top-plate.step" 1.4
freecadcmd "$BASE_DIR/scripts/generate_mold.py" "$OUT_DIR_2D/top-spacer.dxf" "$OUT_DIR_3D/top-spacer-mold.step" 4.5 2