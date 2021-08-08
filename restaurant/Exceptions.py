class CartDiffRestaurantError(Exception):
    def __init__(self):
        self.message = f'Dish is from diff restaurant is present'


class DishDontExist(Exception):
    def __init__(self):
        self.message = f'Dish is from diff restaurant is present'
