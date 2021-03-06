def display(array):
    """
    :param array:
    this function print Tic tac toe ground game
    :return:
    """
    for i in range(0, 7, 3):
        x = shap(array[i])
        y = shap(array[i + 1])
        z = shap(array[i + 2])
        print("{0} | {1} | {2}".format(x, y, z))
        print("- - - - - ")


def shap(item):
    """
    item :
    true
    or
    false
    or
    None
    :param item:

    if item be true
        we return shape of man player

    elif item be false
        we return shape of machine player

    else
        our grand be empty
    :return:
    """
    if item:
        return "X"
    elif item == False:
        return "O"
    else:
        return " "


def find_number(array, param):
    """
    :param array:
     array of true and false
    :param param:
    true or false
    :return:
    number of how much item mush put in this array to full and player be win
    if there are one or more item of other player we return 3
    """
    if array.count(not param) == 0:
        return 3 - array.count(param)
    else:
        return 3


def find_herustic(array, param):
    """

    :param array:
    our ground
    :param param:
    :return:
    find in each way what is the number that we need to be win
    """
    list_herustic = [find_number(array[:3], param), find_number(array[3:6], param), find_number(array[6:], param),
                     find_number([array[2], array[5], array[8]], param),
                     find_number([array[1], array[4], array[7]], param),
                     find_number([array[0], array[3], array[6]], param),
                     find_number([array[2], array[4], array[6]], param),
                     find_number([array[0], array[4], array[8]], param)]

    return min(list_herustic)


class Tree:
    """
    this our min max tree
    """

    def __init__(self, array, is_Man):

        """
        :param array:
        our ground
        :param is_Man:
        show we want to show this min max tree of human or machine
        """
        self.is_Man = is_Man
        self.array = array.copy()
        # number of item in ground
        self.size_array = self.array.count(True) + self.array.count(False)
        self.man_win_with_how_much_move = find_herustic(self.array, True)
        self.machine_win_with_how_much_move = find_herustic(self.array, False)
        self.Next_child = []

    def is_array_full(self):
        return True if self.size_array == 9 else False

    def find_best_way(self):
        """
        this function make min max tree for this tree and find best way that we can choice for next move
        :return:
        """

        self.make_depth(False, 4)
        """
        with this we make for 4 level of tree 
        to find best way by predict in 4 level of tree 
        """
        cost_move = -100
        array = []

        for k in self.Next_child:

            temp = k.find_cost_way()
            # print(temp)
            if cost_move < temp:
                array = k.array.copy()
                cost_move = temp

        return array

    def make_depth(self, Binery, number):

        if number > 0:
            if self.array[4] is None:
                f = self.array.copy()
                f[4] = Binery
                self.Next_child.append(Tree(f, not Binery))

            for i in range(len(self.array)):
                if self.array[i] is None:
                    f = self.array.copy()
                    f[i] = Binery
                    self.Next_child.append(Tree(f, not Binery))

        for k in self.Next_child:
            k.make_depth(not Binery, number - 1)

    def find_cost_way(self):

        if self.Game_stat() == -1 and self.is_Man:
            """
            if machine win and next move is human move
            """
            return 10

        elif self.Game_stat() == 1 and not self.is_Man:
            """
            if human win and next move is machine move
            """

            return -10

        elif self.is_array_full():
            """
                if ground is full and we search condition of game that we win or human win or No one is win
            """
            if self.Game_stat() == -1:
                return 10
            elif self.Game_stat() == 1:
                return -10
            else:
                return 0



        elif len(self.Next_child) == 0 and self.is_Man:

            return self.man_win_with_how_much_move * -1

        elif len(self.Next_child) == 0 and not self.is_Man:

            return 3 - self.machine_win_with_how_much_move

        else:

            if self.is_Man:

                cost_move = 100

                for k in self.Next_child:
                    temp = k.find_cost_way()
                    if cost_move > temp:
                        cost_move = temp

                return cost_move

            else:

                cost_move = -100
                for k in self.Next_child:
                    temp = k.find_cost_way()
                    if cost_move < temp:
                        cost_move = temp
                return cost_move

    def Game_stat(self):

        if self.man_win_with_how_much_move == 0:
            return 1
        elif self.machine_win_with_how_much_move == 0:
            return -1
        else:
            return 0


def main():
    """
    Game_state == 1 User_win
    Game_state == -1 Machine Win
    Game_state == 0 No one win
    """

    Game_state = 0
    array = [None for i in range(9)]
    tree = Tree(array, True)
    display(array)
    while not tree.is_array_full() and Game_state == 0:

        number_choice = int(input("Please Enter your choice square az 1 to 9 and this square must be empty : "))
        while True:

            if 0 < number_choice < 10 and array[number_choice - 1] is None:
                array[number_choice - 1] = True
                tree = Tree(array, True)
                break
            else:
                number_choice = int(input("Please Enter your choice square az 1 to 9 and this square must be empty : "))
        Game_state = tree.Game_stat()
        if tree.is_array_full() or Game_state == 1:
            break
        array = tree.find_best_way()
        tree = Tree(array, False)
        display(array)
        Game_state = tree.Game_stat()

    print("#########################")

    if Game_state == 0:

        display(array)
        print("No one is win")

    elif Game_state == 1:
        display(array)
        print("you  Win")

    else:
        display(array)
        print("Machine win")


if __name__ == '__main__':
    main()
