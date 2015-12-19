#!/usr/bin/env python

from os.path import *
import glob
import re
import json


pgn_dir = 'pgn'
index_file = 'pgn_index.json'


#PGN tag names, as per PGN spec
EVENT_TAG = 'Event'

#PGN parsing states
PARSE_START = 0
PARSE_TAGS = 1
PARSE_MOVES = 2


def main():
	global index_file, pgn_dir

	normalize_paths()

	print 'Updating game metadata...'
	all_metadata = []
	for pgn_file_path in glob.glob(join(pgn_dir, '*.pgn')):
		pgn_file = basename(pgn_file_path)
		print 'Processing pgn file: ' + pgn_file

		pgn_games_data = parse_pgn(pgn_file_path)
		#dump_games(pgn_data)
		add_file_metadata(all_metadata, pgn_file, pgn_games_data)

	write_metadata(all_metadata, index_file)

	print 'Updated index file [' + index_file + ']'


def parse_pgn(pgn_file):
	with open(pgn_file, 'r') as f:
		state = PARSE_START
		pgn_data = []
		i_line = 0
		for line in f:
			line = line.strip()

			if line.startswith('['):
				#TODO: process tag
				#print 'Tag found: ' + line
				if state == PARSE_START:
					curr_game = {}
					state = PARSE_TAGS
				elif state == PARSE_MOVES:
					parse_error(pgn_file, i_line)
					store_game(pgn_data, curr_game)
					curr_game = {}
					state = PARSE_TAGS
				else:
					#continuing tags for curr game
					pass

				tag_name, tag_value = parse_tag(line)
				curr_game[tag_name] = tag_value

			elif line.startswith('1. '): #TODO: make movetext parsing more robust
				if state == PARSE_START or state == PARSE_TAGS:
					parse_error(pgn_file, i_line)
					curr_game = {}
					state = PARSE_MOVES

				#ignore movetext, we only need metadata


			elif line == '':
				if state == PARSE_START:
					pass
				elif state == PARSE_TAGS:
					state = PARSE_MOVES

				elif state == PARSE_MOVES:
					add_game_metadata(pgn_data, curr_game)
					state = PARSE_START
				else:
					parse_error(pgn_file, i_line)

			else:
				parse_error(pgn_file, i_line)
				store_game(pgn_data, curr_game)
				state = PARSE_START

			i_line = i_line + 1

	return pgn_data


def parse_tag(line):
	#tagline_regex = re.compile(r'\[(.+)\] \[\"(.+)\"\]')
	tagline_regex = re.compile('^(.+) "(.+)"$')
	m = tagline_regex.match(line[1:-1])
	return m.group(1), m.group(2)


def normalize_paths():
	global index_file, pgn_dir
	index_file = join(dirname(realpath(__file__)), index_file)
	pgn_dir = join(dirname(realpath(__file__)), pgn_dir)


def parse_error(pgn_file, i_line):
	print '!! Parse error at line ' + str(i_line) + ' of file ' + pgn_file

def add_game_metadata(pgn_data, curr_game):
	if not curr_game is None and len(curr_game) > 0:
		pgn_data.append(curr_game)


def add_file_metadata(all_metadata, pgn_file, games_data):
	pgn_label = pgn_file
	#use event name as label if present
	for g in games_data:
		if EVENT_TAG in g:
			pgn_label = g[EVENT_TAG]
			break

	pgn_data = {}
	pgn_data['file'] = 'pgn/' + pgn_file
	pgn_data['label'] = pgn_label
	pgn_data['games'] = games_data
	all_metadata.append(pgn_data)


def dump_games(pgn_data):
	for g in pgn_data:
		print '------'
		for k in g:
			print k + ':', g[k]


def write_metadata(pgn_data, index_file):
	with open(index_file, 'w') as f:
		json.dump(pgn_data, f)


if __name__ == '__main__':
	main()
