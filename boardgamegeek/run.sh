echo 'Fetching all dtc games'
python fetch_dtc_games.py
echo 'Formatting for the spider'
python extract_ids.py
#echo 'Get everything from bgg'
#scrapy runspider spider.py -o items.csv
echo 'Downloading the info for the dtc games'
python get_game_info.py