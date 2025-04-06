import cv2
import numpy as np


# 非极大值抑制 (NMS) 函数
def non_max_suppression(boxes, overlap_thresh=0.5):
    if len(boxes) == 0:
        return []
    boxes = np.array(boxes)
    pick = []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlap_thresh)[0])))
    return boxes[pick].astype("int")


def cv_detections(source_image, screen_image):
    # 1. 读取图像
    large_image = cv2.imread(source_image, cv2.IMREAD_GRAYSCALE)  # 大图
    # 2. 获取图像尺寸
    height, width = large_image.shape[:2]

    # 3. 计算裁剪区域
    top = int(height * 0.0001)  # 裁剪区域的上边界（70% 高度）
    bottom = height  # 裁剪区域的下边界（100% 高度）

    # 裁剪图像：保持宽度不变，只裁剪高度范围 [top, bottom]
    # cropped_image = large_image[top:bottom, 0:width]
    large_image = large_image[top:bottom, 0:width]

    template_image = cv2.imread(screen_image, cv2.IMREAD_GRAYSCALE)  # 截图

    # 2. 初始化参数
    threshold = 0.7  # 匹配阈值
    scale_factors = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5]  # 缩放比例列表
    matches = []

    # 3. 构建图像金字塔并逐尺度匹配
    for scale in scale_factors:
        resized_template = cv2.resize(template_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        if resized_template.shape[0] > large_image.shape[0] or resized_template.shape[1] > large_image.shape[1]:
            continue  # 如果模板大于大图，则跳过该尺度

        # 模板匹配
        result = cv2.matchTemplate(large_image, resized_template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        # 记录匹配到的位置及其相似度
        for pt in zip(*loc[::-1]):
            similarity = result[pt[1], pt[0]]  # 获取相似度值
            matches.append(
                (pt[0], pt[1], pt[0] + resized_template.shape[1], pt[1] + resized_template.shape[0], similarity))

    # 4. 按相似度排序
    matches.sort(key=lambda x: x[4], reverse=True)  # 按相似度降序排序

    # 5. 非极大值抑制去重
    filtered_matches = non_max_suppression(np.array([[x1, y1, x2, y2] for x1, y1, x2, y2, _ in matches]))

    # 6. 打印匹配到的坐标
    print("匹配到的截图位置坐标：",filtered_matches)
    for (start_x, start_y, end_x, end_y) in filtered_matches:
        print(f"左上角: ({start_x}, {start_y}), 右下角: ({end_x}, {end_y})")

    x_y_list = []
    if len(filtered_matches) == 0:
        return x_y_list
    else:
        for i in filtered_matches:
            x = int((i[0]+i[2])/2+20)
            y = int((i[1]+i[3])/2)
            x_y_list.append((x,y))
    return x_y_list
    # 7. 绘制结果
    # large_image_color = cv2.cvtColor(large_image, cv2.COLOR_GRAY2BGR)
    # for (start_x, start_y, end_x, end_y) in filtered_matches:
    #     # 找到对应的相似度值
    #     match = next(match for match in matches if match[0] == start_x and match[1] == start_y)
    #     similarity = match[4]
    #
    #     # 绘制矩形框
    #     cv2.rectangle(large_image_color, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
    #
    #     # 在矩形框上方标注相似度
    #     text = f"Sim: {similarity:.2f}"
    #     cv2.putText(large_image_color, text, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #
    # # 显示结果
    # cv2.imshow('Detected Matches', large_image_color)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


rs = cv_detections("images/other/full.png", "images/hero/buquzhanshen.png")
print(rs)