/* ---- vanitygaps + fibonacci: add to your config.h (needs dwm-vanitygaps-6.x.diff) ----
 * Why by hand: NixOS replaces the patch's config.def.h with your config.h, so the
 * pieces the patch would have put there must live in your own file.
 * Put 1 and 2 where your old `layouts[]` was; put 3 inside keys[].             */

/* ---- 1. gaps (vanitygaps) ---------------------------------------------- */
static const unsigned int gappih = 6;   /* inner gap, horizontal (between windows) */
static const unsigned int gappiv = 6;   /* inner gap, vertical                      */
static const unsigned int gappoh = 6;   /* outer gap, horizontal (to screen edge)   */
static const unsigned int gappov = 6;   /* outer gap, vertical                      */
static       int smartgaps       = 0;   /* 1 = no outer gap with a single window    */

#define FORCE_VSPLIT 1                  /* setting the patch's code reads (nrowgrid)   */
#include "vanitygaps.c"                 /* must come after the gap variables + define */

/* ---- 2. layouts: the FIRST entry is the one every tag starts with ------- */
static const Layout layouts[] = {
	/* symbol     arrange function */
	{ "[\\]",     dwindle },   /* fibonacci: each new window halves the last   */
	{ "[@]",      spiral },    /* fibonacci: same, but winding inwards         */
	{ "[]=",      tile },      /* classic master + stack                       */
	{ "><>",      NULL },      /* floating                                     */
};

/* ---- 3. keys: add to keys[] (and delete the old t / f / m setlayout lines) ---- */
	{ MODKEY,                       XK_t,      setlayout,      {.v = &layouts[2]} },  /* tile       */
	{ MODKEY,                       XK_r,      setlayout,      {.v = &layouts[0]} },  /* dwindle    */
	{ MODKEY|ShiftMask,             XK_r,      setlayout,      {.v = &layouts[1]} },  /* spiral     */
	{ MODKEY,                       XK_f,      setlayout,      {.v = &layouts[3]} },  /* floating   */
	{ MODKEY,                       XK_minus,  incrgaps,       {.i = -1 } },          /* gaps -     */
	{ MODKEY,                       XK_equal,  incrgaps,       {.i = +1 } },          /* gaps +     */
	{ MODKEY|ShiftMask,             XK_minus,  togglegaps,     {0} },                 /* gaps off   */
	{ MODKEY|ShiftMask,             XK_equal,  defaultgaps,    {0} },                 /* gaps reset */
