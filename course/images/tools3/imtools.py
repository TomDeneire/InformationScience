from functools import reduce
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, UnidentifiedImageError
from PIL.Image import Image as ImageType
from re import sub
from typing import Union, Optional, Tuple

from anet.core.base import copy, FilePath
from anet.core.fs import size

CROSS = 'Cross'
ROUNDED = 'Rounded'

CORNER_ID = 'rounded_corner_r%d_f%d'
CROSS_POS = (CROSS, CROSS, CROSS, CROSS)
ROUNDED_POS = (ROUNDED, ROUNDED, ROUNDED, ROUNDED)
ROUNDED_RECTANGLE_ID = 'rounded_rectangle_r%d_f%d_s%s_p%s'


class CanNotOpenImage(UnidentifiedImageError):
    pass


def has_transparency(image: ImageType) -> bool:
    """Checks if the image has transparency.
    The image has an alpha band or a P mode with transparency.

    :param image: the image to check
    :type image: PIL image object
    :returns: True or False
    :rtype: boolean
    """
    return (image.mode == 'P' and 'transparency' in image.info) or has_alpha(image)


def has_alpha(image: ImageType) -> bool:
    """Checks if the image has an alpha band.
    i.e. the image mode is either RGBA or LA.
    The transparency in the P mode doesn't count as an alpha band

    :param image: the image to check
    :type image: PIL image object
    :returns: True or False
    :rtype: boolean
    """
    return image.mode.endswith('A')


def get_alpha(image: ImageType) -> ImageType:
    """Gets the image alpha band. Can handles P mode images with transpareny.
    Returns a band with all values set to 255 if no alpha band exists.

    :param image: input image
    :type image: PIL image object
    :returns: alpha as a band
    :rtype: single band image object
    """
    if has_alpha(image):
        return image.split()[-1]
    if image.mode == 'P' and 'transparency' in image.info:
        return image.convert('RGBA').split()[-1]
    # No alpha layer, create one.
    return Image.new('L', image.size, 255)


def remove_alpha(image: ImageType) -> ImageType:
    """Returns a copy of the image after removing the alpha band or
    transparency
    :param image: input image
    :type image: PIL image object
    :returns: the input image after removing the alpha band or transparency
    :rtype: PIL image object
    """
    if image.mode == 'RGBA':
        return image.convert('RGB')
    if image.mode == 'LA':
        return image.convert('L')
    if image.mode == 'P' and 'transparency' in image.info:
        img = image.convert('RGB')
        del img.info['transparency']
        return img
    return image


def paste(destination: ImageType, source: ImageType, box: Tuple[int, ...] = (0, 0), mask: Optional[ImageType] = None,
          force: bool = False):
    """Pastes the source image into the destination image while using an
    alpha channel if available.

    :param destination: destination image
    :type destination:  PIL image object
    :param source: source image
    :type source: PIL image object
    :param box:

        The box argument is either a 2-tuple giving the upper left corner,
        a 4-tuple defining the left, upper, right, and lower pixel coordinate,
        or None (same as (0, 0)). If a 4-tuple is given, the size of the
        pasted image must match the size of the region.

    :type box: tuple
    :param mask: mask or None

    :type mask: bool or PIL image object
    :param force:

        With mask: Force the invert alpha paste or not.

        Without mask:

        - If ``True`` it will overwrite the alpha channel of the destination
          with the alpha channel of the source image. So in that case the
          pixels of the destination layer will be abandonned and replaced
          by exactly the same pictures of the destination image. This is mostly
          what you need if you paste on a transparant canvas.
        - If ``False`` this will use a mask when the image has an alpha
          channel. In this case pixels of the destination image will appear
          through where the source image is transparent.

    :type force: bool
    """
    # Paste on top
    if mask and source == mask:
        if has_alpha(source):
            # invert_alpha = the transparant pixels of the destination
            if has_alpha(destination) and (destination.size == source.size or force):
                invert_alpha = ImageOps.invert(get_alpha(destination))
                if invert_alpha.size != source.size:
                    # if sizes are not the same be careful!
                    # check the results visually
                    if len(box) == 2:
                        w, h = source.size
                        box = (box[0], box[1], box[0] + w, box[1] + h)
                    invert_alpha = invert_alpha.crop(box)
            else:
                invert_alpha = None
            # we don't want composite of the two alpha channels
            source_without_alpha = remove_alpha(source)
            # paste on top of the opaque destination pixels
            destination.paste(source_without_alpha, box, source)
            if invert_alpha is not None:
                # the alpha channel is ok now, so save it
                destination_alpha = get_alpha(destination)
                # paste on top of the transparant destination pixels
                # the transparant pixels of the destination should
                # be filled with the color information from the source
                destination.paste(source_without_alpha, box, invert_alpha)
                # restore the correct alpha channel
                destination.putalpha(destination_alpha)
        else:
            destination.paste(source, box)
    elif mask:
        destination.paste(source, box, mask)
    else:
        destination.paste(source, box)
        if force and has_alpha(source):
            destination_alpha = get_alpha(destination)
            source_alpha = get_alpha(source)
            destination_alpha.paste(source_alpha, box)
            destination.putalpha(destination_alpha)


