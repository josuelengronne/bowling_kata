from enum import Enum


class BowlingGame:
    pin_amount = 10
    frame_amount = 10

    def __init__(self):
        self.__frames = []
        self.__extra_roll_1 = None
        self.__extra_roll_2 = None

    def score(self) -> int:
        if self.__is_finished():
            return self.__calculate_score()
        raise BowlingGame.NotFinishedException()

    def roll(self, amount: int) -> None:
        self.__verify_can_roll()
        self.__roll_amount(amount)

    def __verify_can_roll(self) -> None:
        if self.__is_finished():
            raise BowlingGame.AlreadyFinishedException()

    def __roll_amount(self, amount: int) -> None:
        if self.__is_latest_frame_incomplete():
            self.__get_latest_frame().add_roll(amount)
            return
        if self.__has_finished_frames():
            self.__roll_extra(amount)
            return
        self.__create_frame(amount)

    def __roll_extra(self, amount: int) -> None:
        if self.__extra_roll_1 is None:
            self.__extra_roll_1 = amount
            return
        if self.__extra_roll_1 != 10 and self.__extra_roll_1 + amount > BowlingGame.pin_amount:
            raise BowlingGame.TooManyPinsKnockedException()
        self.__extra_roll_2 = amount

    def __create_frame(self, amount: int) -> None:
        new_frame = BowlingGame.Frame()
        new_frame.add_roll(amount)
        self.__frames.append(new_frame)

    def __get_latest_frame(self) -> 'Frame':
        if len(self.__frames) == 0:
            return None
        return self.__frames[-1]

    def __is_latest_frame_incomplete(self):
        latest_frame = self.__get_latest_frame()
        return latest_frame is not None and not latest_frame.is_complete()

    def __is_finished(self) -> bool:
        return self.__has_finished_frames() and self.__has_enough_extra_rolls()

    def __has_finished_frames(self) -> bool:
        return len(self.__frames) == BowlingGame.frame_amount and self.__get_latest_frame().is_complete()

    def __has_enough_extra_rolls(self) -> bool:
        latest_frame = self.__get_latest_frame()
        if latest_frame.frame_type() == BowlingGame.FrameType.SPARE:
            return self.__extra_roll_1 is not None
        if latest_frame.frame_type() == BowlingGame.FrameType.STRIKE:
            return self.__extra_roll_2 is not None
        return True

    def __calculate_score(self) -> int:
        frame_rolls = []
        rolls_multiplicators = [1, 1]
        for frame in self.__frames:
            frame_rolls += frame.rolls()
            rolls_multiplicators = self.__updated_multiplicators(rolls_multiplicators, frame.frame_type())
        return self.__calculate_frame_score(frame_rolls, rolls_multiplicators) + \
            self.__extra_rolls_score(rolls_multiplicators)

    def __extra_rolls_score(self, rolls_multiplicators: list) -> int:
        score = 0
        if self.__extra_roll_1 is not None:
            score = self.__extra_roll_1 * (rolls_multiplicators[-2] - 1)
        if self.__extra_roll_2 is not None:
            score += self.__extra_roll_2 * (rolls_multiplicators[-1] - 1)
        return score

    @staticmethod
    def __calculate_frame_score(rolls: list, rolls_multiplicators: list) -> int:
        score = 0
        for i in range(0, len(rolls)):
            score += rolls[i] * rolls_multiplicators[i]
        return score

    @staticmethod
    def __updated_multiplicators(multiplicators: list, frame_type: 'FrameType') -> list:
        if frame_type == BowlingGame.FrameType.SPARE:
            return multiplicators + [2, 1]
        if frame_type == BowlingGame.FrameType.STRIKE:
            last_updated = multiplicators
            last_updated[-1] = last_updated[-1] + 1
            return last_updated + [2]
        return multiplicators + [1, 1]

    def __str__(self):
        string = '['
        for frame in self.__frames:
            string += frame.__str__()
        if self.__is_finished():
            string += '(' + str(self.__extra_roll_1) + ',' + str(self.__extra_roll_2) + ')'
        string += ']'
        return string

    class NotFinishedException(Exception):
        pass

    class AlreadyFinishedException(Exception):
        pass

    class TooManyPinsKnockedException(Exception):
        pass

    class Frame:
        def __init__(self):
            self.__roll_1 = None
            self.__roll_2 = None

        def add_roll(self, roll: int) -> None:
            if self.__roll_1 is not None:
                self.__roll_second(roll)
                return
            if roll > BowlingGame.pin_amount:
                raise BowlingGame.TooManyPinsKnockedException
            self.__roll_1 = roll

        def rolls(self) -> list:
            rolls = []
            if self.__roll_1 is not None:
                rolls.append(self.__roll_1)
            if self.__roll_2 is not None:
                rolls.append(self.__roll_2)
            return rolls

        def __roll_second(self, roll: int) -> None:
            if self.__roll_1 + roll > BowlingGame.pin_amount:
                raise BowlingGame.TooManyPinsKnockedException
            self.__roll_2 = roll

        def is_complete(self) -> bool:
            is_complete = self.__roll_1 is not None and self.__roll_1 == BowlingGame.pin_amount
            is_complete |= self.__roll_2 is not None
            return is_complete

        def frame_type(self) -> 'BowlingGame.FrameType':
            if self.__roll_1 == BowlingGame.pin_amount:
                return BowlingGame.FrameType.STRIKE
            if self.__roll_1 + self.__roll_2 == BowlingGame.pin_amount:
                return BowlingGame.FrameType.SPARE
            return BowlingGame.FrameType.NORMAL

        def __str__(self) -> str:
            return '(' + str(self.__roll_1) + ',' + str(self.__roll_2) + ') '

    class FrameType(Enum):
        NORMAL = 1
        SPARE = 2
        STRIKE = 3
