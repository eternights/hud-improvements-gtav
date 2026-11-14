# GTA V (Enhanced) scaleforms — what each `.gfx` does

A study of [`eternights/decompiled-scaleforms-gtav`](https://github.com/eternights/decompiled-scaleforms-gtav),
based on the decompiled ActionScript and asset tree. All 182 `.gfx` folders in the
repository are covered below.

---

## 1. What the repository actually contains

The README says only "scaleform gfxs decompiled from gtav enhanced". In practice:

| Part | Contents |
| --- | --- |
| `update/update.rpf/x64/data/cdimages/scaleform_*.rpf/` | **182 decompiled `.gfx`** in Enhanced's patched archives: `frontend`, `frontend_gen9`, `generic`, `generic_2`, `platform_pc`, and (from the `patch` folder) `minimap`, `minigames` |
| each `<name>.gfx/` | `frames/`, `images/`, `shapes/`, `sprites/`, `fonts/`, `morphshapes/`, `scripts/` |
| `scripts/` | decompiled ActionScript 2 — `frame_N/DoAction.as`, `DefineSprite_*/…`, and the real classes under `__Packages/com/rockstargames/…` |
| `x64b.rpf/data/cdimages/scaleform_*.rpf/` | **base-game texture archives only** (11,003 `.dds` in 1,002 folders) — the original (legacy) `.gfx` code is *not* decompiled |
| `common.rpf/data/scaleform/gfxfontlib.gfx/` | the shared font/glyph library |
| `x64e.rpf/levels/gta5/minimap.rpf/` | 65 `minimap_*.ydd` map-tile meshes (the actual 3D minimap geometry, not scaleform) |
| `common.rpf/data/ui/*.xml`, `x64a.rpf/…/minimap.ymt` | frontend/menu configuration and minimap tuning data |

Scale of the decompile: **4,269 `.as` files, 256,484 lines, 8.5 MB** of script;
33,824 PNG frames, 5,607 SVG shapes, 114 TTF fonts. No `.fla` or `.gfx` source is
included, so the Flash timeline exists only as reconstructed `frames/` and
`DefineSprite_*` folders.

Because everything under `update.rpf` is the **Enhanced (gen9) patch** version,
the code here is the newest variant of each scaleform, not necessarily the 2013
one. Anything only present in the base archives is just textures.

### Anatomy of one decompiled scaleform

- `frames/1.png` — the document stage render.
- `DefineSprite_<id>_<name>/` — a movie clip, one PNG per frame.
- `scripts/frame_1/DoAction.as` — the timeline's document script (constructs the
  class, registers with `GameInterface`).
- `scripts/__Packages/com/rockstargames/gtav/<area>/<CLASS>.as` — the class the
  game actually talks to. Duplicate copies at the `scripts/` root are the same
  code linked to the movie.
- `GameInterface.call("METHOD", GENERIC_TYPE, …)` — calls back into the game
  (set text with translation, play sound, request TXD, …).
- `TXD_HAS_LOADED` / `ADD_TXD_REF_RESPONSE` — the async texture-load handshake.
- `SET_DATA_SLOT` / `DISPLAY_VIEW` — the generic list-menu contract used by
  almost every menu-like scaleform.
- `SET_DISPLAY_CONFIG` / `BaseScreenLayout` — game sends screen size and safe-zone
  percentages; layout is computed in a 1280×720 design space
  (`BaseScreenLayout`: `FILE_WIDTH = 1280`, safe defaults 96/54/1184/666).

---

## 2. Shared libraries and fonts

These carry no UI logic; other scaleforms import them for glyphs and icons.

| `.gfx` | Archive | Contents | What it does |
| --- | --- | --- | --- |
| `gfxfontlib` | common | 45 images, 6 fonts, 1 frame, no script | Master font/glyph library (Zeitgeist, Arial, HelveticaNeue LT 65, Pricedown, Andy, SignPainter). Every other gfx links its text fields against this font library. |
| `font_lib_editor` | frontend | 7 fonts | Font library for the Rockstar Editor UI. |
| `font_lib_sc` | frontend | 2 fonts | Social Club font library. |
| `font_lib_efigs` | generic | 7 fonts, 3 images | "EFIGS" (English/French/Italian/German/Spanish) font set with the extra glyph art those languages need. |
| `font_lib_heists` | generic | 1 font | Dedicated heist UI typeface. |
| `font_lib_org` | generic | 18 fonts | Organisation/business UI fonts (CEO/MC laptop text). |
| `font_lib_slots` | generic | 1 font | Slot-machine / casino numerals. |
| `font_lib_taxi` | generic | 1 font | Taxi meter/dispatch font. |
| `font_lib_typewriter` | generic | 1 font | Typewriter face used for documents and letters. |
| `font_lib_web` | generic | 18 fonts | Font set for the in-game internet browser pages. |
| `font_lib_chinese_pc`, `font_lib_chinesesimp_pc`, `font_lib_efigs_pc`, `font_lib_japanese_pc`, `font_lib_korean_pc` | platform_pc | 5–9 fonts each | PC-only CJK/EFIGS font libraries, loaded instead of the console set. |
| `mp_icons` | generic | 251 files, all SVG shapes, **no script** | Vector icon atlas for GTA Online (player states, org icons, etc.). A pure symbol library — importing movies pick symbols out of it. |

