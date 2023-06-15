import math

amount_payment = int(input("payment: ").replace(",", ""))

# list(map(int, input("program ratio (seperator=', '): ").split(", ")))
program_price_list = [479000, 500000, 288000]
print(program_price_list)

sum_price = sum(program_price_list)
ratio_list = list(map(lambda x: x / sum_price, program_price_list))
print(ratio_list)

result_list = list(map(lambda x: math.ceil(x * amount_payment), ratio_list))
print(result_list)
