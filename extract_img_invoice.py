#!/usr/bin/env python3
"""Minimal Line Extractor"""

import os
from typing import List, Tuple, Dict


def extract_lines_from_image(image_path: str) -> List[Tuple[str, float]]:
    from paddle_ocr import TextRecognizer
    
    if not os.path.exists(image_path):
        return []
    
    recognizer = TextRecognizer(lang='en')
    extracted_data = recognizer.extract_text(image_path, threshold=0.3)
    
    if not extracted_data:
        return []
    
    return group_text_into_lines(extracted_data)


def group_text_into_lines(extracted_data: List[Tuple[str, float, list]], line_threshold: float = 15.0) -> List[Tuple[str, float]]:
    elements = []
    for text, confidence, bbox in extracted_data:
        if bbox is not None and len(bbox) >= 4:
            y_pos = (bbox[1] + bbox[3]) / 2 if isinstance(bbox[1], (int, float)) else bbox[1]
            x_pos = (bbox[0] + bbox[2]) / 2 if isinstance(bbox[0], (int, float)) else bbox[0]
            elements.append({'text': text, 'confidence': confidence, 'y_pos': float(y_pos), 'x_pos': float(x_pos)})
    
    if not elements:
        return [(text, conf) for text, conf, _ in extracted_data]
    
    elements.sort(key=lambda x: x['y_pos'])
    
    lines_with_confidence = []
    current_line = [elements[0]]
    current_y = elements[0]['y_pos']
    
    for element in elements[1:]:
        if abs(element['y_pos'] - current_y) <= line_threshold:
            current_line.append(element)
        else:
            line_text, line_confidence = finalize_line_with_confidence(current_line)
            if line_text.strip():
                lines_with_confidence.append((line_text, line_confidence))
            current_line = [element]
            current_y = element['y_pos']
    
    if current_line:
        line_text, line_confidence = finalize_line_with_confidence(current_line)
        if line_text.strip():
            lines_with_confidence.append((line_text, line_confidence))
    
    return lines_with_confidence


def finalize_line_with_confidence(line_elements: List[Dict]) -> Tuple[str, float]:
    line_elements.sort(key=lambda x: x['x_pos'])
    line_text = ' '.join([elem['text'] for elem in line_elements])
    avg_confidence = sum(elem['confidence'] for elem in line_elements) / len(line_elements)
    return line_text, avg_confidence


def save_lines_to_file(lines_with_confidence: List[Tuple[str, float]], image_path: str) -> str:
    output_file = f"{os.path.splitext(image_path)[0]}_clean_lines.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for line_text, confidence in lines_with_confidence:
            f.write(f"{line_text} [conf: {confidence:.3f}]\n")
    
    return output_file


def process_image_to_lines(image_path: str) -> List[Tuple[str, float]]:
    lines_with_confidence = extract_lines_from_image(image_path)
    if lines_with_confidence:
        save_lines_to_file(lines_with_confidence, image_path)
    return lines_with_confidence

if __name__ == "__main__":

    # imgs = os.listdir('img')
    # for img in imgs:
    #     image_path = os.path.join('img', img)
    #     if os.path.exists(image_path):
    image_path = "sample_image.png"
    process_image_to_lines(image_path)