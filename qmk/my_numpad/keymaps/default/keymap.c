// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H

#define _BL 0
#define _FN 1
#define _FN_BOOT 2

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌───┬───┬───┬───┐
     * │Fn │ / │ * │ - │
     * ├───┼───┼───┼───┤
     * │ 7 │ 8 │ 9 │   │
     * ├───┼───┼───┤ + |
     * │ 4 │ 5 │ 6 │   │
     * ├───┼───┼───┼───┤
     * │ 1 │ 2 │ 3 │   │
     * ├───┴───┼───┤Ent|
     * │   0   | . |   |
     * └───┴───┴───┴───┘
     */
    [_BL] = LAYOUT_numpad_5x4(
        MO(_FN), KC_PSLS, KC_PAST, KC_PMNS,
        KC_P7,   KC_P8,   KC_P9,
        KC_P4,   KC_P5,   KC_P6,   KC_PPLS,
        KC_P1,   KC_P2,   KC_P3,
        KC_P0,            KC_PDOT, KC_PENT
    ),

    /* Function Layer: Backlight and Numlock
     * ,---------------.
     * |FN |TOG|BRE|   | toggle / breathing 
     * |---+---+---|---|
     * |   |   |   |   |  
     * |---+---+---|RET|
     * |   |   |   |   | 
     * |---+---+---|---|
     * |   |B- |B+ |NUM| Brightness
     * |---+---+---|   |
     * |FN_BOOT|   |LCK|
     * `---------------'
     */
    [_FN] = LAYOUT_numpad_5x4(
        KC_TRNS, BL_TOGG, KC_NO, KC_NO,
        KC_NO,   KC_NO, KC_NO,
        KC_NO,   BL_BRTG, KC_NO, KC_RETN,
        KC_NO,   BL_DOWN, BL_UP,
        MO(_FN_BOOT),     KC_NO, KC_NUM
    ),

    /* Function Layer 2: Boot mode
     * ,---------------.
     * |FN |   |   |   |
     * |---+---+---|---|
     * |   |   |   |   |  
     * |---+---+---|   |
     * |   |   |   |   | 
     * |---+---+---|---|
     * |   |   |   |   |
     * |---+---+---|BO-|
     * |FN_BOOT|   |OT |
     * `---------------'
     */
    [_FN_BOOT] = LAYOUT_numpad_5x4(
        KC_TRNS, KC_NO, KC_NO, KC_NO,
        KC_NO,   KC_NO, KC_NO,
        KC_NO,   KC_NO, KC_NO, KC_NO,
        KC_NO,   KC_NO, KC_NO,
        KC_TRNS,        KC_NO, QK_BOOT
    ),

};

#if defined(ENCODER_MAP_ENABLE)
const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [_BL] =  { ENCODER_CCW_CW(KC_VOLD, KC_VOLU)},
    [_FN] =  { ENCODER_CCW_CW(BL_DOWN, BL_UP)},
    [_FN_BOOT] =  { ENCODER_CCW_CW(BL_DOWN, BL_UP)},
};
#endif
