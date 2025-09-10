
PCB_FILE=$1

PROJECT_NAME=$(echo $PCB_FILE | rev | cut -d '/' -f 1 | rev | cut -d '.' -f 1)

BASE_DIR=.
GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long) 
OUT_DIR="$BASE_DIR/FAB-OUTPUTS/$PROJECT_NAME-case-$(date +%y-%m-%d)-$GIT_VERSION"

mkdir -p $OUT_DIR

kicad-cli pcb export svg --layers "F.Courtyard,Edge.Cuts" --drill-shape-opt 0 --cl "" --mode-single --exclude-drawing-sheet  -o "$OUT_DIR/top-plate.svg" $PCB_FILE
kicad-cli pcb export svg --layers "B.Courtyard,Edge.Cuts" --drill-shape-opt 0 --cl "" --mode-single --exclude-drawing-sheet  -o "$OUT_DIR/bottom-plate.svg" $PCB_FILE
kicad-cli pcb export svg --layers "User.Eco1,Edge.Cuts" --drill-shape-opt 0 --cl "" --mode-single --exclude-drawing-sheet  -o "$OUT_DIR/spacer.svg" $PCB_FILE