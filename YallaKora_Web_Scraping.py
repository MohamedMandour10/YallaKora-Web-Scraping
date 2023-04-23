
import datetime
import requests
import csv
from bs4 import BeautifulSoup


def get_valid_date():
    while True:
        try:
            date = input("Please enter a date in the format of MM/DD/YYYY: ")
            datetime.datetime.strptime(date, '%m/%d/%Y')
            return date
        except ValueError:
            print("Invalid date format. Please enter the date in the format of MM/DD/YYYY.")


def scrape_match_info(date):
    url = f"https://www.yallakora.com/match-center/?date={date}"
    page = requests.get(url)
    src = page.content
    soup = BeautifulSoup(src, "lxml")
    matches_details = []

    championships = soup.find_all("div", {'class': 'matchCard'})

    def extract_match_info(championship):
        champ_title = championship.contents[1].find('h2').text.strip()
        all_matches = championship.find('ul').find_all('li')
        num_matches = len(all_matches)

        for i in range(num_matches):
            # GET TEAM NAME
            team_A_div = all_matches[i].find('div', {'class': 'teamA'})
            team_A = team_A_div.text.strip() if team_A_div is not None else 'N/A'

            team_B_div = all_matches[i].find('div', {'class': 'teamB'})
            team_B = team_B_div.text.strip() if team_B_div is not None else 'N/A'

            # GET TEAM SCORE
            match_result = all_matches[i].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}" if match_result else 'N/A'

            # GET MATCH TIME
            match_time = all_matches[i].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            # ADD MATCH INFO TO matches_details
            matches_details.append({'League': champ_title, 'TeamA': team_A, 'TeamB': team_B, 'Score': score,
                                     'Time': match_time})

    for championship in championships:
        extract_match_info(championship)

    return matches_details


def write_csv_file(matches_details):
    headers = matches_details[0].keys()
    with open('match_info.csv', 'w', newline='') as match_scrap:
        match_infos = csv.DictWriter(match_scrap, headers)
        match_infos.writeheader()
        match_infos.writerows(matches_details)
        print("Process completed successfully!")


if __name__ == '__main__':
    date = get_valid_date()
    match_details = scrape_match_info(date)
    write_csv_file(match_details)

