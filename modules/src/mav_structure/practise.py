class ManipulateList:
    li: list = []
    iteration_count = 0

    def __init__(self, li) -> None:
        self.li = li

    def remove_duplicate(self):
        di = {}
        fined_li = []
        for item in self.li:
            if item not in di:
                di[item] = item
        for key in di:
            fined_li.append(key)
        return fined_li

    def find_highest_or_lowest_in_list(self):
        highest_num = self.li[0]  # checksum
        lowest_num = self.li[0]
        for index in range(len(self.li)):
            if self.li[index] > highest_num:
                highest_num = self.li[index]
            elif self.li[index] < lowest_num:
                lowest_num = self.li[index]
        return f'highest number in list is {highest_num} and lowest number is {lowest_num}'

    def rearrange_items_in_list(self):  # in ascending and descending order both
        for index in range(1, len(self.li)):
            pass

    @staticmethod
    def sequential_search(li, item):
        found = False
        pos = 0
        while pos < len(li) and not found:
            if li[pos] == item:
                found = True
            else:
                pos += 1
        return found

    @staticmethod
    def sequential_search_ordered_list(li: list, item):  # ordered_list = [10,12,34,56,89,90], 13
        pos = 0
        found = False
        stop = False
        while pos < len(li) and not found and not stop:
            print('iteration count', pos)
            if li[pos] == item:
                found = True
            elif li[pos] > item:
                stop = True
            else:
                pos += 1
        return found

    @staticmethod
    def binary_search_ordered_list(ordered_list, item):  # assuming list is an ordered list
        found = False
        first_index = 0
        last_index = len(ordered_list) - 1
        while first_index < last_index and not found:
            middile_index = (first_index + last_index) // 2
            print('Middle index', middile_index)
            if li[middile_index] == item:
                found = True
            elif item < li[middile_index]:
                last_index = middile_index - 1
            else:
                first_index = middile_index + 1
        return found

    @staticmethod
    def binary_search_without_while(ordered_list, item):  # [12,13,17,19,21]
        first_index = 0
        last_index = len(ordered_list) - 1
        for _ in ordered_list:
            if first_index < last_index:
                print('last_index after first iteration', last_index)
                middle_index = (first_index + last_index) // 2
                print('middle index', middle_index)
                if ordered_list[middle_index] == item:
                    return True
                elif item < ordered_list[middle_index]:
                    last_index = middle_index - 1
                else:
                    first_index = middle_index + 1
        return False

    @staticmethod
    def pattern_list(pt: list):  # [123, 412, 67], save in a sequence of 3 from - [1, 2, 3, 4, 1, 2, 6, 7]
        for index in range(0, len(pt), 3):
            # first iteration 0:3
            # 0,3,6,9,12
            print(pt[index:index + 3])
        return

    @staticmethod
    def sorting_list(li: list) -> list:  # [5,6,1,9,0]
        pass

    @staticmethod
    def find_missing_number(li: list, diff: int) -> int:
        """
        :param li: [1,2,3,4,5,7], [1,3,6,9,13]
        :param diff: 1, 2, 3 etc
        :return: int
        """
        start = li[0]
        index: int
        for i in range(1, len(li)):
            if li[i] - start == diff:
                start = li[i]
            else:
                index = start + 1
                break
        return index


obj = ManipulateList
print(obj.find_missing_number([1, 2, 3, 4, 5, 6, 7, 9], 1))


class MatrixGyan:
    rows: int
    columns: int

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def create_matrix(self):
        li = []
        refined_li = []
        for i in range(self.rows):  # 0,1,2
            internal_list = []  # reinitializing the internal_list after every iteration
            for j in range(self.columns):  # 0,1,2,3
                _add = i + j
                internal_list.append(_add)
            li.append(internal_list)
        # add all the elements of the created matrix
        column_sums = [0] * len(li[0])  # [0,0,0,0]
        for row in li:
            for i in range(len(row)):
                column_sums[i] += row[i]
        return li, column_sums

    def add_two_matrix(self):
        a = [1, 2, 3]
        b = [4, 5, 6]
        new_li = []
        for i in range(len(a)):
            for j in range(len(b)):
                if i == j:
                    new_li.append(a[i] + b[j])
        return new_li

    @staticmethod
    def transpose_matrix(matrix):
        """
        In-place is possible when we have a balanced matrix, 2*2, 3*3 etc
        #  matrix = [
        #     [1, 2, 3],
        #     [4, 5, 6],
            [5, 7, 9]
        # ]
        # Output:
        # [
        # [1,4], [2,5], [3,6]
        # ]
        """
        for i in range(len(matrix)):
            for j in range(i + 1, len(matrix)):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        return matrix

    @staticmethod
    def identify_pattern_in_matrix(matrix):
        """
            :param matrix: list = [
            [1,0,3],
            [4,5,6],
            [7,8,9]
        ]
        :return: list = [
            [0,0,0],
            [4,0,6],
            [7,0,9]
        ]
        """
        position: int
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:

                    matrix[i] = [0,0,0]
        print(position)
        return matrix



    @staticmethod
    def make_dict(input_matrix: list) -> dict:
        """
        input matrix would be like = [[], ['prakash', 'singh'], ['sakshi', 'singh']]
        :return: {'prakash': singh, 'sakshi': 'singh'}
        """
        final_di = {}
        for item in input_matrix:
            if item:
                for index in range(0, len(item), 2):
                    final_di[item[index]] = item[index + 1]
        return final_di


class LinkedListNode:
    def __init__(self):
        pass

# 2 - input digit = [1,2,9] # output = [1,3,0], input = [9], output = [1,0] -> add 1 in last digit
# 3 - cover 2nd through linked list

matrix = [
    [1,2,3],
    [4,0,6],
    [7,8,9]
]
out_put = [
    [0,0,0],
    [4,0,6],
    [7,0,9]
]
obj = MatrixGyan
print(obj.identify_pattern_in_matrix(matrix))
