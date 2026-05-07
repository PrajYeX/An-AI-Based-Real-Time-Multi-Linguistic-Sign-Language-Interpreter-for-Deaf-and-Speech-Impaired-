from PIL import Image
import os

def extract_and_save_kannada_signs(source_image_path, output_dir):
    """
    Extracts individual Kannada sign images from a grid image and saves them as character.jpeg.
    """
    # Load the source image
    try:
        img = Image.open(source_image_path)
    except FileNotFoundError:
        print(f"Error: Source image not found at {source_image_path}")
        return
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define crop coordinates and corresponding Kannada characters
    # These coordinates are estimated from visual inspection of Kannada Signs.jpg (752x869 pixels)
    # Each crop is (left, top, right, bottom)
    
    signs_data = [
        # Row 1: ಕ, ಖ, ಗ, ಘ, ಙ, ಚ, ಛ, ಜ, ಝ, ಞ
        {'char': 'ಕ', 'coords': (10, 40, 75, 130)},
        {'char': 'ಖ', 'coords': (80, 40, 145, 130)},
        {'char': 'ಗ', 'coords': (150, 40, 215, 130)},
        {'char': 'ಘ', 'coords': (220, 40, 285, 130)},
        {'char': 'ಙ', 'coords': (290, 40, 355, 130)},
        {'char': 'ಚ', 'coords': (360, 40, 425, 130)},
        {'char': 'ಛ', 'coords': (430, 40, 495, 130)},
        {'char': 'ಜ', 'coords': (500, 40, 565, 130)},
        {'char': 'ಝ', 'coords': (570, 40, 635, 130)},
        {'char': 'ಞ', 'coords': (640, 40, 705, 130)},

        # Row 2: ಟ, ಠ, ಡ, ಢ, ಣ, ತ, ಥ, ದ, ಧ, ನ
        {'char': 'ಟ', 'coords': (10, 180, 75, 270)},
        {'char': 'ಠ', 'coords': (80, 180, 145, 270)},
        {'char': 'ಡ', 'coords': (150, 180, 215, 270)},
        {'char': 'ಢ', 'coords': (220, 180, 285, 270)},
        {'char': 'ಣ', 'coords': (290, 180, 355, 270)},
        {'char': 'ತ', 'coords': (360, 180, 425, 270)},
        {'char': 'ಥ', 'coords': (430, 180, 495, 270)},
        {'char': 'ದ', 'coords': (500, 180, 565, 270)},
        {'char': 'ಧ', 'coords': (570, 180, 635, 270)},
        {'char': 'ನ', 'coords': (640, 180, 705, 270)},
        
        # Row 3: ಪ, ಫ, ಬ, ಭ, ಮ, ಯ, ರ, ಲ, ವ, ಶ
        {'char': 'ಪ', 'coords': (10, 320, 75, 410)},
        {'char': 'ಫ', 'coords': (80, 320, 145, 410)},
        {'char': 'ಬ', 'coords': (150, 320, 215, 410)},
        {'char': 'ಭ', 'coords': (220, 320, 285, 410)},
        {'char': 'ಮ', 'coords': (290, 320, 355, 410)},
        {'char': 'ಯ', 'coords': (360, 320, 425, 410)},
        {'char': 'ರ', 'coords': (430, 320, 495, 410)},
        {'char': 'ಲ', 'coords': (500, 320, 565, 410)},
        {'char': 'ವ', 'coords': (570, 320, 635, 410)},
        {'char': 'ಶ', 'coords': (640, 320, 705, 410)},

        # Row 4: ಷ, ಸ, ಹ, ಳ, ಕ್ಷ, ಜ್ಞ
        {'char': 'ಷ', 'coords': (10, 460, 75, 550)},
        {'char': 'ಸ', 'coords': (80, 460, 145, 550)},
        {'char': 'ಹ', 'coords': (150, 460, 215, 550)},
        {'char': 'ಳ', 'coords': (220, 460, 285, 550)},
        {'char': 'ಕ್ಷ', 'coords': (290, 460, 355, 550)},
        {'char': 'ಜ್ಞ', 'coords': (360, 460, 425, 550)},
        
        # Row 5 (Vowels): ಅ, ಆ, ಇ, ಈ, ಉ, ಊ, ಋ, ಎ, ಏ, ಐ
        {'char': 'ಅ', 'coords': (10, 600, 75, 690)},
        {'char': 'ಆ', 'coords': (80, 600, 145, 690)},
        {'char': 'ಇ', 'coords': (150, 600, 215, 690)},
        {'char': 'ಈ', 'coords': (220, 600, 285, 690)},
        {'char': 'ಉ', 'coords': (290, 600, 355, 690)},
        {'char': 'ಊ', 'coords': (360, 600, 425, 690)},
        {'char': 'ಋ', 'coords': (430, 600, 495, 690)},
        {'char': 'ಎ', 'coords': (500, 600, 565, 690)},
        {'char': 'ಏ', 'coords': (570, 600, 635, 690)},
        {'char': 'ಐ', 'coords': (640, 600, 705, 690)},

        # Row 6 (Vowels and modifiers): ಒ, ಓ, ಔ, ಅಂ, ಅಃ
        {'char': 'ಒ', 'coords': (10, 740, 75, 830)},
        {'char': 'ಓ', 'coords': (80, 740, 145, 830)},
        {'char': 'ಔ', 'coords': (150, 740, 215, 830)},
        {'char': 'ಅಂ', 'coords': (220, 740, 285, 830)},
        {'char': 'ಅಃ', 'coords': (290, 740, 355, 830)},
    ]
    for sign_data in signs_data:
        char = sign_data['char']
        coords = sign_data['coords']
        
        # Crop the image
        cropped_img = img.crop(coords)
        
        # Save the cropped image
        output_path = os.path.join(output_dir, f"{char}.jpeg")
        cropped_img.save(output_path, "JPEG")
        print(f"Saved {char}.jpeg to {output_path}")

if __name__ == "__main__":
    source_image_file = "D:/Final Year Project/Sign Word Alpha Gesture/Kannada Signs.jpg"
    output_directory = "D:/Final Year Project/dataset/kannada" # Overwrite existing
    
    # IMPORTANT: The coordinates defined in signs_data are placeholders and MUST be
    # accurately adjusted based on the actual layout of 'Kannada Signs.jpg'.
    # Manual inspection and precise coordinate finding is required.
    
    # You might need to run this script, inspect the output, and refine coordinates.
    # The current estimation is very rough.

    extract_and_save_kannada_signs(source_image_file, output_directory)