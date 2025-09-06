
PCB_FILE=$1

PROJECT_NAME=$(echo $PCB_FILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

BASE_DIR=.
GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long) 
OUT_DIR="$BASE_DIR/FAB-OUTPUTS/$PROJECT_NAME-case-$(date +%y-%m-%d)-$GIT_VERSION"

mkdir -p $OUT_DIR

kicad-cli pcb export dxf --layers "F.Courtyard,Edge.Cuts" --drill-shape-opt 0 --ou mm --cl "" --udo --mode-single  -o "$OUT_DIR/top-plate.dxf" $PCB_FILE
kicad-cli pcb export dxf --layers "B.Courtyard,Edge.Cuts" --drill-shape-opt 0 --ou mm --cl "" --udo --mode-single  -o "$OUT_DIR/bottom-plate.dxf" $PCB_FILE