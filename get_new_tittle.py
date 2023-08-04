import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



class Paper:
    def __init__(self, title, authors, abstract, keywords):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.keywords = keywords

    def __str__(self):
        return f"{self.title}\n{self.authors}\n{self.abstract}\n{self.keywords}\n"
    
    def __repr__(self):
        return f"Paper({self.title}, {self.authors}, {self.abstract}, {self.keywords})"

class find_paper:
 
    def search_new(self, keywords, *keywords2):
        
        url_temp='https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={keywords}&terms-0-field=all&terms-1-operator=AND&terms-1-term={keywords2}&terms-1-field=title&terms-2-operator=AND&terms-2-term={keywords2}&terms-2-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first'   
        url=url_temp.format(keywords=keywords,keywords2=','.join(keywords2))
        # url=url_temp.format(keywords=keywords,keywords2=keywords2)
        # url = self.url.format(keywords=keywords,keywords2=keywords2)
        response = requests.get(url)
        search_results = response.text
        results = BeautifulSoup(search_results, "html.parser")
        # titles_list, authors_list, abstracts_list, divs_list= self.ger_info(results)

        rl_divs = results.find_all("div", {"class": "tags is-inline-block"})
        divs_list = [div.get_text().strip() for div in rl_divs]

        rl_papers = results.find_all("p", {"class": "title is-5 mathjax"})
        titles_list = [paper.get_text().strip() for paper in rl_papers]

        rl_authors = results.find_all("p", {"class": "authors"})
        authors_list = [author.get_text().strip() for author in rl_authors]

        rl_abstracts = results.find_all("span", {"class": "abstract-full has-text-grey-dark mathjax"})
        abstracts_list = [abstract.get_text().strip().encode("utf-8") for abstract in rl_abstracts]

        papers_list = []

        for i in range(len(titles_list)):
            papers_list.append(Paper(titles_list[i], authors_list[i], abstracts_list[i], divs_list[i]))
        return papers_list,titles_list
    
    def check_new(titles_list):
        try:
            with open("papers.txt", "r") as f:
                old_titles = f.read().splitlines()
        except FileNotFoundError:
            # If "papers.txt" doesn't exist, create an empty file
            with open("papers.txt", "w"):
                pass
            old_titles = titles_list
        new_titles = []
        for title in titles_list:
            if title not in old_titles:
                new_titles.append(title)

        # Append new titles to "papers.txt"
        with open("papers.txt", "a") as f:
            for title in new_titles:
                f.write(title + "\n")

        return new_titles

    def send_email(new_titles):
        sender = "867048402@qq.com"
        receiver = "gongm3@cardiff.ac.uk"
        if new_titles != []:
            subject = "New RL papers!"
            body = "\n".join(new_titles)
        else:
            subject = "No new RL papers yet."
            body = "Check again later."
        
        try:
            # Set up the SMTP server
            smtp_server = 'smtp.qq.com'  
            smtp_port = 587  

            # Create the email message
            message = MIMEText(body, 'plain')
            message['From'] = sender
            message['To'] = receiver
            message['Subject'] = subject

            # Connect to the SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, "neqrawwomoykbbhb")  

            server.sendmail(sender, receiver, message.as_string())
            server.quit()

            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)


# a = find_paper('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={keywords}&terms-0-field=all&terms-1-operator=AND&terms-1-term={keywords2}&terms-1-field=title&terms-2-operator=AND&terms-2-term={keywords2}&terms-2-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first')
# a=find_paper('https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term={keywords}&terms-0-field=all&terms-1-operator=AND&terms-1-term={keywords2}&terms-1-field=title&terms-2-operator=AND&terms-2-term={keywords2}&terms-2-field=title&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=50&order=-announced_date_first')
papers_list = find_paper.search_new('grasp', 'manipulation', 'reinforcement')[0]
# print(a.search_new('grasp', 'manipulation', 'reinforcement')[1])
titles_list=find_paper.search_new('grasp', 'manipulation', 'reinforcement')[1]
# new_titles = a.check_new(titles_list)
while True:
    time.sleep(200)
    new_titles = find_paper.check_new(titles_list)
    find_paper.send_email(new_titles)
