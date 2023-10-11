class StandardCalories():
    def __init__(self, stage, body, sex, low_carb, moderate_carb, high_carb):
        self.stage = stage
        self.body = body
        self.sex = sex
        self.low_carb = low_carb
        self.moderate_carb = moderate_carb
        self.high_carb = high_carb

class Diet():
    def __init__(self, calories, nutrition, breakfast, lunch, dinner):
        self.calories = calories
        self.nutrition = nutrition
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner

    def get_nutrition_detail(self):
        tmp = self.nutrition.split(';')
        return NutritionDetail(float(tmp[0]), float(tmp[1]), float(tmp[2]), float(tmp[3]))

    def get_breakfast_detail(self):
        tmp = self.breakfast.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)

    def get_lunch_detail(self):
        tmp = self.lunch.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)

    def get_dinner_detail(self):
        tmp = self.dinner.split(':')
        calories = tmp[0]
        temp = tmp[1].split(';')
        id1, amount1 = temp[0].split('x')
        id2, amount2 = temp[1].split('x')
        return DietDetail(calories, id1, amount1, id2, amount2)

class NutritionDetail():
    def __init__(self, calories, carbs, fat, protein):
        self.calories = calories
        self.carbs = carbs
        self.fat = fat
        self.protein = protein

    def get_carbs_percentage(self):
        c = self.carbs * 4 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return c

    def get_fat_percentage(self):
        f = self.fat * 9 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return f

    def get_protein_percentage(self):
        p = self.protein * 4 / (self.carbs * 4 + self.fat * 9 + self.protein * 4)
        return p

class DietDetail():
    def __init__(self, calories, id1, amount1, id2, amount2):
        self.calories = calories
        self.id1 = id1
        self.amount1 = amount1
        self.id2 = id2
        self.amount2 = amount2
