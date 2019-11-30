#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Service that removes files and correspoding emails

import os

def main():

    downloaded_images = os.listdir('/home/pi/work_ssd/email3/images')
    
    trash_images = os.listdir('/home/pi/work_ssd/email3/trash')
    print(downloaded_images)
    print(trash_images)
if __name__ == '__main__':
    main()
