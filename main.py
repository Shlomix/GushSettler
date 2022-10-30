import copy


def round_fairly(amount):
    rounding_diff = sum(amount)
    i = 0
    while rounding_diff != 0:
        if amount[i] < 0:
            d = -1 if rounding_diff > 0 else 1
            amount[i] += d
            rounding_diff += d
        i += 1
        if i == len(amount):
            i = 0
    return amount


def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        for t, subset in enumerate(smaller):
            yield smaller[:t] + [[first] + subset] + smaller[t + 1:]
        yield [[first]] + smaller


def min_cash_flow(gents, balance):
    max_credit_idx = balance.index(max(balance))
    max_debit_idx = balance.index(min(balance))

    if balance[max_credit_idx] == 0. and balance[max_debit_idx] == 0.:
        return 0

    min_ = min(-balance[max_debit_idx], balance[max_credit_idx])
    balance[max_credit_idx] -= min_
    balance[max_debit_idx] += min_

    print(f"{gents[max_debit_idx]} pays {min_} to {gents[max_credit_idx]}")

    min_cash_flow(gents, balance)


def settle_it():
    assert set(INIT_BALANCE.keys()) <= set(GENTS), 'Some of the creditors are non-GENTS!'
    assert all(c >= 0 for c in INIT_BALANCE.values())

    total_amount = sum(INIT_BALANCE.values())
    per_person = total_amount / len(GENTS)

    X = [INIT_BALANCE.get(g, 0) - per_person for g in sorted(GENTS)]

    RE_BALANCE = list(zip(sorted(GENTS), X))
    best_partitions = {}
    for curr_p in partition(RE_BALANCE):
        for t in range(THRESHOLD + 1):
            if all(abs(sum(map(lambda x: x[1], subset_curr_p))) <= t
                   for subset_curr_p in curr_p):
                if len(curr_p) > len(best_partitions.get(t, [])):
                    best_partitions[t] = copy.deepcopy(curr_p)

    for t, best_p in best_partitions.items():
        print()
        print(f"Allowing approximation up to {t} shekels:")
        print("------------------------------")
        for subset in best_p:
            gens_sub, amount_sub = list(zip(*subset))
            amount_sub = list(amount_sub)
            if t != 0:
                amount_sub = round_fairly(list(map(int, amount_sub)))
            min_cash_flow(gens_sub, amount_sub)
        print()
        print(f"Total Transactions: {len(GENTS) - len(best_p)}")
        print()


if __name__ == '__main__':
    GENTS = (
        'Artyom', 'Dima', 'Giora', 'Jenia', 'Leon', 'Rafi', 'Shlomi', 'Tomer'
    )

    INIT_BALANCE = {
        'Artyom': 12,
        'Leon': 181,
        'Jenia': 180,
    }

    THRESHOLD = 10

    settle_it()
