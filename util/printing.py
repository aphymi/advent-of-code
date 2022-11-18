def print_over_current(obj, clear_length: int = 0) -> None:
	printed_obj = str(obj)

	left_fill_length = max(
		0,
		clear_length - len(printed_obj),
	)

	print(printed_obj + (" " * left_fill_length), end="\r")
	# print(" " * clear_length, end="\r")
	# print(obj, end="\r")
