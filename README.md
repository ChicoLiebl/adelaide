# Adelaide

Adelaide é um teclado 75% estilo Alice baseado no [Adelheid](https://github.com/floookay/adelheid) que é um fork do Arisu [Arisu PCB](https://github.com/FateNozomi/arisu-pcb)

Adelaide is a 75% Alice style keyboard based on [Adelheid](https://github.com/floookay/adelheid) which is a fork ofArisu [Arisu PCB](https://github.com/FateNozomi/arisu-pcb)

## ESSE PROJETO NÂO ESTÁ PRONTO NEM TESTADO
## THIS NOT FINISHED AND NOT TESTED

## Geração do case / Case generation

O script `scripts/gen-case-cad.sh` exporta as camadas do PCB como DXF e gera os modelos 3D do case (STEP) em `FAB-OUTPUTS/`. Se o PCB tiver as camadas `top.plate.split` (User.1) e `bottom.plate.split` (User.2) com linhas de corte, cada peça também é exportada dividida em duas metades (`-left`/`-right`) para caber em impressoras 3D menores — as linhas de corte diferentes do top e bottom fazem as emendas intertravarem na montagem. As peças inteiras continuam sendo exportadas para outros métodos de fabricação.

The `scripts/gen-case-cad.sh` script exports the PCB layers as DXF and generates the 3D case models (STEP) into `FAB-OUTPUTS/`. If the PCB has the `top.plate.split` (User.1) and `bottom.plate.split` (User.2) layers with cut lines, each part is also exported split into two halves (`-left`/`-right`) to fit smaller 3D printers — the different top and bottom cut lines make the seams interlock at assembly. The full parts are still exported for other fabrication methods.

```sh
./scripts/gen-case-cad.sh pcb/adelaide.kicad_pcb
# ou / or
./scripts/gen-case-cad.sh macro-pad/macro-pad.kicad_pcb
```

### Dependências / Dependencies

- **git** — usado para nomear a pasta de saída / used to name the output folder
- **KiCad ≥ 9** (testado com/tested with 10.0.5) — o comando `kicad-cli` precisa estar no PATH / the `kicad-cli` command must be on PATH
- **FreeCAD ≥ 1.0** (testado com/tested with 1.1.3) — o comando `freecadcmd` precisa estar no PATH / the `freecadcmd` command must be on PATH

Os scripts Python (`dxf_to_solid.py`, `generate_mold.py`) rodam dentro do Python embutido do FreeCAD, então não é necessário instalar pacotes com pip. O importador DXF legado (`importDXF`) já vem incluído no Draft workbench do FreeCAD 1.x.

The Python scripts (`dxf_to_solid.py`, `generate_mold.py`) run inside FreeCAD's bundled Python, so no pip packages are needed. The legacy DXF importer (`importDXF`) ships with FreeCAD 1.x's Draft workbench.

**Nota / Note:** instalações via Flatpak/Snap não expõem `freecadcmd` diretamente no PATH — prefira o pacote nativo da sua distro ou o AppImage. / Flatpak/Snap installs don't expose `freecadcmd` directly on PATH — prefer your distro's native package or the AppImage.

## Firmware (QMK)

O script `scripts/build-qmk.sh` compila o firmware dos dois teclados (`qmk/adelaide` e `qmk/my_numpad`) e copia os binários `.hex` para `FAB-OUTPUTS/firmware-<data>-<versão>/`. Na primeira execução ele clona o `qmk_firmware` (shallow) em `~/qmk_firmware` (configurável via variável `QMK_HOME`) e cria symlinks dos teclados deste repositório dentro dele.

The `scripts/build-qmk.sh` script builds the firmware for both keyboards (`qmk/adelaide` and `qmk/my_numpad`) and copies the `.hex` binaries to `FAB-OUTPUTS/firmware-<date>-<version>/`. On first run it shallow-clones `qmk_firmware` into `~/qmk_firmware` (configurable via the `QMK_HOME` env var) and symlinks this repo's keyboards into it.

```sh
./scripts/build-qmk.sh
```

### Dependências / Dependencies

- **qmk CLI** (testado com/tested with 1.2.0)
- **avr-gcc** + avr-libc
- **git**

## TO-DO

    - Case project