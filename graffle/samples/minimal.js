/* Attempts at minimal javascript to draw
 * a rectangle on the page.  I want a single
 * rectangle centered on an 8.5x11in sheet,
 * with 1 inch margin all sides.
 * So: left margin = 72 points
 *     top margin = 72 points
 *     width = (8.5 - 2) * 72
 *     height = (11 - 2) * 72
 */
var canvas = document.windows[0].selection.canvas;
var g1 = canvas.newShape();
g1.strokeColor = Color.RGB(0.5, 0.0, 0.0);
g1.fillColor = Color.RGB(0.5, 0.5, 0.5);
g1.geometry = new Rect(72, 72, 6.5*72, 9*72);

/* I'm not sure if it is moving canvas to anchor
 * at upper leftmost point of figure.  To be sure,
 * we'll put a tiny rectangle at 0,0.
 */
var g2 = canvas.newShape();
g2.strokeColor = Color.RGB(0.5, 0.5, 0.5);
g2.fillColor = Color.RGB(0, 0, 0);
g2.geometry = new Rect(0, 0, 72, 72);
