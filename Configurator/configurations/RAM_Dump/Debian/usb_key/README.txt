***** INFORMATIONS *****
This USB key is used to store the data extracted from RAM with the file avml.
In the folder "result" you can find the compressed image of the RAM extracted.

To decompress this image you can use the command :
./avml-convert <file.compressed> <file.uncompressed>

--> Be sure to have enough space when you decompress !



***** IMPORTANT *****
- This USB key must respect the following architecture :
    _
    |- avml
    |- avml-convert
    |- result
    |  |- image_compressed
    |- README.txt

- This USB key must be formated in NTFS or exFAT, otherwise you will not be capable of creating or copying a file larger than 4GB (it will not work with FAT32 format)
