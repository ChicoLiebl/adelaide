

BASE_DIR=$(git rev-parse --show-toplevel)
PCB_FILE="$BASE_DIR/$1"
PROJECT_NAME=$(echo $PCB_FILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long) 
OUT_DIR="$BASE_DIR/FAB-OUTPUTS/$PROJECT_NAME-case-$(date +%y-%m-%d)-$GIT_VERSION"

mkdir -p $OUT_DIR

OUT_DIR_2D="$OUT_DIR/2D"
mkdir -p $OUT_DIR_2D

kicad-cli pcb export dxf --layers "F.Courtyard,User.Eco1,B.Courtyard,User.Eco2" --udo --ou mm --drill-shape-opt 0 --cl "Edge.Cuts" --mode-multi -o "$OUT_DIR_2D" "$PCB_FILE"

OUT_DIR_3D="$OUT_DIR/3D"
mkdir -p "$OUT_DIR_3D"

# Top plate
freecadcmd "$BASE_DIR/scripts/dxf_to_solid.py" "$OUT_DIR_2D/macro-pad-User_Eco1.dxf" "$OUT_DIR_3D/top-plate.step" 1.4
freecadcmd "$BASE_DIR/scripts/dxf_to_solid.py" "$OUT_DIR_2D/macro-pad-User_Eco2.dxf" "$OUT_DIR_3D/bottom-plate.step" 2
freecadcmd "$BASE_DIR/scripts/generate_mold.py" "$OUT_DIR_2D/macro-pad-F_Courtyard.dxf" "$OUT_DIR_3D/top-spacer-mold.step" 4.5 2
freecadcmd "$BASE_DIR/scripts/generate_mold.py" "$OUT_DIR_2D/macro-pad-B_Courtyard.dxf" "$OUT_DIR_3D/bottom-spacer-mold.step" 4.5 2