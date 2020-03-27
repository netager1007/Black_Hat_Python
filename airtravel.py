class Flight:

    def __init__(self, number):
        if not number[:2].isalpha():
            raise ValueError('[Airtravel] 첫 두글자가 알파벳이 아닙니다.')

        if not number[:2].isupper():
            raise ValueError('[Airtravel] 첫 두글자가 대문자가 아닙니다.')

        if not number[2:].isdigit():
            raise ValueError('[Airtravel] 세번째 글자 이상이 숫자가 아닙니다.')

        self.__number = number

    def get_number(self):
        return self.__number

class Korea:
    def __init__(self, name, population, captial):
        self.name = name
        self.population = population
        self.captial = captial

    def show(self):
        print(
            '''
            국가의 이름은 {} 입니다.
            국가의 인구는 {} 입니다.
            국가의 수도는 {} 입니다.
            '''.format(self.name, self.population, self.captial)
        )