#!/usr/bin/env python3
"""Impose supplied PDF label pages in four equal US Letter quarters."""
import argparse
import hashlib
import io
import math
from pathlib import Path

from PIL import ImageChops
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import ContentStream, DictionaryObject, NameObject
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

SAFE_OPS = {b'q', b'Q', b'cm', b're', b'W', b'W*', b'n', b'gs', b'RG',
            b'rg', b'G', b'g', b'K', b'k', b'BDC', b'BMC', b'EMC'}


def image_draws(stream, resources, reader, depth=0):
    if depth > 10:
        raise ValueError('Nested PDF forms exceed supported depth; use page mode.')
    count = 0
    white = False
    stack = []
    for args, op in ContentStream(stream, reader).operations:
        if op == b'q':
            stack.append(white)
        elif op == b'Q':
            white = stack.pop()
        elif op == b'rg':
            white = list(args) == [1, 1, 1]
        elif op == b'g':
            white = list(args) == [1]
        elif op in (b'f', b'f*') and white and count == 0:
            pass  # A white background before the label image.
        elif op == b'Do':
            obj = resources['/XObject'][args[0]].get_object()
            if obj['/Subtype'] == '/Image':
                count += 1
            elif obj['/Subtype'] == '/Form':
                count += image_draws(obj, obj.get('/Resources', resources), reader, depth + 1)
            else:
                raise ValueError('Unsupported drawing object; use page mode.')
        elif op not in SAFE_OPS:
            raise ValueError(f'Non-image drawing operation {op!r}; use page mode.')
    return count


def extract_label(page, reader):
    if page.rotation or page.get('/Annots'):
        raise ValueError('Rotated or annotated page; use page mode.')
    if image_draws(page.get_contents(), page['/Resources'], reader) != 1 or len(page.images) != 1:
        raise ValueError('Image mode requires exactly one image drawn once per page.')
    im = page.images[0].image.convert('RGB')
    bbox = ImageChops.invert(im.convert('L')).getbbox()
    if bbox is None:
        raise ValueError('Blank label image.')
    # Keep horizontal quiet zones; never threshold away faint source content.
    return im.crop((0, bbox[1], im.width, bbox[3]))


def digest(im):
    im = im.convert('RGB')
    return (im.size, hashlib.sha256(im.tobytes()).hexdigest())


def placement(index, width, height):
    if width <= 0 or height <= 0:
        raise ValueError('Invalid source dimensions.')
    row, col = divmod(index % 4, 2)
    scale = min(288 / width, 378 / height)
    dw, dh = width * scale, height * scale
    x, y = col * 306 + (306 - dw) / 2, (1 - row) * 396 + (396 - dh) / 2
    assert x >= col * 306 + 9 - 1e-6 and x + dw <= (col + 1) * 306 - 9 + 1e-6
    assert y >= (1 - row) * 396 + 9 - 1e-6 and y + dh <= (2 - row) * 396 - 9 + 1e-6
    return scale, x, y, dw, dh


def build(args):
    output = args.output.expanduser().resolve()
    if output.exists():
        raise ValueError(f'Output already exists: {output}')
    readers = [PdfReader(p.expanduser()) for p in args.inputs]
    pages = [(r, p) for r in readers for p in r.pages]
    if not pages:
        raise ValueError('No label pages found.')
    if args.single_sheet and len(pages) > 4:
        raise ValueError(f'{len(pages)} labels cannot fit on one four-up sheet.')
    buffer = io.BytesIO()
    writer = PdfWriter()
    expected = {}
    for i, (reader, page) in enumerate(pages):
        if i % 4 == 0:
            dest = writer.add_blank_page(width=612, height=792)
        im = None
        if args.mode != 'page':
            try:
                im = extract_label(page, reader)
            except ValueError as exc:
                if args.mode == 'image':
                    raise
                print(f'Label {i + 1}: preserving full PDF page ({exc})')
        if im is not None:
            layer = io.BytesIO()
            c = canvas.Canvas(layer, pagesize=(612, 792), pageCompression=1)
            _, x, y, dw, dh = placement(i, *im.size)
            c.drawImage(ImageReader(im), x, y, width=dw, height=dh)
            c.showPage()
            c.save()
            dest.merge_page(PdfReader(layer).pages[0])
            expected.setdefault(i // 4, set()).add(digest(im))
        else:
            if page.get('/Annots'):
                raise ValueError('Annotated label requires visual flattening before imposition.')
            page.transfer_rotation_to_content()
            box = page.cropbox
            scale, x, y, _, _ = placement(i, float(box.width), float(box.height))
            transform = Transformation().translate(-float(box.left), -float(box.bottom)).scale(scale).translate(x, y)
            dest.merge_transformed_page(page, transform, expand=False)
    writer.add_metadata({'/Title': 'Shipping Labels - Letter 4-Up'})
    writer._root_object[NameObject('/ViewerPreferences')] = DictionaryObject({NameObject('/PrintScaling'): NameObject('/None')})
    writer.write(buffer)
    result = PdfReader(buffer)
    assert len(result.pages) == math.ceil(len(pages) / 4)
    assert all(list(p.mediabox) == [0, 0, 612, 792] for p in result.pages)
    for i, hashes in expected.items():
        actual = {digest(im.image) for im in result.pages[i].images}
        assert hashes <= actual, 'Embedded pixel mismatch'
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('xb') as f:
        f.write(buffer.getvalue())
    print(f'Created {output}: {len(pages)} labels on {len(result.pages)} Letter sheet(s).')
    print('Print: US Letter, portrait, Actual Size / 100%, one page per sheet.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--mode', choices=('auto', 'page', 'image'), default='auto')
    parser.add_argument('--single-sheet', action='store_true')
    args = parser.parse_args()
    try:
        build(args)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
