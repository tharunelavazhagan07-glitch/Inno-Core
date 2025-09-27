import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Read dataset path from .env (falls back to default if not set)
DATA_DIR = os.getenv("DATA_DIR", "./backend/data/plant_disease")

def get_generators(img_size=(224, 224), batch_size=32):
    # ✅ Debug: Show which dataset path is being used
    print(f"[INFO] Using dataset directory: {DATA_DIR}")

    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2,
        rotation_range=20,
        horizontal_flip=True
    )

    train_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training"
    )

    val_gen = datagen.flow_from_directory(
        DATA_DIR,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation"
    )

    return train_gen, val_gen
