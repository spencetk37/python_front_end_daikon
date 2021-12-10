def add_elems_i_j(my_list, i, j):
    return my_list[i] + my_list[j]

# Driver Code
if __name__ == "__main__":
    pairs_sum = 0
    my_list = list(range(0, 10))
    for i in my_list:
        for j in my_list:
            pairs_sum += add_elems_i_j(my_list, i, j)

