import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def save_data(name_data, url_data, bio_data, course_data):
    with open('names.txt', 'w') as names_file, open('bio_urls.txt', 'w') as bio_urls_file, open('bios.txt',
                                                                                                'w') as bios_file, open(
            'courses_taught.txt', 'w') as courses_file:
        names_file.write(name_data)
        bio_urls_file.write(url_data)
        bios_file.write(bio_data)
        courses_file.write(course_data)


def scrape(baseurl, subpages):
    for page in subpages:
        absolute_url = urljoin(baseurl, page)
        response = requests.get(absolute_url)

        complete_name = ''
        complete_url = ''
        complete_bio = ''
        complete_course = ''

        if response.status_code == 200:
            print("Connected to the webpage")
            soup_data = BeautifulSoup(response.content, 'html.parser')
            faculty_list = soup_data.find_all("div", {"class": "item person cat15 cs"})
            print(f"You have these many faculty: {len(faculty_list)}")
            if len(faculty_list) > 0:
                for faculty in faculty_list:
                    name_data = faculty.find_next("div", {"class": "name"})
                    if name_data is not None:
                        name_tag = name_data.find('a')
                        if name_tag is not None:
                            faculty_name = name_tag.text
                            faculty_link = urljoin(baseurl, name_tag['href'])
                            response_subpage = requests.get(faculty_link)
                            if response_subpage.status_code == 200:
                                print(f"Connected to the webpage for {faculty_name}")
                                soup_data_subpage = BeautifulSoup(response_subpage.content, 'html.parser')
                                try:
                                    biography_tag = soup_data_subpage.find('h2', string='Biography').find_next_sibling(
                                        'p')
                                    faculty_bio = biography_tag.text
                                except Exception:
                                    faculty_bio = f"No Biography for {faculty_name}"
                                try:
                                    courses_tag = soup_data_subpage.find('h2',
                                                                         string='Recent Courses Taught').find_next_sibling(
                                        'ul')
                                    faculty_courses = f"{faculty_name}:\n{courses_tag.text}"
                                except Exception:
                                    faculty_courses = f"No Courses for {faculty_name}\n"

                                # Append all data to beginning variables
                                complete_name += f'{faculty_name}\n'
                                complete_url += f'{faculty_link}\n'
                                complete_bio += f'{faculty_bio}\n'
                                complete_course += f'{faculty_courses}\n'
                                print(f'Saving Data for {faculty_name}')

            save_data(name_data=complete_name, url_data=complete_url, bio_data=complete_bio,
                      course_data=complete_course)
            print("Saved All Data - Please Check Your Files")

        else:
            print("Failed to connect to the the webpage.")


baseurl = "https://cs.illinois.edu"
subpages = ["/about/people/all-faculty"]
scrape(baseurl=baseurl, subpages=subpages)
