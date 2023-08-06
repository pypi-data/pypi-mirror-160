from paddleocr import PaddleOCR
def model():
        ocr = PaddleOCR(lang="en",use_gpu=False,rec_model_dir='paddleocr/rec/',drop_score=0.85,det=False,show_log = False)
        return ocr
