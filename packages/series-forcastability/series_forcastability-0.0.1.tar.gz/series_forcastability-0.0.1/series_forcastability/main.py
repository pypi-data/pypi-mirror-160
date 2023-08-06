from get_cov_2 import main

class sf:
    def __init__(self,series,adi_limit=1.32,cv2_limit=0.49):
        self.series=series
        self.adi_limit=adi_limit
        self.cv2_limit=cv2_limit

    def forecastability(self):
        adi = len(self.series) / len([v for v in self.series if v > 0])
        cv2 = main.get_cov(self.series).cov()

        if (adi<self.adi_limit and cv2<self.cv2_limit):
            return "Smooth series - Low forecasting error"
        elif (adi>=self.adi_limit and cv2<self.cv2_limit):
            return "Intermittent series - High forecasting error"
        elif (adi<self.adi_limit and cv2>=self.cv2_limit):
            return "Erratic series - Very poor forecasting accuracy"
        else:
            return "Lumpy series - Unforecastable"