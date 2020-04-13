#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import os
import re
import face_recognition.api as face_recognition
import multiprocessing
import sys
import itertools
from PIL import Image, ImageFilter
import uuid


def print_result(filename, location):
    top, right, bottom, left = location
    print("{},{},{},{},{}".format(filename, top, right, bottom, left))


def test_image(image_to_check, model):
    unknown_image = face_recognition.load_image_file(image_to_check)
    face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model=model)

    i = 0
    for face_location in face_locations:
        print_result(image_to_check, face_location)
        try:
            with Image.open(image_to_check) as im:
                box = face_location
                region = im.crop(box)
                fname = "/tmp/test_image_" + str(i) + ".jpeg"
                print("Printing: {}".format(fname))
                im.save(fname, "JPEG")
                i = i + 1
        except IOError:
            print("IOError")


def image_files_in_folder(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)]

def process_images_in_process_pool(images_to_check, number_of_cpus, model):
    if number_of_cpus == -1:
        processes = None
    else:
        processes = number_of_cpus

    # macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
    context = multiprocessing
    if "forkserver" in multiprocessing.get_all_start_methods():
        context = multiprocessing.get_context("forkserver")

    pool = context.Pool(processes=processes)

    function_parameters = zip(
        images_to_check,
        itertools.repeat(model),
    )

    pool.starmap(test_image, function_parameters)


@click.command()
@click.argument('image_to_check')
@click.option('--cpus', default=1, help='number of CPU cores to use in parallel. -1 means "use all in system"')
@click.option('--model', default="hog", help='Which face detection model to use. Options are "hog" or "cnn".')
def main(image_to_check, cpus, model):
    for img_file in image_files_in_folder(image_to_check):
        unknown_image = face_recognition.load_image_file(img_file)
        face_locations = face_recognition.face_locations(unknown_image, number_of_times_to_upsample=0, model=model)

        for faceLocation in face_locations:
#            print_result(img_file, faceLocation)
            try:
                with Image.open(img_file) as im:
                    print("Processing {}...".format(img_file))
                    top, right, bottom, left = faceLocation
                    myuuid = uuid.uuid1()

                    print("Face Location: {}".format(faceLocation))
                    print("Format: {0}\tSize: {1}\tMode: {2}".format(im.format, im.size, im.mode))
                    im1 = im.crop((left, top, right, bottom))
                    print("Format: {0}\tSize: {1}\tMode: {2}".format(im1.format, im1.size, im1.mode))

                    im1.save("./" + str(myuuid) + ".jpg", "JPEG")

#                    newImg = Image.new("RGB", )

            except IOError:
                print("Unable to load image")
                sys.exit(1)


if __name__ == "__main__":
    main()