---

## 3. Boot, loading screens and front-end shell

| `.gfx` | Archive | Contents | What it does |
| --- | --- | --- | --- |
| `loadingscreen_startup` | frontend | 1 frame, 6 images, 31 scripts | The startup loading screen. Builds a list of 25 loading screens (`loadingscreen_builtin0`, `loadingscreen1`, `loadingscreen5`, `loadingscreen9`, `loadingscreen12`, `loadingscreen16`–`35`) as layered TXD art with pan/rotate/parallax moves, plus news screens, legal text, install/switch prompts, progress title/text and the "landing" text. `STARTUP_ANIMATED_LOADINGSCREENS`, `SHOW_NEXT_ANIMATED_LOADINGSCREEN`, `SHOW_NEXT_STATIC_LOADINGSCREEN`, `SET_SCREEN_ORDER`, `SET_GTA_LOGO_VISIBLE`. The spinning loading ring is art in this movie, not script. |
| `loadingscreen_newgame` | frontend | 1 frame, 1 image, 1 font | Single-player new-game loading bar: `SET_PROGRESS_BAR`, `SET_PROGRESS_TEXT`. Minimal. |
| `landing_page` | frontend | 1 frame, 1 image | Small startup landing page with one selectable button (`INIT_LANDING_PAGE`, `SET_BUTTON_SELECTED`). |
| `gtav_online` | frontend | 1 frame, 7 images, 67 scripts | GTA Online loading/landing screen: big-feed panel, tabs, news context, title, progress, logo show/hide (`SETUP_BIGFEED`, `SET_BIGFEED_INFO`, `SET_BIGFEED_IMAGE`, `SET_BIGFEED_PROGRESS`, `SET_NEWS_CONTEXT`, `HIDE_ONLINE_LOGO`). |
| `game_stream` | frontend | 27 images, 63 scripts | Social Club "game stream" feed (the HUD component that slides in unlock/activity cards). Componentised: `SET_STREAM_COMPONENT`, `UPDATE_STREAM_COMPONENT`, `SNAP_NEXT_FEED_ITEM_INTO_POSITION`, `UPDATE_STREAM_STATS`, `UPDATE_STREAM_TICKER`, `REMOVE_STREAM_COMPONENT`. |
| `opening_credits` | frontend | 1 frame, 1 image, 2 fonts, 23 scripts | The opening credits crawl and the GTA V logo. Builds credit blocks/roles/names and single lines, animates logo scale/rotation and fades (`SHOW_LOGO`, `SETUP_CREDIT_BLOCK`, `ADD_ROLE_TO_CREDIT_BLOCK`, `ADD_NAMES_TO_CREDIT_BLOCK`, `SHOW_CREDIT_BLOCK`, `SHOW_SINGLE_LINE`). Audio/music is triggered game-side; there are no sound calls in the script. |
| `online_policies` | frontend | 2 images, 50 scripts | Online Terms/EULA/Privacy Policy screen: policy title/intro/body, scroll, download, accept highlight and radio-button state, links. |
| `social_club2` | frontend | 2 frames, 5 images, 142 scripts | Social Club sign-in/welcome flow: welcome tabs, gamertag, presence, news, join/sign-in highlights, crew tag, policy text. The largest frontend class after the pause menu. |
| `busy_spinner` | frontend | 1 frame, 3 images | Full-screen busy spinner with instructional-button support (`INSTRUCTIONAL_BUTTONS` base) — the "please wait" overlay during joins/transitions. |
| `popup_warning` | frontend | 3 images | Generic warning popup (title/body/buttons) built on `POPUP_WARNING` + `INSTRUCTIONAL_BUTTONS`. |
| `custom_warning_screen` | generic | 1 image, 26 scripts | Scrollable warning screen with a list of warning items (`WarningScreenList`, `WarningScreenListItem`, `CUSTOM_WARNING_SCREEN`) — used for multi-line legal/first-run warnings. |
| `text_input_box` | generic | 2 images | On-screen keyboard/text entry field with platform button prompts (`TEXT_INPUT_BOX` + `INSTRUCTIONAL_BUTTONS`). |
| `instructional_buttons` | generic | 3 images | The standard button-prompt strip (icon + label rows), with backgrounds, padding, max width, hit areas, button flashing (`SET_DATA_SLOT`, `DRAW_INSTRUCTIONAL_BUTTONS`, `FLASH_BUTTON_BY_ID`). |
| `generic_instructional_buttons` | frontend | 4 images | Same class, frontend-skinned variant used by menus/loading. |
| `pause_menu_instructional_buttons` | frontend | 3 images | Pause-menu-skinned prompt strip (mouse-aware prompts). |
| `store_instructional_buttons` | frontend | 4 images | Store-skinned prompt strip. |
| `calibration` | frontend_gen9 | 1 frame, 24 scripts | **Enhanced-only HDR calibration**: `SET_HDR_VALUES`, brightness/slider selection, footer text, arrows. |
| `frontend_landing` | frontend_gen9 | 8 images, 125 scripts | **Enhanced-only new landing page**: tile/grid navigation with stickers, spinners, hover/animate-in states (`GridItem`, `BaseItem`) instead of the old list-style landing. |
| `progress_hub` | frontend_gen9 | 5 images, 54 scripts | **Enhanced-only career progress hub**: category → content type → tier progress → rewards screens, carousel navigation, scrollbar. |
| `pause_menu_calibration` | frontend | 18 scripts | Pause-menu brightness calibration (`PAUSE_MENU_CALIBRATION`). |
| `gamepad_calibration` | platform_pc | 2 images | PC gamepad stick/trigger calibration with live bar positions and button-press states. |
| `controller_test` | generic | 44 images, 1 morph, 28 scripts | Input test screen for controllers/keyboard: buttons, analog sticks, triggers, mouse box, wheel. |
| `mouse_pointer` | frontend | 1 image | The software mouse cursor (`MOUSE_POINTER`, `SET_SCREEN_ASPECT`) used by PC menus. |
| `grid_layout` | generic | 9 scripts | Debug-only layout grid: `SET_INFO`, `SET_SAFE`, `SET_SCALE` — overlay for checking safe-zone alignment. |
| `store_background` | frontend | 1 image | Animated backdrop for the in-game store (`ANIMATE_BACKGROUND`). |
| `store_blackout` | frontend | 13 scripts | Fade-to-black / fade-to-transparent overlay used during store transitions. |
| `saving_footer` | generic | 1 image | Online's bottom-of-screen "Saving…/Saving failed" footer (`SET_TEXT`, `SET_WAITING_TEXT`). |

