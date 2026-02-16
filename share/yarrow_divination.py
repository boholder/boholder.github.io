#!/usr/bin/env python3
import functools
import random
from time import sleep
from typing import Callable

# There is a blog post (in Chinese) about this topic which provides more information about yarrow divination.
# https://boholder.github.io/blogs/yarrow-divination-zh/

# 每步骤展示停顿时间
display_interval_sec = 0

# 大衍之数五十
DIVINE_NUM = 50
# 事物本质（起源）
NATURE_NUM = 1
# 其用四十有九
INIT_NUM = DIVINE_NUM - NATURE_NUM


def divide_into_two(total: int) -> tuple[int, int]:
    """分而为二以象二"""
    one_pile = random.SystemRandom().randint(1, total)
    return one_pile, total - one_pile


def pike_one_out(two_piles: tuple[int, int]) -> tuple[int, int]:
    """掛一以象三"""
    take_which = random.SystemRandom().randint(0, 1)
    return two_piles[take_which] - 1, two_piles[abs(take_which - 1)]


def repeat_pike_four_out(two_piles: tuple[int, int]):
    """揲之以四以象四时"""
    return tuple(map(lambda n: list(range(n, 0, -4)), two_piles))


def hold_remainders_between_fingers(two_seq: tuple[list[int], list[int]]) -> int:
    """归奇於扐以象闰"""

    # 有时候上面方法把某一个堆变成0，在揲之以四时会变成空列表，引发下面索引取数抛异常
    two_seq = tuple(map(lambda lst: [0] if not lst else lst, two_seq))

    def hold(lst: list[int]):
        remainder = lst[-1]
        print(f'归於扐: {remainder}')
        return remainder

    return functools.reduce(lambda a, b: a + b, [lst[0] - hold(lst) for lst in two_seq])


def four_operations(total: int):
    """四营成易"""

    def display(func: Callable, param):
        print(func.__doc__)
        result = func(param)
        print(result)
        sleep(display_interval_sec)
        return result

    ops = [total, divide_into_two, pike_one_out, repeat_pike_four_out, hold_remainders_between_fingers]
    return functools.reduce(lambda param, func: display(func, param), ops)


def three_transformation():
    """三变成爻"""

    i = 1

    def display(func, param):
        nonlocal i
        print(f'--第{i}变--')
        i += 1
        return func(param)

    remain = functools.reduce(lambda param, func: display(func, param), [INIT_NUM] + [four_operations] * 3)
    return round(remain / 4)


def generate_hexagram():
    """十有八变而成卦"""

    types = ['老阴 X', '少阳 —', '少阴 - -', '老阳 O']
    # 从wikipedia上复制来的
    sixty_four_hexagrams = ['坤', '剥', '比', '观', '豫', '晋', '萃', '否', '谦', '艮', '蹇', '渐', '小过',
                            '旅', '咸', '遁', '师', '蒙', '坎', '涣', '解', '未济', '困', '讼', '升', '蛊',
                            '井', '巽', '恒', '鼎', '大过', '姤', '复', '颐', '屯', '益', '震',
                            '噬嗑', '随', '无妄', '明夷', '贲', '既济', '家人', '丰', '离',
                            '革', '同人', '临', '损', '节', '中孚', '归妹', '睽', '兑',
                            '履', '泰', '大畜', '需', '小畜', '大壮', '大有', '夬', '乾']
    i = 1

    def display(func):
        nonlocal i
        print(f'====第{i}爻====')
        i += 1
        num = func()
        print(f'第{i}爻： {num} {types[num - 6]}')
        return num

    def change_yinyang(num: int) -> bool:
        if (num == 6 or num == 9) and random.SystemRandom().randint(0, 1):
            # 变爻， 6老阴 -> 阳， 9老阳 -> 阴
            return [True, True, False, False][num - 6]
        else:
            # 不变爻
            return num % 2 == 0

    # 传统是从下往上写爻，第一爻在卦象最下面，第六爻在最上面。
    # 但因为卦象列表的索引顺序是从上向下（剥=从上向下100000），两反相抵，故输出爻次序不变。
    marks = [display(three_transformation) for _ in range(6)]

    print('====总结====')

    explanations = list(map(lambda n: f'{n} {types[n - 6]}', marks))
    print(f'六爻：{explanations}')

    origin_binary = ''.join(list(map(lambda n: '0' if n % 2 == 0 else '1', marks)))
    origin_hexagram = sixty_four_hexagrams[int(origin_binary, 2)]
    print(f'本卦：{origin_binary} {origin_hexagram}')

    changed_binary = ''.join(list(map(lambda n: '0' if change_yinyang(n) else '1', marks)))
    changed_hexagram = sixty_four_hexagrams[int(changed_binary, 2)]
    print(f'变卦：{changed_binary} {changed_hexagram}')

    print('\n请谷先生解卦：')
    print(f'解本卦： https://google.com/search?q=易经+{origin_hexagram}卦')
    print(f'解变卦： https://google.com/search?q=易经+{changed_hexagram}卦')


if __name__ == "__main__":
    generate_hexagram()

# ====第1爻====
# --第1变--
# 分而为二以象二
# (28, 21)
# 掛一以象三
# (27, 21)
# 揲之以四以象四时
# ([27, 23, 19, 15, 11, 7, 3], [21, 17, 13, 9, 5, 1])
# 归奇於扐以象闰
# 归於扐: 3
# 归於扐: 1
# 44
#
# ...
#
# ====总结====
# 六爻：['6 老阴 X', '6 老阴 X', '6 老阴 X', '6 老阴 X', '6 老阴 X', '6 老阴 X']
# 本卦：000000 坤
# 变卦：011100 恒
#
# 请谷先生解卦：
# 解本卦： https://google.com/search?q=易经+坤卦
# 解变卦： https://google.com/search?q=易经+恒卦
