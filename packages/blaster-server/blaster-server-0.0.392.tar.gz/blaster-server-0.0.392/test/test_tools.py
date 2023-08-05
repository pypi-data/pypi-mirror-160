from blaster.tools import get_time_overlaps, retry,\
	SanitizedDict, SanitizedList
from datetime import datetime
from blaster.utils.data_utils import parse_string_to_units, parse_currency_string

_all_funcs_ = {}


def Test(func):
	if(callable(func)):
		_all_funcs_[func.__name__] = func
		return func
	else:
		def wrapper(func2):
			_all_funcs_[func] = func2
			return func2
		return wrapper


@Test
def sanitization():
	sd = SanitizedDict(a="<a>", b="<b>")
	sd["c"] = "<c>"
	sd["d"] = {"e": "<e>", "f": "<f>"}

	for k, v in sd.items():
		print(k, v)
	for k, v in sd["d"].items():
		print(k, v)

	sl = SanitizedList(["<a>", "<b>"])
	sl.append({"c": "<c>", "d": "<d>"})
	sl.extend(["<e>", "<f>"])
	for i in sl:
		print(i)
	for k, v in sl[2].items():
		print(k, v)


@Test
def overlaps():
	print(
		get_time_overlaps(
			datetime(year=2021, month=10, day=1),
			datetime(year=2021, month=10, day=20),
			["Monday 10:30 - 12:30|100EUR", "Tuesday 10:30|200EUR"],
			exclude=["05/10/2021 10:30"]
		)
	)
	print(
		get_time_overlaps(
			datetime(year=2021, month=10, day=1),
			datetime(year=2021, month=10, day=20),
			["5/12/2021 10:30 - 12:30", "07/12/2021 10:30"]
		)
	)
	print(
		get_time_overlaps(
			datetime(year=2021, month=10, day=1),
			datetime(year=2021, month=10, day=20),
			["5/10/2021 10:30 - 6/10/2021 11:30"]
		)
	)

	print(
		get_time_overlaps(
			datetime(year=2021, month=10, day=1),
			datetime(year=2021, month=10, day=20),
			["5/10/2021 10:30 - 6/10/2021 11:30"],
			milliseconds=True
		)
	)

	print(
		get_time_overlaps(
			datetime(year=2022, month=6, day=19),
			datetime(year=2022, month=6, day=27),
			"Monday 2:30 p.m - 6:30 p.m , Tuesday 9:30 a.m-12:30 p.m,  Tuesday 2:30 p.m-6:30 p.m, Wednesday 9:30 a.m - 12:30 p.m, Wednesday 2:30 p.m- 6:30 p.m, Thursday 9:30 a.m -12:30 p.m, Thursday 2:30 p.m-6:30 p.m, Friday 9:30 a.m- 12:30p.m, Friday 2:30 p.m-6:30 p.m, Saturday 9:30 a.m-12:30 p.m",
		)
	)


@Test("retries")
@retry(2)
def test_can_retry():
	raise Exception


@Test
def string_to_units():
	print(parse_string_to_units(".9 units"))
	print(parse_string_to_units("0.9 units"))
	print(parse_string_to_units("rs -1.9"))
	print(parse_currency_string("INR 2000"))


if __name__ == "__main__":
	import sys
	# check and run specific funcs
	for test_name in sys.argv[1:]:
		if(test_name in _all_funcs_):
			_all_funcs_[test_name]()
	# run all funcs
	if(len(sys.argv) < 2):
		for _func in _all_funcs_.values():
			_func()
