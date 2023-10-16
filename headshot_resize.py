from PIL import Image
import os
import glob


def resize_image(name):
    # Define the output path and maximum dimensions
    output_path = f"data/imgs/{name}_.jpg"
    target_size = (600, 600)
    max_size = (1200, 1200)
    max_file_size_kb = 245

    extensions = [".jpg", ".jpeg", ".JPG", ".JPEG"]
    for ext in extensions:
        try:
            with Image.open(f"data/imgs/{name}{ext}") as img:
                # Calculate the center coordinates of the original image
                center_x, center_y = img.width // 2, img.height // 2

                # Calculate the cropping box
                crop_x1 = max(center_x - max_size[0] // 2, 0)
                crop_y1 = max(center_y - max_size[1] // 2, 0)
                crop_x2 = min(center_x + max_size[0] // 2, img.width)
                crop_y2 = min(center_y + max_size[1] // 2, img.height)

                # Crop the image to the specified dimensions
                img = img.crop((crop_x1, crop_y1, crop_x2, crop_y2))

                # Resize the cropped image without antialiasing
                img = img.resize(target_size, Image.BOX)

                # Save the resized image
                img.save(output_path, optimize=True, quality=95)

                # Check and reduce file size if necessary
                while os.path.getsize(output_path) > (max_file_size_kb * 1024):
                    # Reduce the quality to meet the max file size
                    with Image.open(output_path) as img:
                        img.save(output_path, format='JPEG', optimize=True, quality=85)

                print(f"Image cropped and resized to {output_path}")

        except FileNotFoundError:
            pass




if __name__=="__main__":
    import sys
    resize_image(sys.argv[1])