---

## 4. The HUD

The HUD is **not one file**. `hud.gfx` contains the full component set, but the game
also ships one `.gfx` per component; each of those embeds `NEW_HUD` +
`HudComponentConstants` and only the relevant component class, and is loaded on
demand. `NEW_HUD` is the container: it registers components by ID
(`HUD_WANTED_STARS = 1`, `HUD_WEAPON_ICON = 2`, `HUD_CASH = 3`, … `HUD_WEAPON_WHEEL_STATS = 20`,
`MAX_HUD_COMPONENTS = 21`), controls show/hide and display-list ordering, character
colour and weapon-wheel state.

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `hud` | 18 images, 1 font, 98 scripts | Master HUD movie: wanted stars, weapon icon/wheel (+stats), cash/chips, help & floating help text, subtitles (normal/big), MP inventory, radio wheel, director mode, area/vehicle/street names, rank bars, radar-inverted icons. The decompiled "main" class resolves to `HUD_WEAPON_WHEEL`, but the movie carries the full component set — `HUD` plus the 20 numbered components in `HudComponentConstants`, and local extras (big help text, chips + change, director mode, rank bars, MP inventory). |
| `hud_area_name` | 23 scripts | Area-name component (e.g. "Sandy Shores"). |
| `hud_district_name` | 23 scripts | District-name component (smaller neighbour-name strip). |
| `hud_street_name` | 23 scripts | Street-name component under the minimap. |
| `hud_vehicle_name` | 23 scripts | Vehicle-name component (manufacturer + model). |
| `hud_cash` | 23 scripts | Player cash display. |
| `hud_cash_change` | 23 scripts | Green/red "+$X / −$X" cash-change ticker. |
| `hud_mp_cash` | 23 scripts | Online bank cash display (`SET_PLAYER_MP_CASH`). |
| `hud_mp_message` | 23 scripts | Online notification/message line (`SET_MP_MESSAGE`, auto-hide). |
| `hud_mission_passed_message` | 23 scripts | The "Mission Passed" HUD banner component. |
| `hud_reticle` | 5 images, 1 font, 3 morph, 53 scripts | Aiming reticle: reticle type/accuracy/zoom/visibility/position, scope lock/distance, dim/flash/reset, hit marker, colour, boost. |
| `hud_saving` | 3 images, 2 morph, 28 scripts | Saving icon: `SAVEGAME_ICON_STYLE_WORKING/SUCCESS/FAILED/CLOUD_WORKING` plus `LOADING = 5`. Shows `SAVING`, cloud `starMC`, or `spinnerMC`; the spinner sprite loops frames 1→60→`"loop"`. Fades in at `FADE_DURATION/2000`, auto-removes after `ON_SCREEN_DURATION`. |
| `minimap` | 10 images, 62 scripts | **The radar.** `MINIMAP` (68 functions): health/armour/ability/air bars with damage flash, `SET_MASK`/`MINIMAP_MASK`, `MOVE_MAPMASKSQUARE` (empty stub in this build), `FLASH_MINIMAP`, wanted-level circle bitmap fill (`SET_WANTED_LEVEL`), `FLASH_WANTED_OVERLAY` / `STOP_FLASHING_WANTED_OVERLAY` which play the `wantedOverlaySP` timeline, sat-nav direction/distance, depth gauge, sonar sweep, yoke, gang-territory colour cycling, blip labels (`SET_BLIP_LABEL` — label counter-rotates by `-_rotation`), blip flashing, blip death, `REMOVE_BLIP`. `CONTENT.setMask(this.TIMELINE.mapMask)` is the radar's fade/cut mask. |
| `minimap_main_map` | 45 frames, 10 scripts | The **pause-menu map**, not the radar: 45-frame timeline (zoom steps), 18 defined map component slots (23 indices with gaps; `TOGGLE_COMPONENT`), roads/freeway overlay, aircraft-only layers, TXD bitmap overlays (`SET_BITMAP_MAP_ON/OFF`). |
| `player_switch` | 3 images, 37 scripts | Character-switch wheel: slots, multiplayer head, hinted/suggested switches, damage state, switch counter, selection label. |
| `countdown` | 1 image, 19 scripts | Race/mission countdown lights with SP/MP fade, direction, override duration. |

