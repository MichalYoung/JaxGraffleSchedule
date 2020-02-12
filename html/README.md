# SVG

June 2019: 
Small experiments for learning SVG.

Feb 2020:  SVG variants on hold until SVG v2 is widely supported; 
then SVG may become the preferred output format, or 
at least on a par with application-native formats 
like OmniGraffle jax. 

grid.html is a good prototype of grid layout with the 
basics I need ... ideally we will enhance the basic 
graffle support to have drivers for both OmniGraffle jax 
and HTML grid. 

## Experiments: first.html, svg.html

* A JavaScript library is really needed if 
SVG is to be dynamic, because the ability to define
and reference shapes in SVG alone is not 
sufficient.   svg.js seems ok. 

* Positioning and transforming is not too 
hard, although I haven't fully explored 
nested transformation a la PostScript. 
Relative positioning in `<g>` elements might
be enough. 

* Text is a weak spot.  You can't flow 
text in an SVG object.  We have to 
compute line breaks and line spacing 
explicitly, although a JS library 
can help with the latter. 

    * Update: It appears that (until SVG 2 brings us wrapped 
    text native in SVG) the preferred way to do this is with 
    a `<foreignobject>` element, which is tedious but easy 
    to generate.  It is not supported by IE, but it is (?)
    supported by Edge. 

* Type sizes are wacky and don't match 
what one expects from type sizes outside 
of the SVG graphic.  This is probably 
a side effect of how the viewport is scaled, 
but it's not easy to determine what 
values to use for `font-size`.    

Given the weakness of text processing, 
if simple rectangles containing text 
are the intended result, positioning 
divs may be a better choice.  

## Experiments: divs.html

The point of these experiments is to try 
to lay out something like a weekly schedule
using only divs, with computed positions
(world to view coordinate translation). 

It looks like the method for inserting a 
new element should be 

```javascript
element.insertAdjacentHTML(position, text);
```
and position should be `'beforeend'`. 

Results: Absolute positioning is not working as I expected. 
I am not getting wrapper element to take the proper width 
and contain the elements positioned within it.

## Experiments: grid.html

Grid model!  This was introduced in CSS3 and appears 
to give me the basic parts I need. 

Bingo.  This seems to give me the flexibility I need, with 
fairly easy addressing.  Getting columnns to be the same 
width is a bit of a challenge so far, but I'm sure I'll 
figure it out. 

## Experiments: grades.html

A different use for SVG:  Graph of grade progressions 
through courses. 

