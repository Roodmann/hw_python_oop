from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = ('Тип тренировки: {training_type}; '
                'Длительность: {duration:.3f} ч.; '
                'Дистанция: {distance:.3f} км; '
                'Ср. скорость: {speed:.3f} км/ч; '
                'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Вернуть сообщение о тренировке"""
       
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    M_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
       
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
       
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    
    FIRST_CAL: int = 18
    SECOND_CAL: int = 20

    def get_spent_calories(self) -> float:
        
        return ((self.FIRST_CAL
                * self.get_mean_speed()
                - self.SECOND_CAL)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.M_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    
    FIRST_COFF: float = 0.035
    SECOND_COFF: float = 0.029
    DEGREE_COFF: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.FIRST_COFF
                * self.weight
                + (self.get_mean_speed()
                    ** self.DEGREE_COFF
                    // self.height)
                * self.SECOND_COFF
                * self.weight)
                * self.duration
                * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
   
    LEN_STEP: float = 1.38
    FIRST_COF: float = 1.1
    SECOND_COF: int = 2

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.FIRST_COF)
                * self.SECOND_COF
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    
    type_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type in type_dict.keys():
        return type_dict[workout_type](*data)
    else:
        raise ValueError

def main(training: Training) -> None:
    """Главная функция."""
    
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
