from PIL import Image
import tempfile
import config

def genImage(date):
    '''
        Returns file object of created image
    '''

    img = Image.new('RGB', config.size)
    pix = img.load()

    for x in range(img.width):
        for y in range(img.height):
            r = int(256 * (x / img.width + y / img.height) / 2)
            pix[x, y] = (r, r, r)

    file = tempfile.TemporaryFile()
    img.save(file, 'JPEG')
    return file
