def process_metadata(filepath):
    """ 
    Processes metadata 
    """
    with ExifToolHelper() as et:
        return et.get_metadata(filepath)

def process_ela(filepath):
    """ 
    Processes image to produce ELA image
    :filepath - filepath to open
    """
    image = Image.open(filepath)
    compressed_image = Image.open(temp_path)
    ela_image = ImageChops.difference(image, compressed_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0/max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image

def calculate_ela(selfquality=90):
    """ 
        Calculates ELA of image
    """
    image = Image.open(filepath)
    temp_path = "temp_ela.jpg"
    image.save(temp_path, "JPEG", quality=quality)
    compressed_image = Image.open(temp_path)

    ela_image = ImageChops.difference(image, compressed_image)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0/max_diff
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    return ela_image
def detect_edges(filepath):
    """
        Detects edges 
        Returns:
        :edge_image - edge image 
    """
    image = Image.open(filepath)
    edge_image = image.filter(ImageFilter.FIND_EDGES)
    return edge_image
def process_strings(filepath):
    """ 
        Processes image to extract strings 
        :filepath - filepath to open
    """
    self.string_label.delete('1.0', END)
    strings_str = ""
    if self.filepath:
        with open(filepath, 'rb') as image:
            data = image.read()
            strings = re.findall(b'[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};\'"\\|,.<>\/? ]{4,}', data)
            strings = [s.decode('utf-8', 'ignore') for s in strings]
            strings_str = "\n".join(strings)
    self.string_label.insert(END, strings_str)
    return strings_str

def process_hex(filepath):
    """ 
    Processes image to produce hexadecimal conversion
    :filepath - filepath to open
    """
    hex_data = ""
    if filepath:
        with open(filepath, 'rb') as image:
            data = image.read(1024)  # Read the first 1024 bytes for demonstration
            hex_data = binascii.hexlify(data).decode('utf-8')
            hex_str = ' '.join(hex_data[i:i+2] for i in range(0, len(hex_data), 2))
    self.hex_label.insert(END, hex_str)
    return hex_data
def locate_coords(filepath):
    """
        Locates and returns the GPS coordinates via EXIFTool
        If not, returns a default location
    """
    with ExifToolHelper() as et:
        location_data = et.get_tags(filepath, ["EXIF:GPSLatitude","EXIF:GPSLongitude"])
        location = str(location_data[0].get("EXIF:GPSLatitude")) + "," + str(location_data[0].get("EXIF:GPSLongitude"))
        try:
            lat, long = location.split(",")[0], location.split(",")[1]
            return float(long), float(lat)
        except:
            return 1.0,1.0


def hash_file( filepath):
    """ 
    Processes image to produce a hash with MD5 and SHA1
    :filepath - filepath to open
    """
    BUFF_SIZE = 65536
    with open(filepath, 'rb') as file:
        md5 = hashlib.md5(file.read())
        sha1 = hashlib.sha1(file.read())
        return md5, sha1

def process_copymove(filepath):
    """ 
    Processes image to detect copy move
    :filepath - filepath to open
    """
    image = Image.open(filepath).convert('L')
    image_data = numpy.array(image)
    shift = False
    for y_shift in range(1,30):
        for x_shift in range(1, 30):
            shift_data = numpy.roll(image_data, (y_shift, x_shift), axis=(0,1))
            similarity = numpy.mean(image_data == shift_data)
            if similarity > 0.95:
                shift = True
                break
    if shift:
        self.copy_move_text.set("Copy Move Detected")
    else:
        self.copy_move_text.set("Copy Move Not Detected")

def blur_image(image_path, kernel_size=5):
    """
    Applies Gaussian blur to an image to reduce noise.

    
    :image_path: str, path to the input image file
    :kernel_size: int, size of the Gaussian kernel

    
    -blurred_image: 2D numpy array representing the blurred image
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    # Apply Gaussian blur
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image

def sharpen_image( image_path):
    """
    Sharpens an image to enhance its details.

    :filename: str, path to the input image file

    -sharpened_image: 2D numpy array representing the sharpened image
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Define sharpening kernel
    kernel = numpy.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
    
    # Apply the kernel to the image
    sharpened_image = cv2.filter2D(image, -1, kernel)
    
    return sharpened_image
    
def compute_luminance( image_path):
    """
    Computes the luminance gradient of an image using Sobel filters.

    Args:
    - image_path: str, path to the input image file

    Returns:
    - gradient_magnitude: 2D numpy array representing the gradient magnitude
    """
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    # Compute Sobel gradients
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    # Compute gradient magnitude
    gradient_magnitude = numpy.sqrt(sobel_x**2 + sobel_y**2)
    # Normalize gradient magnitude for better visualization
    gradient_magnitude = (gradient_magnitude / gradient_magnitude.max()) * 255
    return gradient_magnitude.astype(numpy.uint8)
    
def equalize_image( image_path):
    """
    Applies histogram equalization to improve the contrast of a grayscale image.

    Args:
    - image_path: str, path to the input image file

    Returns:
    - equalized_image: 2D numpy array representing the equalized image
    """
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        raise ValueError("Image not found or unable to load.")
    
    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(image)
    
    return equalized_image
