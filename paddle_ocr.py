#!/usr/bin/env python3
"""Minimal PaddleOCR Text Recognition"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional
from paddleocr import PaddleOCR


class TextRecognizer:
    def __init__(self, lang: str = "en"):
        self.ocr = PaddleOCR(lang=lang)

    def extract_text(self, image_path: str, threshold: float = 0.5) -> List[Tuple[str, float, list]]:
        if not os.path.exists(image_path):
            return []
        
        result = self.ocr.predict(image_path)
        if not result:
            return []
        
        result = result[0]
        if not isinstance(result, dict):
            return []
        
        texts = result.get('rec_texts', [])
        scores = result.get('rec_scores', [])
        boxes = result.get('rec_boxes', [])
        
        return [(str(texts[i]), float(scores[i]), boxes[i]) 
                for i in range(len(texts)) 
                if (i < len(scores) and scores[i] >= threshold)]

    def save_to_file(self, extracted: List[Tuple[str, float, list]], image_path: str, output_file: Optional[str] = None) -> str:
        if not extracted:
            return ""
        
        output_file = output_file or f"{Path(image_path).stem}_paddleocr.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("PADDLEOCR TEXT EXTRACTION\n" + "="*40 + "\n")
            f.write(f"Source: {image_path}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Count: {len(extracted)}\n" + "="*40 + "\n\n")
            
            for i, (text, score, box) in enumerate(extracted, 1):
                f.write(f"{i:2d}. Text: {text}\n    Confidence: {score:.3f}\n")
                if box is not None and len(box) > 0:
                    f.write(f"    Bounding Box: {box}\n")
                f.write("-" * 20 + "\n")
            
            f.write("\nRAW TEXT:\n" + "-"*20 + "\n")
            for text, _, _ in extracted:
                f.write(f"{text}\n")
        
        return output_file

    def process(self, image_path: str, threshold: float = 0.5, output_file: Optional[str] = None) -> bool:
        extracted = self.extract_text(image_path, threshold)
        return bool(extracted and self.save_to_file(extracted, image_path, output_file))


def main():
    recognizer = TextRecognizer()
    for img in ["img/medbill1.png", "img/medbill3.png", "img/medbill20.jpeg"]:
        if os.path.exists(img):
            recognizer.process(img, threshold=0.5)
            break


if __name__ == "__main__":
    main()
