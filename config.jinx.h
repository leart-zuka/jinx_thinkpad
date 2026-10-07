/* ---- Jinx rice: paste over the matching blocks in your dwm config.h ---- */

/* Bar text font first, Doodlebomb second. The tag glyphs live in the
 * Private Use Area, so Xft falls back to Doodlebomb for them automatically.
 * Bar height comes from the FIRST font; jinxbar picks it up automatically. */
static const char *fonts[]    = { "monospace:size=9", "Doodlebomb:pixelsize=15" };
static const char dmenufont[] =   "monospace:size=9";

/* "Powder keg" palette, pulled from the two wallpapers */
static const char col_bg[]    = "#14141f";  /* night sky            */
static const char col_bg2[]   = "#1c1f34";  /* bruised navy         */
static const char col_dim[]   = "#3a3550";  /* unlit meter / borders */
static const char col_chalk[] = "#d6cbd0";  /* chalk graffiti       */
static const char col_pink[]  = "#e0237f";  /* hot pink spray       */
static const char col_blue[]  = "#4fa8e0";  /* braid blue           */
static const char col_teal[]  = "#61baa5";  /* mint decal           */

static const char *colors[][3] = {
	/*               fg         bg         border   */
	[SchemeNorm] = { col_chalk, col_bg,    col_dim  },
	[SchemeSel]  = { col_bg,    col_pink,  col_pink },
	/* calmer alternative if a full pink title bar is too loud:
	[SchemeSel]  = { col_pink,  col_bg2,   col_pink }, */
};

/* scrawled digits 1-9 from Doodlebomb (U+100000-100008).
 * Prefer the doodles instead? Use "\U00100010"..."\U00100018" (star, pentagram, skull,
 * launch, X, spiral, bomb, bolt, target) — or mix, e.g. a skull on tag 9. */
static const char *tags[] = {
	"\U00100000", "\U00100001", "\U00100002", "\U00100003", "\U00100004",
	"\U00100005", "\U00100006", "\U00100007", "\U00100008",
};

/* colour per tag, same order as tags[] — the decal trio, repeated */
static const char *tagcols[] = {
	col_pink, col_blue, col_teal,
	col_pink, col_blue, col_teal,
	col_pink, col_blue, col_teal,
};

/* dmenu in the same colours — replace your dmenucmd */
static const char *dmenucmd[] = { "dmenu_run", "-fn", dmenufont,
	"-nb", col_bg, "-nf", col_chalk, "-sb", col_pink, "-sf", col_bg, NULL };

static const unsigned int borderpx = 2;  /* pink border on the focused window */
