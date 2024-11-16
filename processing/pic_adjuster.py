import os
from PIL import Image, ExifTags

def process_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)

    # Handle EXIF orientation (common for iPhone photos)
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(image._getexif().items())
        if exif.get(orientation) == 3:
            image = image.rotate(180, expand=True)
        elif exif.get(orientation) == 6:
            image = image.rotate(270, expand=True)
        elif exif.get(orientation) == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # No EXIF orientation info
        pass

    # Crop to a square with the option to shift downward
    width, height = image.size
    min_dimension = min(width, height)
    left = (width - min_dimension) / 2

    # Add an offset to lower the cropping region
    offset = min_dimension * 0.2  # Adjust this value to control how much lower the crop should be

    # Ensure we don't crop outside the image boundaries
    top = max(0, (height - min_dimension) / 2 + offset)
    bottom = min(height, (height + min_dimension) / 2 + offset)
    right = (width + min_dimension) / 2

    image = image.crop((left, top, right, bottom))


    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    # Debugging print statements
    print(f"Input path: {os.path.abspath(input_path)}")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print(f"Output path: {os.path.abspath(output_path)}")

    # Additional check: Ensure output_path is not a directory
    if os.path.isdir(output_path):
        raise IsADirectoryError(f"The output path '{output_path}' is a directory, not a file path.")

    # Save as PNG
    try:
        image.save(output_path, format='PNG')
        print(f"Image successfully saved to {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")
        raise

name = 'trio'

# Example usage
input_path = f'before_pics/{name}.jpeg'
output_path = f'after_pics/{name}.png'

process_image(input_path, output_path)