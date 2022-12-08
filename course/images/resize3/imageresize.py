"""\
Titel: Resizen van afbeeldingen

Beschrijving: |

    Tool om grootte van afbeeldingen aan te passen en zo ook bijvoorbeeld thumbnails te maken.

"""
from os.path import dirname, basename, join, splitext

from anet.imagetools import imtools
from anet.toolcatng.toolcat import toolcat


@toolcat
def resize(args, *, modifiers=None):
    """\
    Titel: Verklein een afbeelding

    Beschrijving: |
        Herleidt de bestandsgrootte van een afbeelding onder een bepaald maximum

    Voorbeelden:
            - imageresize resize rabc.jpg maxsize=100 prefix=s

    Argumenten:
        arg*:
            betekenis:  De file(s) die geresized moeten worden
            aantal: 1..
            type: file
            leesbaar: ja

    Modifiers:
        maxsize:
            betekenis: maximale bestandsgrootte van een image
            default: '512'
            type: string
        prefix:
            betekenis: wordt geplakt vooraan de aangepaste afbeelding
            default: 'smaller'
            type: string

    """
    maxsize = modifiers('maxsize')
    prefix = modifiers('prefix')
    for image in args:
        imtools.resize(image, join(dirname(image), prefix + basename(image)), maxsize=maxsize)


@toolcat
def thumbnail(args, *, modifiers=None):
    """\
    Titel: Maak een thumbnail van een afbeelding

    Beschrijving: |
        Herleidt de afmetingen van een image tot een thumbnail.

    Voorbeelden:
            - imageresize thumbnail rabc.jpg
            - imageresize thumbnail *.jpg rounding=Rounded shadow=5 backgroundcolor=red

    Argumenten:
        arg*:
            betekenis:  De file(s) waarvan een thumbnail gemaakt moet worden
            aantal: 1..
            type: file
            leesbaar: ja

    Modifiers:
        crop:
            betekenis: enkel het centrale gedeelte van de foto wordt gebruikt voor de thumbnail
            default: false
            type: boole
        width:
            betekenis: de gewenste breedte
            default: 100
            type: integer
        height:
            betekenis: de gewenste hoogte
            default: 100
            type: integer
        suffix:
            betekenis: het nieuwe bestand zal met deze suffix eindigen
            default: 'thumb'
            type: string
        rounding:
            betekenis: |
                hoe afronden: Rounded, Square, Cross of niet
            type: string
        radius:
            betekenis: de radius van de afronding
            default: 20
            type: integer
        border:
            betekenis: breedte van de border
            default: 0
            type: integer
        bordercolor:
            betekenis: kleur van de border
            default: 'black'
            type: string
        backgroundcolor:
            betekenis: kleur van de achtergrond
            default: 'white'
            type: string
        shadow:
            betekenis: breedte van de schaduw
            default: 0
            type: integer
        canvasborder:
            betekenis: breedte van de border van het canvas
            default: 0
            type: integer

    """
    crop = modifiers('crop')
    width = modifiers('width')
    height = modifiers('height')
    suffix = modifiers('suffix')
    rounding = modifiers('rounding')
    radius = modifiers('radius')
    border = modifiers('border')
    bordercolor = modifiers('bordercolor')
    backgroundcolor = modifiers('backgroundcolor')
    shadow = modifiers('shadow')
    canvasborder = modifiers('canvasborder')
    for image in args:
        imtools.thumbnail(image, join(dirname(image), splitext(basename(image))[0] + suffix + '.jpg'), width, height, crop,
                          rounding, radius, border, bordercolor, backgroundcolor, shadow, canvasborder)
