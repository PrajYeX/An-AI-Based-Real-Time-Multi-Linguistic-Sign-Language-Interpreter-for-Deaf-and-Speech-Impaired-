import numpy as np
import cv2

CLASS_NAMES = ['Call', 'Good', 'Hello', 'House', 'I Love You', 'No', 'Ok', 'Prayer', 'Thank You', 'Yes']

# Create a list of colors for each class where each color is a tuple of 3 integer values
rng = np.random.default_rng(3)
COLORS = rng.uniform(0, 255, size=(len(CLASS_NAMES), 3))


def non_maximum_suppression(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes


def multi_class_nms(boxes, scores, class_ids, iou_threshold):

    unique_class_ids = np.unique(class_ids)

    keep_boxes = []
    for class_id in unique_class_ids:
        class_indices = np.where(class_ids == class_id)[0]
        class_boxes = boxes[class_indices, :]
        class_scores = scores[class_indices]

        class_keep_boxes = non_maximum_suppression(class_boxes, class_scores, iou_threshold)
        keep_boxes.extend(class_indices[class_keep_boxes])

    return keep_boxes


def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou


def xywh_to_xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def draw_detections(image, boxes, scores, class_ids, mask_alpha=0.3):
    det_image = image.copy()
    is_accident = False
    label = "s"

    img_height, img_width = image.shape[:2]
    font_size = min([img_height, img_width]) * 0.001
    text_thickness = int(min([img_height, img_width]) * 0.001)

    det_image = draw_masks(det_image, boxes, class_ids, mask_alpha)

    for class_id, box, score in zip(class_ids, boxes, scores):
        color = COLORS[class_id]

        draw_box(det_image, box, color)

        label = CLASS_NAMES[class_id]
        caption = f'{label} {int(score * 100)}%'
        draw_text(det_image, caption, box, color, font_size, text_thickness)
    return det_image, label


def draw_box(image, box, color=(0, 0, 255), thickness=2):
    x1, y1, x2, y2 = box.astype(int)
    return cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)


def draw_text(image, text, box, color=(0, 0, 255), font_size=0.001, text_thickness=2):
    x1, y1, x2, y2 = box.astype(int)
    (tw, th), _ = cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                 fontScale=font_size, thickness=text_thickness)
    th = int(th * 1.2)

    cv2.rectangle(image, (x1, y1), (x1 + tw, y1 - th), color, -1)

    return cv2.putText(image, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), text_thickness, cv2.LINE_AA)


def draw_masks(image, boxes, classes, mask_alpha=0.3):
    mask_image = image.copy()

    for box, class_id in zip(boxes, classes):
        color = COLORS[class_id]

        x1, y1, x2, y2 = box.astype(int)

        cv2.rectangle(mask_image, (x1, y1), (x2, y2), color, -1)

    return cv2.addWeighted(mask_image, mask_alpha, image, 1 - mask_alpha, 0)
