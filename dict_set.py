# %%
d = {'b': 1, 'a': 2, 'c': 10}
d.items()
# %%
# ascending sort based on keys
d_sorted_by_key = sorted(d.items(), key=lambda x: x[0])
d_sorted_by_key
# %%
# ascending sort based on values
d_sorted_by_value = sorted(d.items(), key=lambda x: x[1])
d_sorted_by_value
# %%

# find unique values using set


def find_unique_price_using_set(products):
    unique_price_set = set()
    for _, price in products:
        unique_price_set.add(price)
    return len(unique_price_set)


products = [
    (143121312, 100),
    (432314553, 30),
    (32421912367, 150),
    (937153201, 30)
]
print('number of unique price is: {}'.format(
    find_unique_price_using_set(products)))


# %%
