import numpy as np
import cv2


def write_png(buf, width, height):
    import zlib, struct
    width_byte_4 = width * 4
    raw_data = b"".join(\
        b'\x00' + buf[span:span + width_byte_4] for span \
        in range((height - 1) * width * 4, -1, - width_byte_4))
    def png_pack(png_tag, data):
        chunk_head = png_tag + data
        return struct.pack("!I", len(data)) + chunk_head + \
            struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
    return b"".join([
        b'\x89PNG\r\n\x1a\n',
        png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b'IDAT', zlib.compress(raw_data, 9)),
        png_pack(b'IEND', b'')])

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.cv.CV_FOURCC(*'XDIV')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

#while(cap.isOpened()):
ret, frame = cap.read()
#if ret==True:
frame = cv2.flip(frame,0)

# write the flipped frame
out.write(frame)

#cv2.imshow('frame',frame)
#if cv2.waitKey(1) & 0xFF == ord('q'):
    #break
#else:
#break

c = b''
for ll in frame:
    for l in ll:
        t = l.tolist() + [255]
        for tt in t:
            c = c.join(str(tt))
data = c
png = write_png(data, 1280, 720)
f = open('foto.png', 'w')
f.write(png)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
