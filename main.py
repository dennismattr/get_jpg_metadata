import sys
import os
from exif import Image  # Could also use PIL
 
def main(image_directory):
      
    def get_image_metadata(image_path, round_coords=4):

        def decimal_coords(coords, ref):
            decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
            if ref=="S" or ref=='W':
                decimal_degrees = -decimal_degrees
            return decimal_degrees

        with open(image_path, 'rb') as src:
            img = Image(src)

        if img.has_exif:
            try:
                coords = (
                    decimal_coords(
                        img.gps_latitude, img.gps_latitude_ref
                    ),
                    decimal_coords(
                        img.gps_longitude, img.gps_longitude_ref
                    )
                )
            except AttributeError:
                print ('Invalid coordinates!')
        else:
            print ('Image has no EXIF information!')
    
        return({
            "timestamp":img.datetime_original, 
            "lat":round(coords[0], round_coords),
            "lng":round(coords[1], round_coords)
            })

    metadata_dict = {}
    for image_file in os.listdir(image_directory):
        metadata_dict.update({
            image_file: get_image_metadata(f"{image_directory}/{image_file}")
        })

    print(metadata_dict)
    return None

if __name__ == "__main__":
    image_directory = sys.argv[1]
    main(image_directory)
