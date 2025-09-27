import os
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from .dataset import get_generators
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH", "./weights.h5")

def train_model(epochs=5):
    # Load generators
    train_gen, val_gen = get_generators()
    
    # ✅ Debug: Print dataset directory being used
    print(f"[INFO] Training with dataset from: {train_gen.directory}")

    # Build model
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    predictions = Dense(train_gen.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)

    # Freeze base layers
    for layer in base_model.layers:
        layer.trainable = False

    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train
    history = model.fit(train_gen, validation_data=val_gen, epochs=epochs)

    # Save model
    model.save(MODEL_PATH)

    return history.history

def evaluate_model():
    from .predict import load_model_and_classes
    model, classes = load_model_and_classes()
    _, val_gen = get_generators()

    # ✅ Debug: Print dataset directory for evaluation
    print(f"[INFO] Evaluating with dataset from: {val_gen.directory}")

    loss, acc = model.evaluate(val_gen)
    return {"loss": loss, "accuracy": acc}
