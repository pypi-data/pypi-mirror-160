import MultiCloudOCR as MultiCloudOCR
import time
# ourput the performance of ocr detect result
def computePerformance(data, correct_answer):
    # use MultiCloudOCR to analyze the image, and running time
    ali_start = time.perf_counter()
    ali = MultiCloudOCR.OCRAli(data)
    ali_end = time.perf_counter()
    baidu_start = time.perf_counter()
    baidu = MultiCloudOCR.OCRBaidu(data)
    baidu_end = time.perf_counter()
    local_start = time.perf_counter()
    local = MultiCloudOCR.OCRLocal(data)
    local_end = time.perf_counter()
    # if user input correct answer, directly compute correctness based on that
    ali_precision = ""
    ali_recall = ""
    baidu_precision = ""
    baidu_recall = ""
    local_precision = ""
    local_recall = ""
    if correct_answer != "":
        ali_intersection = 0
        for i in range(min(len(ali), len(correct_answer))):
            if ali[i] == correct_answer[i]:
                ali_intersection += 1
        baidu_intersection = 0
        for i in range(min(len(baidu), len(correct_answer))):
            if baidu[i] == correct_answer[i]:
                baidu_intersection += 1
        local_intersection = 0
        for i in range(min(len(local), len(correct_answer))):
            if local[i] == correct_answer[i]:
                local_intersection += 1
        ali_precision = ali_intersection / len(ali)
        ali_recall = ali_intersection / len(correct_answer)
        baidu_precision = baidu_intersection / len(baidu)
        baidu_recall = baidu_intersection / len(correct_answer)
        local_precision = local_intersection / len(local)
        local_recall = local_intersection / len(correct_answer)
    # else, use some color thing to mar diff if no correct answer provided
    response = [
        {
            'name': 'ali',
            'id': 1,
            'ocrvalue': ali,
            'performance': [ali_end - ali_start, ali_precision, ali_recall]
    }, {
        'name': 'baidu',
        'id': 2,
        'ocrvalue': baidu,
        'performance': [baidu_end - baidu_start, baidu_precision, baidu_recall]
    }, {
        'name': 'local',
        'id': 3,
        'ocrvalue': local,
        'performance': [local_end - local_start, local_precision, local_recall]
    }]
    return response
