#!/usr/bin/env python
# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.graphics import Fbo
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.graphics import Rectangle, Color


class Tabla(Widget):
    fboo = ObjectProperty(None)
    button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Tabla, self).__init__(**kwargs)
        self.canvas.clear()
        with self.canvas:
            self.f = Fbo(size=(4,4))
            Rectangle(size=(300,300), pos=(0,0), texture=self.f.texture)
        with self.f:
            Color(.5, .3, .2, 1)
            Rectangle(size=(2,4), pos=(2,0))
            Color(1, 0, 0, 1)
            Rectangle(size=(2,4), pos=(0,0))
            Color(.4, 1, 0, 1)
            Rectangle(size=(4,2), pos=(0,2))
            Color(1, 1, 1, 1)
        self.f.texture.mag_filter = 'nearest'

    def llorar(self):
        print('El boton es: %s' % (self.button))
        print('el array es: %s' % (len(self.f.pixels)))
        b = self.write_png(self.f.pixels, 4, 4)
        print(b)
        f = open('a.png', 'w')
        f.write(b)
        
    def write_png(self, buf, width, height):
        import zlib, struct
        width_byte_4 = width * 4
        raw_data = b"".join(\
            b'\x00' + buf[span:span + width_byte_4] for span \
            in range((height - 1) * width * 4, -1, - width_byte_4))
        def png_pack(png_tag, data):
            chunk_head = png_tag + data
            return struct.pack("!I", len(data)) + chunk_head + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
        return b"".join([
            b'\x89PNG\r\n\x1a\n',
            png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
            png_pack(b'IDAT', zlib.compress(raw_data, 9)),
            png_pack(b'IEND', b'')])


class VentanaApp(App):
    def __init(self, **kwargs):
        super(VentanaApp, self).__init__(**kwargs)


if __name__ == '__main__':
    kivy.require('1.9.0')
    VentanaApp().run()
