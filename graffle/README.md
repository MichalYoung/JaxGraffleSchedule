# Graffle charts

Produce charts as OmniGraffle
javascript.  
See [https://omni-automation.com/tutorial/og-macos/index.html](https://omni-automation.com/tutorial/og-macos/index.html)

## Origin and dimensions

It appears that in a default document, 
the upper-left corner of the page 
is positioned at the upper-left corner 
of the graphics bounding box, so 
the origin of the inserted graphics really
has no effect.  The displayed page already
has a page margin of (approximately?)
0.5 inches.   (This might be 
printer dependent.)

The following displays two 
rectangles.  The red border 
of the large grey rectangle
is not visible, perhaps because 
its stroke width defaults to 0. 

```javascript
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

/* Second rectangle pushes first 
 * into relative position. 
 */
var g2 = canvas.newShape();
g2.strokeColor = Color.RGB(0.5, 0.5, 0.5);
g2.fillColor = Color.RGB(0, 0, 0);
g2.geometry = new Rect(0, 0, 72, 72);

```