def resize(source: FilePath, target: FilePath, maxsize: Union[str, int] = "1000K", dpi: Optional[str] = None) -> None:
    if isinstance(maxsize, str):
        maxsize = maxsize.upper()
        maxsize = sub(r'[^1234567890MKG]', '', maxsize)
        if 'K' in maxsize:
            m = 1024
        elif 'M' in maxsize:
            m = 1024 * 1024
        elif 'G' in maxsize:
            m = 1024 * 1024 * 1024
        else:
            m = 1
        maxsize = int(sub(r'[^1234567890]', '', maxsize)) * m
    copy(source, target)
    if size(target) < maxsize:
        return
    fail = 95 * 2  # The image quality, on a scale from 1 (worst) to 95 (best)
    success = 0
    im = None
    while size(target) > maxsize:
        quality = (fail + success) // 2
        if quality < 1:
            break
        if quality <= success:
            break
        if quality >= fail:
            break
        if not im:
            im = Image.open(source)
            im = imageTransposeExif(im)
        if dpi:
            im.save(target, quality=quality, dpi=(int(dpi), int(dpi)))
        else:
            im.save(target, quality=quality)
        if size(target) <= maxsize:
            success = quality
        else:
            fail = quality


def round_image(image: ImageType, cache: Optional[dict] = None, round_all: bool = True, rounding_type: str = ROUNDED,
                radius: int = 100, opacity: int = 255, pos: Tuple[str, ...] = ROUNDED_POS,
                back_color: str = '#FFFFFF'):
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    if round_all:
        pos = 4 * (rounding_type,)

    mask = create_rounded_rectangle(image.size, cache, radius, opacity, pos)

    paste(image, Image.new('RGB', image.size, back_color), (0, 0), ImageChops.invert(mask))
    image.putalpha(mask)
    return image


def create_rounded_rectangle(size: Tuple[int, int] = (600, 400), cache: Optional[dict] = None, radius=100, opacity=255,
                             pos: Tuple[str, ...] = ROUNDED_POS):
    im_x, im_y = size
    cache = cache or {}
    rounded_rectangle_id = ROUNDED_RECTANGLE_ID % (radius, opacity, size, pos)
    if rounded_rectangle_id in cache:
        return cache[rounded_rectangle_id]
    else:
        # cross
        cross_id = ROUNDED_RECTANGLE_ID % (radius, opacity, size, CROSS_POS)
        if cross_id in cache:
            cross = cache[cross_id]
        else:
            cross = cache[cross_id] = Image.new('L', size, 0)
            draw = ImageDraw.Draw(cross)
            draw.rectangle((radius, 0, im_x - radius, im_y), fill=opacity)
            draw.rectangle((0, radius, im_x, im_y - radius), fill=opacity)
        if pos == CROSS_POS:
            return cross
        # corner
        corner_id = CORNER_ID % (radius, opacity)
        if corner_id in cache:
            corner = cache[corner_id]
        else:
            corner = cache[corner_id] = create_corner(radius, opacity)
        # rounded rectangle
        rectangle = Image.new('L', (radius, radius), 255)
        rounded_rectangle = cross.copy()
        for index, angle in enumerate(pos):
            if angle == CROSS:
                continue
            if angle == ROUNDED:
                element = corner
            else:
                element = rectangle
            if index % 2:
                x = im_x - radius
                element = element.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                x = 0
            if index < 2:
                y = 0
            else:
                y = im_y - radius
                element = element.transpose(Image.FLIP_TOP_BOTTOM)
            paste(rounded_rectangle, element, (x, y))
        cache[rounded_rectangle_id] = rounded_rectangle
        return rounded_rectangle


