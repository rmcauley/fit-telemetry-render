from src.fit import get_fit_dict

d = get_fit_dict("e:\\downloads\\test.fit")
for k, v in d.items():
    print(k, v)