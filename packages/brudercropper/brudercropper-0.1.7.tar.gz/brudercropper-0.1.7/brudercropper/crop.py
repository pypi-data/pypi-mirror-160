#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from abc import ABC, abstractmethod

import barcode
import cv2
import pytesseract
from PIL import Image
from barcode.writer import ImageWriter
from pylibdmtx import pylibdmtx
import re


class Barcode:
    @staticmethod
    def decode(im):
        image = im
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filename = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names())+".png")
        cv2.imwrite(filename, gray)

        text = pytesseract.image_to_string(Image.open(filename).rotate(270, expand=True))
        os.remove(filename)
        #print("{fn} = ".format(fn=filename) + text)
        return text

    @staticmethod
    def createbarcode(image):
        tlcnfn = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()) + ".png")
        image.save(tlcnfn)

        text = Barcode.decode(cv2.imread(tlcnfn))
        escaped_barcode = re.sub(r"\s", "", text)
        number_barcode = re.sub(r"\D", "", escaped_barcode)
        itf = barcode.get_barcode_class('itf')
        bc = itf(number_barcode, writer=ImageWriter())

        outf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names())+".png")

        with open(outf, "wb") as f:
            bc.write(f, text=escaped_barcode, options={
                "module_width": 0.22,
                "module_height": 24.0,
                "font_size": 13
            })

        return Image.open(outf)

    @staticmethod
    def create_datamatrix(image):
        dm_tmp = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()) + ".png")
        image.save(dm_tmp)
        tmp_img = cv2.imread(dm_tmp)
        data_matrix = pylibdmtx.decode(tmp_img, timeout=100, max_count=1, corrections=3)

        encoded = pylibdmtx.encode(data_matrix[0].data, size="48x48")
        resized_matrix = Image.frombytes("RGB", (encoded.width, encoded.height), encoded.pixels)
        return resized_matrix

GSPATH = None
separator = ";" if ";" in os.getenv("PATH") else ":"
for i in os.getenv("PATH").split(separator):
    cp = os.path.join(i, "gswin32c.exe")
    if os.path.exists(cp):
        GSPATH = cp
        break

    cp = os.path.join(i, "gs")
    if os.path.exists(cp):
        GSPATH = cp
        break

if GSPATH is None:
    print("gs / gswin32c not in path")
    sys.exit(1)


class Section:
    xpos = 0.0
    ypos = 0.0

    xwidth = 0.0
    yheight = 0.0

    xbox = 0.0
    ybox = 0.0

    data = None

    def __init__(self, xpos, ypos, xwidth=None, yheight=None, xbox=None, ybox=None, margin=0):
        self.xpos = xpos
        self.ypos = ypos
        self.xwidth = xwidth
        self.yheight = yheight
        self.margin = margin

        if xbox:
            self.xbox = xbox
        else:
            self.xbox = self.xpos + self.xwidth

        if ybox:
            self.ybox = ybox
        else:
            self.ybox = self.ypos + self.yheight


class Crop(ABC):
    infile = ""
    sections = []
    srcimg = None
    logofile = None

    def __init__(self, infile, outfile):
        self.infile = self.pdf2tif(infile)
        self.outfile = outfile

        self.srcimg = Image.open(self.infile)
        self.dpi = self.srcimg.info['dpi']

    @staticmethod
    def mmtopixels(mm, resolution):
        return round(mm/254*resolution)

    @staticmethod
    def pixelstomm(pixels, resolution):
        return round(pixels/resolution*254)

    def addsection(self, xoff, yoff, xwidth, yheight):
        s = Section(xoff, yoff, xwidth, yheight)
        self.sections.append(s)

    def cut(self):
        for key,val in self.sections.items():
            c = val["section"]

            cropped = self.srcimg.crop((c.xpos, c.ypos, c.xbox, c.ybox))
            cropped.load()
            val["imageData"] = cropped

    def pdf2tif(self, fp):
        outf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))
        inf = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))

        shutil.copy(fp, inf)

        tpl = "\"{gs}\" -q -dNOPAUSE -sDEVICE=tiffg4 -sOutputFile={out} {inf} -c quit".format(gs=GSPATH, out=outf, inf=inf)
        proc = subprocess.run(tpl, shell=True)

        if proc.returncode != 0:
            print("Error converting {inf} to TIFF. Error:\n\n{stdout}\n{stderr}".format(inf=self.infile,
                                                                                        stdout=proc.stdout,
                                                                                        stderr=proc.stderr))
            sys.exit(1)

        os.remove(inf)

        return outf

    @abstractmethod
    def save(self):
        pass