### HUD component ↔ per-component `.gfx`

| `.gfx` | Component class |
| --- | --- |
| `hud_area_name` | `HUD_AREA_NAME` |
| `hud_cash` | `HUD_CASH` |
| `hud_cash_change` | `HUD_CASH_CHANGE` |
| `hud_district_name` | `HUD_DISTRICT_NAME` |
| `hud_mission_passed_message` | `HUD_MISSION_PASSED_MESSAGE` |
| `hud_mp_cash` | `HUD_MP_CASH` |
| `hud_mp_message` | `HUD_MP_MESSAGE` |
| `hud_reticle` | `HUD_RETICLE` |
| `hud_saving` | `HUD_SAVING` |
| `hud_street_name` | `HUD_STREET_NAME` |
| `hud_vehicle_name` | `HUD_VEHICLE_NAME` |

Each also carries `HUD_RADIO_STATIONS_WHEEL` as a shared library dependency.

---

## 5. Messages, awards and celebrations

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `midsized_message` | 1 image | Mid-size "shard" message banner: `SHOW_MIDSIZED_MESSAGE`, `SHOW_BRIDGES_KNIVES_PROGRESS`, `SHOW_COND_SHARD_MESSAGE`, `SHARD_SET_TEXT`, `SHARD_ANIM_OUT`. |
| `mp_big_message_freemode` | 5 images, 27 morph, 68 scripts | Online's big message system: busted/wasted, rank-up, crew rank-up, locked-up, mission passed/failed, weapon purchased, plane message, territory change, centred/strap variants, resupply bar (`SHOW_BUSTED_MP_MESSAGE`, `SHOW_RANKUP_MP_MESSAGE`, …). |
| `mp_award_freemode` | 11 scripts | Award/unlock banner (`SHOW_AWARD_AND_MESSAGE`, `SHOW_UNLOCK_AND_MESSAGE`). |
| `mp_celebration` | 2 images, 1 font, 27 scripts | Generic Online stat wall: score, position, job/arena points, rep + rank bar, winner, objective, unlocks, flash; supports breakpoints/pauses and duration queries. |
| `mp_celebration_bg` | 22 images, 2 fonts, 33 scripts | Background/asset layer of the same celebration wall (shares `MP_CELEBRATION.as`). |
| `heist2_celebration` | 2 images, 1 font, 42 scripts | Heist celebration sequence ("Big Dollars" step and friends) — the post-heist take/stat animation. |
| `heist2_celebration_bg` / `heist2_celebration_fg` | 2 images each | Background and foreground render layers of the heist celebration. |
| `heist_endscreen` | 10 scripts | Heist payout screen: pie chart of the take, colours, numbers (`SET_PIE_CHART`, `SHOW_PIECHART_NUMBERS`, `SET_PIECHART_COLOURS`). |
| `mp_menu_glare` | 2 images, 2 morph | Animated glare/reflection overlay for Online menus (`SET_DATA_SLOT`). |
| `mp_mission_details_card` | 4 images, 47 scripts | Mission details card (freemode details component) shown in job lists/menus: title, slots, TXDs. |
| `mp_gamer_info` | 2 images | Player info card: gamertag, crew tag, rank (`MP_GAMER_INFO`, `CREW_TAG_MOVIECLIP`). |
| `mp_matchmaking_card` | 3 images, 50 scripts | Online freemode/matchmaking player-list card (`MP_FREEMODE_PLAYER_LIST`, model/view/item classes). |

---

## 6. Phones (5 shells, alert popups, 7 apps, 31 cutscene screens)

### Phone shells

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `cellphone_badger` | 11 images, 63 scripts | **Badger** smartphone shell (Android-style). Full phone OS: title-bar clock, header, soft keys, theme/background/provider icon/signal strength, data slots, `CELLPHONE_APP` launching, `LOAD_APP`/`REMOVE_CHILD_MOVIE`, sleep mode, TXD loading. |
| `cellphone_ifruit` | 13 images, 76 scripts | **iFruit** phone shell (iOS-style) — Michael's and the Online character's phone. Same contract plus crew background image and `REPLACE_BACKGROUND_IMAGE`. |
| `cellphone_facade` | 10 images, 64 scripts | **Facade** phone shell — the third smartphone skin; header-bar colouring and theme switching, otherwise the same app contract. |
| `cellphone_prologue` | 2 images, 32 scripts | The 2004-era phone used in the prologue: simplified home menu, contact list, call screen, no app streaming. |
| `cellphone_cutscene` | 11 images, 4 scripts | Not a phone OS: a still-frame viewer. `DISPLAY_VIEW(viewID)` does `CONTENT.gotoAndStop(viewID + 1)`. Every `*_connected_*`, `*_blank_*` phone screen below is this class with different art. |
| `cellphone_alert_popup` | 15 SVG shapes, 5 scripts | In-world phone alert popups: `CREATE_ALERT(iconID, x, y, title)` attaches an `alertDialogBox` clip at a screen position, picks the icon frame from `IconLabels.lookUp(iconID)`, sets the title; `CLEAR_ALL` rebuilds the alert layer. (This is the one whose red beacon drifts off-centre on ultrawide.) |

