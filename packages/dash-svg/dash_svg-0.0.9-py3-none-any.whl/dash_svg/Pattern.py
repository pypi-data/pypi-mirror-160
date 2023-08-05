# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Pattern(Component):
    """A Pattern component.
Pattern is a wrapper for the <pattern> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/pattern

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

- clip (string | number; optional):
    Deprecated: This feature is no longer recommended. Though some
    browsers might still support it, it may have already been  removed
    from the relevant web standards, may be in the  process of being
    dropped, or may only be kept for compatibility  purposes. Avoid
    using it, and update existing code if  possible; see the
    compatibility table at the bottom of  this page to guide your
    decision. Be aware that this feature  may cease to work at any
    time.The clip attribute is a  presentation attribute defining the
    visible region of  an element.This attribute has the same
    parameter values  as defined for the css clip property. Unitless
    values,  which indicate current user coordinates, are permitted
    on the coordinate values on the rect(). The value of auto  defines
    a clipping path along the bounds of the viewport  created by the
    given element.You can use this attribute  with the following SVG
    elements:Warning: This property  is deprecated. Use clip-path
    instead.The value auto defines  a clipping path along the bounds
    of the viewport created  by the given element. The value rect()
    defines a clipping  rectangle following the following syntax:
    rect(<top>,  <right>, <bottom>, <left>). The <top> and <bottom>
    values  specify offsets from the top border edge of the element
    viewport, while <right> and <left> specify offsets from  the left
    border edge of the element viewport.BCD tables  only load in the
    browser with JavaScript enabled. Enable  JavaScript to view
    data.Last modified: Jun 28, 2022, by  MDN contributors.

- clipPath (string; optional):
    The clip-path presentation attribute defines or associates a
    clipping path with the element it is related to.Note:  As a
    presentation attribute clip-path can be used as a  CSS
    property.You can use this attribute with the following  SVG
    elements:An extra information to tell how a <basic-shape>  is
    applied to an element: fill-box indicates to use the  object
    bounding box; stroke-box indicates to use the object  bounding box
    extended with the stroke; view-box indicates  to use the nearest
    SVG viewport as the reference box.Note:  For more details on the
    clip-path syntax, see the CSS  property clip-path reference
    page.BCD tables only load  in the browser with JavaScript enabled.
    Enable JavaScript  to view data.Last modified: May 13, 2022, by
    MDN contributors.

- colorInterpolation (string | number; optional):
    The color-interpolation attribute specifies the color space for
    gradient interpolations, color animations, and alpha
    compositing.Note:  For filter effects, the
    color-interpolation-filters property  controls which color space
    is used.The color-interpolation  property chooses between color
    operations occurring in  the sRGB color space or in a (light
    energy linear) linearized  RGB color space. Having chosen the
    appropriate color space,  component-wise linear interpolation is
    used.When a child  element is blended into a background, the value
    of the  color-interpolation property on the child determines the
    type of blending, not the value of the color-interpolation  on the
    parent. For gradients which make use of the href  or the
    deprecated xlink:href attribute to reference another  gradient,
    the gradient uses the property's value from  the gradient element
    which is directly referenced by the  fill or stroke property. When
    animating colors, color  interpolation is performed according to
    the value of the  color-interpolation property on the element
    being animated.Note:  As a presentation attribute,
    color-interpolation can be  used as a CSS property.You can use
    this attribute with  the following SVG elements:Indicates that the
    user agent  can choose either the sRGB or linearRGB spaces for
    color  interpolation. This option indicates that the author
    doesn't  require that color interpolation occur in a particular
    color space.Indicates that color interpolation should  occur in
    the sRGB color space.Indicates that color interpolation  should
    occur in the linearized RGB color space as described  in the sRGB
    specification.BCD tables only load in the  browser with JavaScript
    enabled. Enable JavaScript to  view data.Last modified: May 13,
    2022, by MDN contributors.

- data-* (string; optional):
    A wildcard data attribute.

- enableBackground (string | number; optional):
    Deprecated: This feature is no longer recommended. Though some
    browsers might still support it, it may have already been  removed
    from the relevant web standards, may be in the  process of being
    dropped, or may only be kept for compatibility  purposes. Avoid
    using it, and update existing code if  possible; see the
    compatibility table at the bottom of  this page to guide your
    decision. Be aware that this feature  may cease to work at any
    time.The enable-background attribute  specifies how the
    accumulation of the background image  is managed.Note: As a
    presentation attribute, enable-background  can be used as a CSS
    property.You can use this attribute  with the following SVG
    elements:If an ancestor container  element has a property value of
    enable-background: new,  then all graphics elements within the
    current container  element are rendered both onto the parent
    container element's  background image canvas and onto the target
    device.Otherwise,  there is no current background image canvas, so
    graphics  elements are only rendered onto the target device.This
    value enables the ability of children of the current container
    element to access the background image.It also indicates  that a
    new (i.e., initially transparent black) background  image canvas
    is established and that in effect all children  of the current
    container element shall be rendered into  the new background image
    canvas in addition to being rendered  onto the target device.
    The optional <x>, <y>, <width>,  and <height> parameters are
    <number> values that indicate  the subregion of the container
    element's user space where  access to the background image is
    allowed to happen. Those  values act as a clipping rectangle on
    the background image  canvas.       Negative values for <width> or
    <height>  are forbidden. If one, two, or three values are
    specified  or if neither <width> nor <height> are specified, the
    BackgroundImage and BackgroundAlpha of a filter primitive  are
    processed as if background image processing were not  enabled.
    BCD tables only load in the browser with  JavaScript enabled.
    Enable JavaScript to view data.Last  modified: May 17, 2022, by
    MDN contributors.

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

- mask (string; optional):
    The mask attribute is a presentation attribute mainly used to
    bind a given <mask> element with the element the attribute
    belongs to.Note: As a presentation attribute mask can  be used as
    a CSS property.You can use this attribute with  the following SVG
    elements:Since SVG2, the mask attribute  is defined as a css
    property and is a shorthand for many  other properties:
    mask-image, mask-mode, mask-repeat,  mask-position, mask-clip,
    mask-origin, mask-size, and  mask-composite.BCD tables only load
    in the browser with  JavaScript enabled. Enable JavaScript to view
    data.Last  modified: May 13, 2022, by MDN contributors.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- n_clicks_timestamp (number; default -1):
    An integer that represents the time (in ms since 1970) at which
    n_clicks changed. This can be used to tell which button was
    changed most recently.

- overflow (string | number; optional):
    The overflow attribute sets what to do when an element's content
    is too big to fit in its block formatting context. This  feature
    is not widely implemented yet.This attribute has  the same
    parameter values and meaning as the css overflow  property,
    however, the following additional points apply:Note:  Although the
    initial value for overflow is auto, it is  overwritten in the User
    Agent style sheet for the <svg>  element when it is not the root
    element of a stand-alone  document, the <pattern> element, and the
    <marker> element  to be hidden by default.Note: As a presentation
    attribute,  overflow can be used as a CSS property. See the CSS
    overflow  property for more information.You can use this attribute
    with the following SVG elements:For a description of the  values,
    please see the css overflow property.BCD tables  only load in the
    browser with JavaScript enabled. Enable  JavaScript to view
    data.Last modified: May 13, 2022, by  MDN contributors.

- patternContentUnits (string; optional):
    The patternContentUnits attribute indicates which coordinate
    system to use for the contents of the <pattern> element.Note:
    That this attribute has no effect if attribute viewBox  is
    specified on the <pattern> element.You can use this  attribute
    with the following SVG elements:For <pattern>,
    patternContentUnits defines the coordinate system in use  for the
    content of the element.This value indicates that  all coordinates
    inside the <pattern> element refer to  the user coordinate system
    as defined when the pattern  tile was created.This value indicates
    that all coordinates  inside the <pattern> element are relative to
    the bounding  box of the element the pattern is applied to. A
    bounding  box could be considered the same as if the content of
    the <pattern> were bound to a \"0 0 1 1\" viewbox for a  pattern
    tile of width and height of 100%.BCD tables only  load in the
    browser with JavaScript enabled. Enable JavaScript  to view
    data.Last modified: May 13, 2022, by MDN contributors.

- patternTransform (string | number; optional):
    The patternTransform attribute defines a list of transform
    definitions  that are applied to a pattern tile.You can use this
    attribute  with the following SVG elements:For <pattern>,
    patternTransform  defines a list of transform definitions that are
    applied  to a pattern tile.Note: As of SVG2, it is also allowed
    to use the CSS transform property. However, the current  state of
    implementation isn't very good. For backward  compatibility
    reason, it is highly suggested to keep using  the patternTransform
    attribute.To know more about the  definition of transform
    functions, see the transform attribute  definition.BCD tables only
    load in the browser with JavaScript  enabled. Enable JavaScript to
    view data.Last modified:  May 13, 2022, by MDN contributors.

- patternUnits (string; optional):
    The patternUnits attribute indicates which coordinate system  to
    use for the geometry properties of the <pattern> element.You  can
    use this attribute with the following SVG elements:For  <pattern>,
    patternUnits defines the coordinate system  in use for the
    geometry properties (x, y, width and height)  of the element.This
    value indicates that all coordinates  for the geometry properties
    refer to the user coordinate  system as defined when the pattern
    was applied.This value  indicates that all coordinates for the
    geometry properties  represent fractions or percentages of the
    bounding box  of the element to which the pattern is applied. A
    bounding  box could be considered the same as if the content of
    the <pattern> were bound to a \"0 0 1 1\" viewbox.BCD tables  only
    load in the browser with JavaScript enabled. Enable  JavaScript to
    view data.Last modified: May 13, 2022, by  MDN contributors.

- pointerEvents (string | number; optional):
    The pointer-events attribute is a presentation attribute that
    allows defining whether or when an element may be the  target of a
    mouse event.Note: As a presentation attribute  pointer-events can
    be used as a CSS property.You can use  this attribute with the
    following SVG elements:For a detailed  explanation of each
    possible value, have a look at the  CSS pointer-events
    documentation.BCD tables only load  in the browser with JavaScript
    enabled. Enable JavaScript  to view data.Last modified: May 13,
    2022, by MDN contributors.

- preserveAspectRatio (string; optional):
    The preserveAspectRatio attribute indicates how an element with  a
    viewBox providing a given aspect ratio must fit into  a viewport
    with a different aspect ratio.Because the aspect  ratio of an SVG
    image is defined by the viewBox attribute,  if this attribute
    isn't set, the preserveAspectRatio attribute  has no effect (with
    one exception, the <image> element,  as described below).Its value
    is made of one or two keywords:  A required alignment value and an
    optional \"meet or slice\"  reference as described below:The
    alignment value indicates  whether to force uniform scaling and,
    if so, the alignment  method to use in case the aspect ratio of
    the viewBox  doesn't match the aspect ratio of the viewport. The
    alignment  value must be one of the following keywords:The meet or
    slice reference is optional and, if provided, must be  one of the
    following keywords:You can use this attribute  with the following
    SVG elements:For <feImage>, preserveAspectRatio  defines how the
    referenced image should fit in the rectangle  define by the
    <feImage> element.For <image>, preserveAspectRatio  defines how
    the referenced image should fit in the rectangle  define by the
    <image> element.For <marker>, preserveAspectRatio  indicates if a
    uniform scaling must be performed to fit  the element viewport.For
    <pattern>, preserveAspectRatio  indicates if a uniform scaling
    must be performed to fit  the element viewport.For <svg>,
    preserveAspectRatio indicates  if a uniform scaling must be
    performed to fit the element  viewport.For <symbol>,
    preserveAspectRatio indicates if  a uniform scaling must be
    performed to fit the element  viewport.For <view>,
    preserveAspectRatio indicates if  a uniform scaling must be
    performed to fit the element  viewport.Last modified: May 13,
    2022, by MDN contributors.

- requiredFeatures (string | number; optional):
    Deprecated: This feature is no longer recommended. Though some
    browsers might still support it, it may have already been  removed
    from the relevant web standards, may be in the  process of being
    dropped, or may only be kept for compatibility  purposes. Avoid
    using it, and update existing code if  possible; see the
    compatibility table at the bottom of  this page to guide your
    decision. Be aware that this feature  may cease to work at any
    time.The requiredFeatures attribute  takes a list of feature
    strings, with the individual strings  separated by white space. It
    determines whether or not  all of the named features are supported
    by the browser;  if all of them are supported, the attribute
    evaluates  to True end the element is rendered; otherwise, the
    attribute  evaluates to False and the current element and its
    children  are skipped and thus will not be rendered. This provides
    a way to design SVG that gracefully falls back when features
    aren't available.If the attribute is not present, then  its
    implicit evaluated value is True. If a None string  or empty
    string value is given to attribute requiredFeatures,  the
    attribute is evaluate to False.requiredFeatures is  often used in
    conjunction with the <switch> element. If  requiredFeatures is
    used in other situations, it represents  a simple switch on the
    given element whether to render  the element or not.To detect
    availability of an SVG feature  from script, there is the (also
    deprecated) DOMImplementation.hasFeature()  method.You can use
    this attribute with the following SVG  elements:This is a list of
    feature strings, separated  using white space. Determines whether
    all of the named  features are supported by the browser. See
    Feature strings  below for a list of allowed values.The following
    are the  feature strings for the requiredFeatures attribute. These
    same feature strings apply to the hasFeature method call  that is
    part of the SVG DOM's support for the DOMImplementation
    interface. In some cases the feature strings map directly  to a
    set of attributes, properties or elements, in others  they
    represent some functionality of the browser. Note  that the format
    and naming for feature strings changed  from SVG 1.0 to SVG 1.1.
    The SVG 1.0 feature strings are  not listed here but can be found
    in the SVG Specification.  Some browser support SVG 1.0 Feature
    strings for compatibility  reasons. However, the SVG 1.0 feature
    strings are considered  deprecated.At least one of the following
    feature is supported:At  least one of the following feature is
    supported:The browser  supports all the following features:The
    browser supports  all of the DOM interfaces and methods that
    correspond  to the language features for
    http://www.w3.org/TR/SVG11/feature#SVG-static.The  browser
    supports all of the language features from
    http://www.w3.org/TR/SVG11/feature#SVG-static  plus the feature
    http://www.w3.org/TR/SVG11/feature#Animation.The  browser supports
    all of the DOM interfaces and methods  that correspond to the
    language features for
    http://www.w3.org/TR/SVG11/feature#SVG-animation.The  browser
    supports all of the language features from
    http://www.w3.org/TR/SVG11/feature#SVG-animation  plus the
    following features:The browser supports all of  the DOM interfaces
    and methods that correspond to the  language features for
    http://www.w3.org/TR/SVG11/feature#SVG-dynamic.The  browser
    supports the id, xml:base, xml:lang and xml:space  attributesThe
    browser supports <svg>, <g>, <defs>, <desc>,  <title>, <metadata>,
    <symbol> and <use> elements.The browser  supports <svg>, <g>,
    <defs>, <desc>, <title>, <metadata>  and <use> elements.The
    browser supports the enable-background  attributeThe browser
    supports the <switch> element, and  the requiredFeatures,
    requiredExtensions, systemLanguage  attributesThe browser supports
    the <image> element.The  browser supports the <style> element.The
    browser supports  the clip and overflow attributes.The browser
    supports  the <rect>, <circle>, <line>, <polyline>, <polygon>,
    <ellipse>  and <path> elements.The browser supports the <text>,
    <tspan>,  <tref>, <textPath>, <altGlyph>, <altGlyphDef>,
    <altGlyphItem>  and <glyphRef> elements.The browser supports the
    <text>  elementThe browser supports the color, fill, fill-rule,
    stroke, stroke-dasharray, stroke-dashoffset, stroke-linecap,
    stroke-linejoin, stroke-miterlimit, stroke-width,
    color-interpolation  and color-rendering attributesThe browser
    supports the  color, fill, fill-rule, stroke, stroke-dasharray,
    stroke-dashoffset,  stroke-linecap, stroke-linejoin,
    stroke-miterlimit, stroke-width  and color-rendering attributesThe
    browser supports the  opacity, stroke-opacity and fill-opacity
    attributesThe  browser supports the display, image-rendering,
    pointer-events,  shape-rendering, text-rendering and visibility
    attributesThe  browser supports the display and visibility
    attributesThe  browser supports the <marker> elementThe browser
    supports  the <linearGradient>, <radialGradient> and <stop>
    elementsThe  browser supports the <pattern> elementThe browser
    supports  the <clipPath> element and the clip-path, clip-rule
    attributesThe  browser supports the <clipPath> element and the
    clip-path  attributeThe browser supports the <mask> elementThe
    browser  supports the <filter>, <feBlend>, <feColorMatrix>,
    <feComponentTransfer>,  <feComposite>, <feConvolveMatrix>,
    <feDiffuseLighting>,  <feDisplacementMap>, <feFlood>,
    <feGaussianBlur>, <feImage>,  <feMerge>, <feMergeNode>,
    <feMorphology>, <feOffset>,  <feSpecularLighting>, <feTile>,
    <feDistantLight>, <fePointLight>,  <feSpotLight>, <feFuncR>,
    <feFuncG>, <feFuncB> and <feFuncA>  elementsThe browser supports
    the <filter>, <feBlend>,  <feColorMatrix>, <feComponentTransfer>,
    <feComposite>,  <feFlood>, <feGaussianBlur>, <feImage>, <feMerge>,
    <feMergeNode>,  <feOffset>, <feTile>, <feFuncR>, <feFuncG>,
    <feFuncB>  and <feFuncA> elementsThe browser supports the
    onunload,  onabort, onerror, onresize, onscroll and onzoom
    attributesThe  browser supports the onfocusin, onfocusout,
    onactivate,  onclick, onmousedown, onmouseup, onmouseover,
    onmousemove,  onmouseout and onload attributesThe browser supports
    the  onbegin, onend, onrepeat and onload attributesThe browser
    supports the <cursor> elementThe browser supports the  <a>
    elementThe browser supports the xlink:type, xlink:href,
    xlink:role, xlink:arcrole, xlink:title, xlink:show and
    xlink:actuate attributesThe browser supports the <view>
    elementThe browser supports the <script> elementThe browser
    supports the <animate>, <set>, <animateMotion>,
    <animateTransform>,  <animateColor> and <mpath> elementsThe
    browser supports  the <font>, <font-face>, <glyph>,
    <missing-glyph>, <hkern>,  <vkern>, <font-face-src>,
    <font-face-uri>, <font-face-format>  and <font-face-name>
    elementsThe browser supports the  <font>, <font-face>, <glyph>,
    <missing-glyph>, <hkern>,  <font-face-src> and <font-face-name>
    elementsThe browser  supports the <foreignObject> elementSee also
    requiredFeatures.svgBCD  tables only load in the browser with
    JavaScript enabled.  Enable JavaScript to view data.Last modified:
    May 13,  2022, by MDN contributors.

- role (string; optional):
    The ARIA role attribute.

- systemLanguage (string | number; optional):
    The systemLanguage attribute represents a list of supported
    language  tags. This list is matched against the language defined
    in the user preferences.You can use this attribute with  the
    following SVG elements:The value is a set of comma-separated
    tokens, each of which must be a language tag, as defined  in RFC
    5646: Tags for Identifying Languages (also known  as BCP
    47).systemLanguage is often used in conjunction  with the <switch>
    element. If the attribute is used in  other situations, then it
    represents a simple switch on  the given element whether to render
    the element or not.Note:  If several alternative language objects
    are enclosed in  a <switch> and none of them matches, this may
    lead to  situations where no content is displayed. It is thus
    recommended  to include a \"catch-all\" choice at the end of such
    a <switch>  which is acceptable in all cases.The attribute
    evaluates  to \"True\" if one of the language tags indicated by
    user  preferences is a case-insensitive match or prefix (followed
    by a \"-\") of one of the language tags given in the value  of
    this parameter. Otherwise it evaluates to \"False\".Note:  The
    prefix matching rule does not imply that if a user  understands a
    language with a certain tag, that the user  will also understand
    all languages with the tag as prefix.If  the attribute is not
    present, then it implicitly evaluates  to \"True\". If a None
    string or empty string value is given,  the attribute evaluates to
    \"False\".The prefix rule allows  the use of prefix tags if this
    is the case.Multiple languages  may be listed for content that is
    intended for multiple  audiences. For example, content that is
    presented simultaneously  in the original Maori and English
    versions, would call  for:However, just because multiple languages
    are present  within the object on which the systemLanguage test
    attribute  is placed, this does not mean that it is intended for
    multiple linguistic audiences. An example would be a beginner's
    language primer, such as \"A First Lesson in Latin,\" which  is
    clearly intended to be used by an English-literate  audience. In
    this case, the attribute should only include  en.BCD tables only
    load in the browser with JavaScript  enabled. Enable JavaScript to
    view data.Last modified:  May 13, 2022, by MDN contributors.

- viewBox (string; optional):
    The viewBox attribute defines the position and dimension, in  user
    space, of an SVG viewport.The value of the viewBox  attribute is a
    list of four numbers: min-x, min-y, width  and height. The
    numbers, which are separated by whitespace  and/or a comma,
    specify a rectangle in user space which  is mapped to the bounds
    of the viewport established for  the associated SVG element (not
    the browser viewport).You  can use this attribute with the
    following SVG elements:The  exact effect of this attribute is
    influenced by the preserveAspectRatio  attribute.Note: Values for
    width or height lower or equal  to 0 disable rendering of the
    element.For <marker>, viewBox  defines the position and dimension
    for the content of  the <marker> element.For <pattern>, viewBox
    defines the  position and dimension for the content of the pattern
    tile.For <svg>, viewBox defines the position and dimension  for
    the content of the <svg> element.For <symbol>, viewBox  defines
    the position and dimension for the content of  the <symbol>
    element.For <view>, viewBox defines the position  and dimension
    for the content of the <view> element.Last  modified: May 13,
    2022, by MDN contributors.

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
    _type = 'Pattern'
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, clip=Component.UNDEFINED, clipPath=Component.UNDEFINED, colorInterpolation=Component.UNDEFINED, enableBackground=Component.UNDEFINED, height=Component.UNDEFINED, mask=Component.UNDEFINED, overflow=Component.UNDEFINED, patternContentUnits=Component.UNDEFINED, patternTransform=Component.UNDEFINED, patternUnits=Component.UNDEFINED, pointerEvents=Component.UNDEFINED, preserveAspectRatio=Component.UNDEFINED, requiredFeatures=Component.UNDEFINED, systemLanguage=Component.UNDEFINED, viewBox=Component.UNDEFINED, width=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'clip', 'clipPath', 'colorInterpolation', 'data-*', 'enableBackground', 'height', 'key', 'loading_state', 'mask', 'n_clicks', 'n_clicks_timestamp', 'overflow', 'patternContentUnits', 'patternTransform', 'patternUnits', 'pointerEvents', 'preserveAspectRatio', 'requiredFeatures', 'role', 'systemLanguage', 'viewBox', 'width', 'x', 'y']
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'clip', 'clipPath', 'colorInterpolation', 'data-*', 'enableBackground', 'height', 'key', 'loading_state', 'mask', 'n_clicks', 'n_clicks_timestamp', 'overflow', 'patternContentUnits', 'patternTransform', 'patternUnits', 'pointerEvents', 'preserveAspectRatio', 'requiredFeatures', 'role', 'systemLanguage', 'viewBox', 'width', 'x', 'y']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Pattern, self).__init__(children=children, **args)
