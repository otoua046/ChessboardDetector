import cv2
import numpy as np
import glob
import os
import argparse

def order_points(pts):
    """
    Order points in the order:
    top-left, top-right, bottom-right, bottom-left.
    """
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum,
    # the bottom-right will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # compute the difference between the points:
    # the top-right will have the smallest difference,
    # the bottom-left will have the largest difference.
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    return rect

def detect_and_warp_board_contour(image_path, output_size=(800, 800)):
    """
    Detect the largest 4-point contour (assumed to be the chessboard border),
    order its points, and warp the region to a top-down view.
    Returns the warped image (BGR) or None if detection fails.
    """
    print(f"Processing image: {image_path}")
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image {image_path}")
        return None
    
    orig = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection (Canny)
    edged = cv2.Canny(blurred, 50, 150)
    
    # Optionally, dilate and erode to close gaps in the edges
    edged = cv2.dilate(edged, None, iterations=2)
    edged = cv2.erode(edged, None, iterations=2)
    
    # Find contours in the edged image
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print("No contours found.")
        return None

    # Sort contours by area, descending
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    board_contour = None
    
    # Loop over the contours and look for a quadrilateral
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        if len(approx) == 4:
            board_contour = approx
            break
    
    if board_contour is None:
        print("No quadrilateral contour found.")
        return None

    pts = board_contour.reshape(4, 2)
    rect = order_points(pts)
    print("Ordered board corners:")
    print(rect)
    
    # Set destination points for the perspective transform
    dst = np.array([
        [0, 0],
        [output_size[0]-1, 0],
        [output_size[0]-1, output_size[1]-1],
        [0, output_size[1]-1]
    ], dtype="float32")
    
    # Compute perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(orig, M, output_size)
    print("Board successfully warped to top-down view.")
    return warped

def main():
    parser = argparse.ArgumentParser(
        description="Detect a chessboard by contour detection, warp it, and export to 800x800 JPEG."
    )
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing input images.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save processed images.")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Gather image files from input_dir
    img_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    image_paths = []
    for ext in img_extensions:
        image_paths.extend(glob.glob(os.path.join(input_dir, ext)))
    
    print(f"Found {len(image_paths)} images in {input_dir}")
    if not image_paths:
        print("No images found in the specified directory.")
        return

    for image_path in image_paths:
        warped = detect_and_warp_board_contour(image_path, output_size=(800, 800))
        if warped is not None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_cropped.jpg")
            cv2.imwrite(output_path, warped)
            print(f"Saved warped board to {output_path}")
        else:
            print(f"Skipping {image_path} due to detection issues.")

if __name__ == "__main__":
    main()