All four real shells share the same API surface (`SET_TITLEBAR_TIME`,
`SET_SLEEP_MODE`, `SET_SOFT_KEYS`, `SET_THEME`, `SET_DATA_SLOT`, `DISPLAY_VIEW`,
`LOAD_APP`, `SHUTDOWN_MOVIE`), which is why a phone "model" swap is a movie/asset
swap and not a code change.

### Phone apps

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `app_trackify` | 9 images, 17 scripts | Trackify: vehicle tracker with blips/range (`APP_TRACKIFY`). |
| `app_job_list` | 20 scripts | Scrolling job/contact list app (`APP_ScrollingList`). |
| `app_todo_list` | 10 scripts | Scrolling to-do list (Daily Objectives style) (`APP_ScrollingList`). |
| `app_todo_view` | 10 scripts | Detail view for one to-do entry (`APP_ScrollingView`). |
| `app_mission_stats_view` | 10 scripts | Mission stats readout (`APP_MISSION_STATS_VIEW`). |
| `app_numberpad` | 1 image | Number pad for dialling/enter codes (`APP_NUMBERPAD`). |
| `app_securoserv_hacking` | 1 font, 15 scripts | SecuroServ hacking app (the signal-tracing minigame) (`APP_SECUROSERV_HACKING`, `APP_FUNCTION`). |

### Cutscene phone stills (31)

These are single-frame (or few-frame) phone screens displayed on the in-world
phone prop during missions and cutscenes. They have no logic beyond
`gotoAndStop`, and most are one PNG each.

`arm1_connected_baby`, `arm3_connected_lara`, `exl2_blank_jimmy`,
`exl2_connected_jimmy`, `fam2_playmusic`, `fam3_01_ncallingmartin`,
`fam3_02_ncallingmartin`, `fam3_03_ncallingmartin`, `fam3_04_ncallingmartin`,
`fam3_05_ncallingmartin`, `fam3_all_ncallingmartin`, `fib3_daven`, `fib3_steveh`,
`fib4_eyefindmap`, `fib5_lestertext`, `finb_connected_amanda`, `finc1_eyefind`,
`finc1_merrysite`, `badger_blank_home`, `badger_blank_inprogress`,
`badger_blank_lamar`, `badger_blank_lester`, `badger_blank_michael`,
`badger_dialing_michael`, `facade_blank_home`, `facade_blank_inprogress`,
`facade_blank_michael`, `facade_computer_desktopwide`, `dlc_arena_int2`,
`dlc_sol`, `dre1_badger_lj`.

`facade_computer_desktopwide` is the odd one: a computer desktop shown on a wide
screen rather than a phone. `fam3_all_ncallingmartin` is the only one with
5 images (all the call states in one movie).

---

## 7. Computers, laptops and business boards

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `desktop_pc` | 31 images, 1 morph, 42 scripts | Generic in-game PC desktop: programs, run/close, popups, antivirus, scan bar/speed, cursor, restart. Used for Lifeinvader-style mission computers. |
| `hacking_pc` | 17 images, 1 font, 1 morph, 57 scripts | Hacking minigame PC: labels, map show/hide, programs, buttons, cursor, loading/download progress, apps. |
| `fib_pc` | 7 images, 1 font | FIB laptop desktop (programs + `MousePointer`). |
| `hacker_truck_desktop` | 6 images, 40 scripts | Terrorbyte ("hacker truck") desktop: main screen + screen stack. |
| `bank_job_login` | 5 images | Static bank-job login screen; sets the title and plays the hand-scanner sound (`DLC_BTL_Hacker_Truck_Computer_Sounds`). |
| `securoserv` | 10 images, 74 scripts | CEO SecuroServ laptop: map screen, import/export, warehouse selection. |
| `warehouse` | 4 images, 29 scripts | CEO warehouse stock/sales screen. |
| `biker_businesses` | 4 images, 52 scripts | MC businesses laptop (coke/meth/cash/weed/forgery) with supply/stock/sale screens. |
| `biker_mission_wall` | 2 images | Clubhouse mission wall: mission list, stats, selection. |
| `nightclub` | 3 images, 61 scripts | Nightclub management: stats, warehouse, DJs, stock, technicians, assignments, upgrades, buyers, audio buttons. |
| `arcade_business_hub` | 11 images, 1 morph, 37 scripts | Arcade business hub (cabinet placement/income). |
| `arcade_management` | 16 images, 41 scripts | Arcade cabinet management: add cabinet/upgrade, history, overlays. |
| `hangar_cargo` | 3 images, 1 morph, 43 scripts | Hangar cargo: stats, cargo list, active organisations, steal/sell cooldowns. |
| `disruption_logistics` | 2 images, 52 scripts | Bunker laptop ("Disruption Logistics"): stats, resupplies, upgrades, research + unlockables, fast-track, sell prices. |
| `arena_career_wall` | 2 images | Arena War career wall: stats, textures, unlock popup. |
| `auto_shop_board` | 34 images | Auto Shop job board: selection/main/blank screens, styles. |
| `avenger_operations_terminal` | 27 images | Avenger operations terminal: home, Avenger ops, smuggling ops, idle screens. |
| `bounty_computer` | 20 images | Bounty computer (Bottom Dollar Bounties): bounty targets, gamertag, overlays. |
| `fixer_app` | 47 images, 37 scripts | Fixer contracts app: data-leak/security-contract screens. |
| `robbery_computer` | 8 images, 44 scripts | Robbery computer (Chop Shop): robberies, missions, active index, login animation, gamertag. |
| `kortz_heist_board` | 51 images, 37 scripts | Kortz Center heist board (new DLC): main screen + sub-screens. |
| `covert_ops` | 1 image, 45 scripts | Covert-ops laptop: main screen and screen stack. |
| `starter_pack_browser` | 5 images | Criminal Enterprise Starter Pack browser: items, screens, purchase buttons. |
| `new_editor` | 13 images, 142 scripts | Rockstar Editor UI: movie/clip headers, columns, list items, project size, help text, icons. |

