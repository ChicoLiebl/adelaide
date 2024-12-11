function log_green {
  echo -e "\033[1;32m$1\033[0m"
}

function log_yellow {
  echo -e "\033[1;33m$1\033[0m"
}

function log_red {
  echo -e "\033[1;31m$1\033[0m"
}



BASE_DIR=.
GIT_VERSION=$(git describe --abbrev=6 --dirty --always --tags --long) OUT_DIR="$BASE_DIR/FAB-OUTPUTS/Fab-$(date +%y-%m-%d)-$GIT_VERSION"
# Create out dir
mkdir -p $OUT_DIR
mkdir -p $BASE_DIR/.temp

PROJECT_NAME="adelaide"

PCB_FILE="pcb/$PROJECT_NAME.kicad_pcb"
SCHEMATIC_FILE="pcb/$PROJECT_NAME.kicad_sch"
OUT_NAME="adelaide_{}"


cp $BASE_DIR/$PCB_FILE $BASE_DIR/.temp/temp-pcb.kicad_pcb
sed -i "s/--GIT HASH--/$GIT_VERSION/g" $BASE_DIR/$PCB_FILE

function finish {
  cp $BASE_DIR/.temp/temp-pcb.kicad_pcb $BASE_DIR/$PCB_FILE
  rm -rf $BASE_DIR/.temp
}

function check_status {
  if [ "$1" != "0" ]; then
    log_red Failed
    finish
    exit
  fi
}

# Generate output files

if [ "$1" = "--pcbway" ]; then

log_yellow 'Generating board files for PCBWay'

kikit fab pcbway --nametemplate "$OUT_NAME" --assembly --schematic $SCHEMATIC_FILE $PCB_FILE $OUT_DIR
check_status $?

log_green Success

else
log_yellow 'Generating board files for JLCPCB'

kikit fab jlcpcb --nametemplate "$OUT_NAME" --assembly --schematic $SCHEMATIC_FILE $PCB_FILE $OUT_DIR
check_status $?

log_green Success

fi

finish