def create_corner(radius: int = 100, opacity: int = 255, factor: int = 2) -> ImageType:
    corner = Image.new('L', (factor * radius, factor * radius), 0)
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, 2 * factor * radius, 2 * factor * radius),
                  180, 270, fill=opacity)
    corner = corner.resize((radius, radius), Image.ANTIALIAS)
    return corner


def border_image(image: ImageType, border_width: int = 0, border_color: int = 0, opacity: int = 100) -> ImageType:
    # set up sizes, and make the target img
    left, right, top, bottom = (border_width,) * 4

    # new image size attributes could get really messed up by negatives...
    new_width = sum([x for x in [image.size[0], left, right] if x >= 0])
    new_height = sum([x for x in [image.size[1], top, bottom] if x >= 0])

    # only need to do conversions when preserving transparency, or when
    # dealing with transparent overlays
    negative = [x for x in [left, right, top, bottom] if x < 0]
    if (negative and (opacity < 100)) or has_transparency(image):
        new_image = Image.new('RGBA', (new_width, new_height), border_color)
    else:
        new_image = Image.new('RGB', (new_width, new_height), border_color)

    # now for the masking component. The size of the mask needs to be the size
    # of the original image, and totally opaque. then we will have draw in
    # negative border values with an opacity scaled appropriately.
    # NOTE: the technique here is that rotating the image allows me to do
    # this with one simple draw operation, no need to add and subtract and
    # otherwise introduce geometry errors
    if negative:
        # draw transparent overlays
        mask = Image.new('L', image.size, 255)
        drawcolor = int(255 - (opacity / 100.0 * 255))
        for val in left, top, right, bottom:
            if val < 0:
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rectangle((0, 0, abs(val), max(mask.size)),
                                    drawcolor)
                del mask_draw
            mask = mask.rotate(90)
    else:
        mask = None

    # negative paste position values mess with the result.
    left = max(left, 0)
    top = max(top, 0)
    paste(new_image, image, (left, top), mask)

    return new_image


def drop_shadow_image(image: ImageType, horizontal_offset: int = 5, vertical_offset: int = 5,
                      background_color: str = '(255, 255, 255, 0)', shadow_color: str = '#444444', border=8,
                      shadow_blur: int = 3, force_background_color=True, cache=None) -> ImageType:
    """Add a gaussian blur drop shadow to an image.

    :param image: The image to overlay on top of the shadow.
    :param type: PIL Image

    :param background_color: Background color behind the image.
    :param shadow_color: Shadow color (darkness).
    :param border:

        Width of the border around the image.  This must be wide
        enough to account for the blurring of the shadow.

    :param shadow_blur:

        Number of times to apply the filter.  More shadow_blur
        produce a more blurred shadow, but increase processing time.
    """
    if cache is None:
        cache = {}

    if has_transparency(image) and image.mode != 'RGBA':
        # Make sure 'LA' and 'P' with trasparency are handled
        image = image.convert('RGBA')

    # get info
    size = image.size
    mode = image.mode

    back = None

    # assert image is RGBA
    if mode != 'RGBA':
        if mode != 'RGB':
            image = image.convert('RGB')
            mode = 'RGB'
        # create cache id
        id = ''.join([str(x) for x in ['shadow_', size,
                                       horizontal_offset, vertical_offset, border, shadow_blur,
                                       background_color, shadow_color]])

        # look up in cache
        if id in cache:
            # retrieve from cache
            back, back_size = cache[id]

    if back is None:
        # size of backdrop
        back_size = (size[0] + abs(horizontal_offset) + 2 * border,
                     size[1] + abs(vertical_offset) + 2 * border)

        # create shadow mask
        if mode == 'RGBA':
            image_mask = get_alpha(image)
            shadow = Image.new('L', back_size, 0)
        else:
            image_mask = Image.new(mode, size, shadow_color)
            shadow = Image.new(mode, back_size, background_color)

        shadow_left = border + max(horizontal_offset, 0)
        shadow_top = border + max(vertical_offset, 0)
        paste(shadow, image_mask, (shadow_left, shadow_top,
                                   shadow_left + size[0], shadow_top + size[1]))
        del image_mask  # free up memory

        # blur shadow mask

        # Apply the filter to blur the edges of the shadow.  Since a small
        # kernel is used, the filter must be applied repeatedly to get a decent
        # blur.
        n = 0
        while n < shadow_blur:
            shadow = shadow.filter(ImageFilter.BLUR)
            n += 1

        # create back
        if mode == 'RGBA':
            back = Image.new('RGBA', back_size, shadow_color)
            back.putalpha(shadow)
            del shadow  # free up memory
        else:
            back = shadow
            cache[id] = back, back_size

    # Paste the input image onto the shadow backdrop
    image_left = border - min(horizontal_offset, 0)
    image_top = border - min(vertical_offset, 0)
    if mode == 'RGBA':
        paste(back, image, (image_left, image_top), image)
        if force_background_color:
            mask = get_alpha(back)
            paste(back, Image.new('RGB', back.size, background_color),
                  (0, 0), ImageChops.invert(mask))
            back.putalpha(mask)
    else:
        paste(back, image, (image_left, image_top))

    return back


