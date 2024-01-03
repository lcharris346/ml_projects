# RESOURCES
import os
import sys
import argparse
import random
import time
import copy

# CONSTANTS
ITEMS = {
	"022s":{"val": 2, "cat": 4}, 
	"033s":{"val": 3, "cat": 4}, 
	"044s":{"val": 4, "cat": 4}, 
	"055s":{"val": 5, "cat": 4}, 
	"066s":{"val": 6, "cat": 4}, 
	"077s":{"val": 7, "cat": 4}, 
	"088s":{"val": 8, "cat": 4}, 
	"099s":{"val": 9, "cat": 4}, 
	"10Ts":{"val": 10, "cat": 4}, 
	"11Js":{"val": 11, "cat": 4}, 
	"12Qs":{"val": 12, "cat": 4}, 
	"13Ks":{"val": 13, "cat": 4}, 
	"14As":{"val": 14, "cat": 4},

	"022h":{"val": 2, "cat": 3}, 
	"033h":{"val": 3, "cat": 3}, 
	"044h":{"val": 4, "cat": 3}, 
	"055h":{"val": 5, "cat": 3}, 
	"066h":{"val": 6, "cat": 3}, 
	"077h":{"val": 7, "cat": 3}, 
	"088h":{"val": 8, "cat": 3}, 
	"099h":{"val": 9, "cat": 3}, 
	"10Th":{"val": 10, "cat": 3}, 
	"11Jh":{"val": 11, "cat": 3}, 
	"12Qh":{"val": 12, "cat": 3}, 
	"13Kh":{"val": 13, "cat": 3}, 
	"14Ah":{"val": 14, "cat": 3},

	"022d":{"val": 2, "cat": 2}, 
	"033d":{"val": 3, "cat": 2}, 
	"044d":{"val": 4, "cat": 2}, 
	"055d":{"val": 5, "cat": 2}, 
	"066d":{"val": 6, "cat": 2}, 
	"077d":{"val": 7, "cat": 2}, 
	"088d":{"val": 8, "cat": 2}, 
	"099d":{"val": 9, "cat": 2}, 
	"10Td":{"val": 10, "cat": 2}, 
	"11Jd":{"val": 11, "cat": 2}, 
	"12Qd":{"val": 12, "cat": 2}, 
	"13Kd":{"val": 13, "cat": 2}, 
	"14Ad":{"val": 14, "cat": 2},

	"022c":{"val": 2, "cat": 1}, 
	"033c":{"val": 3, "cat": 1}, 
	"044c":{"val": 4, "cat": 1}, 
	"055c":{"val": 5, "cat": 1}, 
	"066c":{"val": 6, "cat": 1}, 
	"077c":{"val": 7, "cat": 1}, 
	"088c":{"val": 8, "cat": 1}, 
	"099c":{"val": 9, "cat": 1}, 
	"10Tc":{"val": 10, "cat": 1}, 
	"11Jc":{"val": 11, "cat": 1}, 
	"12Qc":{"val": 12, "cat": 1}, 
	"13Kc":{"val": 13, "cat": 1}, 
	"14Ac":{"val": 14, "cat": 1},
}

ITEMS_KEYS = list(ITEMS.keys())

CATEGORY = {
	"s": 4, "h": 3, "d": 2, "c":1
}

CATEGORY_KEYS = list(CATEGORY.keys())

RETURNS_JoB_9_6 = {
	'RF': 800,
	'SF': 50,
	'4K': 25,
	'FH': 9,
	'F':  6,
	'S':  4,
	'3K': 3,
	'2P': 2,
	'JoB':1,
}

RETURNS_KEYS = list(RETURNS_JoB_9_6.keys())

NUM_ITEMS = range(1,6)

ALL_ITEMS = "12345"

NO_ITEMS = ""

STRAIGHT = [1,1,1,1]
AL_STRAIGHT = [1,1,1,9]
FLUSH = [0,0,0,0]
FOUR_TO_A_STRIGHT = [1,1,1]
FOUR_TO_A_STRIGHT2 = [1,1,9]
FOUR_TO_A_FLUSH = [0,0,0]
THREE_TO_A_FLUSH = [0,0]

THREE_TO_RF = (
	range(11,14),
	range(10,13),
	range(9,12),
	range(8,11),
	range(7,10),
	range(6,9),
	range(5,8),
	range(4,7),
	range(3,6),
	range(2,5),
	range(1,4),
)


QUIT = ("q", "quit")

ALL = ("a", "all")
NONE = ("n", "none")

# TESTS
GROUP_RF =   ["10Ts", "11Js", "12Qs", "13Ks", "14As"]
GROUP_SF =   ["022s", "033s", "044s", "055s", "066s"]
GROUP_ALSF = ["14As", "022s", "033s", "044s", "055s"]
GROUP_4K =   ["022s", "022h", "022d", "022c", "055d"]
GROUP_FH =   ["022s", "022h", "022d", "055h", "055d"]
GROUP_F =    ["022s", "033s", "044s", "055s", "077s"]
GROUP_S =    ["022s", "033s", "044s", "055s", "066h"]
GROUP_3K =   ["022s", "022h", "022d", "055h", "088d"]
GROUP_2P =   ["022s", "022h", "055s", "055h", "088d"]
GROUP_JoB =  ["11Js", "11Jh", "055s", "077h", "088d"]

# FUNCTIONS
def is_rf(group):
	condition = False 
	if group["d_cats"] == FLUSH and group["d_vals"] == STRAIGHT and group["vals"][4] == 14:
		condition = True
	return condition

def is_sf(group):
	condition = False 
	if group["d_cats"] == FLUSH and group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
		condition = True
	return condition

def is_4k(group):
	condition = False
	if group["d_vals"].count(0) == 3 and \
		(
			(group["d_vals"][0] == 0 and group["d_vals"][1] == 0 and group["d_vals"][2] == 0) or 
			(group["d_vals"][1] == 0 and group["d_vals"][2] == 0 and group["d_vals"][3] == 0)
		):
		condition = True
	return condition

def is_fh(group):
	condition = False
	if group["d_vals"].count(0) == 3 and \
		(
			(group["d_vals"][0] == 0 and group["d_vals"][1] == 0 and group["d_vals"][3] == 0) or 
			(group["d_vals"][0] == 0 and group["d_vals"][2] == 0 and group["d_vals"][3] == 0)
		):
		condition = True
	return condition

def is_f(group):
	condition = False 
	if group["d_cats"] == FLUSH:
		condition = True
	return condition

def is_s(group):
	condition = False
	if group["d_vals"] in (STRAIGHT, AL_STRAIGHT):
		condition = True
	return condition

def is_3k(group):
	condition = False
	if group["d_vals"].count(0) == 2 and \
		(
			(group["d_vals"][0] == 0 and group["d_vals"][1] == 0) or 
			(group["d_vals"][1] == 0 and group["d_vals"][2] == 0) or 
			(group["d_vals"][2] == 0 and group["d_vals"][3] == 0)
		):
		condition = True
	return condition

def is_2p(group):
	condition = False
	if group["d_vals"].count(0) == 2:
		condition = True
	return condition

def is_job(group):
	condition = False 
	if group["d_vals"].count(0) == 1:
		index = group["d_vals"].index(0)
		if group["vals"][index] > 10:
			condition = True
	return condition