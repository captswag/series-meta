import sys
import os
import requests
import json

__version__ = '0.0.2'


APP_NAME = 'series_meta'

BASE_URL = 'https://api.themoviedb.org/3'
API_KEY = '9a2a9c19247fe23f3aaea69b743fb0a6'

VIDEO_FORMATS = ['mp4', 'mkv', 'avi']
SUBTITLE_FORMATS = ['srt']


def create_args_dictionary(args):
	args_dictionary = {}
	while args:
		if args[0][0] == '-':
			args_dictionary[args[0]] = args[1]
		args = args[1:]
	return args_dictionary


def create_search_url(search_query):
	return ('{base_url}/search/tv?query={search_query}&api_key={api_key}').format(base_url = BASE_URL, search_query = search_query, api_key = API_KEY)


def create_episode_list_url(tv_series_id, season_number):
	return ('{base_url}/tv/{tv_series_id}/season/{season_number}?api_key={api_key}').format(base_url = BASE_URL, tv_series_id = tv_series_id, season_number = season_number, api_key = API_KEY)


def create_tv_episode_name(tv_series_name, season_number, episode_number, tv_episode_name):
	episode_number = '%02d' % episode_number
	season_number = '%02d' % season_number
	return ('{tv_series_name} - s{season_number}e{episode_number} - {tv_episode_name}').format(tv_series_name = tv_series_name, season_number = season_number, episode_number = episode_number, tv_episode_name = tv_episode_name)  


def create_file_path(root_dir, file_name):
	return root_dir + file_name


def rename_file_name(file_path, current_file_name, expected_file_name):
	file_name_extension = os.path.splitext(current_file_name)[1]
	expected_file_name += file_name_extension
	current_file_path = create_file_path(file_path, current_file_name)
	expected_file_path = create_file_path(file_path, expected_file_name)
	os.rename(current_file_path, expected_file_path)
	print 'Renamed ' + current_file_name + ' to ' + expected_file_name

def get_file_extension(file):
	file_extension = os.path.splitext(file)[1]
	return file_extension[1:]

def is_video_file(file):
	file_extension = get_file_extension(file)
	return file_extension in VIDEO_FORMATS

def is_subtitle_file(file):
	file_extension = get_file_extension(file)
	return file_extension in SUBTITLE_FORMATS

def group_files(list):
	list_videos = []
	list_subtitles = []
	list_trash = []
	for file in list:
		if is_video_file(file):
			list_videos.append(file)
		elif is_subtitle_file(file):
			list_subtitles.append(file)
		else:
			list_trash.append(file)
	return list_videos, list_subtitles, list_trash


def main():
	args = sys.argv
	args_dictionary = create_args_dictionary(args)
	file_directory = os.getcwd()
	# file_directory should always end with a /

	try: 
		tv_series_name = args_dictionary['-s']
		season_number = args_dictionary['-n']
	except KeyError, e:
		if e.message == '-s':
			print ('{app_name}: error: You must provide a series name.').format(app_name = APP_NAME)
		elif e.message == '-n':
			print ('{app_name}: error: You must provide a series number.').format(app_name = APP_NAME)
		sys.exit()

	list_videos = []
	list_subtitles = []
	list_trash = []

	list = os.listdir(file_directory)
	list_videos, list_subtitles, list_trash = group_files(list)

	response = requests.get(create_search_url(tv_series_name))
	response_json = response.json()
	total_results = response_json['total_results']

	if total_results == 0:
		print ('ERROR: Unable to find metadata for {tv_series_name}').format(tv_series_name = tv_series_name)
		sys.exit()

	tv_series_id = response_json['results'][0]['id']
	response = requests.get(create_episode_list_url(tv_series_id, season_number))
	response_json = response.json()
	season_number = response_json['season_number']
	tv_episodes_array = response_json['episodes']

	if len(list_videos) == len(tv_episodes_array):
		for index in range(len(tv_episodes_array)):
			tv_episode_name = tv_episodes_array[index]['name']
			expected_file_name = create_tv_episode_name(tv_series_name, season_number, index + 1, tv_episode_name)
			rename_file_name(file_directory, list_videos[index], expected_file_name)
	else:
		print 'Episode count differs, can\'t continue with renaming'

	if len(list_subtitles) == len(tv_episodes_array):
		for index in range(len(tv_episodes_array)):
			tv_episode_name = tv_episodes_array[index]['name']
			expected_file_name = create_tv_episode_name(tv_series_name, season_number, index + 1, tv_episode_name)
			rename_file_name(file_directory, list_subtitles[index], expected_file_name)
	else:
		print 'Subtitle count differs, can\'t continue with renaming'

if __name__ == '__main__':
	main()