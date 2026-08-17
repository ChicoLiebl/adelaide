# adelaide

A 75% Alice-style keyboard based on the [Adelheid](https://github.com/floookay/adelheid), with rotary encoder, ISO enter, split backspace-less layout and per-switch backlight.

* Keyboard Maintainer: [ChicoLiebl](https://github.com/ChicoLiebl)
* Hardware Supported: Adelaide PCB (ATmega32U4)

Hardware details (derived from `pcb/adelaide.kicad_pcb`):

| Function  | Pins |
|-----------|------|
| Columns 0-13 | F0, F1, E6, C7, F6, B6, D4, B1, B0, B7, B5, B4, D7, D6 |
| Rows 0-5     | D0, D1, D2, D3, D5, F7 |
| Encoder A/B  | F4, F5 (push button on matrix [5, 10]) |
| Backlight    | C6 (Timer3 PWM, N-MOSFET on LED ground rail) |

Make example for this keyboard (after setting up your build environment):

    make adelaide:default

Flashing example for this keyboard:

    make adelaide:default:flash

See the [build environment setup](https://docs.qmk.fm/#/getting_started_build_tools) and the [make instructions](https://docs.qmk.fm/#/getting_started_make_guide) for more information. Brand new to QMK? Start with our [Complete Newbs Guide](https://docs.qmk.fm/#/newbs).

## Bootloader

Enter the bootloader in 3 ways:

* **Bootmagic reset**: Hold down the key at (0,0) in the matrix (Escape) and plug in the keyboard
* **Physical reset button**: Briefly press the button on the back of the PCB
* **Keycode in layout**: Press Fn+Del (`QK_BOOT` on the function layer)

If the encoder direction feels reversed, swap `pin_a`/`pin_b` in `keyboard.json`.
