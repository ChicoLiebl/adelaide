// Copyright 2026 ChicoLiebl
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H

#define _BL 0
#define _FN 1

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /*
     * ┌───┐ ┌───┬───┬───┬───┐┌───┬───┐ ┌───┬───┬───┬───┐┌───┬───┐ ┌───┐
     * │Esc│ │F1 │F2 │F3 │F4 ││F5 │F6 │ │F7 │F8 │F9 │F10││F11│F12│ │Del│ (Mute)
     * └───┘ └───┴───┴───┴───┘└───┴───┘ └───┴───┴───┴───┘└───┴───┘ └───┘
     * ┌───┬───┬───┬───┬───┬───┬───┐┌───┬───┬───┬───┬───┬───┬───────┐
     * │ ` │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 ││ 7 │ 8 │ 9 │ 0 │ - │ = │ Bksp  │
     * ├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┘└─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─────┤
     * │ Tab │ Q │ W │ E │ R │ T │    │ Y │ U │ I │ O │ P │ [ │ ]   │┌────┐
     * ├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┐   └┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬───┐││Ent │
     * │ Caps │ A │ S │ D │ F │ G │    │ H │ J │ K │ L │ ; │ ' │ # │││    │
     * ├────┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴┐   └─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┘└┴────┘
     * │Shft│ \ │ Z │ X │ C │ V │ B│     │ N │ M │ , │ . │ / │Shft│Up │PgUp│
     * ├────┴┬──┴─┬─┴──┬┴───┴┬──┴──┴┐    └┬──┴───┴──┬┴───┴┬──┴────┴───┴────┤
     * │Ctrl │GUI │Alt │Space│  Fn  │     │  Space  │AltGr │  ← │ ↓ │ →   │
     * └─────┴────┴────┴─────┴──────┘     └─────────┴──────┴────┴───┴─────┘
     */
    [_BL] = LAYOUT(
        KC_ESC,  KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,  KC_F11,  KC_F12,  KC_DEL,  KC_MUTE,
        KC_GRV,  KC_1,    KC_2,    KC_3,    KC_4,    KC_5,    KC_6,    KC_7,    KC_8,    KC_9,    KC_0,    KC_MINS, KC_EQL,  KC_BSPC,
        KC_TAB,  KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,    KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,    KC_LBRC, KC_RBRC, KC_ENT,
        KC_CAPS, KC_A,    KC_S,    KC_D,    KC_F,    KC_G,    KC_H,    KC_J,    KC_K,    KC_L,    KC_SCLN, KC_QUOT, KC_NUHS,
        KC_LSFT, KC_NUBS, KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,    KC_N,    KC_M,    KC_COMM, KC_DOT,  KC_SLSH, KC_RSFT, KC_UP,   KC_PGUP,
        KC_LCTL, KC_LGUI, KC_LALT, KC_SPC,  MO(_FN), KC_SPC,  KC_RALT, KC_LEFT, KC_DOWN, KC_RGHT
    ),

    /* Function layer: backlight on F1-F4, QK_BOOT on Fn+Del */
    [_FN] = LAYOUT(
        KC_TRNS, BL_TOGG, BL_BRTG, BL_DOWN, BL_UP,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   QK_BOOT, KC_TRNS,
        KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,
        KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,
        KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,
        KC_TRNS, KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_NO,   KC_TRNS, KC_VOLU, KC_PGDN,
        KC_TRNS, KC_TRNS, KC_TRNS, KC_NO,   KC_TRNS, KC_NO,   KC_TRNS, KC_MPRV, KC_VOLD, KC_MNXT
    ),
};

#if defined(ENCODER_MAP_ENABLE)
const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [_BL] = { ENCODER_CCW_CW(KC_VOLD, KC_VOLU) },
    [_FN] = { ENCODER_CCW_CW(BL_DOWN, BL_UP) },
};
#endif
