// Copyright 2023 QMK
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H

#define _BL 0
#define _FN 1

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌───┬───┬───┬───┐
     * │ - │ * │ / │Fn │
     * ├───┼───┼───┼───┤
     * │   │ 9 │ 8 │ 7 │
     * | + ├───┼───┼───┤
     * │   │ 6 │ 5 │ 4 │
     * ├───┼───┼───┼───┤
     * │   │ 3 │ 2 │ 1 │
     * |Ent├───┼───┴───┤
     * │   │Del│   0   |
     * └───┴───┴───────┘
     */
    [_BL] = LAYOUT_numpad_5x4(
        KC_PMNS, KC_PAST, KC_PSLS, MO(_FN),
                 KC_P9,   KC_P8,   KC_P7,
        KC_PPLS, KC_P6,   KC_P5,   KC_P4,
                 KC_P3,   KC_P2,   KC_P1,
        KC_PENT, KC_PDOT, KC_P0
    ),

    /*
     * ┌───┬───┬───┬───┐
     * │Rst│ * │ / │Fn │
     * ├───┼───┼───┼───┤
     * │   │ 9 │ ↑ │ 7 │
     * | + ├───┼───┼───┤
     * │   │ ← │ 5 │ → │
     * ├───┼───┼───┼───┤
     * │   │ 3 │ ↓ │ 1 │
     * |Ent├───┼───┴───┤
     * │   │Del│   0   |
     * └───┴───┴───────┘
     */
    [_FN] = LAYOUT_numpad_5x4(
        QK_BOOT, KC_PAST, KC_PSLS, MO(_FN),
                 KC_P9,   KC_UP,   KC_P7,
        KC_PPLS, KC_LEFT, KC_P5,   KC_RGHT,
                 KC_P3,   KC_DOWN, KC_P1,
        KC_PENT, KC_PDOT, KC_P0
    ),
};
