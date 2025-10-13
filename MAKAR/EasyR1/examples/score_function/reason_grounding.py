import re
from typing import List, Optional
from mathruler.grader import grade_answer
from typing import Dict  # 显式导入

def iou_reward(predict_str: str, ground_truth: str) -> float:
    """
    Calculate the Intersection over Union (IoU) between the predicted bounding box and the ground truth bounding box. Return 1.0 if IoU >= 0.5; otherwise, return 0.0.
    """
    def parse_bbox(s: str) -> Optional[List[float]]:
        # match <answer>[x, y, w, h]</answer> format
        match = re.search(r"<answer>\s*\[\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)\s*\]\s*</answer>", s)
        if match:
            return [float(x) for x in match.groups()]
        return None

    pred_bbox = parse_bbox(predict_str)
    true_bbox = parse_bbox(ground_truth)

    # print("pred_bbox:", pred_bbox)
    # print("true_bbox:", true_bbox)

    if not pred_bbox or not true_bbox:
        return 0.0

    if pred_bbox == true_bbox:
        return 1.0

    x1, y1, x2, y2 = pred_bbox
    x1_true, y1_true, x2_true, y2_true = true_bbox

    x1 = min(x1, x2)
    x2 = max(x1, x2)
    y1 = min(y1, y2)
    y2 = max(y1, y2)

    x1_true = min(x1_true, x2_true)
    x2_true = max(x1_true, x2_true)
    y1_true = min(y1_true, y2_true)
    y2_true = max(y1_true, y2_true)

    inter_x1 = max(x1, x1_true)
    inter_y1 = max(y1, y1_true)
    inter_x2 = min(x2, x2_true)
    inter_y2 = min(y2, y2_true)

    if inter_x1 >= inter_x2 or inter_y1 >= inter_y2:
        return 0.0  

    inter_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
    pred_area = (x2 - x1) * (y2 - y1)
    true_area = (x2_true - x1_true) * (y2_true - y1_true)

    iou = inter_area / (pred_area + true_area - inter_area)
    return 1.0 if iou >= 0.5 else 0.0


def format_reward(predict_str: str) -> float:
    pattern = re.compile(r"<think>.*?</think>\s*<answer>.*?</answer>", re.DOTALL)
    format_match = re.fullmatch(pattern, predict_str)
    return 1.0 if format_match else 0.0


def accuracy_reward(predict_str: str, ground_truth: str) -> float:
    try:
        content_match = re.search(r"<answer>(.*?)</answer>", predict_str)
        given_answer = content_match.group(1).strip() if content_match else predict_str.strip()
        if grade_answer(given_answer, ground_truth.strip()):
            return 1.0

    except Exception:
        pass

    return 0.0


def compute_score(predict_str: str, ground_truth: str, format_weight: float = 0.5) -> Dict[str, float]:
    format_score = format_reward(predict_str)

    accuracy_score  = iou_reward(predict_str, ground_truth)
    return {
        "overall": (1 - format_weight) * accuracy_score   + format_weight * format_score,
        "format": format_score,
        "accuracy": accuracy_score,
    }