---

## 8. Heists and mission UI

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `heist_agency` | 8 images, 1 morph, 42 scripts | Agency heist planning board: crew selection, gameplay select, to-do items (`HEIST_AGENCY`, `HeistControllerBase/Model/View`). |
| `heist_docks` | 5 images, 1 morph, 43 scripts | Docks heist planning board, same controller family. |
| `heist_finale` | 8 images, 1 morph, 41 scripts | Heist finale board (approach/crew confirmation). |
| `casino_heist_board_prep` | 2 images, 69 scripts | Casino heist prep board: screens, selections, overlays. |
| `casino_heist_board_finale` | 5 images, 41 scripts | Casino heist finale board. |
| `mission_complete` | 33 scripts | SP mission-complete checklist (see messages). |
| `mission_target_complete` | 21 scripts | Objective-complete banner. |
| `mission_quit` | 13 scripts | Mission quit/fail transition. |

---

## 9. Vehicles, cameras and world overlays

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `dashboard` | 2 fonts, 68 scripts | Car dashboard: dials, warning lights, radio station, vehicle type, background toggle. |
| `aircraft_dials` | 1 image, 1 font | Aircraft instrument panel (dials, lights, HUD). |
| `dials_lazer` | 1 image, 1 font | Lazer-specific dial layout (same `AIRCRAFT_DIALS` class). |
| `dials_lazer_vintage` | 1 image | Vintage Lazer dial skin (same class). |
| `arena_gun_cam_apocalypse`, `arena_gun_cam_consumer`, `arena_gun_cam_scifi` | 0–1 images, 1 font each | Arena War turret camera overlays: compass, heading, FOV, altitude, logo; three art skins sharing `TURRET_CAM`. |
| `drone_cam` | 4 images, 34 scripts | Drone HUD: reticle, zoom/heading meters, shock/detonate/tranquilize/boost/missile/EMP/cannon/MG meters, info list, sound wave, warnings, stripes. |
| `binoculars` | 1 image | Binocular vignette overlay (static, no logic). |
| `digital_camera` | 1 image, 23 scripts | Camera viewfinder: remaining photos, photo border/frame, focus lock, shutter open/close. |
| `camera_gallery` | 12 scripts | Phone camera gallery/photo frame: remaining photos, flash, focus lock, shutter. |
| `camera_shutter` | 9 scripts | Standalone shutter animation (`OPEN_SHUTTER`, `CLOSE_SHUTTER`). |
| `fame_or_shame_camera` | 1 frame, 1 image, 2 SVG, sprites, **no script** | Static "Fame or Shame" camera overlay (CONTENT + BOUNDING_BOX art only). |
| `digiscanner` | 2 images | Digiscanner readout: distance + colour. |
| `ecg_monitor` | 16 scripts | Heart-rate/ECG monitor: rate, beat, health, colour. |
| `drilling` | 1 image | Drilling meter: speed, depth, temperature. |

---

## 10. World props, signs and misc UI

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `atm` | 3 images, 31 scripts | ATM: balance, transactions, cash options, menu, cursor, page scroll. |
| `epsilon_tract` | 2 images | Epsilon tract/letter reader (`LETTER_SCRAPS`): letter text, append text, background visibility. |
| `clubhouse_name` | 3 scripts | Renders the player's MC clubhouse name on the clubhouse sign/prop. |
| `blimp_text` | 1 image | Blimp message ticker: scroll speed, colour, message. |
| `breaking_news` | 5 images | Weazel News "Breaking News" overlay with scrolling ticker and static variant. |
| `hair_colour_card` | 37 scripts | Barber-shop hair colour card: colour bar list, scroll, selection. |
| `colour_switcher_01`, `colour_switcher_02` | 43 scripts each | Character-creator colour picker (two instances/skins) built on `GUIView` + `GenericColourBar` + `PAUSE_MENU_HAIR_COLOUR_LIST`. |
| `horse_racing_console` | 11 images, 1 morph, 56 scripts | Inside Track betting console: race type, horse selection, betting values, countdown, error, positions, screen stack. |

---

## 11. Pause menu and store

