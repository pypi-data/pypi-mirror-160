# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeComposite(Component):
    """A FeComposite component.
FeComposite is a wrapper for the <feComposite> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feComposite

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- aria-* (string; optional):
    A wildcard aria attribute.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- colorInterpolationFilters (a value equal to: '"auto"|"inherit"|"linearRGB"|"sRGB"' | boolean; optional):
    The color-interpolation-filters attribute specifies the color
    space for imaging operations performed via filter effects.Note:
    This property just has an affect on filter operations.  Therefore,
    it has no effect on filter primitives like  <feOffset>, <feImage>,
    <feTile> or <feFlood>.color-interpolation-filters  has a different
    initial value than color-interpolation.
    color-interpolation-filters has an initial value of linearRGB,
    whereas color-interpolation has an initial value of sRGB.  Thus,
    in the default case, filter effects operations occur  in the
    linearRGB color space, whereas all other color  interpolations
    occur by default in the sRGB color space.It  has no affect on
    filter functions, which operate in the  sRGB color space.Note: As
    a presentation attribute, color-interpolation-filters  can be used
    as a CSS property.You can use this attribute  with the following
    SVG elements:Indicates that the user  agent can choose either the
    sRGB or linearRGB spaces for  color interpolation. This option
    indicates that the author  doesn't require that color
    interpolation occur in a particular  color space.Indicates that
    color interpolation should  occur in the sRGB color
    space.Indicates that color interpolation  should occur in the
    linearized RGB color space as described  in the sRGB
    specification.BCD tables only load in the  browser with JavaScript
    enabled. Enable JavaScript to  view data.Last modified: May 13,
    2022, by MDN contributors.

- data-* (string; optional):
    A wildcard data attribute.

- height (string | number; optional):
    The height attribute defines the vertical length of an element  in
    the user coordinate system.You can use this attribute  with the
    following SVG elements:For <feBlend>, height  defines the vertical
    length for the rendering area of  the primitive.For
    <feColorMatrix>, height defines the  vertical length for the
    rendering area of the primitive.For  <feComponentTransfer>, height
    defines the vertical length  for the rendering area of the
    primitive.For <feComposite>,  height defines the vertical length
    for the rendering area  of the primitive.For <feConvolveMatrix>,
    height defines  the vertical length for the rendering area of the
    primitive.For  <feDiffuseLighting>, height defines the vertical
    length  for the rendering area of the primitive.For
    <feDisplacementMap>,  height defines the vertical length for the
    rendering area  of the primitive.For <feDropShadow>, height
    defines the  vertical length for the rendering area of the
    primitive.For  <feFlood>, height defines the vertical length for
    the  rendering area of the primitive.For <feGaussianBlur>,  height
    defines the vertical length for the rendering area  of the
    primitive.For <feImage>, height defines the vertical  length for
    the rendering area of the primitive.For <feMerge>,  height defines
    the vertical length for the rendering area  of the primitive.For
    <feMorphology>, height defines the  vertical length for the
    rendering area of the primitive.For  <feOffset>, height defines
    the vertical length for the  rendering area of the primitive.For
    <feSpecularLighting>,  height defines the vertical length for the
    rendering area  of the primitive.For <feTile>, height defines the
    vertical  length for the rendering area of the primitive.For
    <feTurbulence>,  height defines the vertical length for the
    rendering area  of the primitive.For <filter>, height defines the
    vertical  length for the rendering area of the filter.For
    <foreignObject>,  height defines the vertical length for the
    rendering area  for the referenced document.Note: Starting with
    SVG2,  height is a Geometry Property meaning this attribute can
    also be used as a CSS property for <foreignObject>.For  <image>,
    height defines the vertical length for the image.Note:  Starting
    with SVG2, height is a Geometry Property meaning  this attribute
    can also be used as a CSS property for  images.For <mask>, height
    defines the vertical length  of its area of effect. The exact
    effect of this attribute  is influenced by the maskUnits
    attribute.For <pattern>,  height defines the vertical length of
    the tile pattern.  The exact effect of this attribute is
    influenced by the  patternUnits and patternTransform
    attributes.For <rect>,  height defines the vertical length for the
    rectangle.Note:  Starting with SVG2, height is a Geometry Property
    meaning  this attribute can also be used as a CSS property for
    rectangles.For <svg>, height defines the vertical length  for the
    rendering area of the SVG viewport.Note: In an  HTML document if
    both the viewBox and height attributes  are omitted, the svg
    element will be rendered with a height  of 150pxNote: Starting
    with SVG2, height is a Geometry  Property meaning this attribute
    can also be used as a  CSS property for <svg>.For <use>, height
    defines the vertical  length for the referenced element.Note:
    height has no  effect on use elements, unless the element
    referenced  has a viewbox - i.e. they only have an effect when use
    refers to a svg or symbol element.Note: Starting with  SVG2,
    height is a Geometry Property meaning this attribute  can also be
    used as a CSS property for used elements.Last  modified: Jun 29,
    2022, by MDN contributors.

- in (string | number; optional):
    The in attribute identifies input for the given filter
    primitive.The  value can be either one of the six keywords defined
    below,  or a string which matches a previous result attribute
    value within the same <filter> element. If no value is  provided
    and this is the first filter primitive, then  this filter
    primitive will use SourceGraphic as its input.  If no value is
    provided and this is a subsequent filter  primitive, then this
    filter primitive will use the result  from the previous filter
    primitive as its input.If the  value for result appears multiple
    times within a given  <filter> element, then a reference to that
    result will  use the closest preceding filter primitive with the
    given  value for attribute result.You can use this attribute  with
    the following SVG elements:This keyword represents  the graphics
    elements that were the original input into  the <filter>
    element.This keyword represents the graphics  elements that were
    the original input into the <filter>  element. SourceAlpha has all
    of the same rules as SourceGraphic  except that only the alpha
    channel is used.This keyword  represents an image snapshot of the
    SVG document under  the filter region at the time that the
    <filter> element  was invoked.Same as BackgroundImage except only
    the alpha  channel is used.This keyword represents the value of
    the  fill property on the target element for the filter effect.
    In many cases, the FillPaint is opaque everywhere, but  that might
    not be the case if a shape is painted with  a gradient or pattern
    which itself includes transparent  or semi-transparent parts.This
    keyword represents the  value of the stroke property on the target
    element for  the filter effect. In many cases, the StrokePaint is
    opaque  everywhere, but that might not be the case if a shape  is
    painted with a gradient or pattern which itself includes
    transparent or semi-transparent parts.This value is an  assigned
    name for the filter primitive in the form of  a <custom-ident>. If
    supplied, then graphics that result  from processing this filter
    primitive can be referenced  by an in attribute on a subsequent
    filter primitive within  the same filter element. If no value is
    provided, the  output will only be available for re-use as the
    implicit  input into the next filter primitive if that filter
    primitive  provides no value for its in attribute.BackgroundImage
    is not supported as a filter source in modern browsers  (see the
    feComposite compatibility table). We therefore  need to import one
    of the images to blend inside the filter  itself, using an
    <feImage> element.Note: Firefox Bug 455986  means that feImage
    cannot load partial images, including  circles, rectangles, paths
    or other fragments defined  in the document. So that this example
    works on more browsers,  a full external image of the logo is
    loaded.Last modified:  Jul 1, 2022, by MDN contributors.

- in2 (string | number; optional):
    The in2 attribute identifies the second input for the given filter
    primitive. It works exactly like the in attribute.You  can use
    this attribute with the following SVG elements:For  <feBlend>, in2
    defines the second input image to the blending  operation.For
    <feComposite>, in2 defines the second input  image to the
    compositing operation.For <feDisplacementMap>,  in2 defines the
    second input image, which is used to displace  the pixels in the
    image defined in the in attribute.Last  modified: May 13, 2022, by
    MDN contributors.

- k1 (string | number; optional):
    The k1 attribute defines one of the values to be used within  the
    arithmetic operation of the <feComposite> filter primitive.The
    pixel composition is computed using the following formula:You  can
    use this attribute with the following SVG elements:BCD  tables
    only load in the browser with JavaScript enabled.  Enable
    JavaScript to view data.Last modified: May 13,  2022, by MDN
    contributors.

- k2 (string | number; optional):
    The k2 attribute defines one of the values to be used within  the
    arithmetic operation of the <feComposite> filter primitive.The
    pixel composition is computed using the following formula:You  can
    use this attribute with the following SVG elements:BCD  tables
    only load in the browser with JavaScript enabled.  Enable
    JavaScript to view data.Last modified: May 13,  2022, by MDN
    contributors.

- k3 (string | number; optional):
    The k3 attribute defines one of the values to be used within  the
    arithmetic operation of the <feComposite> filter primitive.The
    pixel composition is computed using the following formula:You  can
    use this attribute with the following SVG elements:BCD  tables
    only load in the browser with JavaScript enabled.  Enable
    JavaScript to view data.Last modified: May 13,  2022, by MDN
    contributors.

- k4 (string | number; optional):
    The k4 attribute defines one of the values to be used within  the
    arithmetic operation of the <feComposite> filter primitive.The
    pixel composition is computed using the following formula:You  can
    use this attribute with the following SVG elements:BCD  tables
    only load in the browser with JavaScript enabled.  Enable
    JavaScript to view data.Last modified: May 13,  2022, by MDN
    contributors.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- n_clicks_timestamp (number; default -1):
    An integer that represents the time (in ms since 1970) at which
    n_clicks changed. This can be used to tell which button was
    changed most recently.

- operator (string | number; optional):
    The operator attribute has two meanings based on the context  it's
    used in. Either it defines the compositing or morphing  operation
    to be performed.You can use this attribute with  the following SVG
    elements:For <feComposite>, operator  defines the compositing
    operation that is to be performed.This  value indicates that the
    source graphic defined in the  in attribute is placed over the
    destination graphic defined  in the in2 attribute.This value
    indicates that the parts  of the source graphic defined in the in
    attribute that  overlap the destination graphic defined in the in2
    attribute,  replace the destination graphic.This value indicates
    that  the parts of the source graphic defined in the in attribute
    that fall outside the destination graphic defined in the  in2
    attribute, are displayed.This value indicates that  the parts of
    the source graphic defined in the in attribute,  which overlap the
    destination graphic defined in the in2  attribute, replace the
    destination graphic. The parts  of the destination graphic that do
    not overlap with the  source graphic stay untouched.This value
    indicates that  the non-overlapping regions of the source graphic
    defined  in the in attribute and the destination graphic defined
    in the in2 attribute are combined.This value indicates  that the
    sum of the source graphic defined in the in attribute  and the
    destination graphic defined in the in2 attribute  is
    displayed.This value indicates that the source graphic  defined in
    the in attribute and the destination graphic  defined in the in2
    attribute are combined using the following  formula:result =
    k1*i1*i2 + k2*i1 + k3*i2 + k4       where:        i1 and i2
    indicate the corresponding pixel channel  values of the input
    image, which map to in and in2 respectively,  and k1, k2, k3, and
    k4 indicate the values of the attributes  with the same name.
    For <feMorphology>, operator defines  whether to erode (i.e.,
    thin) or dilate (fatten) the source  graphic.This value thins the
    source graphic defined in  the in attribute.This value fattens the
    source graphic  defined in the in attribute.Last modified: Jul 12,
    2022,  by MDN contributors.

- result (string; optional):
    The result attribute defines the assigned name for this filter
    primitive. If supplied, then graphics that result from  processing
    this filter primitive can be referenced by  an in attribute on a
    subsequent filter primitive within  the same <filter> element. If
    no value is provided, the  output will only be available for
    re-use as the implicit  input into the next filter primitive if
    that filter primitive  provides no value for its in attribute.You
    can use this  attribute with the following SVG elements:This value
    is  a <custom-ident> and defines the name for the filter
    primitive.  It is only meaningful within a given <filter> element
    and thus has only local scope. It is legal for the same
    <filter-primitive-reference> to appear multiple times  within the
    same <filter> element. When referenced, this  value will use the
    closest preceding filter primitive  with the given result.Last
    modified: May 13, 2022, by  MDN contributors.

- role (string; optional):
    The ARIA role attribute.

- width (string | number; optional):
    The width attribute defines the horizontal length of an element
    in the user coordinate system.You can use this attribute  with the
    following SVG elements:For <feBlend>, width defines  the
    horizontal length for the rendering area of the primitive.For
    <feColorMatrix>, width defines the horizontal length for  the
    rendering area of the primitive.For <feComponentTransfer>,  width
    defines the horizontal length for the rendering  area of the
    primitive.For <feComposite>, width defines  the horizontal length
    for the rendering area of the primitive.For  <feConvolveMatrix>,
    width defines the horizontal length  for the rendering area of the
    primitive.For <feDiffuseLighting>,  width defines the horizontal
    length for the rendering  area of the primitive.For
    <feDisplacementMap>, width defines  the horizontal length for the
    rendering area of the primitive.For  <feDropShadow>, width defines
    the horizontal length for  the rendering area of the primitive.For
    <feFlood>, width  defines the horizontal length for the rendering
    area of  the primitive.For <feGaussianBlur>, width defines the
    horizontal length for the rendering area of the primitive.For
    <feImage>, width defines the horizontal length for the  rendering
    area of the primitive.For <feMerge>, width defines  the horizontal
    length for the rendering area of the primitive.For
    <feMorphology>, width defines the horizontal length for  the
    rendering area of the primitive.For <feOffset>, width  defines the
    horizontal length for the rendering area of  the primitive.For
    <feSpecularLighting>, width defines  the horizontal length for the
    rendering area of the primitive.For  <feTile>, width defines the
    horizontal length for the  rendering area of the primitive.For
    <feTurbulence>, width  defines the horizontal length for the
    rendering area of  the primitive.For <filter>, width defines the
    horizontal  length for the rendering area of the filter.For
    <foreignObject>,  width defines the horizontal length for the
    rendering  area for the referenced document.Note: Starting with
    SVG2,  width is a Geometry Property meaning this attribute can
    also be used as a CSS property for <foreignObject>.For  <image>,
    width defines the horizontal length for the image.Note:  Starting
    with SVG2, width is a Geometry Property meaning  this attribute
    can also be used as a CSS property for  images.For <mask>, width
    defines the horizontal length  of its area of effect. The exact
    effect of this attribute  is influenced by the maskUnits
    attribute.For <pattern>,  width defines the horizontal length of
    the tile pattern.  The exact effect of this attribute is
    influenced by the  patternUnits and patternTransform
    attributes.For <rect>,  width defines the horizontal length for
    the rectangle.Note:  Starting with SVG2, width is a Geometry
    Property meaning  this attribute can also be used as a CSS
    property for  rectangles.For <svg>, width defines the horizontal
    length  for the rendering area of the SVG viewport.Note: In an
    HTML document if both the viewBox and width attributes  are
    omitted, the svg element will be rendered with a width  of
    300pxNote: Starting with SVG2, width is a Geometry  Property
    meaning this attribute can also be used as a  CSS property for
    <svg>.For <use>, width defines the horizontal  length for the
    referenced element.Note: width has no effect  on use elements,
    unless the element referenced has a viewbox  - i.e. they only have
    an effect when use refers to a svg  or symbol element.Note:
    Starting with SVG2, width is a  Geometry Property meaning this
    attribute can also be used  as a CSS property for used
    elements.Last modified: Jun  29, 2022, by MDN contributors.

- x (string | number; optional):
    The x attribute defines an x-axis coordinate in the user
    coordinate  system.You can use this attribute with the following
    SVG  elements:Warning: As of SVG2 <altGlyph> is deprecated  and
    shouldn't be used.For <altGlyph>, x defines the x-axis  coordinate
    of the alternate glyph.For <feBlend>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For
    <feColorMatrix>, x defines the minimum x  coordinate for the
    rendering area of the primitive.For  <feComponentTransfer>, x
    defines the minimum x coordinate  for the rendering area of the
    primitive.For <feComposite>,  x defines the minimum x coordinate
    for the rendering area  of the primitive.For <feConvolveMatrix>, x
    defines the  minimum x coordinate for the rendering area of the
    primitive.For  <feDiffuseLighting>, x defines the minimum x
    coordinate  for the rendering area of the primitive.For
    <feDisplacementMap>,  x defines the minimum x coordinate for the
    rendering area  of the primitive.For <feDropShadow>, x defines the
    minimum  x coordinate for the rendering area of the primitive.For
    <feFlood>, x defines the minimum x coordinate for the  rendering
    area of the primitive.For <feFuncA>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For <feFuncB>,
    x defines the minimum x coordinate  for the rendering area of the
    primitive.For <feFuncG>,  x defines the minimum x coordinate for
    the rendering area  of the primitive.For <feFuncR>, x defines the
    minimum  x coordinate for the rendering area of the primitive.For
    <feGaussianBlur>, x defines the minimum x coordinate for  the
    rendering area of the primitive.For <feImage>, x defines  the
    minimum x coordinate for the rendering area of the  primitive.For
    <feMerge>, x defines the minimum x coordinate  for the rendering
    area of the primitive.For <feMergeNode>,  x defines the minimum x
    coordinate for the rendering area  of the primitive.For
    <feMorphology>, x defines the minimum  x coordinate for the
    rendering area of the primitive.For  <feOffset>, x defines the
    minimum x coordinate for the  rendering area of the primitive.For
    <fePointLight>, x  defines the x location for the light source in
    the coordinate  system defined by the primitiveUnits attribute on
    the  <filter> element.For <feSpecularLighting>, x defines the
    minimum x coordinate for the rendering area of the primitive.For
    <feSpotLight>, x defines the x location for the light  source in
    the coordinate system defined by the primitiveUnits  attribute on
    the <filter> element.For <feTile>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For
    <feTurbulence>, x defines the minimum x  coordinate for the
    rendering area of the primitive.For  <filter>, x defines the x
    coordinate of the upper left  corner for the rendering area of the
    filter.For <foreignObject>,  x defines the x coordinate of the
    upper left corner of  its viewport.Note: Starting with SVG2, x is
    a Geometry  Property meaning this attribute can also be used as a
    CSS property for <foreignObject>.Warning: As of SVG2 <glyphRef>
    is deprecated and shouldn't be used.For <glyphRef>, x  defines the
    x-axis coordinate of the glyph.For <image>,  x defines the x
    coordinate of the upper left corner of  the image.Note: Starting
    with SVG2, x is a Geometry Property  meaning this attribute can
    also be used as a CSS property  for images.For <mask>, x defines
    the x coordinate of the  upper left corner of its area of effect.
    The exact effect  of this attribute is influenced by the maskUnits
    attribute.For  <pattern>, x defines the x coordinate of the upper
    left  corner of the tile pattern. The exact effect of this
    attribute  is influenced by the patternUnits and patternTransform
    attributes.For <rect>, x defines the x coordinate of the  upper
    left corner of the shape.Note: Starting with SVG2,  x is a
    Geometry Property meaning this attribute can also  be used as a
    CSS property for rectangles.For <svg>, x  defines the x coordinate
    of the upper left corner of its  viewport.Note: Starting with
    SVG2, x is a Geometry Property  meaning this attribute can also be
    used as a CSS property  for <svg>.For <text>, if it contains a
    single value, x  defines the x coordinate where the content text
    position  must be placed. The content text position is usually a
    point on the baseline of the first line of text. The exact
    content text position is influenced by other properties,  such as
    text-anchor or direction.If it contains multiple  values, x
    defines the x coordinate of each individual  glyph from the text.
    If there are fewer values than glyphs,  the remaining glyphs are
    placed in line with the last  positioned glyph. If there are more
    values than glyphs,  the extra values are ignored.Warning: As of
    SVG2 <tref>  is deprecated and shouldn't be used.For <tref>, if it
    contains a single value, x defines the x coordinate where  the
    content text position must be placed. The content  text position
    is usually a point on the baseline of the  first line of text. The
    exact content text position is  influenced by other properties,
    such as text-anchor or  direction.If it contains multiple values,
    x defines the  x coordinate of each individual glyph from the
    text. If  there are fewer values than glyphs, the remaining glyphs
    are placed in line with the last positioned glyph. If  there are
    more values than glyphs, the extra values are  ignored.For
    <tspan>, if it contains a single value, x  defines the x
    coordinate where the content text position  must be placed. The
    content text position is usually a  point on the baseline of the
    first line of text. The exact  content text position is influenced
    by other properties,  such as text-anchor or direction.If it
    contains multiple  values, x defines the x coordinate of each
    individual  glyph from the text. If there are fewer values than
    glyphs,  the remaining glyphs are placed in line with the last
    positioned glyph. If there are more values than glyphs,  the extra
    values are ignored.For <use>, x defines the  x coordinate of the
    upper left corner of the referenced  element.Note: Starting with
    SVG2, x is a Geometry Property  meaning this attribute can also be
    used as a CSS property  for used elements.Last modified: Jun 17,
    2022, by MDN  contributors.

- y (string | number; optional):
    The y attribute defines a y-axis coordinate in the user coordinate
    system.You can use this attribute with the following SVG
    elements:Warning: As of SVG2 <altGlyph> is deprecated  and
    shouldn't be used.For <altGlyph>, y defines the y-axis  coordinate
    of the alternate glyph.For <feBlend>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For
    <feColorMatrix>, y defines the minimum y  coordinate for the
    rendering area of the primitive.For  <feComponentTransfer>, y
    defines the minimum y coordinate  for the rendering area of the
    primitive.For <feComposite>,  y defines the minimum y coordinate
    for the rendering area  of the primitive.For <feConvolveMatrix>, y
    defines the  minimum y coordinate for the rendering area of the
    primitive.For  <feDiffuseLighting>, y defines the minimum y
    coordinate  for the rendering area of the primitive.For
    <feDisplacementMap>,  y defines the minimum y coordinate for the
    rendering area  of the primitive.For <feDropShadow>, y defines the
    minimum  y coordinate for the rendering area of the primitive.For
    <feFlood>, y defines the minimum y coordinate for the  rendering
    area of the primitive.For <feFuncA>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For <feFuncB>,
    y defines the minimum y coordinate  for the rendering area of the
    primitive.For <feFuncG>,  y defines the minimum y coordinate for
    the rendering area  of the primitive.For <feFuncR>, y defines the
    minimum  y coordinate for the rendering area of the primitive.For
    <feGaussianBlur>, y defines the minimum y coordinate for  the
    rendering area of the primitive.For <feImage>, y defines  the
    minimum y coordinate for the rendering area of the  primitive.For
    <feMerge>, y defines the minimum y coordinate  for the rendering
    area of the primitive.For <feMergeNode>,  y defines the minimum y
    coordinate for the rendering area  of the primitive.For
    <feMorphology>, y defines the minimum  y coordinate for the
    rendering area of the primitive.For  <feOffset>, y defines the
    minimum y coordinate for the  rendering area of the primitive.For
    <fePointLight>, y  defines the y location for the light source in
    the coordinate  system defined by the primitiveUnits attribute on
    the  <filter> element.For <feSpecularLighting>, y defines the
    minimum y coordinate for the rendering area of the primitive.For
    <feSpotLight>, y defines the y location for the light  source in
    the coordinate system defined by the primitiveUnits  attribute on
    the <filter> element.For <feTile>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For
    <feTurbulence>, y defines the minimum y  coordinate for the
    rendering area of the primitive.For  <filter>, y defines the y
    coordinate of the upper left  corner for the rendering area of the
    filter.For <foreignObject>,  y defines the y coordinate of the
    upper left corner of  its viewport.Note: Starting with SVG2, y is
    a Geometry  Property meaning this attribute can also be used as a
    CSS property for <foreignObject>.Warning: As of SVG2 <glyphRef>
    is deprecated and shouldn't be used.For <glyphRef>, y  defines the
    y-axis coordinate of the glyph.For <image>,  y defines the y
    coordinate of the upper left corner of  the image.Note: Starting
    with SVG2, y is a Geometry Property  meaning this attribute can
    also be used as a CSS property  for images.For <mask>, y defines
    the y coordinate of the  upper left corner of its area of effect.
    The exact effect  of this attribute is influenced by the maskUnits
    attribute.For  <pattern>, y defines the y coordinate of the upper
    left  corner of the tile pattern. The exact effect of this
    attribute  is influenced by the patternUnits and patternTransform
    attributes.For <rect>, y defines the y coordinate of the  upper
    left corner of the shape.Note: Starting with SVG2,  y is a
    Geometry Property meaning this attribute can also  be used as a
    CSS property for rectangles.For <svg>, y  defines the y coordinate
    of the upper left corner of its  viewport.Note: Starting with
    SVG2, y is a Geometry Property  meaning this attribute can also be
    used as a CSS property  for <svg>.For <text>, if it contains a
    single value, y  defines the y coordinate where the content text
    position  must be placed. The content text position is usually a
    point on the baseline of the first line of text. The exact
    content text position is influenced by other properties,  such as
    text-anchor or direction.If it contains multiple  values, y
    defines the y coordinate of each individual  glyph from the text.
    If there are fewer values than glyphs,  the remaining glyphs are
    placed in line with the last  positioned glyph. If there are more
    values than glyphs,  the extra values are ignored.Warning: As of
    SVG2 <tref>  is deprecated and shouldn't be used.For <tref>, if it
    contains a single value, y defines the y coordinate where  the
    content text position must be placed. The content  text position
    is usually a point on the baseline of the  first line of text. The
    exact content text position is  influenced by other properties,
    such as text-anchor or  direction.If it contains multiple values,
    y defines the  y coordinate of each individual glyph from the
    text. If  there are fewer values than glyphs, the remaining glyphs
    are placed in line with the last positioned glyph. If  there are
    more values than glyphs, the extra values are  ignored.For
    <tspan>, if it contains a single value, y  defines the y
    coordinate where the content text position  must be placed. The
    content text position is usually a  point on the baseline of the
    first line of text. The exact  content text position is influenced
    by other properties,  such as text-anchor or direction.If it
    contains multiple  values, y defines the y coordinate of each
    individual  glyph from the text. If there are fewer values than
    glyphs,  the remaining glyphs are placed in line with the last
    positioned glyph. If there are more values than glyphs,  the extra
    values are ignored.For <use>, y defines the  y coordinate of the
    upper left corner of the referenced  element.Note: Starting with
    SVG2, y is a Geometry Property  meaning this attribute can also be
    used as a CSS property  for used elements.Last modified: Jun 14,
    2022, by MDN  contributors."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_svg'
    _type = 'FeComposite'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, colorInterpolationFilters=Component.UNDEFINED, height=Component.UNDEFINED, in2=Component.UNDEFINED, k1=Component.UNDEFINED, k2=Component.UNDEFINED, k3=Component.UNDEFINED, k4=Component.UNDEFINED, operator=Component.UNDEFINED, result=Component.UNDEFINED, width=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'colorInterpolationFilters', 'data-*', 'height', 'in', 'in2', 'k1', 'k2', 'k3', 'k4', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'operator', 'result', 'role', 'width', 'x', 'y']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'colorInterpolationFilters', 'data-*', 'height', 'in', 'in2', 'k1', 'k2', 'k3', 'k4', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'operator', 'result', 'role', 'width', 'x', 'y']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FeComposite, self).__init__(children=children, **args)