class DHL(Crop):
    def __init__(self, infile, outfile):
        super(DHL, self).__init__(infile, outfile)

        # edit here
        self.xofs = 0
        self.yofs = 0
        self.sections = {
            "strichSimple": {
                "section": Section(
                    xpos=599,
                    ypos=191,
                    xwidth=3,
                    yheight=765
                )
            },
            "strichFat": {
                "section": Section(
                    xpos=1295,
                    ypos=191,
                    xwidth=13,
                    yheight=765
                )
            },
            "paketNameLogo": {"section": Section(xpos=59,
                                                 ypos=192,
                                                 xwidth=80,
                                                 yheight=766)
                          },
            "securityCode": {
                "section": Section(
                    xpos=150,
                    ypos=208,
                    xwidth=215,
                    yheight=206
                )
            },
            "securityCodeText": {
                "section": Section(
                    xpos=173,
                    ypos=186,
                    xwidth=132,
                    yheight=16
                )
            },
            "senderName": {
                "section": Section(
                    xpos=145,
                    ypos=420,
                    xwidth=143,
                    yheight=536
                )
            },
            "recipientName": {
                "section": Section(
                    xpos=287,
                    ypos=420,
                    xwidth=305,
                    yheight=537
                )
            },

            "trackingNo": {
                "section": Section(
                    xpos=664,
                    ypos=191,
                    xwidth=101,
                    yheight=765
                )
            },

            "goGreen": {
                "section": Section(
                    xpos=602,
                    ypos=191,
                    xwidth=59,
                    yheight=765
                )
            },

            "routingCode": {
                "section": Section(
                    xpos=1009,
                    ypos=191,
                    xwidth=283,
                    yheight=765
                )
            },
            "routingCodeNumber": {
                "section": Section(
                    xpos=1264,
                    ypos=470,
                    xwidth=27,
                    yheight=208
                )
            },
            "identCode": {
                "section": Section(
                    xpos=1308,
                    ypos=191,
                    xwidth=280,
                    yheight=765
                )
            },
            "identCodeNumber": {
                "section": Section(
                    xpos=1559,
                    ypos=488,
                    xwidth=24,
                    yheight=174
                )
            }
        }

    def save(self):
        resolution_dpi = 300

        width_mm = 170*10
        height_mm = 62*10

        width_pixels = Crop.mmtopixels(width_mm, resolution_dpi)
        height_pixels = Crop.mmtopixels(height_mm, resolution_dpi)
        timg = Image.new("RGB", (width_pixels, height_pixels), (255,255,255))

        def paste_image(section, rotate=270, x=20, y=-1, margin=10, scaleFact=0):
            if y == -1:
                y = self.yofs
            source_img = section["imageData"].rotate(rotate, expand=True)

            # resize to height_pixels
            if scaleFact:
                img = source_img.resize((int(source_img.width*scaleFact), int(source_img.height*scaleFact)))
            else:
                img = source_img

            timg.paste(img, (x, y))
            self.yofs = self.yofs + img.height + margin
            #self.xofs = self.xofs + img.width

        strich_simple = self.sections["strichSimple"]
        strich_fat = self.sections["strichFat"]

        # first column
        paket_name_logo = self.sections["paketNameLogo"]
        paste_image(paket_name_logo)
        paste_image(strich_simple)

        sender_name = self.sections["senderName"]
        paste_image(sender_name)

        recipient_name = self.sections["recipientName"]
        paste_image(recipient_name)
        paste_image(strich_simple)

        tracking_no = self.sections["trackingNo"]
        paste_image(tracking_no)
        paste_image(strich_simple)

        # second column
        paste_image(strich_simple, rotate=0, x=strich_simple["imageData"].height+20, y=0)

        security_code = self.sections["securityCode"]
        security_matrix = Barcode.create_datamatrix(security_code["imageData"])
        paste_image({"imageData": security_matrix}, x=strich_simple["imageData"].height + 50, y=175, scaleFact=1.3, rotate=0)

        security_code_text = self.sections["securityCodeText"]
        paste_image(security_code_text, x=strich_simple["imageData"].height + 380, y=250, scaleFact=1.5, rotate=270)

        paste_image(strich_simple, rotate=0, x=1190, y=0)

        # third column
        routing_code_number = self.sections["routingCodeNumber"]
        routing_code_barcode = Barcode.createbarcode(routing_code_number["imageData"])
        paste_image({"imageData": routing_code_barcode}, x=1250, y=0, rotate=0, scaleFact=0.9)
        paste_image(strich_fat, rotate=90, x=1220, y=330)

        ident_code_number = self.sections["identCodeNumber"]
        ident_code_barcode = Barcode.createbarcode(ident_code_number["imageData"])
        paste_image({"imageData": ident_code_barcode}, x=1300, y=350, rotate=0, scaleFact=0.9)
        paste_image(strich_fat, rotate=90, x=1220, y=700)

        timg.save(self.outfile, dpi=(300, 300))
        print(f"Saved to {self.outfile}")
        # sys.exit(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dhl", help="Cropped ein DHL A4 Etikett auf 62mm", action='store_true', required=False)
    parser.add_argument("-i", "--input", help="Inputfile", required=True)
    parser.add_argument("-o", "--output", help="Output file", required=False, default="result.png")
    args = parser.parse_args()

    if args.dhl:
        d = DHL(args.input, args.output)
        d.cut()
        d.save()


if __name__ == "__main__":
    main()