# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeSpotLight(Component):
    """A FeSpotLight component.
FeSpotLight is a wrapper for the <feSpotLight> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feSpotLight

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

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- limitingConeAngle (string | number; optional):
    The limitingConeAngle attribute represents the angle in degrees
    between the spot light axis (i.e. the axis between the  light
    source and the point to which it is pointing at)  and the spot
    light cone. So it defines a limiting cone  which restricts the
    region where the light is projected.  No light is projected
    outside the cone.You can use this  attribute with the following
    SVG elements:BCD tables only  load in the browser with JavaScript
    enabled. Enable JavaScript  to view data.Last modified: May 13,
    2022, by MDN contributors.

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

- pointsAtX (string | number; optional):
    The pointsAtX attribute represents the x location in the
    coordinate  system established by attribute primitiveUnits on the
    <filter> element of the point at which the light source  is
    pointing.You can use this attribute with the following  SVG
    elements:BCD tables only load in the browser with  JavaScript
    enabled. Enable JavaScript to view data.Last  modified: May 13,
    2022, by MDN contributors.

- pointsAtY (string | number; optional):
    The pointsAtY attribute represents the y location in the
    coordinate  system established by attribute primitiveUnits on the
    <filter> element of the point at which the light source  is
    pointing.You can use this attribute with the following  SVG
    elements:BCD tables only load in the browser with  JavaScript
    enabled. Enable JavaScript to view data.Last  modified: May 13,
    2022, by MDN contributors.

- pointsAtZ (string | number; optional):
    The pointsAtZ attribute represents the y location in the
    coordinate  system established by attribute primitiveUnits on the
    <filter> element of the point at which the light source  is
    pointing, assuming that, in the initial local coordinate  system,
    the positive z-axis comes out towards the person  viewing the
    content and assuming that one unit along the  z-axis equals one
    unit in x and y.You can use this attribute  with the following SVG
    elements:BCD tables only load in  the browser with JavaScript
    enabled. Enable JavaScript  to view data.Last modified: May 13,
    2022, by MDN contributors.

- role (string; optional):
    The ARIA role attribute.

- specularExponent (string | number; optional):
    The specularExponent attribute controls the focus for the light
    source. The bigger the value the brighter the light.You  can use
    this attribute with the following SVG elements:For
    <feSpecularLighting>, specularExponent defines the exponent  value
    for the specular term.For <feSpotLight>, specularExponent  defines
    the exponent value controlling the focus for the  light
    source.Last modified: May 13, 2022, by MDN contributors.

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
    2022, by MDN  contributors.

- z (string | number; optional):
    The z attribute defines the location along the z-axis for a light
    source in the coordinate system established by the primitiveUnits
    attribute on the <filter> element, assuming that, in the  initial
    coordinate system, the positive z-axis comes out  towards the
    person viewing the content and assuming that  one unit along the
    z-axis equals one unit in x and y.You  can use this attribute with
    the following SVG elements:For  <fePointLight>, z defines the
    location along the z-axis  for the light source in the coordinate
    system established  by the primitiveUnits attribute on the
    <filter> element.For  <feSpotLight>, z defines the location along
    the z-axis  for the light source in the coordinate system
    established  by the primitiveUnits attribute on the <filter>
    element.Last  modified: May 13, 2022, by MDN contributors."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_svg'
    _type = 'FeSpotLight'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, colorInterpolationFilters=Component.UNDEFINED, limitingConeAngle=Component.UNDEFINED, pointsAtX=Component.UNDEFINED, pointsAtY=Component.UNDEFINED, pointsAtZ=Component.UNDEFINED, specularExponent=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, z=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'colorInterpolationFilters', 'data-*', 'key', 'limitingConeAngle', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'pointsAtX', 'pointsAtY', 'pointsAtZ', 'role', 'specularExponent', 'x', 'y', 'z']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'colorInterpolationFilters', 'data-*', 'key', 'limitingConeAngle', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'pointsAtX', 'pointsAtY', 'pointsAtZ', 'role', 'specularExponent', 'x', 'y', 'z']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FeSpotLight, self).__init__(children=children, **args)
