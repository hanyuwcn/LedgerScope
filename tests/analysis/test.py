from src.utils import fmt

if __name__ == "__main__":
    VARIABLE_FORMATTING_MAP_2 = {

    }

    # formatted_string = VARIABLE_FORMATTING_MAP.get(EXPENSE, lambda v: str(v))(123456.789)
    # print(formatted_string)

    v = 6543210.78956
    # v = 0.26456
    print(fmt(v))
    # print(fmt(v, 1))
    # print(fmt(v, 2, p=True))
    print(fmt(v, s='$'))