| `.gfx` | Contents | What it does |
| --- | --- | --- |
| `pause_menu_header` | 30 scripts | Pause-menu header: title/details, crew tag, character/crew images, header background image (alpha tween), menu items, highlight/alert/lock, scrolling and weighting. |
| `pause_menu_shared_components` | 2 images, 49 scripts | Shared pause-menu component library; the decompiled main class is `PAUSE_MENU_SP_CONTENT` — columns, items, header, mouse hover/click, menu building. |
| `pause_menu_shared_components_02` | 4 images, 37 scripts | Second shared set, resolving to `PAUSE_MENU_SETTINGS` (settings list, control images/labels, video-memory bars, tips, state/focus). |
| `pause_menu_shared_components_03` | 4 images, 28 scripts | Third set, resolving to `PAUSE_MENU_FREEMODE_DETAILS` (Online details card). |
| `pause_menu_sp_content` | 2 images, 52 scripts | Single-player pause menu content: full column/item/mouse/menu-building implementation (90 functions). |
| `pause_menu_store_content` | 5 images, 33 scripts | In-game store (Shark Card/ecommerce) menu: columns, slots, header, crew/char images, PlayStation logo, shop logo, highlight. |
| `pause_menu_pages_keymap` | 1 image, 29 scripts | Key-mapping page: configuration items and input labels. |
| `pause_menu_pages_settings` | 2 images, 22 scripts | Settings page: data slots, control images/labels, video-memory bar, tips, state/focus/input. |
| `pause_menu_pages_friends` | 30 scripts | Friends/player-card page (`SP_PLAYER_CARD`): title + player card slots. |
| `pause_menu_calibration` | 18 scripts | Brightness calibration page. |

---

## 12. Notable details for modding the HUD

These are observations from the code, relevant to common HUD work.

**Radar fade / mask.** `MINIMAP.INITIALISE` does
`CONTENT.setMask(TIMELINE.mapMask)`. The fade is the `mapMask` artwork plus
whatever the game does with it; `SET_MASK` only stores a reference and
`MOVE_MAPMASKSQUARE` is an empty function in this Enhanced build. There is no
alpha-fade loop for the map in ActionScript, so a smoother/ray-traced-looking
fade would be new mask art (a gradient ring) driven by AS, not a flag flip.

**Wanted overlay sync.** `FLASH_WANTED_OVERLAY` plays `wantedOverlaySP` from
frame 1 and sets `wantedOverlayActive`; `STOP_FLASHING_WANTED_OVERLAY` hides it.
Police blips flash independently through `START_BLIP_FLASHING(mc, blinkSpeed)`
and `STOP_BLIP_FLASHING`. Synchronising the red/blue overlay with police blips
means giving both the same clock — either drive the overlay from the blip flash
timer or expose one blink rate to both.

**Blips.** Icon symbols live in the minimap library and are listed by
`com.rockstargames.gtav.constants.Blips.getListOfBlips()` (966 entries).
Rotating/animated families are named explicitly: `radar_police_heli_spin`,
`radar_police_plane_move`, `radar_player_heli`, `radar_player_plane`,
`radar_oppressor_2`, `radar_nhp_mg_mir_rotate`, `radar_blimp`.
`MINIMAP.SET_BLIP_LABEL` creates `blipLabel` and sets
`_rotation = -mc._rotation`, i.e. the label counter-rotates with the blip.
Blimp/oppressor heading rotation itself is applied game-side; the scaleform only
owns the symbol and label. A "rotating blip" that loops cleanly therefore needs
its symbol to be a seamless animation inside `minimap.gfx`.

**Loading rings.** The ring animation is not in one file; it is duplicated across five places:

| Where it appears | `.gfx` | Symbol / code | Frames | Ring texture in that movie's `.ytd` |
| --- | --- | --- | --- | --- |
| HUD save/load icon | `hud_saving.gfx` | `CONTENT.dialogMC.iconMC.spinnerMC`; `DefineSprite_16` | 60, frame 60 `gotoAndStop("loop")` | `gtav_savingspinner_hs.dds` |
| Online saving footer | `saving_footer.gfx` | `CONTENT.attachMovie("spinner","spinnerMC",1,{_x:24,_y:20})`; `DefineSprite_4_spinner` | 59 | none — vector art (`saving_footer_i1.dds` is the background) |
| Loading screen / legal screen / progress button | `loadingscreen_startup.gfx` | `LEGALSCREEN.spinner`, `LEGALSCREEN.LOADING_SPINNER` / `SAVING_SPINNER` / `CLOUD_SPINNER` (text), `PROGRESS_TEXT.BUTTON.icon.spinner` | library symbol (no named sprite) | `gtav_savingspinner.dds` (base), `_g`, `_ib` |
| Button-strip saving/respawn spinner (`ICON_SPINNER = 44`) | `instructional_buttons`, `generic_instructional_buttons`, `pause_menu_instructional_buttons`, `store_instructional_buttons`, `busy_spinner`, `popup_warning`, `custom_warning_screen`, `text_input_box` | `INSTRUCTIONAL_BUTTONS.respawn_spinnerMC.spinner`; `button_50` symbol | 59 | `gtav_savingspinner_ib.dds` / `_g` |
| Social Club / gen9 image-loading spinners | `social_club2` (`PAGES_WELCOME.imageSpinner`, `PAGES_QR_CODE.imageSpinner`); `frontend_landing` / `progress_hub` (`GridItem._spinner`, `SET_SPINNER_VISIBLE`) | `spinner` symbol | — | `_v2` (SC), `_ib` / plain (gen9) |

