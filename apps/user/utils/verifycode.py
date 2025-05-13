import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def verify_code(width=150, height=40, char_length=5, font_file='BuxtonSketch.ttf', font_size=28):
    # 定义空列表来存放验证码
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    # 画笔
    draw = ImageDraw.Draw(img, mode='RGB')

    def randChar():
        """生成随机字母"""
        return chr(random.randint(65, 90))

    def randColor():
        """生成随机颜色"""
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = randChar()
        code.append(char)  # 把生成的随机字母添加到列表中
        h = random.randint(0, 4)
        draw.text((i * width / char_length, h), char, font=font, fill=randColor())
    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=randColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=randColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=randColor())

    # 化干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=randColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)