def thumbnail(source: FilePath, target: FilePath, width: int, height: int, crop: bool = False,
              rounding_type: Optional[str] = None, radius: int = 20, border_width: int = 0, border_color: int = 0,
              thumb_background: str = 'white', drop_shadow_width: int = 0, canvas_border_width: int = 0,
              embed: bool = False):
    if not source:
        return
    try:
        img = Image.open(source)
    except UnidentifiedImageError:
        raise CanNotOpenImage
    img = imageTransposeExif(img)

    if img.mode not in ('L', 'RGB'):
        img = img.convert('RGB')

    if width == 0 and height == 0:
        raise ValueError("Breedte en hoogte kunnen niet beiden nul zijn")

    width = width or ((height * img.size[0]) // img.size[1])
    height = height or ((width * img.size[1]) // img.size[0])

    # calculate the cropping box and get the cropped part
    if crop:
        x1 = y1 = 0
        x2, y2 = img.size
        wRatio = 1.0 * x2 / width
        hRatio = 1.0 * y2 / height
        if hRatio > wRatio:
            y1 = int(y2 / 2 - height * wRatio / 2)
            y2 = int(y2 / 2 + height * wRatio / 2)
        else:
            x1 = int(x2 / 2 - width * hRatio / 2)
            x2 = int(x2 / 2 + width * hRatio / 2)
        img = img.crop((x1, y1, x2, y2))
    # Round corners
    if rounding_type:
        img = round_image(img, rounding_type=rounding_type, radius=radius, back_color=thumb_background)
    # Border
    if border_width > 0:
        img = border_image(img, border_width=border_width, border_color=border_color)
    # Shadow
    if drop_shadow_width > 0:
        img = drop_shadow_image(img, border=drop_shadow_width, background_color=thumb_background)
    # Resize the image with best quality algorithm LANCZOS
    img.thumbnail((width, height), Image.LANCZOS)
    # Paste the image on top of the background
    if embed:
        background = Image.new('RGB', (width, height), thumb_background)
        w, h = img.size
        W, H = background.size
        x = (W - w) // 2
        y = (H - h) // 2
        paste(background, img, (x, y))
        if canvas_border_width > 0:
            background = ImageOps.expand(background, border=canvas_border_width, fill='black')
        img = background.copy()
    # save
    if has_alpha(img):
        # jpeg can not handle transparency
        img = img.convert('RGB')
    img.save(target, 'jpeg')


def imageTransposeExif(im: ImageType) -> ImageType:
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.

    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.

    Parameters
    ----------
    im: PIL.Image
       The image to be rotated.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [  # Val  0th row  0th col
        [],  # 0    (reserved)
        [],  # 1   top      left
        [Image.FLIP_LEFT_RIGHT],  # 2   top      right
        [Image.ROTATE_180],  # 3   bottom   right
        [Image.FLIP_TOP_BOTTOM],  # 4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  # 5   left     top
        [Image.ROTATE_270],  # 6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  # 7   right    bottom
        [Image.ROTATE_90],  # 8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[im._getexif()[exif_orientation_tag]]
    except Exception:
        return im
    else:
        return reduce(type(im).transpose, seq, im)