`HUD_SAVING.SET_SAVING_TEXT` selects the icon: `1 = WORKING` (SAVING icon), `4 = CLOUD_WORKING` (starMC), `5 = LOADING` (spinnerMC). Only `LOADING` shows `spinnerMC`; `WORKING` shows the `SAVING` icon and `CLOUD_WORKING` the star. The rest of the look (SAVING text, orange gradient) is separate art (`orange_grad.dds`).

For the 2013 ring specifically, the repo's base-game archives contain the old textures at
`x64b.rpf/data/cdimages/scaleform_frontend.rpf/loadingscreen_startup/gtav_savingspinner.dds`
and `x64b.rpf/data/cdimages/scaleform_generic.rpf/hud_saving/gtav_savingspinner_hs.dds`
(64×64). The Enhanced `_g` variant is the same arc artwork at a different compression/size,
so a texture-only swap will not change the animation: the distinctive ring is the 59/60-frame
sprite, and the `"loop"` label at frame 60 must be preserved or rebuilt when replacing it.
Many other `.ytd`s also carry a `gtav_savingspinner_*` texture (including `hud.ytd`,
`pause_menu_*`, `font_lib_*_pc`, `shop_menu_dlc`) purely because they embed the button strip;
they do not draw a loading ring themselves.

**Phones.** `cellphone_ifruit`, `cellphone_badger` and `cellphone_facade` are
separate movies with the same method contract; Michael's and the Online
character's phones both run `cellphone_ifruit`, so a distinct Online phone means
a new shell movie (or a reskin of the iFruit symbols) plus the same
`SET_DATA_SLOT`/`DISPLAY_VIEW`/`LOAD_APP` plumbing. The cutscene stills are
`cellphone_cutscene` (`gotoAndStop(viewID + 1)`), i.e. one PNG per view.

**Ultrawide.** Layout classes derive positions from
`SET_DISPLAY_CONFIG(screenWidth, screenHeight, safeTop, safeBottom, safeLeft, safeRight, …)`
and compute safe edges in pixels (`BaseScreenLayout` defaults: 1280×720, safe
96/54/1184/666). A HUD element that pins to `safeLeft`/`safeRight` will follow a
21:9 screen automatically *if* the game sends the real safe-zone percentages;
art baked at 16:9 (the radar's fixed 142×142 stage, the loading screen art,
`pause_menu_header`'s background image) will not. The radar's position on screen
is not computed here at all — the scaleform only builds a 142×142 radar; the game
places it.

**Pause-menu header.** The gradient is a texture set by `SET_HEADER_BG_IMG`
(alpha tween 0→100); there is no gradient code to make transparent — that is an
art edit.

**Instructional buttons** are a shared class with many skins
(`instructional_buttons`, `generic_instructional_buttons`,
`pause_menu_instructional_buttons`, `store_instructional_buttons`,
`busy_spinner`, `popup_warning`, `text_input_box`, `loadingscreen_startup`,
`custom_warning_screen`). Editing `INSTRUCTIONAL_BUTTONS.as` in one place is
enough for prompt behaviour across all of them; the skins differ by art only.

**Scaleform ↔ game direction.** All of these movies *receive* calls; nothing in
the repo shows which native/script triggers them. `GameInterface.call` is the
only outbound path (text localisation, sound, TXD requests). So questions like
"what sets the wanted level colour" or "who positions the radar" cannot be
answered from this repo alone — only the receiving side is here.

---

## 13. Coverage check

- 182 `.gfx` folders: 1 in `common.rpf`, 178 in
  `update/update.rpf/x64/data/cdimages/` (`frontend` 27, `frontend_gen9` 3,
  `generic` 136, `generic_2` 6, `platform_pc` 6), and 3 from the patch folder
  (`minimap`, `minimap_main_map`, `horse_racing_console`).
- 4,269 `.as` files, 256,484 lines.
- Largest gfx-specific classes: `MP_CELEBRATION` (115 KB), `SOCIAL_CLUB2`
  (65 KB), `PAUSE_MENU_SP_CONTENT` (52 KB), `LOADINGSCREEN_STARTUP` (50 KB),
  `MINIMAP` (46 KB), `MP_BIG_MESSAGE_FREEMODE` (46 KB).
- Every entry above maps to a folder in the repository; the archive column uses
  the repo's own path (`scaleform_frontend.rpf`, `scaleform_generic.rpf`,
  `scaleform_generic_2.rpf`, `scaleform_platform_pc.rpf`,
  `scaleform_frontend_gen9.rpf`, `scaleform_minimap.rpf`,
  `scaleform_minigames.rpf`).

### Limits of this study

- The repo is the **Enhanced** patch set. Legacy-gen scaleforms are absent except
  for their DDS textures in `x64b.rpf`.
- No `.fla`/timeline source: frame counts and sprite nesting are reconstructed,
  so "what happens on frame N" is only visible where a `DoAction.as` exists.
- Local variable names are decompiler-generated (`_loc2_`), and several
  functions are empty stubs in this build (e.g. `MOVE_MAPMASKSQUARE`,
  `SET_MASK` is a setter only).
- No game-side scripts/natives are included, so the triggers, timing and
  placement of these movies are outside the repository.
