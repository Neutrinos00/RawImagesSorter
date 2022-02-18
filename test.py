import exifread
import pyperclip

def main():
    path_name='./Photos/DSC01311.ARW'

    pyperclip.copy(path_name)

    with open(path_name, 'rb') as f:
        tags = exifread.process_file(f)
        for key, val in tags.items():
            if 'Image Orientation' in key:
                if 'Rotated 90 CCW' in str(val):
                    print(1)
                else:
                    print(0)


if __name__ == '__main__':
    main()
