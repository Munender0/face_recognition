import face_recognition
import os
import shutil

def recognize_and_copy_images(target_image_path, album_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Load the target image and get the face encoding
    target_image = face_recognition.load_image_file(target_image_path)
    target_face_encoding = face_recognition.face_encodings(target_image)
    
    # If no face is detected in the target image, exit the function
    if not target_face_encoding:
        print(f"No faces found in the target image: {target_image_path}")
        return
    
    target_face_encoding = target_face_encoding[0]  # We assume the first face is the target face
    
    # Iterate through all the images in the wedding album directory
    for filename in os.listdir(album_directory):
        file_path = os.path.join(album_directory, filename)
        
        # Check if the file is an image (you can extend this list of extensions)
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Load the current image in the album
                album_image = face_recognition.load_image_file(file_path)
                face_encodings = face_recognition.face_encodings(album_image)

                # If no faces are found in the album image, skip it
                if not face_encodings:
                    continue
                
                # Compare each face encoding in the album image with the target face encoding
                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces([target_face_encoding], face_encoding)
                    if match[0]:  # If a match is found
                        # Copy the matching photo to the output folder
                        output_path = os.path.join(output_directory, filename)
                        shutil.copy(file_path, output_path)
                        print(f"Copied {filename} to {output_directory}")
                        break  # No need to check other faces once a match is found
                
            except Exception as e:
                print(f"Error processing image {filename}: {e}")

# Example usage
target_image_path = input("Enter the path to the target image: ")  # Path to the target image (person's photo)
album_directory = input("Enter the path to the wedding album directory: ")  # Path to the wedding album photos folder
output_directory = input("Enter the path to the output directory: ")  # Path to the output directory where matched photos will be saved

# Run the function
recognize_and_copy_images(target_image_path, album_directory, output_directory)
